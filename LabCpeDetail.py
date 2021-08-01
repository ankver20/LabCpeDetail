# Get L3CPE details in Lab.
# Check reacahbility from server. If reacable, then telnet.
# Get sh ver output.


from netmiko import ConnectHandler
import os
import time
from time import gmtime, strftime

def LabCpeDetails():

    l3cpe_login = {
        'username': 'colt123',
        'password': 'colt123',
        'device_type': 'cisco_ios_telnet'
    }
    
    c = 'ip;version;hostname;hardware;sn\n'
    createLog(c)

    c = open('CpeIP.txt', 'r')
    IPs = c.readlines()
    c.close()
    
    for ip in IPs:
        print(ip)
        l3cpe_login['ip'] = ip.strip('\n')
        # print(l3cpe_login)

        pingCmd = 'ping -c 5  %s' %(ip)
        pingResponse = os.system(pingCmd)
        if pingResponse == 0:
            status = 'L3 CPE is reachable'
            # print(status)
        
            try:
                net_connect = ConnectHandler(**l3cpe_login)
                telnet_res = net_connect.find_prompt()
                # print(telnet_res)
                telnet_res = net_connect.send_command("show version", use_textfsm=True)
                time.sleep(1)
                c = ('%s;%s;%s;%s;%s\n') %(ip.strip('\n'), telnet_res[0]['version'], telnet_res[0]['hostname'], telnet_res[0]['hardware'][0], telnet_res[0]['serial'][0])
                createLog(c)
                telnet_res = net_connect.disconnect()
            
            except Exception as e:
                c = ('%s;;;;;%s\n') %(ip.strip('\n'), e)
                createLog(c)

        
        else:
            status = 'L3 CPE not is reachable'
            c = ('%s;;;;;%s\n') %(ip.strip('\n'), status)
            createLog(c)


def createLog(c):
    file_path = os.path.dirname(os.path.realpath(__file__))
    print(file_path)
    LocalTime= strftime("%d%m", gmtime())
    f = open(file_path + '/CpeDetails-' + LocalTime + '.txt', 'a')
    f.write(c)
    f.close()

LabCpeDetails()
