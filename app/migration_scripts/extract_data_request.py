import json
import os
import logging
import xml.etree.ElementTree as ET
import requests
from urllib.parse import quote
from .authenticate import get_access_token

# Configure logging
logger = logging.getLogger(__name__)

def load_fetchxml_queries():
    """
    Load FetchXML queries from XML files in the 'xml_queries' directory.

    Returns:
        dict: A dictionary where the key is the filename without extension,
              and the value is the FetchXML query as a string.
    """
    queries = {}
    # Construct the directory path where the XML files are located
    directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'xml_queries')
    logger.debug(f"Trying to access directory: {directory}")

    try:
        # List all files in the directory
        files = os.listdir(directory)
        logger.debug(f"Files found: {files}")
        for filename in files:
            if filename.endswith('.xml'):
                # Parse the XML file
                filepath = os.path.join(directory, filename)
                logger.debug(f"Trying to parse file: {filepath}")
                tree = ET.parse(filepath)
                root = tree.getroot()
                query_as_string = ET.tostring(root, encoding='unicode')
                # Store the query with the filename (without extension) as the key
                queries[filename[:-4]] = query_as_string
        logger.info("FetchXML queries loaded successfully.")
        return queries
    except FileNotFoundError:
        logger.error(f"Directory not found: {directory}")
        raise FileNotFoundError(f"Directory not found: {directory}")
    except ET.ParseError as e:
        logger.error(f"Error parsing XML file: {filepath}: {e}")
        raise

def fetch_all_data(access_token, base_url, save_to_file=False):
    """
    Fetch data from Dataverse using the loaded FetchXML queries.

    Args:
        access_token (str): The access token for authenticating API requests.
        base_url (str): The base URL of the Dataverse instance.
        save_to_file (bool): Whether to save the fetched data to JSON files.

    Returns:
        dict: A dictionary where the key is the query name, and the value is the fetched data.
    """
    queries = load_fetchxml_queries()
    all_data = {}

    for key, query in queries.items():
        logger.info(f"Fetching {key} data using FetchXML.")
        try:
            # Correctly construct the URL with the entity set name based on the key
            entity_set = f"{key}s"  # Assuming the entity set name follows this pattern
            url = f"{base_url}/api/data/v9.1/{entity_set}?fetchXml={quote(query)}"
            logger.debug(f"FetchXML Query URL: {url}")
            
            # Make the API request to fetch data using the FetchXML query
            response = requests.get(
                url,
                headers={
                    "Authorization": f"Bearer {access_token}",
                    "Content-Type": "application/json",
                    "OData-MaxVersion": "4.0",
                    "OData-Version": "4.0"
                }
            )
            response.raise_for_status()

            data = response.json()
            all_data[key] = data
            if save_to_file:
                # Save the fetched data to a JSON file
                file_path = os.path.join(os.path.dirname(__file__), f"{key}_data.json")
                with open(file_path, 'w') as f:
                    json.dump(data, f, indent=4)
                logger.info(f"Successfully fetched and saved {key} data to {file_path}.")

        except requests.exceptions.HTTPError as e:
            logger.error(f"HTTP error fetching data for {key}: {e.response.status_code} - {e.response.text}", exc_info=True)
        except requests.exceptions.RequestException as e:
            logger.error(f"Request failed for {key}: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Unexpected error occurred while fetching data for {key}: {e}", exc_info=True)

    return all_data

if __name__ == "__main__":
    # Example usage
    client_id = "0e24dcbb-d286-4dc1-b203-5b0969749f9a"
    client_secret = "xGl8Q~GherFkKfg4I1EEAvO-u2qNmVopxlXoNa3z"
    tenant_id = "0e24dcbb-d286-4dc1-b203-5b0969749f9a"
    resource = "https://ox2dev.crm4.dynamics.com"

    # Authenticate to obtain the access token
    token = get_access_token(client_id, client_secret, tenant_id, resource)
    base_url = "https://ox2dev.crm4.dynamics.com"

    # Fetch all data using the loaded FetchXML queries and save to files
    all_data = fetch_all_data(token, base_url, save_to_file=True)
    logger.info(f"All Data: {all_data}")
