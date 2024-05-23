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

logger = logging.getLogger(__name__)

#Process file - add the Metadata & save into source directory
# def process_and_save_file (datajson):
    
#     # Decode the file and create a ContentFile
#     file_data = ContentFile(base64.b64decode(datajson['file-body']), name=datajson['file-name'])
        
#     # Define the path where you want to save the file
#     # Ensure the 'uploads' directory exists and is writable
#     save_path = settings.DIRECTORY_TO_SCAN + datajson['file-name'] +'.'+datajson['file-type']
        
#     # Write the file to the filesystem
#     try:
#         with open(save_path, 'wb+') as destination:
#             for chunk in file_data.chunks():
#                 destination.write(chunk)
#     except IOError as e:
#         logger.error (f'An exception occured in storing file : {e}')
#         return 500
    
#     #create metadata json for the file
#     keys_to_exclude = ["file-body"]
#     # Create a shallow copy of source excluding specified keys
#     metadata = {k: v for k, v in datajson.items() if k not in keys_to_exclude}
#     metadata_path = settings.DIRECTORY_TO_SCAN + datajson['file-name'] +'.info'

#     try:
#         with open(metadata_path, "w", encoding="utf-8") as output_text_file:
#             output_text_file.write(json.dumps (metadata))
#     except IOError as e:
#         logger.error (f'An exception occured in storing metadata : {e}')
#         os.remove (settings.DIRECTORY_TO_SCAN + datajson['file-name'] +'.'+datajson['file-type'])
#         return 500


#     logger.info(f'File {datajson["file-name"]}.{datajson["file-type"]} is stored with metadata')
#     return 201




def process_and_save_file(datajson):
    # Decode the file and create a ContentFile
    file_data = ContentFile(base64.b64decode(datajson['file-body']), name=datajson['file-name'])
        
    # Define the path where you want to save the file
    # Ensure the 'uploads' directory exists and is writable
    save_path = settings.DIRECTORY_TO_SCAN + datajson['file-name'] + '.' + datajson['file-type']
        
    # Write the file to the filesystem
    try:
        with open(save_path, 'wb+') as destination:
            for chunk in file_data.chunks():
                destination.write(chunk)
    except IOError as e:
        logger.error(f'An exception occurred in storing file: {e}')
        return 500
    
    # Create metadata for the file
    metadata = {
        "file-name":datajson['file-name'],
        "file-type": datajson['file-type'],
        "creator": datajson['creator'],
        "owner": datajson['owner'],
        "web-url": datajson['web-url'],
        "material-type": datajson['material-type'],
    }

    metadata_path = settings.DIRECTORY_TO_SCAN + datajson['file-name'] + '.info'

    try:
        with open(metadata_path, "w", encoding="utf-8") as output_text_file:
            output_text_file.write(json.dumps(metadata))
    except IOError as e:
        logger.error(f'An exception occurred in storing metadata: {e}')
        os.remove(settings.DIRECTORY_TO_SCAN + datajson['file-name'] + '.' + datajson['file-type'])
        return 500

    logger.info(f'File {datajson["file-name"]}.{datajson["file-type"]} is stored with metadata')
    return 201



# Process file - add the Metadata & save into source directory



