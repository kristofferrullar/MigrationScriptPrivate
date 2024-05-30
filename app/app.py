from flask import Flask, request, render_template
from migration_scripts import get_access_token, execute_fetchxml_query, read_fetchxml, load_data_to_target, transform_data, setup_logging, load_config
import logging
from migration_scripts.utilities import inspect_temp_data

# Import the inspection function

# Initialize Flask app
app = Flask(__name__)

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

@app.route('/')
def index():
    # Load configuration from 'config.json'
    config = load_config('config.json')
    fetchxml_files = config.get('fetchxml_files', [])
    logger.debug(f"FetchXML files from config: {fetchxml_files}")
    return render_template('index.html', fetchxml_files=fetchxml_files)

@app.route('/migrate', methods=['POST'])
def migrate_data():
    try:
        # Load configuration from 'config.json'
        config = load_config('config.json')
        
        # Extract required values from the configuration
        tenant_id = config['tenant_id']
        client_id = config['client_id']
        client_secret = config['client_secret']
        source_base_url = config['source_base_url']
        target_base_url = config['target_base_url']
        fetchxml_files = config['fetchxml_files']
        user_mapping = config['user_mapping']
        date_field = config['date_field']
        date_value = config['date_value']
        batch_config = config['batch_config']
        target_db_type = config['target_db_type']
        
        # Define file names for temporary and transformed data
        temp_storage_file = 'temp_data.json'
        transformed_storage_file = 'transformed_data.json'

        # Authenticate to source Dataverse
        source_access_token = get_access_token(client_id, client_secret, tenant_id, source_base_url)
        # Authenticate to target Dataverse
        target_access_token = get_access_token(client_id, client_secret, tenant_id, target_base_url)
        
        # Read FetchXML queries from files
        fetchxml_queries = [read_fetchxml(file) for file in fetchxml_files]
        
        # Extract data from source using FetchXML queries
        raw_data = execute_fetchxml_query(source_access_token, fetchxml_queries, source_base_url, temp_storage_file)
        logger.debug(f"Extracted raw data: {raw_data}")
        
        # Transform the raw data
        transformed_data = transform_data(temp_storage_file, transformed_storage_file, user_mapping, date_field, date_value, target_db_type)
        logger.debug(f"Transformed data: {transformed_data}")
        
        # Inspect the transformed data
        logger.info(f"Transformed data: {transformed_data}")
        
        # Load transformed data to target
        load_data_to_target(transformed_data, target_base_url, batch_config, target_access_token)
        
        return "Migration completed successfully!"
    except Exception as e:
        logger.error(f"Migration failed: {e}", exc_info=True)
        return "Migration failed. Check logs for details.", 500

if __name__ == '__main__':
    # Run the inspection to see the raw data structure
    inspect_temp_data('temp_data.json')
    
    app.run(debug=True)
