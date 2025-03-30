from django.urls import path
from .views import GooglePlacesAPIView, GooglePlaceDetailsAPIView
from . import views


urlpatterns = [
    path('api/places/autocomplete/', GooglePlacesAPIView.as_view(), name='google-places-autocomplete'),
    path('api/places/details/', GooglePlaceDetailsAPIView.as_view(), name='google-places-details'),
    path('s3/upload/', views.upload_file, name='s3_upload_file'),
    path('s3/download/<path:file_path>/', views.get_download_url, name='s3_get_download_url'),
    path('s3/list/', views.list_files, name='s3_list_files'),
    path('s3/delete/<path:file_path>/', views.delete_file, name='s3_delete_file'),
]