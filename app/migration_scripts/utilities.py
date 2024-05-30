import os
import json
import logging

# Create a logger object for this module
logger = logging.getLogger(__name__)

# Function to save data to a temporary storage file
def save_to_temp_storage(data, filename):
    try:
        # Open the file in write mode and dump the data as JSON
        with open(filename, 'w') as file:
            json.dump(data, file)
        # Log a message indicating successful save
        logger.info(f"Data saved to temporary storage file {filename}.")
    except IOError as e:
        # Log an error message if there's an issue saving the data
        logger.error(f"Error saving to temporary storage: {e}", exc_info=True)
        raise

# Function to load data from a temporary storage file
def load_from_temp_storage(filename):
    try:
        # Open the file in read mode and load the data as JSON
        with open(filename, 'r') as file:
            data = json.load(file)
        # Log a message indicating successful load
        logger.info(f"Data loaded from temporary storage file {filename}.")
        return data
    except IOError as e:
        # Log an error message if there's an issue loading the data
        logger.error(f"Error loading from temporary storage: {e}", exc_info=True)
        raise

# Function to set up logging configuration
def setup_logging():
    # Configure the logging level and format
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # Log a message indicating successful setup
    logger.info("Logging is set up.")

# Function to load configuration from a file
def load_config(config_file):
    try:
        # Open the configuration file in read mode and load the data as JSON
        with open(config_file, 'r') as file:
            config = json.load(file)
        # Log a message indicating successful load
        logger.info(f"Configuration loaded from {config_file}.")
        return config
    except IOError as e:
        # Log an error message if there's an issue loading the configuration
        logger.error(f"Error loading configuration file: {e}", exc_info=True)
        raise

# Function to inspect data from a temporary storage file
def inspect_temp_data(temp_storage_file):
    try:
        # Open the file in read mode and load the data as JSON
        with open(temp_storage_file, 'r') as file:
            data = json.load(file)
        # Log a message indicating the inspection of the data
        logger.info(f"Inspection of temp data: {data}")
        return data
    except IOError as e:
        # Log an error message if there's an issue loading the temporary data
        logger.error(f"Error loading temporary data for inspection: {e}", exc_info=True)
        raise
