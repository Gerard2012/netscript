from scrapli.driver.core import IOSXEDriver

device = {
    "host": "172.27.252.23",
    "auth_username": "mcgrattg",
    "auth_password": "V5zorA",
    "auth_strict_key": False,
}


def main(target_device):

    with IOSXEDriver(**target_device) as conn:
        result = conn.send_command("show version")

    hostname = result.textfsm_parse_output()[0]['hostname']
    hardware = result.textfsm_parse_output()[0]['hardware'][0]
    version = result.textfsm_parse_output()[0]['version']

    return hostname, hardware, version
    





##############################################################################################
# Run
##############################################################################################


if __name__ == '__main__':

    try:

        print(main(device))

    except Exception as e:

        print(e)