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
import shutil
import logging
import re

logger = logging.getLogger(__name__)

def chunk_text(text):
    # Split the text into words
    chunk_size = settings.EMBEDDING_CHUNK_SIZE
    sentences = re.split(r'(?<=[.!?]) +', text)

    #Now take each sentence add it to a chunks until you reach the chunk size
    chunk = ''
    chunks = []
    running_count = 0
    for sentence in sentences:
        words = sentence.split()
        if running_count + len(words) < 500:
            running_count = running_count + len(words)
            chunk = chunk + sentence + "."
        else:
            chunks.append (chunk)
            chunk = sentence + "."
            running_count = len(words)
    
    #if any chunk left to add
    if len(chunk) > 0:
        chunks.append (chunk)

    return chunks

