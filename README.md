# DD2476_project

## Install elastic search elasticsearch-7.12.1
Link
## Recover the elastic search index
Create a recovery folder where to store it. 
Make sure the to all the permissions to every user of that folder
On linux and MACOS: chmod 777 (recovery folder)
### Edit the elastic search configuration file
Path: (Root of ElasticSearch Program)/config/elasticsearch.yml
Add the following line to the end of the file
path.repo: (Path of the folder you want to save the index in)

### Open Postman
Now we need to register the folder for the snapshot
For this, send those two HTTP PUT requests with the following body: 
{
  "type": "fs",
  "settings": {
    "location": (address of the recovery folder),
    "compress": true
  }
}

Now download the following zip file and unzip it into the recovery folder

Firstly to the address: http://localhost:9200/_snapshot/backup/
You should get the following response:
{
    "acknowledged": true
}

Secondly to the address: http://localhost:9200/_snapshot/backup/krawlub/_restore
You should get the following response:
{
    "accepted": true
}

### Fix a KivyMD bug
Fix kivyMD bug:
The GUI will not start due to a bug in the DataTables component of KivyMD. In order to run it correctly:
1. Try to run the GUI
2. Go to the python file where the error occurs (kivymd/uix/datatables.py), a link will be shown in Python's error message.
3. Remove the line 'orientation: "vertical"' in class MDDataTable (row 167)
4. Re-run the GUI
