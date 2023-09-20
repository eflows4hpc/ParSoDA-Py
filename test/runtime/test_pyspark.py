import os
from .test_runtime import TestRuntime
    
class PySparkScalabTestRuntime(TestRuntime):    
    def run(self, app, chunk_size, cores, log_file_path) -> int:
        exit_code = os.system(
            f"/spark/bin/spark-submit "
            f"--driver-memory 200G "
            f"--master \"spark://spark-master:7077\" "
            #f"--executor-memory {mem}M "
            #f"--conf \"spark.memory.fraction=0.3\" "
            #"--conf \"spark.driver.extraJavaOptions=-Xss512M\" "
            #f"--conf \"spark.dynamicAllocation.enabled=true\" " 
            #f"--conf \"spark.dynamicAllocation.executorIdleTimeout=120m\" " 
            f"--conf \"spark.network.timeout=10000000\" " 
            f"--conf \"spark.executor.heartbeatInterval=1000000\" " 
            #f"--conf \"spark.rpc.message.maxSize=2047\" "
            #f"--conf \"spark.rpc.io.serverThreads=64\" "
            f"--conf \"spark.executor.extraJavaOptions=-XX:ThreadStackSize=2048\" "
            #f"--executor-cores {cores/nodes}"
            #f"--num-executors {cores} "
            f"--total-executor-cores {cores} "
            f"--py-files ./parsoda_src.zip "
            f"{app} pyspark --chunk-size {chunk_size} "
            f"> {log_file_path}"
        )
        return exit_code