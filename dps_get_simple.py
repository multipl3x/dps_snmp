import __builtin__
import itertools
import sys, traceback 
import time
import re
from snmp_helper import snmp_get_oid,snmp_extract
import thread
import json

notfound = getattr(__builtin__,"IOError","FileNotFoundError")

timestr = time.strftime("%Y.%m.%d-%H.%M.%S")

COMMUNITY_STRING = 'public'
SNMP_PORT = 161
FAIL_LIST =[]
IP_ADDRESS_LIST = ['10.4.8.9', '10.4.0.10']
HOSTNAME_OID = '1.3.6.1.2.1.1.6.0'

POINTS = {'1.3.6.1.4.1.2682.1.2.2.1.4.99.1.2': '1.3.6.1.4.1.2682.1.2.6.1.4.2',
'1.3.6.1.4.1.2682.1.2.2.1.4.99.1.3': '1.3.6.1.4.1.2682.1.2.6.1.4.3',
'1.3.6.1.4.1.2682.1.2.2.1.4.99.1.4': '1.3.6.1.4.1.2682.1.2.6.1.4.4',
'1.3.6.1.4.1.2682.1.2.2.1.4.99.1.5': '1.3.6.1.4.1.2682.1.2.6.1.4.5',
'1.3.6.1.4.1.2682.1.2.2.1.4.99.1.6': '1.3.6.1.4.1.2682.1.2.6.1.4.6',
'1.3.6.1.4.1.2682.1.2.2.1.4.99.1.7': '1.3.6.1.4.1.2682.1.2.6.1.4.7',
'1.3.6.1.4.1.2682.1.2.2.1.4.99.1.8': '1.3.6.1.4.1.2682.1.2.6.1.4.8',
'1.3.6.1.4.1.2682.1.2.2.1.4.99.1.9': '1.3.6.1.4.1.2682.1.2.6.1.4.9'}


# This function gets the SNMP data for each device and stores it in a respective list
def get_snmp_data(device):
	a_device = device
	hostname_list = []
	label_list = []
	value_list = []
	try:
		snmp_host_label = snmp_get_oid(a_device, oid=HOSTNAME_OID, display_errors=True)
		hostname_output = snmp_extract(snmp_host_label)
		hostname_list.append(hostname_output)
	except Exception as e:
		error = str(e)
		print error
		pass
	except KeyboardInterrupt:
	   print('\n' + 'INTERRUPTED, EXIT...')
	   sys.exit(0)	
	try:
		for key, value in POINTS.iteritems():
			snmp_data_label = snmp_get_oid(a_device, oid=key, display_errors=True)
			snmp_data_value = snmp_get_oid(a_device, oid=value, display_errors=True)
			label_output = snmp_extract(snmp_data_label)
			value_output = snmp_extract(snmp_data_value)
			clean_label = re.sub(r'\s+' , r'', label_output)
			clean_value = re.sub(r'\s+' , r'', value_output)
			label_list.append(clean_label)
			value_list.append(clean_value)
	except Exception as e:
		error = str(e)
		print error
		pass
	except KeyboardInterrupt:
	   print('\n' + 'INTERRUPTED, EXIT...')
	   sys.exit(0)
	return hostname_list, label_list, value_list

# This function iterates over the list of IP addresses and  passes the devices to the get_snmp_data function
def iter_ip(community, port, ip_address_list, points):
	data_list = []
	for ip_address in ip_address_list:
		try:
			a_device = (ip_address, COMMUNITY_STRING, SNMP_PORT)
			snmp_data = get_snmp_data(a_device)
			data_list.append(snmp_data)
		except Exception as e:
			error = str(e)
			print error
			pass
		except KeyboardInterrupt:
		   print('\n' + 'INTERRUPTED, EXIT...')
		   sys.exit(0)
	return data_list


results = iter_ip(COMMUNITY_STRING, SNMP_PORT, IP_ADDRESS_LIST, POINTS)

print(json.dumps(results, indent=2))

