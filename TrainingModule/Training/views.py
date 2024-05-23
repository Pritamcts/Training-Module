
import random
import uuid
import sys
import base64
import requests
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import logging
from django.conf import settings
from os.path import dirname, join
from Training.process.file_processing import *
from Training.process.query import *
from Training.process.model import *

from django.http import FileResponse
from django.http import HttpResponse
import os

INSERT_DATA_ENDPOINT = "http://127.0.0.1:5002/insert_db"
FEEDBACK_ENDPOINT = "http://127.0.0.1:5002/submit_feedback"

logger = logging.getLogger(__name__)
class FileUploadView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication for this view

    def post(self, request, *args, **kwargs):
        # Extract file information from the request
       
        data_json = {"file-name" : request.data.get('filename'), "file-body": request.data.get('filebody'), "file-type" : request.data.get('filetype'), "creator": request.data.get('author'), "owner": request.data.get('publisher'), "web-url": request.data.get('url'),"material-type": request.data.get('material_type') }
        # Assuming 'filebody' is the Base64 encoded content of the file
        if not request.data.get('filename') or not request.data.get('filebody') or not request.data.get('filetype'):
            logger.error('File is corrupted')
            return JsonResponse({'error': 'Filename , Filetype or file body missing'}, status=400)
        response = process_and_save_file (data_json)
        if response == 201:
            return JsonResponse({'message': 'File uploaded successfully'}, status=201)
        else :
            return JsonResponse({'message': 'File uploaded failed'}, status=500)



class StartTraining(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication for this view

    def post(self, request, *args, **kwargs):
        # Extract  information from the request
       embed_type = request.data.get ('embed')
       logger.info (f'Embedding for {embed_type} initiated')
       response = {}
       if embed_type == 'all':
        response ['result'] = scan_directory (embed_type)
       
       if len(response) > 0:
            return JsonResponse(response, status=200)
       else :
            return JsonResponse({'message': 'File uploaded failed'}, status=500)


class QueryTheAI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        global prompt, refined_prompt
        prompt = request.data.get('prompt')
        user_type = request.data.get('user_type') #edited
        refined_prompt = query_refiner(prompt)
        result=get_rasa_output(refined_prompt)

        if result:
            result=result[0]['text']
            print(result)
            if result=="This query is irrelevant.":
                return JsonResponse({"uid":"irrelevant"})
        response = query(prompt,user_type) #changed
        return JsonResponse(response, safe=False, status=200) if "ERROR" not in response else JsonResponse({'message': 'No record found'}, status=500)


class PollTheAI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        uid = request.data.get('uid')
        user_type = request.data.get('user_type') #edited
        response = accumulate_result(uid,user_type) #edited
        return JsonResponse(response, safe=False, status=200) if "ERROR" not in response else JsonResponse({'message': 'No record found'}, status=500)

class SummarizeResults(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        global summary
        results = request.data.get('results')
        combined_text = "\n".join(result['summary'] for result in results)
        summary = summarize_combined_text_lc(combined_text)
        if summary:
            insert_db(summary)
        return JsonResponse({'summary': summary}, status=200) if summary else JsonResponse({'message': 'Empty'}, status=500)

        
class ViewPDF(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, filename):
        filename=filename+'.pdf'
        pdf_path = os.path.join(settings.PROCESSED_FILES, filename)
        print(pdf_path)
        # Check if the file exists
        if not os.path.exists(pdf_path):
            logger.error(f"File not found: {pdf_path}")
            return JsonResponse({'message': 'File not found'}, status=404)
        
        # Try to open the file
        try:
            with open(pdf_path, 'rb') as pdf_file:
                response = HttpResponse(pdf_file.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'inline; filename="{filename}"'
                return response
        
        # Catch any specific exceptions
        except PermissionError:
            logger.error(f"Permission denied for file: {pdf_path}")
            return JsonResponse({'message': 'Permission denied'}, status=403)
        
        except Exception as e:
            logger.error(f"Error serving PDF file: {e}")
            return JsonResponse({'message': 'Error serving PDF file'}, status=500)
class Feedback(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        rating = request.data.get('rating')
        feedback = request.data.get('feedback')
        if rating and feedback:
            submit_feedback(rating, feedback)
            return JsonResponse({'rating': rating, 'feedback': feedback}, safe=False, status=200)
        else:
            return JsonResponse({'message': 'No record found'}, status=500)
def insert_db(summary):
    data = {
        'prompt': prompt,
        'refined_prompt': refined_prompt,
        'summary': summary
    }
    response = requests.get(INSERT_DATA_ENDPOINT, json=data)
    if response.status_code == 200:
        print("Data submitted")
    else:
        print(f"Failed to submit data: {response.content}")

def submit_feedback(rating, feedback):
    data = {
        'rating': rating,
        'feedback': feedback,
        'prompt': prompt,
        'refined_prompt': refined_prompt,
        'summary': summary
    }
    response = requests.post(FEEDBACK_ENDPOINT, json=data)
    if response.status_code == 200:
        print("Feedback submitted successfully")
    else:
        print(f"Failed to submit feedback: {response.content}")



def get_rasa_output(query):
    url = "http://54.162.133.116:5005/webhooks/rest/webhook"
    data = {"sender": "test_user", "message": query}
    response = requests.post(url, json=data)
    return response.json()