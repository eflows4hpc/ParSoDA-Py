import os
from .test_runtime import TestRuntime
    
class PyCompssDev(TestRuntime):    
    def run(self, app, chunk_size, cores, log_file_path) -> int:
        exit_code = os.system(
            f"runcompss --python_interpreter=python3 "
            f"--resources=./test/config/pycompss-dev-docker/dev-resources.xml "
            f"--project=./test/config/pycompss-dev-docker/dev-project.xml "
            f"--jvm_workers_opts=\"-Xmx20g\" "
            f"{app} pycompss --chunk-size {chunk_size}"
            f" > {log_file_path}"
        )
        return exit_code
    
class PyCompssScalab(TestRuntime):    
    def run(self, app, chunk_size, cores, log_file_path) -> int:
        exit_code = os.system(
            f"runcompss --python_interpreter=python3 "
            f"--resources=./test/config/pycompss-scalab-docker/resources.xml "
            f"--project=./test/config/pycompss-scalab-docker/project-{cores}cores.xml "
            f"--jvm_workers_opts=\"-Xmx20g\" "
            f"{app} pycompss --chunk-size {chunk_size}"
            f" > {log_file_path}"
        )
        return exit_code