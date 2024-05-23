from django.urls import path 
from .views import *

urlpatterns = [
    path ("upload/", FileUploadView.as_view(), name='file-upload'),
    path ("start-training/", StartTraining.as_view(), name = 'embed-and-train'),
    path ("query/", QueryTheAI.as_view(), name = 'query-ai'),
    path ("poll/", PollTheAI.as_view(), name = 'poll-ai'),
    path("summarize/", SummarizeResults.as_view(), name='summarize-results'),  # New endpoint for summarizing results
    path("feedback/",Feedback.as_view(), name='Feedback'),
    path('view-pdf/<str:filename>/', ViewPDF.as_view(), name='view_pdf'),
]