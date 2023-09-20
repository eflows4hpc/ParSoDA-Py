import argparse
import os
from datetime import datetime
from pathlib import Path
from typing import List
import pandas as pd
import test.runtime as rt


runtimes: List[rt.TestRuntime] = [rt.PyCompssScalabTestRuntime(), rt.PySparkScalabTestRuntime()]
use_cases = [
    #"trajectory_mining_40m", 
    "trajectory_mining_1m", 
    #"emoji_polarization_pycompss",
]
cores_list = [8]
chunk_size = 64
test_num = 1

if __name__ == '__main__':

    now_time = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
    test_dir = f"./test_out/performance/{now_time}"
    test_results_file = f"{test_dir}/results"
    test_logs_dir = f"{test_dir}"
    apps_dir = "./test/usecase"

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)
            
    results_columns = [
        "runtime",
        "app",
        "cores",
        "partitions",
        "crawling-time",
        "filter-time",
        "map-time",
        "split-time",
        "reduce-time",
        "analysis-time",
        "visualization-time",
        "fiter-reduce-time",
        "total-execution-time",
        "total-time",
        "test",
    ]
    
    result_df = pd.DataFrame(columns=results_columns)
    
    
    for app in use_cases:
        app_file = Path(f"{apps_dir}/{app}.py")
        if not app_file.is_file:
            print(f"WARNING: application file \"{app_file}\" not found!")

    for runtime in runtimes:
        for app in use_cases:
            app_file = Path(f"{apps_dir}/{app}.py")
            if not app_file.is_file:
                print(f"WARNING: skipping application file \"{app_file}\", not found!")
                continue
                
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
                    print(f"Starting app {app} using {cores} cores (test #{test_index})...")
                
                    app_logs_dir = f"{test_logs_dir}/{app}/{cores}cores.test{test_index}"
                    if not os.path.exists(app_logs_dir):
                        os.makedirs(app_logs_dir)
                        
                    log_file_path = f"{app_logs_dir}/{app}.cores{cores}.chunk{chunk_size}.test{test_index}.log"
                    
                    runtime: rt.TestRuntime   
                    exit_code = runtime.run(app_file, chunk_size, cores, log_file_path)
                    
                    if exit_code == 0:
                        try:
                            with open("parsoda_report.csv", "r") as f:
                                report_line = f.readline()
                                fields = report_line.split(";")
                                
                                result_df.loc[len(result_df)] = [type(runtime).__name__, app, cores]+fields[0:11]+[test_index]
                                result_df.to_excel(f"{test_results_file}.xlsx", index=False)
                                result_df.to_excel(f"{test_results_file}.csv", index=False)
                        except: 
                            pass