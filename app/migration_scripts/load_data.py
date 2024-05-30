# load_data.py

import requests
import logging

logger = logging.getLogger(__name__)

def load_data_to_target(data, target_base_url, batch_config, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    for table, batch_order in sorted(batch_config.items(), key=lambda item: item[1]):
        table_data = [item for item in data if item.get('logical_name') == table]
        logger.info(f"Loading data for table {table} with batch order {batch_order}. Total records: {len(table_data)}")

        for item in table_data:
            try:
                item.pop('logical_name', None)  # Ensure logical_name is not in the payload
                url = f"{target_base_url}/api/data/v9.1/{table}s"
                logger.debug(f"Loading record into table {table} with URL: {url}")
                logger.debug(f"Data to be sent: {item}")
                
                response = requests.post(url, headers=headers, json=item)
                response.raise_for_status()
                
                logger.info(f"Successfully loaded record with ID {item.get('id', 'unknown')} into table {table}. Response: {response.json()}")
            except requests.RequestException as e:
                error_message = e.response.text if e.response else str(e)
                logger.error(f"Error loading record with ID {item.get('id', 'unknown')} into table {table}: {error_message}", exc_info=True)

                if e.response is not None:
                    logger.error(f"Request URL: {url}")
                    logger.error(f"Request Headers: {headers}")
                    logger.error(f"Request Payload: {item}")
                    logger.error(f"Response Status Code: {e.response.status_code}")
                    logger.error(f"Response Text: {e.response.text}")
