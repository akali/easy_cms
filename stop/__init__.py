import subprocess
import config

def run(ip, id):

    commands = ""
    commands += "tmux kill-session -t cms;"
    subprocess.call(config.commands.ssh + ["ubuntu@{}".format(ip), commands])
