# DD2476_project

Fix kivyMD bug:
The GUI will not start due to a bug in the DataTables component of KivyMD. In order to run it correctly:
1. Go to kivymd/uix/datatables.py
2. Remove the line "orientation: "vertical" in class MDDataTable (row 994)
3. Re-run the GUI
