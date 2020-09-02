import os


def read_vpn_status_log():
    with open('/etc/openvpn/server/openvpn-status.log', 'r') as log_file:
        log_text = log_file.read()
        log_file.close()
    return log_text


def save_file_to_server(file_name: str, file: bytes) -> str:
    with open(os.path.join('/home/tg_files/', file_name), 'br+') as new_file:
        new_file.write(file)
        new_file.close()
        return os.path.join('/home/tg_files/', file_name)
