
import subprocess
import config

def install(ip):
    commands = ""
    commands += "wget https://github.com/cms-dev/cms/releases/download/v1.3.rc0/v1.3.rc0.tar.gz;"
    commands += "tar -xvf v1.3.rc0.tar.gz;"
    subprocess.call(config.commands.ssh + ["ubuntu@{}".format(ip), commands])
    subprocess.call(config.commands.scp + ["./config/generated/cms.conf", "ubuntu@{}:~/cms/config/".format(ip)])
    subprocess.call(config.commands.scp + ["./config/generated/cms.ranking.conf", "ubuntu@{}:~/cms/config/".format(ip)])
    commands = ""
    commands += "cd cms;"
    commands += "sudo ./prerequisites.py install -y;"
    commands += "sudo pip2 install -r requirements.txt;"
    commands += "sudo python2 setup.py install;"
    subprocess.call(config.commands.ssh + ["ubuntu@{}".format(ip), commands])
    commands = ""
    commands += "cmsInitDB;"
    commands += "cmsAddAdmin -p {1} {0};".format(config.passwords.awslogin, config.passwords.awspass)
    subprocess.call(config.commands.ssh + ["ubuntu@{}".format(ip), commands])
