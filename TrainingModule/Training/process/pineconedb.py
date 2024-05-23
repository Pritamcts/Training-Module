
from pinecone import Pinecone, ServerlessSpec
import logging
from django.core.files.base import ContentFile
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
import logging
from django.conf import settings
import json
logger = logging.getLogger(__name__)

# Connect to Pinecone

vector_dimension_map = {
    'BERT':768,
    'OPENAI': 1536
}

# Function to store vector in Pinecone

def store_vector_in_pinecone(vector, identifier, metadata):
    print ("started storing vector ")
    # pinecone.init(api_key=settings.PINECONE_API_KEY)
    # # List all indexes
    # indexes = pinecone.list_indexes()
    pc=Pinecone(api_key=settings.PINECONE_API_KEY)
    PINECONE_INDEX_NAME = settings.PINECONE_INDEX
    index=pc.Index(PINECONE_INDEX_NAME)
    model = settings.TXT_MODEL
    if model not in vector_dimension_map:
        logging.error(f"Unknown Model for Pinecone: {model}")
        return "ERROR"
    
    # Index the vector in Pinecone
    try:
        logging.info ("Writing to Pinecone")
        upserts = [(str(identifier), vector,metadata)]
        print(upserts)
        index.upsert(vectors=upserts)
        return "SUCCESS"

    except Exception as e:
        logging.error(f"Error storing data in Pinecone: {e}")
        return "ERROR"




# Deleting the vector from pinecone
# def delete_vector_from_pinecone(key, model, filetype, identifier,config_data):
#     #pinecone.api_key = key
#     pinecone.init(api_key=settings.PINECONE_API_KEY, environment='gcp-starter')

#     # List all indexes
#     indexes = pinecone.list_indexes()

#     if model not in vector_dimension_map:
#         logging.error(f"Unknown Model for Pinecone: {model}")
#         return False
    
#     PINECONE_INDEX_NAME = config_data ['pinecone_index']

#     if PINECONE_INDEX_NAME not in indexes:
#         logging.error(f"Index not found in Pinecone for: {model}")
#         return False
    
#     index = pinecone.Index(PINECONE_INDEX_NAME)
#     # Delete the vector from Pinecone
#     try:
#         logging.info ("Deleting from Pinecone")
#         index.delete(ids=[str(identifier)])
#         return True
#     except Exception as e:
#         logging.error(f"Error deleting data from Pinecone: {e}")
#         return False
    


def query_vector_in_pinecone(vector, user_type):
    print("started querying vector ")
    pc=Pinecone(api_key=settings.PINECONE_API_KEY)

    model = settings.TXT_MODEL
    if model not in vector_dimension_map:
        logging.error(f"Unknown Model for Pinecone: {model}")
        return "ERROR"

    PINECONE_INDEX_NAME = "langchain-app"  # Hardcoded, you might want to change this

    # if PINECONE_INDEX_NAME not in indexes:
    #     logging.error(f"Index not found in Pinecone for: {model}")
    #     return "ERROR"

    index = pc.Index(PINECONE_INDEX_NAME)

    try:
        logging.info("Querying Pinecone")
        response = index.query(vector=vector, top_k=6, include_metadata=True)

        # Filter the response based on user_type and prioritize certain material types
        filtered_response = []
        for item in response['matches']:
            metadata = item['metadata']
            material_type = metadata.get("material-type")

            if user_type == "Parent":
                if material_type == "Parental Guide":
                    filtered_response.append(item)
                elif material_type == "Cheat Sheet":
                    filtered_response.append(item)
                elif material_type == "Book":
                    filtered_response.append(item)
                elif material_type == "Research Paper":
                    filtered_response.append(item)
            elif user_type == "BCBA":
                if material_type == "Cheat Sheet":
                    filtered_response.append(item)
                elif material_type == "Parental Guide":
                    filtered_response.append(item)
                elif material_type == "Book":
                    filtered_response.append(item)
                elif material_type == "Research Paper":
                    filtered_response.append(item)
            elif user_type == "RBT":
                if material_type == "Book":
                    filtered_response.append(item)
                elif material_type == "Cheat Sheet":
                    filtered_response.append(item)
                elif material_type == "Parental Guide":
                    filtered_response.append(item)
                elif material_type == "Research Paper":
                    filtered_response.append(item)
        response['matches'] = filtered_response
        return response
    except Exception as e:
        logging.error(f"Error Querying data in Pinecone: {e}")
        return "ERROR"
