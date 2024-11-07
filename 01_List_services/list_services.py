########################################## Author: Ayyaz Mahmood Paracha ########################################
########################################## Date: Nov 07 2024 ####################################################
########################################## List all services published on ArcGIS Server Site ####################

import csv
import os, time, configparser, logging, sys
from arcgis.gis.server import Server
############################## START THE PROCESS ##############################################
timeStart = time.time()
taskname = 'Services_Cleanup'
############################## CREATE LOG FILE ##############################################
WorkSpaceFolder = os.path.dirname(__file__)
time_stamp = str(time.strftime("%Hh%Mm%Ss",time.gmtime(timeStart)))
log_file_name = taskname + "_" + time_stamp + ".txt"
log_file = log_file = os.path.join(WorkSpaceFolder, log_file_name)
handlers = [logging.FileHandler(log_file), logging.StreamHandler()]
# Configuring logging settings
logging.basicConfig(
    format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S',
    level=logging.INFO,
    handlers=handlers)
############################## READ INPUT ARGUMENTS (CONFUG FILE) ###########################
Config = configparser.ConfigParser()
Config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), "config.ini"))
############################## READ INPUT SOURCE VARIBALES ##################################
targetServer = Config.get('target', 'targetServer')
logging.info("Target ArcGIS Enterprise Server to list is : " + targetServer)
targetServerTokenEndpoint = Config.get('target', 'targetServerTokenEndpoint')
logging.info("Target ArcGIS Enterprise Server Token Endpoint is : " + targetServerTokenEndpoint)
targetUserName = Config.get('target', 'targetUserName')
logging.info("Target ArcGIS Enterprise Portal Enterprise User is : " + targetUserName)
targetPassword = Config.get('target', 'targetPassword')
############################## Connect to Portal ###########################
############################## Connect to ArcGIS Server ###########################
# Connect to your ArcGIS Server
gis_admin_object = Server(url = targetServer, token_url = targetServerTokenEndpoint, username = targetUserName, password = targetPassword)
gis_server_token = gis_admin_object._con.token
logging.info("The Token generated for Target ArcGIS Server is " + gis_server_token)
##################################### CREATE CSV FILE #################################
fieldnames_services = ['Service_Name', 'Folder_Name', 'Service_Type', 'ProviderName', 'minimum_instace', 'maximum_instace', 'configured_state']
CSVReport = 'Service_List' + time_stamp + '.csv'
target_CsvFile = os.path.join(WorkSpaceFolder,CSVReport)
if not os.path.exists(target_CsvFile):
    with open(target_CsvFile, 'a', newline='\n') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_services)
        writer.writeheader()

############################## Iterate Over Gis  Object ###########################

services_in_root = gis_admin_object.services.list()
for service in services_in_root:
        logging.info('Iterating Over Root Folder')
        Folder_Name = 'ROOT FOLDER'
        Service_Name = service.properties.serviceName
        ProviderName = service.properties.provider
        Service_Type = service.properties.type
        minimum_instace = service.properties.minInstancesPerNode
        maximum_instace = service.properties.maxInstancesPerNode
        configured_state = service.properties.configuredState

        with open(target_CsvFile, 'a', newline='\n') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames_services)
                writer.writerow({'Service_Name':Service_Name, 'Folder_Name':Folder_Name, 'ProviderName':ProviderName,
                                 'Service_Type':Service_Type, 'minimum_instace':minimum_instace, 'maximum_instace':maximum_instace,
                                 'configured_state':configured_state})


folders = gis_admin_object.content.folders
for folder in folders:
        logging.info('Iterating Over ' + folder + ' Folder')

        services_in_root = gis_admin_object.services.list(folder=folder)
        for service in services_in_root:
                Folder_Name = folder
                Service_Name = service.properties.serviceName
                ProviderName = service.properties.provider
                Service_Type = service.properties.type
                minimum_instace = service.properties.minInstancesPerNode
                maximum_instace = service.properties.maxInstancesPerNode
                configured_state = service.properties.configuredState

                with open(target_CsvFile, 'a', newline='\n') as csvfile:
                        writer = csv.DictWriter(csvfile, fieldnames=fieldnames_services)
                        writer.writerow({'Service_Name':Service_Name, 'Folder_Name':Folder_Name, 'ProviderName':ProviderName,
                                'Service_Type':Service_Type, 'minimum_instace':minimum_instace, 'maximum_instace':maximum_instace,
                                'configured_state':configured_state})      
logging.info("The end of process")