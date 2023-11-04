import streamlit as st
import json
import os
import base64
from zipfile import ZipFile
import tempfile

# Step 1: Read the query parameters
query_params = st.experimental_get_query_params()
serialized_project = query_params.get('project', [None])[0]

# This function will parse the serialized project data and create a ZIP file
def create_zip_from_serialized_data(serialized_data):
    # Step 2: Parse the serialized data
    project_data = json.loads(serialized_data)

    # Step 3: Create files and folders
    with tempfile.TemporaryDirectory() as tmpdirname:
        for path, content in project_data.items():
            # Make sure the folder structure exists
            os.makedirs(os.path.join(tmpdirname, os.path.dirname(path)), exist_ok=True)
            # Write the file content
            with open(os.path.join(tmpdirname, path), 'w') as file:
                file.write(content)

        # Step 4: Compress to ZIP
        zip_path = os.path.join(tmpdirname, 'project.zip')
        with ZipFile(zip_path, 'w') as zipf:
            for root, dirs, files in os.walk(tmpdirname):
                for file in files:
                    zipf.write(os.path.join(root, file), 
                               os.path.relpath(os.path.join(root, file), 
                               os.path.join(tmpdirname, '..')))

        # Read the created ZIP file and encode it to Base64
        with open(zip_path, 'rb') as zipf:
            encoded_zip = base64.b64encode(zipf.read()).decode()

    return encoded_zip

# Step 5: Serve the ZIP file
if serialized_project:
    zip_base64 = create_zip_from_serialized_data(serialized_project)
    st.download_button(
        label="Download ZIP",
        data=base64.b64decode(zip_base64),
        file_name="project.zip",
        mime="application/zip"
    )

# Instructions for the user
st.write("Please provide the serialized project as a query parameter named 'project'.")
