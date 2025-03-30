from django.urls import path
from .views import GooglePlacesAPIView, GooglePlaceDetailsAPIView


urlpatterns = [
    path('api/places/autocomplete/', GooglePlacesAPIView.as_view(), name='google-places-autocomplete'),
    path('api/places/details/', GooglePlaceDetailsAPIView.as_view(), name='google-places-details'),
]