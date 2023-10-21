import os
from chattdd.tools import load_config


def write_to_file(content, filename):
    config = load_config()
    output_folder = config['OUTPUTFOLDER']
    file_path = os.path.join(output_folder, filename)
    
    if not os.path.exists(file_path):
        directory = os.path.dirname(file_path)
        if directory and not os.path.exists(directory):  # check if directory is not empty
            os.makedirs(directory)
        with open(file_path, 'w') as f:
            f.write(content)
        print(f"File {file_path} has been created.")
    else:
        decision = input(f"File {file_path} already exists. Replace (R), Append (A), or Cancel (C)? ").upper()
        if decision == "R":
            with open(file_path, 'w') as f:
                f.write(content)
            print(f"File {file_path} has been replaced.")
        elif decision == "A":
            print("Append operation: Not implemented yet.")
        else:
            print("Operation cancelled.")
