import subprocess
from .deps import *
from .db import *
from .cms import *
from .cms_alpha import *
from .nginx import *

def run(ip, id):

    subprocess.call(["scp", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "./config/hosts", "ubuntu@{}:~/".format(ip)])
    subprocess.call(["ssh", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "ubuntu@{}".format(ip), "sudo cp hosts /etc/hosts;"])

    deps.install(ip)
    if id == 0:
        db.configure(ip)
    if id != 0:
        cms.install(ip)
    else:
        cms_alpha.install(ip)
    if id == 0:
        nginx.configure(ip)
