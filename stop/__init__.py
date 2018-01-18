import subprocess

def run(ip, id):

    commands = ""
    commands += "tmux kill-session -t cms;"
    subprocess.call(["ssh", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "ubuntu@{}".format(ip), commands])
