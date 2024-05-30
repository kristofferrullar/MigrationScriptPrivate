import unittest
import logging
import app
from migration_scripts.authenticate import authenticate_to_dataverse
from migration_scripts.extract_data_logic import fetch_all_data
from migration_scripts.transform_data import transform_data
from migration_scripts.load_data import load_data_into_target

class TestMigrationScripts(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        logging.basicConfig(filename='application.log', level=logging.DEBUG)
        logging.debug('Starting a new test suite')
        cls.config = app.load_config()
        logging.debug(f"Configuration for tests: {cls.config}")

    def setUp(self):
        logging.debug('Starting a new test case')

    def test_load_config(self):
        try:
            config = app.load_config()
            self.assertIsNotNone(config)
            logging.debug(f"Test load_config passed with config: {config}")
        except Exception as e:
            logging.error(f"Test load_config failed: {e}")
            self.fail(f"load_config raised an exception: {e}")

    def test_load_fetchxml(self):
        try:
            filename = self.config.get('fetchxml_filename', 'sample_fetch.xml')  # Ensure this file exists
            xml_string = app.load_fetchxml(filename)
            self.assertTrue(xml_string.startswith('<fetch'))
            logging.debug(f"Test load_fetchxml passed with XML: {xml_string}")
        except Exception as e:
            logging.error(f"Test load_fetchxml failed: {e}")
            self.fail(f"load_fetchxml raised an exception: {e}")

    def test_authenticate_to_dataverse(self):
        try:
            access_token = authenticate_to_dataverse(self.config['tenant_id'], self.config['client_id'], self.config['client_secret'])
            self.assertIsNotNone(access_token)
            logging.debug(f"Test authenticate_to_dataverse passed with token: {access_token}")
        except Exception as e:
            logging.error(f"Test authenticate_to_dataverse failed: {e}")
            self.fail(f"authenticate_to_dataverse raised an exception: {e}")

    def test_fetch_all_data(self):
        try:
            access_token = authenticate_to_dataverse(self.config['tenant_id'], self.config['client_id'], self.config['client_secret'])
            fetchxml_query = app.load_fetchxml(self.config.get('fetchxml_filename', 'sample_fetch.xml'))  # Ensure this file exists
            data = fetch_all_data(access_token, self.config['source_base_url'], fetchxml_query)
            self.assertIsInstance(data, list)
            logging.debug(f"Test fetch_all_data passed with data: {data}")
        except Exception as e:
            logging.error(f"Test fetch_all_data failed: {e}")
            self.fail(f"fetch_all_data raised an exception: {e}")

    def test_transform_data(self):
        try:
            sample_data = [{'sample_key': 'sample_value'}]  # Use actual sample data structure
            transformed_data = transform_data(sample_data, self.config['user_mapping'], self.config['masking_fields'], self.config['batch_config'])
            self.assertIsInstance(transformed_data, dict)  # Assuming the transformed data is returned as a dict
            logging.debug(f"Test transform_data passed with transformed data: {transformed_data}")
        except Exception as e:
            logging.error(f"Test transform_data failed: {e}")
            self.fail(f"transform_data raised an exception: {e}")

    def test_load_data_into_target(self):
        try:
            sample_transformed_data = {'sample_entity': [{'sample_key': 'sample_value'}]}  # Use actual sample transformed data structure
            access_token = authenticate_to_dataverse(self.config['tenant_id'], self.config['client_id'], self.config['client_secret'])
            load_results = load_data_into_target(sample_transformed_data, access_token, self.config['target_base_url'])
            self.assertIsInstance(load_results, dict)
            logging.debug(f"Test load_data_into_target passed with load results: {load_results}")
        except Exception as e:
            logging.error(f"Test load_data_into_target failed: {e}")
            self.fail(f"load_data_into_target raised an exception: {e}")

if __name__ == '__main__':
    unittest.main()
