import os
import shutil
from datetime import datetime
import time

now = datetime.now()
now_string = now.strftime("%d/%m/%Y %H:%M:%S")

source_folder_path = input("Input source folder's path: ")
replica_folder_path = input("Input replica folder's path: ")
sync_interval = int(input("Input sync interval (in minutes): "))

source_folder_content = os.listdir(source_folder_path)
replica_folder_content = os.listdir(replica_folder_path)

def refresh_folder_content():
    global source_folder_content
    global replica_folder_content
    source_folder_content = os.listdir(source_folder_path)
    replica_folder_content = os.listdir(replica_folder_path)

def sync_folders(source_folder_content, source_folder_path, replica_folder_content, replica_folder_path):
    for file in source_folder_content:
        if file not in replica_folder_content:
            if os.path.isfile(source_folder_path+f"\{file}"):
                shutil.copy(source_folder_path+f"\{file}", replica_folder_path)
                print(f"{file} copied from source folder to replica folder")
                with open("Sync log.txt", "a") as log:
                    log.write(f"{now_string} - {file} copied from source folder to replica folder")
                    log.write("\n")
            if os.path.isdir(source_folder_path+f"\{file}"):
                print(replica_folder_content)
                shutil.copytree(source_folder_path+f"\{file}", replica_folder_path+f"\{file}")
                print(f"{file} and its content copied from source folder to replica folder")
                with open("Sync log.txt", "a") as log:
                    log.write(f"{now_string} - {file} and its content copied from source folder to replica folder")
                    log.write("\n")
        else:
            if os.path.isdir(source_folder_path+f"\{file}"):
                new_source_folder_path = source_folder_path+f"\{file}"
                new_replica_folder_path = replica_folder_path+f"\{file}"
                new_source_folder_content = os.listdir(new_source_folder_path)
                new_replica_folder_content = os.listdir(new_replica_folder_path)
                sync_folders(new_source_folder_content, new_source_folder_path, new_replica_folder_content, new_replica_folder_path)

    for file in replica_folder_content:
        if file not in source_folder_content:
            if os.path.isfile(replica_folder_path+f"\{file}"):
                os.remove(replica_folder_path+f"\{file}")
                print(f"{file} removed from replica folder")
                with open("Sync log.txt", "a") as log:
                    log.write(f"{now_string} - {file} removed from replica folder")
                    log.write("\n")
            if os.path.isdir(replica_folder_path+f"\{file}"):
                shutil.rmtree(replica_folder_path+f"\{file}", ignore_errors=True)
                print(f"{file} and its content removed from replica folder")
                with open("Sync log.txt", "a") as log:
                    log.write(f"{now_string} - {file} and its content removed from replica folder")
                    log.write("\n")
        else:
            if os.path.isdir(replica_folder_path+f"\{file}"):
                new_source_folder_path = source_folder_path+f"\{file}"
                new_replica_folder_path = replica_folder_path+f"\{file}"
                new_source_folder_content = os.listdir(new_source_folder_path)
                new_replica_folder_content = os.listdir(new_replica_folder_path)
                sync_folders(new_source_folder_content, new_source_folder_path, new_replica_folder_content, new_replica_folder_path)


if __name__ == "__main__":
    while True:

        sync_folders(source_folder_content, source_folder_path, replica_folder_content, replica_folder_path)
        time.sleep(sync_interval*60)
        refresh_folder_content()
