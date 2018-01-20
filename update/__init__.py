import subprocess
import config

def run(ip, id):

    subprocess.call(config.commands.scp + ["./config/generated/hosts", "ubuntu@{}:~/".format(ip)])
    subprocess.call(config.commands.ssh + ["ubuntu@{}".format(ip), "sudo cp hosts /etc/hosts;"])

    subprocess.call(config.commands.scp + ["./config/generated/cms.conf", "ubuntu@{}:~/cms/config/".format(ip)])
    subprocess.call(config.commands.scp + ["./config/generated/cms.ranking.conf", "ubuntu@{}:~/cms/config/".format(ip)])
    commands = ""
    commands += "cd cms;"
    commands += "sudo ./prerequisites.py install -y;"
    subprocess.call(config.commands.ssh + ["ubuntu@{}".format(ip), commands])
