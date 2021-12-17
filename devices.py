
from scrapli.driver.core import AsyncIOSXEDriver, AsyncNXOSDriver, IOSXEDriver
from getpass import getpass

username = input('username: ')
password = getpass('password: ')


nxos_switches = [
    {
    'NXOS_SW1': {
        'host': '10.57.252.12',
        'auth_username': username,
        'auth_password': password,
        'auth_strict_key': False,
        'transport': 'asyncssh',
        'driver': AsyncNXOSDriver
        }
    },
    {
    'NXOS_SW2': {
        'host': '10.190.252.12',
        'auth_username': username,
        'auth_password': password,
        'auth_strict_key': False,
        'transport': 'asyncssh',
        'driver': AsyncNXOSDriver
        }
    }
    }
]


iosxe_switches = [
    {
    'IOSXE_SW1': {
        'host': '10.40.15.1',
        'auth_username': username,
        'auth_password': password,
        'auth_strict_key': False,
        'transport': 'asyncssh',
        'driver': AsyncIOSXEDriver
        }
    },
    {
    'IOSXE_SW2': {
        'host': '10.191.15.1',
        'auth_username': username,
        'auth_password': password,
        'auth_strict_key': False,
        'transport': 'asyncssh',
        'driver': AsyncIOSXEDriver
        }
    }
]


ios_switches = [
    {
    'IOS_SW1': {
        'host': '10.53.15.1',
        'username': username,
        'password': password,
        'device_type': 'cisco_ios'
        }
    },
    {
    'IOS_SW1': {
        'host': '10.45.15.1',
        'username': username,
        'password': password,
        'device_type': 'cisco_ios'
        }
    }
]


if __name__ == '__main__':

    pass