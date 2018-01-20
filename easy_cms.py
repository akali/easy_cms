#!/usr/bin/env python

import argparse, subprocess
import config, install, update, start, stop, start_admin
from multiprocessing import Process, Queue

def getlocalip(q, ip, i):
    command = "ifconfig eth0 | sed -En 's/127.0.0.1//;s/.*inet (addr:)?(([0-9]*\.){3}[0-9]*).*/\\2/p'"
    ssh = subprocess.Popen(config.commands.ssh + ["ubuntu@{}".format(ip), command], shell=False, stdout=subprocess.PIPE)
    localip = str(ssh.stdout.readlines()[0].strip())[2:-1]
    q.put("{} {}\n".format(localip, 'alpha' if i == 0 else 'beta' + str(i)))

def genhosts(ips):
    f = open("config/generated/hosts", "w");
    f.write("127.0.0.1 localhost\n")
    qp = []
    q = Queue()
    for i, ip in enumerate(ips):
        print('Updating local ip for {}'.format(ip))
        p = Process(target=getlocalip, args=(q, ip, i))
        p.start()
        qp.append(p)

    for pr in qp:
        pr.join()

    while not q.empty():
        f.write(q.get())

def genconfigs(ips):
    fr = open("config/templates/cms.conf", "r")
    all = ''.join(fr.readlines())
    resource_services = ", ".join(["[\"{}\", 28000]".format('alpha' if id == 0 else 'beta' + str(id)) for id, ip in enumerate(ips)])
    workers = ", ".join(["[\"{}\", 28000]".format('alpha' if id == 0 else 'beta' + str(id)) for id, ip in enumerate(ips)][1:])
    fw = open("config/generated/cms.conf", "w")
    fw.write(all.format(resource_services, workers, config.passwords.dblogin, config.passwords.dbpass, config.passwords.rwstalklogin, config.passwords.rwstalkpass))

    fr = open("config/templates/cms.ranking.conf", "r")
    all = ''.join(fr.readlines())
    fw = open("config/generated/cms.ranking.conf", "w")
    fw.write(all.format(config.passwords.rwstalklogin, config.passwords.rwstalkpass))

if __name__ == "__main__":

    ip_file = open('config/ip_addresses', 'r')
    ips = [line.strip() for line in ip_file.readlines() if line.strip()[0] != '#']
    alpha_ip = ips[0]

    parser = argparse.ArgumentParser()
    parser.add_argument('ids', action='store', type=int, nargs='+', help='machines id\'s')
    parser.add_argument('-i', '--install', action='store_true', default=False, dest='install', help='installs cms on some machines. do not forget to update configs for other machines.')
    parser.add_argument('-u', '--update', action='store_true', default=False, dest='update', help='updates configs on some machines.')
    parser.add_argument('-s', '--start', action='store', default=None, type=int, dest='start_contest', help='starts cms on some machines. takes id of contest as argument.')
    parser.add_argument('--stop', action='store_true', default=False, dest='stop', help='stops cms on some machines.')
    parser.add_argument('--start_admin', action='store_true', default=False, dest='start_admin', help='starts only admin web server on alpha.')
    parser.add_argument('-n', action='store_true', default=False, dest='no_gen', help='skip generating config files and use old ones.')


    results = parser.parse_args()

    if not results.no_gen:
        genhosts(ips)
        genconfigs(ips)


    ips = [{'id': id, 'ip': ips[id]} for id in results.ids]


    if results.install:
        print("Installing cms")
        qp = []
        for ip in ips:
            p = Process(target=install.run, args=(ip['ip'], ip['id']))
            p.start()
            qp.append(p)
        for pr in qp:
            pr.join()
        print("Done")

    if results.update:
        print("Updating configs")
        qp = []
        for ip in ips:
            p = Process(target=update.run, args=(ip['ip'], ip['id']))
            p.start()
            qp.append(p)
        for pr in qp:
            pr.join()
        print("Done")


    if results.start_admin:
        print("Starting admin")
        qp = []
        p = Process(target=start_admin.run, args=(alpha_ip, 0))
        p.start()
        qp.append(p)
        for pr in qp:
            pr.join()
        print("Done")


    if results.stop:
        print("Stopping cms")
        qp = []
        for ip in ips:
            p = Process(target=stop.run, args=(ip['ip'], ip['id']))
            p.start()
            qp.append(p)
        for pr in qp:
            pr.join()
        print("Done")


    if not (results.start_contest is None):
        print("Starting contest")
        qp = []
        for ip in ips:
            p = Process(target=start.run, args=(ip['ip'], ip['id'], results.start_contest))
            p.start()
            qp.append(p)
        for pr in qp:
            pr.join()
        print("Done")
