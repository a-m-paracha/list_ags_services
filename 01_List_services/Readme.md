The script can be run from any machine where ArcGIS Pro or ArcGIS Server is installed
It needs Python3.x along with ArcGIS API for python
in config.ini file following parameters are requried: 

targetServer = This is target server admin endpoint the format is https://server.esri.com:6443/arcgis/admin
targetServerTokenEndpoint = This is target server token generation endpoint the format is https://server.esri.com:6443/arcgis/tokens/generateToken
targetUserName = ArcGIS Server Site admin username
targetPassword = ArcGIS Server Site admin Password

The script is run by command --> python.exe list_services.py

This generates a log file along with CSV file which contains all service properties