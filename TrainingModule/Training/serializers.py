from rest_framework import serializers
from .models import UploadedFile
import base64
from django.core.files.base import ContentFile


#class UploadedFileSerializer (serializers.ModelSerializer):
#    filebody = serializers.CharField(write_only=True)  # For receiving the Base64-encoded file content

#    class Meta:
#        model = UploadedFile
#        fields = ('filename', 'filetype', 'filebody', 'author','publisher', 'url', 'file')  # Include 'file' to return the file URL
#        extra_kwargs = {'file': {'read_only': True}}

#    def create(self, validated_data):
#        filebody = validated_data.pop('filebody', None)
#        if filebody:
            # Decode the Base64-encoded file
#            data = ContentFile(base64.b64decode(filebody), name=validated_data.get('filename'))
#            validated_data['file'] = data

#        return UploadedFile.objects.create(**validated_data)