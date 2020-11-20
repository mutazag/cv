About the logs folder:
logs/
  azureml/    : azureml logs
  user/       : Including errors and logs from users.
    <node ip>
        error/    : Error from input, entry script validation or running.
                    Output to the sys.stderr in entry script.
        log/      : The logs from entry script using entry script helper and print() in entry script.
  sys/        : sys error folder.
    error/    : sys error logs
    perf/     : node and process resource usages, each node has a sub folder.
                Check sys.csv for the resource usages of the node.
                Check other files for the resource usages of a process.
                Try a larger VM size or more nodes.
                Reduce the value of --process_count_per_node if it's larger than 1.
    report/     : processing results, which can be used to check task distribution, succeeded or failed tasks.
    node/     : logs from nodes. each node has a sub folder
        <node ip>
            _main.txt           : Log for the node main file, which starts the task server and agent manager.
            _master_poller.txt  : Log for the master poller.
            _task_server.txt    : Log for the task server.
            agentNNN.task.csv   : Tasks picked and processed by the agent.
            agentNNN.txt        : Logs of the agent.
    simulator/  : Logs for the master-less simulator.
    warning/    : warning logs
    master.txt  : the master logs, including task creation, progress monitoring, run result.
    overview.txt: high level progress.

Links:
https://channel9.msdn.com/Shows/AI-Show/Batch-Inference-using-Azure-Machine-Learning
https://aka.ms/batch-inference-notebooks
https://aka.ms/batch-inference-documentation
    