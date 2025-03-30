import logging
from django.http import HttpResponse

logger = logging.getLogger(__name__)

class CORSMiddleware:
    """
    Middleware to handle CORS headers for CloudFront and file-related endpoints
    
    This middleware adds the necessary CORS headers to responses from the files app
    to prevent CORS errors when loading resources from CloudFront or other domains.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        logger.info("CORS Middleware initialized")
        
    def __call__(self, request):
        # Process the request as usual
        response = self.get_response(request)
        
        # Check if this is a request to the files app
        if request.path.startswith('/api/files/') or request.path.startswith('/files/'):
            # Add CORS headers to the response
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response["Access-Control-Max-Age"] = "86400"  # 24 hours
            
            logger.debug(f"Added CORS headers to response for path: {request.path}")
            
        return response
    
    def process_request(self, request):
        # Handle OPTIONS requests
        if request.method == "OPTIONS" and (request.path.startswith('/api/files/') or request.path.startswith('/files/')):
            response = HttpResponse()
            response["Access-Control-Allow-Origin"] = "*"
            response["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response["Access-Control-Allow-Headers"] = "Content-Type, Authorization"
            response["Access-Control-Max-Age"] = "86400"  # 24 hours
            return response
        
        return None 