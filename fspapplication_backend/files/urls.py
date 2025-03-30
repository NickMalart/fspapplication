from django.urls import path
from .views import FileUploadView, FileListView, FileDeleteView, FileDownloadView, DiagnosticView

urlpatterns = [
    path('upload/', FileUploadView.as_view(), name='file-upload'),
    path('list/', FileListView.as_view(), name='file-list'),
    path('delete/', FileDeleteView.as_view(), name='file-delete'),
    path('download/', FileDownloadView.as_view(), name='file-download'),
    path('diagnostic/', DiagnosticView.as_view(), name='file-diagnostic'),
] 