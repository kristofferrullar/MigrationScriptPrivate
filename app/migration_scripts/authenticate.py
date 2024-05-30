import requests  # Importing the requests library for making HTTP requests
import logging  # Importing the logging module for logging messages

logger = logging.getLogger(__name__)  # Creating a logger object for logging messages

def get_access_token(client_id, client_secret, tenant_id, resource):
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"  # Constructing the URL for token endpoint
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}  # Setting the headers for the request
    body = {
        'grant_type': 'client_credentials',  # Grant type for client credentials flow
        'client_id': client_id,  # Client ID for authentication
        'client_secret': client_secret,  # Client secret for authentication
        'scope': f'{resource}/.default'  # Scope for the requested access token
    }
    
    logger.debug(f"Request URL: {url}")  # Logging the request URL
    logger.debug(f"Request headers: {headers}")  # Logging the request headers
    logger.debug(f"Request body: {body}")  # Logging the request body
    
    try:
        response = requests.post(url, headers=headers, data=body)  # Sending the POST request to get the access token
        response.raise_for_status()  # Raising an exception if the response status code is not successful
        access_token = response.json().get('access_token')  # Extracting the access token from the response
        if not access_token:
            raise ValueError("No access token found in the response.")  # Raising an exception if access token is not found
        logger.info("Authentication successful.")  # Logging a success message
        return access_token  # Returning the access token
    except requests.exceptions.RequestException as e:
        logger.error(f"Authentication failed: {e}", exc_info=True)  # Logging an error message with exception details
        raise  # Raising the exception again to propagate it to the caller
