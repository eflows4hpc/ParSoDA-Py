import shutil

import os
from datetime import datetime

apps_list = [
    "trajectory_mining_spark", 
    "emoji_polarization_spark"
]
cores_list = [2, 4, 8, 16, 32, 64]
chunk_sizes = [128]
test_num = 1

now_time = datetime.now().strftime("%Y.%m.%d_%H.%M.%S")
test_dir = f"./test/parsoda_pyspark/parsoda_pyspark_{now_time}"
test_results_file = f"{test_dir}/results.csv"
test_logs_dir = f"{test_dir}/logs"

if __name__ == '__main__':

    if not os.path.exists(test_dir):
        os.makedirs(test_dir)

    if not os.path.exists(test_results_file):
        with open(test_results_file, mode="w") as f:
            f.write(
                "App;Cores;Partitions;Chunk-Size;Crawling-Time;Filter-Time;Map-Time;Split-Time;Reduce-Time;Analysis-Time;Visualization-Time;Filter-Reduce-Time;Total-Execution-Time;Total-Time\n"
            )
            
    # create archive for making sources available to spark
    shutil.make_archive("./parsoda_src", 'zip', "./src")

    for app in apps_list:
        for chunk_size in chunk_sizes:            
            for cores in cores_list:
                num_partitions=0
                chunk_size_given=0
                crawling_time = 0
                filter_time = 0
                map_time = 0
                split_time = 0
                reduce_time = 0
                analysis_time = 0
                visualization_time = 0
                filter_to_reduce_time = 0
                total_execution_time = 0
                total_time=0

                for test_index in range(0, test_num):
                    print(f"Starting app {app} using {cores} cores ({test_index})...")
                    
                    app_logs_dir = f"{test_logs_dir}/{app}/{cores}cores.test{test_index}"
                    if not os.path.exists(app_logs_dir):
                        os.makedirs(app_logs_dir)
                        
                    exit_code = os.system(
                        f"spark-submit "
                        f"--driver-memory 200G "
                        f"--master \"local[{cores}]\" "
                        f"--executor-memory 25G "
                        f"--executor-cores 1 "
                        f"--num-executors {cores} "
                        f"--py-files ./parsoda_src.zip "
                        f"./src/{app}.py --chunk-size {chunk_size} "
                        #f"./src/{app}.py --partitions {cores} "
                        f"> {app_logs_dir}/{app}.{cores}cores.chunk{chunk_size}.test{test_index}.log"
                    )

                    if exit_code == 0:
                        with open("parsoda_report.csv", "r") as f:
                            report_line = f.readline()
                            fields = report_line.split(";")
                            
                            num_partitions += int(fields[1])
                            chunk_size_given += int(fields[2])
                            crawling_time += int(fields[3])
                            filter_time += int(fields[4])
                            map_time += int(fields[5])
                            split_time += int(fields[6])
                            reduce_time += int(fields[7])
                            analysis_time += int(fields[8])
                            visualization_time += int(fields[9])
                            filter_to_reduce_time += int(fields[10])
                            total_execution_time += int(fields[11])
                            total_time += int(fields[12])
                    
                num_partitions /= test_num
                chunk_size_given /= test_num
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
                    f.write(f"{app};{cores};{num_partitions};{chunk_size_given};{crawling_time};{filter_time};{map_time};{split_time};{reduce_time};{analysis_time};{visualization_time};{filter_to_reduce_time};{total_execution_time};{total_time}\n".replace(".", ","))

    # remove sources used for running spark
    os.remove("./parsoda_src.zip")