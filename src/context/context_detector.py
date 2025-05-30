import os
import platform
import datetime
import psutil  # You might need to install psutil: pip install psutil


def detect_context():
    system_platform = platform.system().lower()  # e.g. 'windows', 'darwin', 'linux'
    arch = platform.machine()  # e.g. 'x86_64', 'arm64'

    # Map platform to deviceType
    if system_platform == 'windows':
        device_type = 'Windows'
    elif system_platform == 'darwin':
        device_type = 'macOS'
    elif system_platform == 'linux':
        device_type = 'Linux'
    else:
        device_type = 'Unknown'

    try:
        user = os.getlogin()
    except Exception:
        user = os.environ.get('USER') or os.environ.get('USERNAME') or 'unknown'

    hostname = platform.node()

    # Gather network info using psutil
    network_context = []
    net_if_addrs = psutil.net_if_addrs()
    for iface_name, addrs in net_if_addrs.items():
        for addr in addrs:
            if addr.family.name == 'AF_INET' and not addr.address.startswith('127.'):
                network_context.append({
                    "name": iface_name,
                    "address": addr.address,
                    "netmask": addr.netmask,
                })

    timestamp = datetime.datetime.utcnow().isoformat() + 'Z'

    return {
        "deviceType": device_type,
        "platform": system_platform,
        "arch": arch,
        "hostname": hostname,
        "user": user,
        "timestamp": timestamp,
        "network": network_context,
    }
