import os
#######################################
# params for api
####################################
path_to_models_folder = os.path.join("api","models")
path_to_entire_dataset = os.path.join("data_sets","df_merged_total.csv")

#API url
host_api = "uvicorn"
if host_api == "uvicorn":
    url_base = "http://127.0.0.1:8000"
