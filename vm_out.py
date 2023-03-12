import os
import pwd
import datetime


def create_log(az_log, gcp_log):

    ts_string = get_timestamp()
    with open(f'VMcreation_{ts_string}.txt', 'w') as f:
        f.write(f"Time Stamp: {ts_string}\n")
        f.write(f"Admin Username: {pwd.getpwuid(os.getuid())[0]}\n")
        f.write("---------GCP VMs---------\n")
        for o in gcp_log:
            f.write('\n')
            f.write(o)
        f.write("----------AZURE VMs--------\n")
        for o in az_log:
            f.write('\n')
            f.write(o)

    move_conf("gcp.conf")
    move_conf("azure.conf")


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
