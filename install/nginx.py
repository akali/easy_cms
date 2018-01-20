
import subprocess
import config

def configure(ip):

    subprocess.call(config.commands.scp + ["./config/generated/nginx.conf", "ubuntu@{}:~/cms/config/".format(ip)])
    commands = ""
    commands += "sudo cp cms/config/nginx.conf /etc/nginx/nginx.conf;"
    commands += "printf \"{1}\\n{1}\\n\" | sudo htpasswd -c /etc/nginx/htpasswd_AWS {0};".format(config.passwords.awsaclogin, config.passwords.awsacpass);
    commands += "printf \"{1}\\n{1}\\n\" | sudo htpasswd -c /etc/nginx/htpasswd_RWS {0};".format(config.passwords.rwsaclogin, config.passwords.rwsacpass);
    commands += "sudo service nginx restart;"
    subprocess.call(config.commands.ssh + ["ubuntu@{}".format(ip), commands])
