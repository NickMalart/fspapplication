from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
import requests

class GooglePlacesAPIView(APIView):
    """
    API view to proxy requests to Google Places API for address auto-completion
    """
    
    def get(self, request):
        try:
            # Get the query parameter from the request
            input_text = request.query_params.get('input', '')
            
            if not input_text:
                return Response(
                    {"error": "Input parameter is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Build request to Google Places API
            url = "https://maps.googleapis.com/maps/api/place/autocomplete/json"
            params = {
                'input': input_text,
                'key': settings.GOOGLE_PLACES_API_KEY,
            }
            
            # Make request to Google API
            response = requests.get(url, params=params)
            data = response.json()
            
            return Response(data)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    
class GooglePlaceDetailsAPIView(APIView):
    """
    API view to get full address details from a Place ID
    """
    
    def get(self, request):
        try:
            # Get the place_id parameter from the request
            place_id = request.query_params.get('place_id', '')
            
            if not place_id:
                return Response(
                    {"error": "place_id parameter is required"}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Build request to Google Place Details API
            url = "https://maps.googleapis.com/maps/api/place/details/json"
            params = {
                'place_id': place_id,
                'key': settings.GOOGLE_PLACES_API_KEY,
                'fields': 'address_component,formatted_address,geometry'
            }
            
            # Make request to Google API
            response = requests.get(url, params=params)
            data = response.json()
            
            return Response(data)
            
        except Exception as e:
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )