#!/usr/bin/python3

from ConfigParser import ConfigParser
import subprocess
import paramiko

class RabbitMigration(object):
    
    def __init__(self):
        try:
            cfg = ConfigParser()
            cfg.read("server")
            self.source = {"host":cfg.get("source","server"),"password":cfg.get("source","password")}
            self.dest = {"host":cfg.get("dest","server"),"password":cfg.get("dest","password")}
            self.ZMPROV="/opt/zimbra/bin/zmprov"
            self.ZMCONTROL="/opt/zimbra/bin/zmcontrol"
        except Exception as e:
            print("Error! ",e)

    def ssh_connect(self, host, cmd):
        try:
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            ssh.connect(hostname=host,key_filename="rabbit.pem")
            stdin, stdout, stderr = ssh.exec_command(cmd)
            if stdout.recv_exit_status() == 0:
                return stdout.read()
            else:
                print("Error! ",stderr.read())
        except Exception as e:
            print("Error! ",e)

    def create_domains(self):
        print("create all domains server on %s"%self.dest.get("host"))
        all_domains = self.ssh_connect(self.dest.get("host"), "/opt/zimbra/bin/zmprov gad")
        print("Dominios remotos: ",all_domains)
        local_domains = subprocess.Popen(["/opt/zimbra/bin/zmprov gad"],shell=True,stdout=subprocess.PIPE)
        print("Dominios locais: ",local_domains)
        #echo "your domain $domain already exists in server $HOST2"
        print(all_domains)
        print("==============================")
        print(local_domains)
        new_domain = subprocess.Popen(["/opt/zimbra/bin/zmprov cd %s"%domain], shell=True, stdout=subprocess.PIPE)
        local_domains = subprocess.Popen(["/opt/zimbra/bin/zmprov gad"],shell=True,stdout=subprocess.PIPE)
        #if domain in local_domains:
        #    print(" your domain $domain create success :D ")
        #else: 
        #    print("Domain $domain is not create :(")

if __name__ == "__main__":
    rm = RabbitMigration()
    rm.create_domains()