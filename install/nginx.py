#!/home/akim/.virtualenvs/easy_cms/bin/python

import subprocess

def configure(ip):

    f = open("config/passwords")
    _ = f.readlines()
    loginaws = _[2].strip()
    passaws = _[3].strip()
    loginrws = _[5].strip()
    passrws = _[6].strip()
    subprocess.call(["scp", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "./config/nginx.conf", "ubuntu@{}:~/cms/config/".format(ip)])
    commands = ""
    commands += "sudo cp cms/config/nginx.conf /etc/nginx/nginx.conf;"
    commands += "printf \"{}\\n{}\\n\" | sudo htpasswd -c /etc/nginx/htpasswd_AWS {};".format(passaws, passaws, loginaws);
    commands += "printf \"{}\\n{}\\n\" | sudo htpasswd -c /etc/nginx/htpasswd_RWS {};".format(passrws, passrws, loginrws);
    commands += "sudo service nginx restart;"
    subprocess.call(["ssh", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "ubuntu@{}".format(ip), commands])
