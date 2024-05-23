import base64
from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import logging
from django.conf import settings
import json
import os 
import uuid
from PyPDF2 import PdfReader
import PyPDF2
import shutil
from Training.process.utility import *
from Training.process.model import *
from Training.process.pineconedb import *
import copy
from django.core.cache import cache
from threading import Thread
import time
import requests
logger = logging.getLogger(__name__)
# Define a unique sentinel object that will never be cached


class Sentinel:
    pass


def query (question,user_type):  #edited
    # prompt=question
    # refined_prompt=query_refiner(prompt)
    #First Generate new prompts
    num_related_questions = settings.NUM_RELATED_QUESTIONS
    prompt_result = generate_prompt (question,num_related_questions)
    prompt_result.insert (0,query_refiner(question))    # Calling the query_refiner function


    unique_identifier = str(uuid.uuid4())
    count = 0
    for item in prompt_result:
    # Start the async task
        print ("Starting thread")
        async_thread = Thread (target=start_query, args = (item, unique_identifier+"-"+str(count),user_type) ) #edited
        async_thread.start()
        count = count + 1
        time.sleep (5)

    return {"uid":unique_identifier}


def start_query(argument1, unique_id,user_type):  #edited
    print ("inside query")
    print (argument1)
    print (unique_id)

    try:
        vector = []
        if settings.TXT_MODEL == 'BERT':
            vector = generate_document_vector_bert (argument1)
        if settings.TXT_MODEL == 'OPENAI':
            vector = generate_document_vector_openai (argument1)
        response = query_vector_in_pinecone(vector,user_type)   #edited


        response = response ['matches']
        combined_text = []
        unique_data = {}
        for item in response:
           # print ("----------------------------------------")    
           # print (item ['id'] + " "  + str (item ["score"]) + " " + item ['metadata'] ['file-name'])
           # print ("----------------------------------------")    
           # print ( item ['metadata'] ['text'] )
            if item ['score'] > 0.79:
                combined_text.append (item ['metadata'] ['text'])
                result_object = {}
                if 'creator' in item ['metadata']:
                    result_object ['creator'] = item ['metadata'] ['creator']
                if 'file-name' in item ['metadata']:
                    result_object ['file-name'] = item ['metadata'] ['file-name']
                if 'owner' in item ['metadata']:
                    result_object ['owner'] = item ['metadata'] ['owner']
                if 'web-url' in item ['metadata']:
                    result_object ['url'] = item ['metadata'] ['web-url']
                if 'material-type' in item ['metadata']: #edited
                    result_object ['material-type'] = item ['metadata'] ['material-type'] #edited

                id = item ['id'].split("|")[0]
                unique_data [id] = result_object
        source = []
        for items in unique_data.values():
            source.append(items)
        #summary = summarize_combined_text (combined_text)
        print ("-------------Summarizing now------------")
        summary = summarize_combined_text_lc (combined_text)
        data_json = {"prompt": argument1, "summary": summary, "source": source}
        print (data_json)
        print ("Writing Result " + unique_id )
        cache.set(unique_id, data_json, timeout=None)  
        return {"summary": summary, "source": source}

    except ValueError as e:
        print(f"Error: {e}")
        return {"ERROR":"ERROR"}
    


def accumulate_result (unique_identifier,user_type): #edited
    global summary
    sentinel = Sentinel()
    found = 0
    result = []
    for i in range(4):
        cache_key = unique_identifier + "-"+str(i)
        value = cache.get(cache_key, sentinel)

        if value is not sentinel:
            found = found + 1 
            result.append (value)           
            # You can now use the value
    if found == 4:
        print (result)
        print ("cleaning Cache")
        for i in range(4):
            cache_key = unique_identifier + "-"+str(i)
            cache.delete (cache_key)
        return {"status": "DONE", "Data" : result}
    else:
        return {"status": "PENDING"}


