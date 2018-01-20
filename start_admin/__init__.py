
import subprocess
import config

def run(ip, id):

    commands = ""
    commands += "tmux kill-session -t cms;"
    commands += "tmux new-session -d -s cms -n AdminServer 'cmsAdminWebServer'\;"
    subprocess.call(config.commands.ssh + ["ubuntu@{}".format(ip), commands])
