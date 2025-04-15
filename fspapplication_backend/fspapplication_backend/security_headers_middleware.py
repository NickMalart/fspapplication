class SecurityHeadersMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # Define your security headers here
        self.headers = {
            # Controls how much referrer information is sent with requests
            # 'strict-origin-when-cross-origin' is a good default balance
            'Referrer-Policy': 'strict-origin-when-cross-origin',
            # Controls browser features access (camera, geolocation, etc.)
            # Define a policy based on features your frontend *needs*
            # Example: Disable common sensitive APIs if not used
            'Permissions-Policy': (
                'camera=(), '
                'microphone=(), '
                'geolocation=(), '
                'payment=(), '
                'usb=()'
                # Add other features as needed, e.g., 'fullscreen=(self)'
            ),
            # You could add other headers here too if needed
            # 'Content-Security-Policy': "default-src 'self'", # Example CSP (complex to configure)
        }

    def __call__(self, request):
        response = self.get_response(request)
        # Add the defined headers to the response
        for header, value in self.headers.items():
            response[header] = value
        return response 