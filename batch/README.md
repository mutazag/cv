# 1. batch processing using AZ Machine Learning


<!-- TOC -->

- [1. batch processing using AZ Machine Learning](#1-batch-processing-using-az-machine-learning)
    - [1.1. References](#11-references)
- [2. Code Structure](#2-code-structure)
    - [2.1. Authenticate to AML](#21-authenticate-to-aml)
    - [2.2. Create AML Artefacts](#22-create-aml-artefacts)
    - [2.3. Scoring script](#23-scoring-script)
    - [2.4. Parallel Run Config and Step](#24-parallel-run-config-and-step)
    - [2.5. Calling AML Pipeline from ADF](#25-calling-aml-pipeline-from-adf)
        - [2.5.1. Parametrise the Pipeline](#251-parametrise-the-pipeline)
        - [2.5.2. Parameterise Datasets](#252-parameterise-datasets)
    - [2.6. Workflow](#26-workflow)

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

## 2.1. Authenticate to AML

Download the `config.json` from AML: [link](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-manage-workspace#download-a-configuration-file).
It is best to place the `config.json` file inside a subfolder name `.azureml`, then add the subfolder to `.gitignore`.

Install libraries from `requirements.txt`.

Running `ws.from_config()` will authenticate using login page, follow instructions [here](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-setup-authentication#use-a-service-principal-from-the-sdk) to setup service principal authentication.

## 2.2. Create AML Artefacts

Key artefacts that should be created in the Azure ML workspace:
* Datasources: blog storage for images with access/authentation. if Azure Blob then use Access Keys
* Datasets: datasets in datasources, in this case the images folder in datasource, dataset will be mapped as input to the pipeline step, and is going to be mounted as a /tmp/ folder in the container instance runnig the python task
* compute cluster: using AML compute for now
* Experiment object: to be the host of pipeline - will be autocrated when pipline is submited
* model object: not required and could do without, will be required if processs is improved to use custom model instead of cog services
* key vault secrets: outside of AML, add secrets needed by the process, specially the python scoring script, into keyvault

## 2.3. Scoring script


entry script file to be passed on to the ParallelRunConfig, minibatch process file is invoked by the pipeline to process one minibatch at a time
key components in the file are:
- init() function:
    is called to initialise process, arguments are parsed here, include all intiialisation steps here, like retrieving urls for cog services or other required settings arguments are passed on from ParallelRunStep as specified by the `arugments` param
- run(mini_batch) function:
    run function will recieve a minibatch list of items to be processed in the task instance, the returned value of run function is then appended to the output result set if output_action (in ParallelRunConfig) was set to 'append_row'



azureml libraries are imported of scripts needs access to aml artefacts this could be if scripts needs to download a model file or log metrics no need to reach out to data sets from python script as all data will be setup using input or pipelinedata datasets which will make it appear as local files in the container instance that runs the task

datasets in pipeline can be retrieved using `Run.input_datasets`. `Run.get_context()` provide access to the contes of the current run, and access to retrieve associated experient and wrkspace: `ws = Run.get_context().experiment.workspace`.


## 2.4. Parallel Run Config and Step


The ParallelRunConfig class is used to provide configuration for the ParallelRunStep class. The two are used to for processing large amounts of data in parallel. In this case, we will be processing large number of files on daily basis, and want the ability to distrubte the processing of files to be processed in parallel on a batch cluster that is specified by the AML compute option.

ParallelRunStep works by breaking up your data into batches that are processed in parallel. The batch size, node count, and other tunable parameters to speed up your parallel processing can be controlled with the ParallelRunConfig class.


To use ParallelRunStep and ParallelRunConfig:

* Create a ParallelRunConfig object to specify how batch processing is performed, with parameters to control batch size, number of nodes per compute target, * and a reference to your custom Python script.
* Create a ParallelRunStep object that uses the ParallelRunConfig object, defines inputs and outputs for the step.
* Use the configured ParallelRunStep object in a Pipeline just as you would with other pipeline step types.

```python
ParallelRunConfig(environment, entry_script, error_threshold, output_action, compute_target, node_count, process_count_per_node=None, mini_batch_size=None, source_directory=None, description=None, logging_level='INFO', run_invocation_timeout=60, run_max_try=3, append_row_file_name=None)
```

- `output_action=append_row`: all values output by `run()` method will be aggregated into one unique file specified by `append_row_file_name`, if no file name is provided, results are appended into file `parallel_run_step.txt`
- `entry_script` and `source_direcoty` specify the code files to be copied over to the docker container

ParallelRunConfig can be authored declaretively using yamp, parking this option for another day!

```python
ParallelRunStep(name, parallel_run_config, inputs, output=None, side_inputs=None, arguments=None, allow_reuse=True)
```

- `inputs`: list of input data sets, this will be the images data set, this list will be *mounted* locally on the container filesystem. Datasets referenced *as download* will be copied to the compute, but if dataset is large, best to reference it *as mount* [to avoid downloading very large](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-train-with-datasets#mount-vs-download) data sets to compute conainers.
    ```python
    inputs=[anpr_images.as_named_inputs('images').as_mount()]
    ```
- `outputs`: pipeline data that could be used for later steps, An object reference in the outputs array becomes available as an input for a subsequent pipeline step, for scenarios where there is more than one step.
- `arguments`: command line argues that are passed to the entry script, these are parsed in the `init()` function. these areguments need to be passed into the pipeline from ADF - more on that later.
        ```python
        arguments=['--input_partition', '2020/08/07', '--kv_customimage', 'customimagesecret', '--kv_readapi', 'readapisecret']
        ```


## 2.5. Calling AML Pipeline from ADF

After AML pipeline is published, ADF will orchastrate rerunnig the pipeline on new data as specified by the input_partition param. ADF will use the azure machine learning pipeline step, passing in parameters to control the execution. these parameters will then be packaged and passed into the pythn step.


When you first run a pipeline, Azure Machine Learning:

* Downloads the project snapshot to the compute target from the Blob storage associated with the workspace.
* Builds a Docker image corresponding to each step in the pipeline.
* Downloads the Docker image for each step to the compute target from the container registry.
* Configures access to Dataset and PipelineData objects. For as as_mount() access mode, FUSE is used to provide virtual access. If mount is not supported or if the user specified access as as_download(), the data is instead copied to the compute target.
* Runs the step in the compute target specified in the step definition.
* Creates artifacts, such as logs, stdout and stderr, metrics, and output specified by the step. These artifacts are then uploaded and kept in the user's  default datastore.

![pipeline_flow](https://docs.microsoft.com/en-us/azure/machine-learning/media/how-to-create-your-first-pipeline/run_an_experiment_as_a_pipeline.png)



### 2.5.1. Parametrise the Pipeline

* Use `PipelineParameter` to [create/retrieve a pipeline argument](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-create-your-first-pipeline#publish-a-pipeline).
* Pipeline argument then can be used in pipeline steps, example python step arguments can now refer to pipeline argument string
* ADF will feed in the pipeline parameters when calling the AML pipeline step
* Pass a parameter values to a published pipeline using the `ParameterAssignment` argument
* Dynamic datasets cannot be passed using `ParameterAssignment`, instead `DatasetDefinitionValueAssignments` must be used.


To pass a parameter using `ParameterAssignment` in REST api call:

```python

response = requests.post(pipeline_endpoint,
                         headers=auth_header,
                         json={'ExperimentName': 'BatchScoringPipelineExp-datasetinput',
                               'ParameterAssignments': {
                                   'pipeline_inpart': 'partition1',
                                    'pipeline_kv_customimg': '123',
                                    'pipeline_kv_readapi': '342'}})
```


The same can be achieved in ADF when using the [Machine Learning Execute Pipeline](https://docs.microsoft.com/en-us/azure/data-factory/transform-data-machine-learning-service) activity type

![batch\adf_aml_pipeline_execute_params](batch/adf_aml_pipeline_execute_params.png)

### 2.5.2. Parameterise Datasets

`azureml` python sdk allows passing datasets as params
Passing a dataset as paramater to a published pipeline as achieved through  using the `DatasetDefinitionValueAssignments` in REST api.

## 2.6. Workflow

![Impressions](https://PixelServer20190423114238.azurewebsites.net/api/impressions/MachineLearningNotebooks/how-to-use-azureml/README.png)