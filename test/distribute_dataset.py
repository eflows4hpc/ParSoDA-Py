import argparse
import os
import math
from datetime import datetime

def type_check_port(arg)->int:
    value = int(arg)
    if value > 0 and value <= 65535:
        return value
    else:
        raise Exception("the value is not a valid port")

def send_data_to_remote_file(user: str, host: str, data: str, filename: str, port: int=22):
    port=type_check_port(port)
    exit_code = os.system(f"echo {data} | ssh {user}@{host} -p {port} -c \"cat > {filename}\"")
    return True if exit_code == 0 else False

