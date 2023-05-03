##############################################################################################
# modules
##############################################################################################

from scrapli.driver.core import IOSXEDriver
import csv
from getpass import getpass
import time
from datetime import date


##############################################################################################
# Global Variables & Config
##############################################################################################

input_file = input('INPUT FILE NAME: ')
username = input('USERNAME: ')
password = getpass('PASSWORD: ')


##############################################################################################
# Functions
##############################################################################################

def get_show_ver(target_device):

    with IOSXEDriver(**target_device) as conn:
        result = conn.send_command("show version")

    return result.textfsm_parse_output()


##############################################################################################
# Run
##############################################################################################

if __name__ == '__main__':

    start = time.perf_counter()

    print(f'\n\n<<<< SCRIPT STARTED: @ {time.strftime("%X")} >>>>\n')
        

    try:

        try:

            with open(input_file) as f:
                print('<<<< INPUT FILE OPEN >>>>\n')
                device_ips = [row['Asset IPV4'] for row in csv.DictReader(f) if row['CVE'] == 'CVE-2017-6742']
                print('<<<< INPUT FILE READ >>>>\n')

        except Exception as e:

            print(e)

        output_file = f'DEVICE-INFO_{date.today()}.csv\n'

        with open(output_file, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(['device_ip','hostname','device_type','ios_version','exception'])
            print(f'<<<< OUTPUT FILE CREATED: {output_file} >>>>\n')


        for device_ip in device_ips:

            device = {
                    'host': device_ip,
                    'auth_username': username,
                    'auth_password': password,
                    'auth_strict_key': False,
                    'transport': 'ssh2',
                    }

            try:

                show_version = get_show_ver(device)

                hostname = show_version[0]['hostname']
                hardware = show_version[0]['hardware'][0]
                version = show_version[0]['version']

                with open(output_file, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([device_ip,hostname,hardware,version,'',])

            except Exception as e:

                with open(output_file, 'a') as f:
                    writer = csv.writer(f)
                    writer.writerow([device_ip,'','','',e])


        finish = time.perf_counter()
        print(f'\n\n<<<< SCRIPT COMPLETE: @ {time.strftime("%X")} IN {round(finish-start, 2)} SECONDS >>>>\n')


    except KeyboardInterrupt:
        print('\n\n<<<< QUITTING SCRIPT !!! >>>>')