# 1. batch processing using AZ Machine Learning 


<!-- TOC -->

- [1. batch processing using AZ Machine Learning](#1-batch-processing-using-az-machine-learning)
    - [1.1. References](#11-references)
- [2. Code Structure](#2-code-structure)
    - [Authenticate to AML](#authenticate-to-aml)
    - [2.1. Parallel Run Config](#21-parallel-run-config)
    - [2.2. Workflow](#22-workflow)

<!-- /TOC -->

## 1.1. References 


* [Setup for Tutorials](https://docs.microsoft.com/en-us/azure/machine-learning/tutorial-1st-experiment-sdk-setup)
* [Tutorial](https://docs.microsoft.com/en-us/azure/machine-learning/tutorial-pipeline-batch-scoring-classification)
* [Parallel Run Config](https://docs.microsoft.com/en-us/python/api/azureml-pipeline-steps/azureml.pipeline.steps.parallelrunconfig?view=azure-ml-py)



# 2. Code Structure

The following is the code structure for the python notebook that drives the AML batch configuration: 
1. Connect and authentication to AML 
2. Test key vault access from driver notebook
3. Attach DataStore for blob, requires AML authentication on data store
4. Create a dataset for image folders 
5. Create a minibatch processing py script: 
    5.1. `init()`: access to keyvault, get secrets required by scripts
    5.2. `run()`: iterate over mini batch and append row to output

## Authenticate to AML 

Download the `config.json` from AML: [link](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace#download-a-configuration-file). 
It is best to place the `config.json` file inside a subfolder name `.azureml`, then add the subfolder to `.gitignore`. 

Install libraries from `requirements.txt`.

Running `ws.from_config()` will authenticate using login page, follow instructions [here](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-setup-authentication#use-a-service-principal-from-the-sdk) to setup service principal authentication. 
## 2.1. Parallel Run Config


## 2.2. Workflow 

![Impressions](https://PixelServer20190423114238.azurewebsites.net/api/impressions/MachineLearningNotebooks/how-to-use-azureml/README.png)