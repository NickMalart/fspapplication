from django.urls import path
from .views import GooglePlacesAPIView, GooglePlaceDetailsAPIView


urlpatterns = [
    path('places/autocomplete/', GooglePlacesAPIView.as_view(), name='google-places-autocomplete'),
    path('places/details/', GooglePlaceDetailsAPIView.as_view(), name='google-places-details'),
]