#!/home/akim/.virtualenvs/easy_cms/bin/python

import subprocess

def install(ip):
    commands = ""
    commands += "wget https://github.com/cms-dev/cms/releases/download/v1.3.rc0/v1.3.rc0.tar.gz;"
    commands += "tar -xvf v1.3.rc0.tar.gz;"
    subprocess.call(["ssh", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "ubuntu@{}".format(ip), commands])
    subprocess.call(["scp", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "./config/cms.conf", "ubuntu@{}:~/cms/config/".format(ip)])
    subprocess.call(["scp", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "./config/cms.ranking.conf", "ubuntu@{}:~/cms/config/".format(ip)])
    commands = ""
    commands += "cd cms;"
    commands += "sudo ./prerequisites.py install -y;"
    commands += "sudo pip2 install -r requirements.txt;"
    commands += "sudo python2 setup.py install;"
    subprocess.call(["ssh", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "ubuntu@{}".format(ip), commands])
    commands = ""
    commands += "cmsInitDB;"
    commands += "cmsAddAdmin -p LA3AL6Y3 cmsadmin;"
    subprocess.call(["ssh", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "ubuntu@{}".format(ip), commands])
