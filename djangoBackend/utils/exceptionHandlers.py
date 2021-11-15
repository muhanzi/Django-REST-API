from rest_framework.views import exception_handler
from rest_framework.exceptions import ValidationError, AuthenticationFailed
from rest_framework import status

def send_response(success, message, data):
    return {"success": success, "message": message,"data": data}
def custom_exception_handler(exc, context):
    # Call REST framework's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    # Update the structure of the response data.
    if isinstance(exc, ValidationError): 
        if response is not None:
            customized_response = {}
            customized_response['errors'] = []
            print('......',response.data.items())


            for key, value in response.data.items():
                error = {}
                if isinstance(value[0],dict):
                    error2 = {}
                    for key2 in value[0]:
                        error2 ={key2: value[0][key2][0]}
                    error = {key: error2}
                else:
                    error = {key: value[0]}
                customized_response['errors'].append(error)

            response.data = send_response(False,"missing attributes",customized_response)
            
    if isinstance(exc, AuthenticationFailed): 
        if response is not None:
            response.data = send_response(False,response.data["detail"],{})

    return response

class CustomAPIException(ValidationError):
    """
    raises API exceptions with custom messages and custom status codes
    """
    status_code = status.HTTP_400_BAD_REQUEST
    default_code = 'error'

    def __init__(self, detail, status_code=None):
        self.detail = detail
        if status_code is not None:
            self.status_code = status_code    