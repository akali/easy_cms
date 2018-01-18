import subprocess

def run(ip, id):

    subprocess.call(["scp", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "./config/hosts", "ubuntu@{}:~/".format(ip)])
    subprocess.call(["ssh", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "ubuntu@{}".format(ip), "sudo cp hosts /etc/hosts;"])

    subprocess.call(["scp", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "./config/cms.conf", "ubuntu@{}:~/cms/config/".format(ip)])
    subprocess.call(["scp", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "./config/cms.ranking.conf", "ubuntu@{}:~/cms/config/".format(ip)])
    commands = ""
    commands += "cd cms;"
    commands += "sudo ./prerequisites.py install -y;"
    subprocess.call(["ssh", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "ubuntu@{}".format(ip), commands])
