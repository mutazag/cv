import os
import argparse
import pandas as pd

# import datetime
# import time

# from azureml.core import Run
# from azureml.core.model import Model
# from azureml.core.dataset import Dataset
# from azureml.core import Workspace

# import numpy as np
# import pandas

script_args = {}
args = None

def init():
    print('init goes here')
    print('parsing arguments')
    # using argparse for this step
    parser = argparse.ArgumentParser(description='batch processing arguments')
    parser.add_argument('--input_partition', dest='input_partition', required=True)
    parser.add_argument('--kv_customimage', dest='kv_customimage', required=True)
    parser.add_argument('--kv_readapi', dest='kv_readapi')
    parser.add_argument('--metadata_config', dest='metadata_config')
    parser.add_argument('--metadata', dest='metadata')

    global args
    args, _ = parser.parse_known_args()
    print('input partition: ', args.input_partition)
    print('kv customimage: ', args.kv_customimage)
    print('kv readapi: ', args.kv_readapi)
    print('metadatafile: ', args.metadata)
    print('metadata_config: ', args.metadata_config)

    global script_args
    script_args = {
        'input partition': args.input_partition,
        'kv customimage': args.kv_customimage,
        'kv readapi': args.kv_readapi,
        'metadatafile': args.metadata,
        'metadata_config': args.metadata_config
    }


def run(mini_batch):
    print('length of mini batch: ', len(mini_batch))
    print('metadata file: \n\t', script_args['metadata_config'], '\n\t', script_args['metadatafile'])
    metadata_fn = os.path.join(script_args['metadata_config'], script_args['metadatafile'])
    print('args variable')
    print('input partition: ', args.input_partition)
    print('kv customimage: ', args.kv_customimage)
    print('kv readapi: ', args.kv_readapi)
    print('metadatafile: ', args.metadata)
    print('metadata_config: ', args.metadata_config)


    metadata_df = pd.read_csv(metadata_fn)
    print(metadata_df)
    # initalise an empty result list
    result_list = []

    # process files
    for file_path in mini_batch:
        # process file in filepath
        # processed_result = ProcesssImage(file_path, metadatadict)
        # append processing result to a result list
        result_list.append(f'{os.path.basename(file_path)},auditid123,noimagefound,1,2,3,90.9')

    # returned result_list
    return result_list
