# DD2476_project
KTH students while they are doing their own course and project work. In order to help students finding relevant code at GitHub, we introduce the search engine **K**, which allows students to search for Python code snippet related their courses.

## Set up before running the search engine

### Elastic search

#### Install Elastic search:  
https://www.elastic.co/downloads/elasticsearch

#### Recover our elastic search index
Create a recovery folder where to store it. 
Make sure the to all the permissions to every user of that folder
On linux and MACOS: chmod 777 (recovery folder)

#### Download our index data
Now download the zip file at this link: [Backup](https://drive.google.com/file/d/1D7F5iBnQwOBlDnYWfRe2K8m25D9YxUlT/view?usp=sharing) 
Unzip it into the recovery folder. 

#### Edit the elastic search configuration file
Path to the file: ```(Root of ElasticSearch Program)/config/elasticsearch.yml```

Add the following line to the end of the file
```
path.repo: (Path of the folder you want to save the index in)
```
#### Run the following HTTP requests
Now we need to register the folder for the snapshot
For this, send those two HTTP PUT requests with the following body: 
```
{
  "type": "fs",
  "settings": {
    "location": (address of the recovery folder),
    "compress": true
  }
}
```

Firstly to the address: http://localhost:9200/_snapshot/backup/
You should get the following response:
```
{
    "acknowledged": true
}
```

Secondly to the address: http://localhost:9200/_snapshot/backup/krawlubv2/_restore
You should get the following response:
```
{
    "accepted": true
}
```
### Install the dependencies 
Run the following command in the shell in the root of the folder
```
pip install -r requirements.txt
```

## Run the Search engine
Run following command on the shell in the root folder
```
python main.py
```

## Known bugs

### KivyMD bug
Fix the kivyMD bug
The GUI will not start due to a bug in the DataTables component of KivyMD. In order to run it correctly:
1. Try to run the GUI
2. Go to the python file where the error occurs (kivymd/uix/datatables.py), a link will be shown in Python's error message.
3. Remove the line 'orientation: "vertical"' in class MDDataTable (row 167)
4. Re-run the GUI
