
import subprocess
import config

def configure(ip):
    commands = ""
    commands += "printf \"{1}\\n{1}\\n\" | sudo su - postgres -c 'createuser --username=postgres --pwprompt {0}';".format(config.passwords.dblogin, config.passwords.dbpass)
    commands += "sudo su - postgres -c 'createdb --username=postgres --owner={} cmsdb';".format(config.passwords.dblogin)
    commands += "sudo su - postgres -c \"psql --username=postgres --dbname=cmsdb --command='ALTER SCHEMA public OWNER TO {}'\";".format(config.passwords.dblogin)
    commands += "sudo su - postgres -c \"psql --username=postgres --dbname=cmsdb --command='GRANT SELECT ON pg_largeobject TO {}'\";".format(config.passwords.dblogin)
    commands += "echo 'host    all             all             {}            md5' | sudo tee -a /etc/postgresql/9.5/main/pg_hba.conf;".format(config.constants.localipmask)
    commands += "echo \"listen_addresses = '*'\" | sudo tee -a /etc/postgresql/9.5/main/postgresql.conf;"
    commands += "sudo service postgresql restart;"
    subprocess.call(config.commands.ssh + ["ubuntu@{}".format(ip), commands])
