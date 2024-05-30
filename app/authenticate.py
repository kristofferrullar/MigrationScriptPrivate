import requests
import logging

logger = logging.getLogger(__name__)

def get_access_token(client_id, client_secret, tenant_id, resource):
    """
    Authenticate to Microsoft Dataverse and return an access token.

    Parameters:
    client_id (str): The client ID of the Azure AD application.
    client_secret (str): The client secret of the Azure AD application.
    tenant_id (str): The tenant ID of the Azure AD tenant.
    resource (str): The resource (Dataverse URL) to access.

    Returns:
    str: Access token for the Microsoft Dataverse.
    """
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    body = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
        'scope': f'{resource}'
    }
    try:
        logger.debug(f"Authenticating to URL: {url} with client_id: {client_id}")
        response = requests.post(url, headers=headers, data=body)
        response.raise_for_status()
        access_token = response.json().get('access_token')
        if not access_token:
            raise ValueError("No access token found in the response.")
        logger.info("Authentication successful.")
        return access_token
    except requests.exceptions.RequestException as e:
        logger.error(f"Authentication failed: {e}", exc_info=True)
        raise
