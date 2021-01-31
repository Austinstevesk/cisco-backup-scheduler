from netmiko import ConnectHandler
from netmiko.ssh_exception import NetMikoTimeoutException
from netmiko.ssh_exception import NetMikoAuthenticationException
from paramiko.ssh_exception import SSHException
import time
import datetime
import schedule


def Backup():
	TNow = datetime.datetime.now().replace(microsecond=0)
	IP_List = open("15_devices")
	for IP in IP_List:
		RTR = {
		'device_type': 'cisco_ios',
		'ip': IP,
		'username': 'admin',
		'password': 'admin'
		}

		print('\n ### Connecting to the device ' + IP.strip() + ' ### \n')
		try:
			net_connect = ConnectHandler(**RTR)
		except NetMikoTimeoutException:
			print('device not reachable')
			continue

		except NetMikoAuthenticationException:
			print("Authentication Failure")
			continue

		except SSHException:
			print('Make sure SSH is enabled')
			continue

		print('Initiating config Backup at ' + str(TNow))
		output = net_connect.send_command('show run')
		SAVE_FILE = open('ROUTER_' + IP + str(TNow), 'w')
		SAVE_FILE.write(output)
		SAVE_FILE.close()
		print('Finished config backup')

schedule.every().minute.at(":00").do(Backup) #Call the backup function at the specified time
while True:
	schedule.run_pending()
	time.sleep(1)
