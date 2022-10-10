import argparse
import os
from datetime import datetime

apps_list = [
    "trajectory_mining_pycompss", 
    #"emoji_polarization_pycompss",
]
cores_list = [32, 64]
test_num = 1

def parse_commandline():
    parser = argparse.ArgumentParser("ParSoDA-PyCOMPSs test")
    parser.add_argument(
        "--apps",
        nargs="*",
        help="List of applications to test. "
            "Each application is specified by the name of the python file without the .py extension."
    )

if __name__ == '__main__':

    now_time = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
    test_dir = f"./test/parsoda_pycompss/parsoda_pycompss_{now_time}"
    test_results_file = f"{test_dir}/results.csv"
    test_logs_dir = f"{test_dir}/logs"

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    if not os.path.exists(test_results_file):
        with open(test_results_file, mode="w") as f:
            f.write(
                "App;Cores;Partitions;Crawling-Time;Filter-Time;Map-Time;Split-Time;Reduce-Time;Analysis-Time;Visualization-Time;Filter-Reduce-Time;Total-Execution-Time;Total-Time\n"
            )

    for app in apps_list:
        app_logs_dir = f"{test_logs_dir}/{app}"
        if not os.path.exists(app_logs_dir):
            os.makedirs(app_logs_dir)
            
        for cores in cores_list:
            num_partitions = 0
            crawling_time = 0
            filter_time = 0
            map_time = 0
            split_time = 0
            reduce_time = 0
            analysis_time = 0
            visualization_time = 0
            filter_to_reduce_time = 0
            total_execution_time = 0
            total_time = 0

            for test_index in range(0, test_num):
                print(f"Starting app {app} using {cores} cores ({test_index})...")
                exit_code = os.system(
                    f"runcompss --python_interpreter=python3 "
                    f"--resources=./config/resources.xml "
                    f"--project=./config/project.xml "
                    f"--jvm_workers_opts=\"-Xmx4g\" "
                    f"./src/{app}.py {cores} "
                    f" > {app_logs_dir}/{cores}cores.test{test_index}.log"
                )
                
                if exit_code == 0:
                    try:
                        with open("parsoda_report.csv", "r") as f:
                            report_line = f.readline()
                            fields = report_line.split(";")
                            
                            num_partitions += int(fields[0])
                            crawling_time += int(fields[1])
                            filter_time += int(fields[2])
                            map_time += int(fields[3])
                            split_time += int(fields[4])
                            reduce_time += int(fields[5])
                            analysis_time += int(fields[6])
                            visualization_time += int(fields[7])
                            filter_to_reduce_time += int(fields[8])
                            total_execution_time += int(fields[9])
                            total_time += int(fields[10])
                    except: 
                        pass
                

            num_partitions /= test_num
            crawling_time /= test_num
            filter_time /= test_num
            map_time /= test_num
            split_time /= test_num
            reduce_time /= test_num
            analysis_time /= test_num
            visualization_time /= test_num
            filter_to_reduce_time /= test_num
            total_execution_time /= test_num
            total_time /= test_num

            with open(test_results_file, "a") as f:
                f.write(f"{app};{cores};{num_partitions};{crawling_time};{filter_time};{map_time};{split_time};{reduce_time};{analysis_time};{visualization_time};{filter_to_reduce_time};{total_execution_time};{total_time}\n".replace(".", ","))
