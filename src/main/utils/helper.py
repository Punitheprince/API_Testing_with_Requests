import json
def get_headers():
    header_file_path = '../../resources/req_spec/headers/header.json'
    # -------------------------------
    # Load headers
    # -------------------------------
    with open(header_file_path, 'r') as file:
        header_data = json.load(file)

    # Ensure header values are strings
    header_data = {k: str(v) for k, v in header_data.items()}

    return header_data

