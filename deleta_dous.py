import os
import shutil

def deleta_dous_xml(folder_path):
    folder_list = [f for f in os.listdir(folder_path) if os.path.isdir(os.path.join(folder_path, f))]
    for folder_name in folder_list:
        folder_path_to_delete = os.path.join(folder_path, folder_name)
        shutil.rmtree(folder_path_to_delete)
        print(f"Deleted folder: {folder_name}")

# Specify the folder path
folder_path = "C:\\Users\\gab36\\OneDrive\\Documentos\\Development\\fetchDOU\\DOUS"

# Call the function to delete folders in the folder
deleta_dous_xml(folder_path)



