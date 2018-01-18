#!/home/akim/.virtualenvs/easy_cms/bin/python

import subprocess

def configure(ip):
    commands = ""
    commands += "printf \"XD5AZQH5\\nXD5AZQH5\\n\" | sudo su - postgres -c 'createuser --username=postgres --pwprompt cmsuser';"
    commands += "sudo su - postgres -c 'createdb --username=postgres --owner=cmsuser cmsdb';"
    commands += "sudo su - postgres -c \"psql --username=postgres --dbname=cmsdb --command='ALTER SCHEMA public OWNER TO cmsuser'\";"
    commands += "sudo su - postgres -c \"psql --username=postgres --dbname=cmsdb --command='GRANT SELECT ON pg_largeobject TO cmsuser'\";"
    commands += "echo 'host    all             all             172.31.0.0/16            md5' | sudo tee -a /etc/postgresql/9.5/main/pg_hba.conf;"
    commands += "echo \"listen_addresses = '*'\" | sudo tee -a /etc/postgresql/9.5/main/postgresql.conf;"
    commands += "sudo service postgresql restart;"
    subprocess.call(["ssh", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "ubuntu@{}".format(ip), commands])