def scan_directory(embed_type):
    unique_identifier_list = []
    directory_path = settings.DIRECTORY_TO_SCAN 
    logger.info ("Scanning Started")
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            unique_identifier = uuid.uuid4()
            
            file_path = os.path.join(root, file)
            try:
                if file.endswith('.txt') and (embed_type == 'all' or embed_type == file.suffix) :
                    logging.info (f"Processing {file}")
                    extractor = extract_text_from_txt (file_path)
                    if extractor['status'] == 200:
                        response = vectorize_and_store(file_path,extractor['message'], unique_identifier)
                        if response == "SUCCESS":
                             unique_identifier_list.append ({"File Name" : file, "ID" : str (unique_identifier)  })
                        else:
                            unique_identifier_list.append ({"File Name" : file, "ID" : "Error in file processing" })   
                    else:
                        unique_identifier_list.append ({"File Name" : file, "ID" : "Error in file processing" })

                
                elif file.endswith('.pdf') and (embed_type == 'all' or embed_type == file.suffix):
                    logging.info (f"Processing {file}")
                    extractor = extract_text_from_pdf (file_path)
                    if extractor['status'] == 200:
                        response = vectorize_and_store(file_path,extractor['message'], unique_identifier)
                        if response == "SUCCESS":
                             unique_identifier_list.append ({"File Name" : file, "ID" : str (unique_identifier)  })
                        else:
                            unique_identifier_list.append ({"File Name" : file, "ID" : "Error in file processing" })   
                    else:
                        unique_identifier_list.append ({"File Name" : file, "ID" : "Error in file processing" })

                
                
                elif file.endswith(('.mp3', '.wav', '.mp4', '.avi')) and (embed_type == 'all' or embed_type == file.suffix):
                    print ("Later")
                
                
                else:
                    logging.info(f"Unsupported file type: {file_path}")
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")
                unique_identifier_list.append ({"File Name" : file, "ID" : "Upload not successfull" })
    return (unique_identifier_list)


def extract_text_from_txt (file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text_content = file.read()
        if len (text_content) == 0:
            logger.error (f"Cannot extract text from file - {os.path.basename (file_path)} ") 
            return {'message': f'Cannot Extract Text from file - {os.path.basename (file_path)}', "status" : 500}
        else:
            return {'message': text_content, "status" : 200}
    
    except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
            return {'message': f'Error reading the file content - {os.path.basename (file_path)}', "status" : 500}
  
def extract_text_from_pdf (file_path):
    try:
        with open(file_path, 'rb') as file:
            pdf = PdfReader(file)
            text = ''
            for page_num in range(len(pdf.pages)):
                text += pdf.pages[page_num].extract_text()

        if len (text) == 0:
            logger.error (f"Cannot extract text from file - {os.path.basename (file_path)} ") 
            return {'message': f'Cannot Extract Text from file - {os.path.basename (file_path)}', "status" : 500}
        else:
            return {'message': text, "status" : 200}
    
    except Exception as e:
            logging.error(f"Error processing file {file_path}: {e}")
            return {'message': f'Error reading the file content - {os.path.basename (file_path)}', "status" : 500}
            

def vectorize_and_store (file_path,file_body, unique_identifier):
    processed_folder = settings.PROCESSED_FILES 
    error_folder = settings.ERROR_FILES
    unique_identifier = unique_identifier

    #First Read the file Meta data from .info files
    meta_name = os.path.basename (file_path)[:-4] + ".info"
    meta_path = settings.DIRECTORY_TO_SCAN+meta_name
    meta = {}
    try :
        with open(meta_path, 'r') as meta_file:
            meta = json.load(meta_file)            
    except Exception as e:
            logging.error(f"Error processing Metadata file {file_path}: {e}")
            return "ERROR"
    
    #Now chunk the text in words 

    chunks = chunk_text (file_body)
    if len(chunks) > 0:
        count = 0
        for chunk in chunks:
            count = count + 1
            try:
                vector = generate_document_vector_openai (chunk)
                metadata = {}
                metadata = copy.copy (meta)
                metadata ["text"] = chunk
                response = store_vector_in_pinecone(vector, str (unique_identifier) + "|" + str(count), metadata)
                if response == "ERROR" :
                    logging.error(f"Error processing file {file_path}")
                    shutil.move(file_path, error_folder + os.path.basename (file_path))   
                    return "ERROR"
            except Exception as e:
                logging.error(f"Error processing file {file_path}: {e}")
                shutil.move(file_path, error_folder + os.path.basename (file_path))    
                return "ERROR"
    else:
        logging.error(f"No chunk found for {file_path}: {e}")
        return "ERROR"
    shutil.move(file_path, processed_folder + os.path.basename (file_path))
    shutil.move(meta_path, processed_folder + os.path.basename (meta_path))

    return "SUCCESS"

