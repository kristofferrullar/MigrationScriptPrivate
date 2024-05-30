import os
import nbformat as nbf

# Define the base directory of your project
base_dir = r'C:\\Users\\KristofferAllåker\\ProfDevToCustomer\\OX2\\DataMigrationProject\\app'

# List of script files to include in the notebook with relative paths
script_files = [
    'migration_scripts/utilities.py',
    'migration_scripts/authenticate.py',
    'migration_scripts/extract_data_logic.py',
    'migration_scripts/transform_data.py',
    'migration_scripts/load_data.py',
]

# Create a new notebook
nb = nbf.v4.new_notebook()

# Function to read a script file and create a cell
def script_to_cell(script_file):
    script_path = os.path.join(base_dir, script_file)
    with open(script_path, 'r') as file:
        code = file.read()
    return nbf.v4.new_code_cell(f"# %load {script_file}\n\n{code}")

# Create cells from script files
cells = [script_to_cell(script_file) for script_file in script_files]

# Add an additional cell to run the test code
test_code = """
# Load configuration
config = load_config('config.json')

# Test authentication
access_token = get_access_token(config['client_id'], config['client_secret'], config['tenant_id'], config['source_base_url'])
print(f"Access Token: {access_token}")

# Test data extraction
fetchxml_queries = [read_fetchxml(file) for file in config['fetchxml_files']]
raw_data = execute_fetchxml_query(access_token, fetchxml_queries, config['source_base_url'], 'temp_data.json')
print(f"Data Extracted: {len(raw_data)} records")

# Test data transformation
transformed_data = transform_data('temp_data.json', 'transformed_data.json', config['user_mapping'], config['date_field'], config['date_value'])
print(f"Data Transformed: {len(transformed_data)} records")

# Test data loading
load_data_to_target(transformed_data, config['target_base_url'], config['batch_config'])
print("Data Loaded Successfully")
"""

cells.append(nbf.v4.new_code_cell(test_code))

# Add cells to the notebook
nb['cells'] = cells

# Write the notebook to a file
notebook_path = os.path.join(base_dir, 'DataMigrationTesting.ipynb')
with open(notebook_path, 'w') as f:
    nbf.write(nb, f)

print(f"Notebook {notebook_path} has been created.")
