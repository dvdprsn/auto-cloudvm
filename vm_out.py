import os
import datetime


def create_log(az_log, gcp_log):

    ts_string = get_timestamp()
    with open(f'VMcreation_{ts_string}.txt', 'w') as f:
        f.write(f"Time Stamp: {ts_string}")
        f.write(f"Admin Username: {os.getlogin()}")
        for o in az_log:
            print(o)
            f.write(o)

        for o in gcp_log:
            print(o)
            f.write(o)

    # move_conf("gcp.conf")
    # move_conf("azure.conf")


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
