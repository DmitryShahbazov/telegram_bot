import os
import subprocess


def read_vpn_status_log() -> str:
    with open('/etc/openvpn/server/openvpn-status.log', 'r') as log_file:
        log_text = log_file.read()
        log_file.close()
    return log_text


def create_vpn_profile(profile_name: str):
    subprocess.Popen(["/root/openvpn-install.sh"], stdin=subprocess.PIPE).communicate("1\n")


def save_file_to_server(file_name: str, file: bytes) -> str:
    with open(os.path.join('/home/tg_files/', file_name), 'wb') as new_file:
        new_file.write(file)
        new_file.close()
        return os.path.join('/home/tg_files/', file_name)
