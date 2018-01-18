#!/home/akim/.virtualenvs/easy_cms/bin/python

import argparse, subprocess
import install, update, start, stop, start_admin

def getlocalip(ip):
    print('Updating local ip for {}'.format(ip))
    command = "ifconfig eth0 | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\\2/p'"
    ssh = subprocess.Popen(["ssh", "-i", "./config/cms.pem", "-o StrictHostKeyChecking=no", "ubuntu@{}".format(ip), command], shell=False, stdout=subprocess.PIPE)
    localip = str(ssh.stdout.readlines()[0].strip())[2:-1]
    return localip

def genhosts(ips):
    f = open("config/hosts", "w");
    f.write("127.0.0.1 localhost\n")
    for i, ip in enumerate(ips):
        f.write("{} {}\n".format(getlocalip(ip), 'alpha' if i == 0 else 'beta' + str(i)))



if __name__ == "__main__":

    ip_file = open('config/ip_addresses', 'r')
    ips = [line.strip() for line in ip_file.readlines() if line.strip()[0] != '#']

    parser = argparse.ArgumentParser()
    parser.add_argument('-n', action='store_true', default=False, dest='no_hosts_gen', help='skip generating hosts file and use old one')
    parser.add_argument('-i', '--install', action='store', dest='i_ip_ids', help='installs cms on some machines. takes id\'s of machines, numbered from 0, as arg. do not forget to update configs for other machines. example: -i \'1 3 5\'')
    parser.add_argument('-u', '--update', action='store', dest='u_ip_ids', help='updates configs on some machines. takes id\'s of machines, numbered from 0, as arg. example: -u \'2 4\'')
    parser.add_argument('-s', '--start', action='store', dest='s_ip_ids', help='starts cms on some machines. takes id\'s of machines, numbered from 0, as arg. example: -s \'1 2 3 4 5\'')
    parser.add_argument('-c', '--contest', action='store', dest='contest', help='means contest id to start if start flag enabled')
    parser.add_argument('--stop', action='store', dest='st_ip_ids', help='stops cms on some machines. takes id\'s of machines, numbered from 0, as arg. example: -s \'1 2 3 4 5\'')
    parser.add_argument('--start_admin', action='store_true', dest='start_admin', help='starts only admin web server on alpha')


    results = parser.parse_args()

    if not results.no_hosts_gen:
        genhosts(ips)

    if results.i_ip_ids:
        i_ips = [{'id': id, 'ip': ips[id]} for id in map(int, results.i_ip_ids.split(' '))]
        for ip in i_ips:
            print('#' * 70)
            print('Installing cms for {}, known as {}'.format(ip['ip'], 'alpha' if ip['id'] == 0 else 'beta' + str(ip['id'])))
            install.run(ip['ip'], ip['id'])
            print('Done! Installed cms for {}, known as {}'.format(ip['ip'], 'alpha' if ip['id'] == 0 else 'beta' + str(ip['id'])))
            print('#' * 70)

    if results.u_ip_ids:
        u_ips = [{'id': id, 'ip': ips[id]} for id in map(int, results.u_ip_ids.split(' '))]
        for ip in u_ips:
            print('#' * 70)
            print('Updating cms configs for {}, known as {}'.format(ip['ip'], 'alpha' if ip['id'] == 0 else 'beta' + str(ip['id'])))
            update.run(ip['ip'], ip['id'])
            print('Done! Updated cms configs for {}, known as {}'.format(ip['ip'], 'alpha' if ip['id'] == 0 else 'beta' + str(ip['id'])))
            print('#' * 70)


    if results.start_admin:
        s_ips = [{'id': 0, 'ip': ips[0]}]
        for ip in s_ips:
            print('#' * 70)
            print('Starting aws for {}, known as {}'.format(ip['ip'], 'alpha' if ip['id'] == 0 else 'beta' + str(ip['id'])))
            start_admin.run(ip['ip'], ip['id'])
            print('Done! Started aws for {}, known as {}'.format(ip['ip'], 'alpha' if ip['id'] == 0 else 'beta' + str(ip['id'])))
            print('#' * 70)




    if results.s_ip_ids:
        if results.contest:
            s_ips = [{'id': id, 'ip': ips[id]} for id in map(int, results.s_ip_ids.split(' '))]
            for ip in s_ips:
                print('#' * 70)
                print('Starting cms for {}, known as {}'.format(ip['ip'], 'alpha' if ip['id'] == 0 else 'beta' + str(ip['id'])))
                start.run(ip['ip'], ip['id'], results.contest)
                print('Done! Started cms for {}, known as {}'.format(ip['ip'], 'alpha' if ip['id'] == 0 else 'beta' + str(ip['id'])))
                print('#' * 70)
        else:
            print('#' * 70)
            print('No contest specified')
            print('#' * 70)


    if results.st_ip_ids:
        st_ips = [{'id': id, 'ip': ips[id]} for id in map(int, results.st_ip_ids.split(' '))]
        for ip in st_ips:
            print('#' * 70)
            print('Stopping cms for {}, known as {}'.format(ip['ip'], 'alpha' if ip['id'] == 0 else 'beta' + str(ip['id'])))
            stop.run(ip['ip'], ip['id'])
            print('Done! Stopped cms for {}, known as {}'.format(ip['ip'], 'alpha' if ip['id'] == 0 else 'beta' + str(ip['id'])))
            print('#' * 70)
