import logging
from .utilities import load_from_temp_storage, save_to_temp_storage

logger = logging.getLogger(__name__)

def transform_data(temp_storage_file, transformed_storage_file, user_mapping, date_field, date_value, target_db_type):
    """
    Transform the data by updating the owner and date fields based on target database type.

    Args:
        temp_storage_file (str): Path to the file with raw data.
        transformed_storage_file (str): Path to the file where transformed data will be saved.
        user_mapping (dict): Mapping of old user IDs to new user IDs.
        date_field (str): The field name for date.
        date_value (str): The value to set for the date field.
        target_db_type (str): The type of the target database.

    Returns:
        list: A list of dictionaries containing the transformed data.
    """
    try:
        raw_data = load_from_temp_storage(temp_storage_file)  # Load raw data from temporary storage
        logger.info(f"Raw data: {raw_data}")
        
        transformed_data = []
        for item in raw_data:
            try:
                if target_db_type == "dynamics365":
                    transformed_item = transform_for_dynamics365(item, user_mapping, date_field, date_value)
                else:
                    transformed_item = transform_for_other_db(item, user_mapping, date_field, date_value)
                
                transformed_data.append(transformed_item)  # Add transformed item to the list
                logger.debug(f"Transformed item: {transformed_item}")
            except Exception as e:
                logger.error(f"Error transforming item: {item}, Error: {e}", exc_info=True)

        save_to_temp_storage(transformed_data, transformed_storage_file)  # Save transformed data to temporary storage
        logger.info(f"Transformed data: {transformed_data}")
        logger.info(f"Transformed {len(transformed_data)} records.")
        return transformed_data
    except Exception as e:
        logger.error(f"Error transforming data: {e}", exc_info=True)
        raise

# transform_data.py

# transform_data.py

def transform_for_dynamics365(item, user_mapping, date_field, date_value):
    """
    Transform data for Dynamics 365.

    Args:
        item (dict): The raw data item.
        user_mapping (dict): Mapping of old user IDs to new user IDs.
        date_field (str): The field name for date.
        date_value (str): The value to set for the date field.

    Returns:
        dict: The transformed data item.
    """
    item = item.copy()
    
    logical_name = item.get('Item.crmk_itemid') and 'crmk_item' or \
                   item.get('LandObject.crmk_denominationname') and 'crmk_landobject' or 'crmk_unknown'
    
    # Remove properties not applicable to Dynamics 365
    item.pop('@odata.etag', None)
    item.pop('Item.crmk_itemid@OData.Community.Display.V1.AttributeName', None)
    item.pop('LandObject.crmk_denominationname@OData.Community.Display.V1.AttributeName', None)
    
    # Add or update necessary fields
    item["OwnerId"] = user_mapping.get(item.get("owner_id"), user_mapping["default"])
    
    if logical_name == 'crmk_plant':
        item[date_field] = date_value
        item[date_field] = 'crmk_MigratedOn'

    # Remove invalid properties
    item.pop('logical_name', None)
    item.pop('address1_latitude', None)
    item.pop('description', None)
    item.pop('revenue', None)

    logger.debug(f"Transformed item for Dynamics 365: {item}")
    return item

def transform_for_other_db(item, user_mapping, date_field, date_value):
    """
    Transform data for other target database types.

    Args:
        item (dict): The raw data item.
        user_mapping (dict): Mapping of old user IDs to new user IDs.
        date_field (str): The field name for date.
        date_value (str): The value to set for the date field.

    Returns:
        dict: The transformed data item.
    """
    transformed_item = item.copy()  # Create a copy of the raw data item
    transformed_item["owner"] = user_mapping.get(item.get("owner_id"), user_mapping["default"])  # Add owner field
    transformed_item[date_field] = date_value  # Add date field
    return transformed_item
