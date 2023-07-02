import subprocess

def stop_and_clean():
    cmd = ["systemctl", "stop", "ml-container@\*", "--all"]
    p = subprocess.run(cmd)
    if p.returncode != 0:
        return False

    cmd = ["rm", "-rf", "/var/run/ml-containers/*"]
    p = subprocess.run(cmd)
    if p.returncode != 0:
        return False

    return True

def start_container(port):
    cmd = ["systemctl", "start", f"ml-container@{port}"]
    p = subprocess.run(cmd)
    if p.returncode != 0:
        return False
    return True

def stop_container(port):
    cmd = ["systemctl", "stop", f"ml-container@{port}"]
    p = subprocess.run(cmd)
    if p.returncode != 0:
        return False
    return True

