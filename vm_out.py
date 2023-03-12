import os
import datetime


def create_log():
    ts_string = get_timestamp()
    print(ts_string)
    # VM INFO
    # Name
    # Project
    # Purpose
    # Team
    # OS
    # Relevant info about VM
    # VM status


def move_conf(config_path):
    # move conf files to time stamp
    if not os.path.exists(config_path):
        return
    ts_string = get_timestamp()
    conf_name = config_path.replace(".conf", "")
    os.rename(config_path, conf_name + f"_{ts_string}.conf")


def get_timestamp():
    timestamp = datetime.datetime.now()
    return timestamp.strftime("%Y-%m-%d;%H;%M;%S")
