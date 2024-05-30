import json
import os
import logging
import requests
from urllib.parse import quote
from .utilities import save_to_temp_storage

import xml.etree.ElementTree as ET

logger = logging.getLogger(__name__)

def load_fetchxml_queries():
    """
    Load FetchXML queries from XML files in the 'xml_queries' directory.

    Returns:
        dict: A dictionary where the key is the filename without extension,
              and the value is the FetchXML query as a string.
    """
    queries = {}
    directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'xml_queries')
    logger.debug(f"Trying to access directory: {directory}")

    try:
        files = os.listdir(directory)
        logger.debug(f"Files found: {files}")
        for filename in files:
            if filename.endswith('.xml'):
                filepath = os.path.join(directory, filename)
                logger.debug(f"Trying to parse file: {filepath}")
                tree = ET.parse(filepath)
                root = tree.getroot()
                query_as_string = ET.tostring(root, encoding='unicode')
                queries[filename[:-4]] = query_as_string
        logger.info("FetchXML queries loaded successfully.")
        return queries
    except FileNotFoundError:
        logger.error(f"Directory not found: {directory}")
        raise FileNotFoundError(f"Directory not found: {directory}")
    except ET.ParseError as e:
        logger.error(f"Error parsing XML file: {filepath}: {e}")
        raise

def extract_entity_name(fetchxml_query):
    """
    Extract the entity name from a FetchXML query.

    Args:
        fetchxml_query (str): The FetchXML query as a string.

    Returns:
        str: The name of the entity being queried.
    """
    try:
        root = ET.fromstring(fetchxml_query)
        entity_name = root.find(".//entity").attrib["name"]
        return entity_name
    except ET.ParseError as e:
        logger.error(f"Error parsing FetchXML query: {e}", exc_info=True)
        raise
    except AttributeError as e:
        logger.error(f"Error finding entity name in FetchXML query: {e}", exc_info=True)
        raise

def pluralize_entity_name(entity_name):
    """
    Pluralize the entity name to match Dataverse entity set naming conventions.

    Args:
        entity_name (str): The singular entity name.

    Returns:
        str: The pluralized entity set name.
    """
    if entity_name.endswith('y'):
        return entity_name[:-1] + 'ies'
    elif entity_name.endswith('s'):
        return entity_name + 'es'
    else:
        return entity_name + 's'

def execute_fetchxml_query(access_token, fetchxml_queries, base_url, temp_storage_file):
    """
    Fetch data from Dataverse using the FetchXML queries.

    Args:
        access_token (str): The access token for authenticating API requests.
        fetchxml_queries (list): List of FetchXML queries as strings.
        base_url (str): The base URL of the Dataverse instance.
        temp_storage_file (str): Path to the file where the raw data will be temporarily stored.

    Returns:
        list: A list of dictionaries containing the fetched data.
    """
    all_data = []
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json",
        "OData-MaxVersion": "4.0",
        "OData-Version": "4.0",
        "Prefer": "odata.include-annotations=\"*\""
    }

    for fetchxml_query in fetchxml_queries:
        # Extract the entity name from the FetchXML query
        entity_name = extract_entity_name(fetchxml_query)
        # Pluralize the entity name to get the entity set name
        entity_set = pluralize_entity_name(entity_name)
        # Construct the correct URL using the entity set name
        url = f"{base_url}/api/data/v9.1/{entity_set}?fetchXml={quote(fetchxml_query)}"
        logger.debug(f"FetchXML Query URL: {url}")

        while url:
            try:
                response = requests.get(url, headers=headers)
                response.raise_for_status()
                data = response.json().get('value', [])
                all_data.extend(data)
                url = response.json().get('@odata.nextLink', None)
            except requests.RequestException as e:
                logger.error(f"Error fetching data: {e}", exc_info=True)
                raise

    save_to_temp_storage(all_data, temp_storage_file)
    return all_data

# Additional functions can be added here as needed
def read_fetchxml(file_path):
    """
    Read a FetchXML query from a file.

    Args:
        file_path (str): Path to the FetchXML file.

    Returns:
        str: The FetchXML query as a string.
    """
    try:
        tree = ET.parse(file_path)
        root = tree.getroot()
        fetchxml_query = ET.tostring(root, encoding='unicode')
        logger.info(f"Read FetchXML query from {file_path}.")
        return fetchxml_query
    except ET.ParseError as e:
        logger.error(f"Error parsing FetchXML file {file_path}: {e}", exc_info=True)
        raise
