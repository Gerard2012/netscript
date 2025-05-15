import asyncio
import time
from datetime import date
import os
from sys import exit
from netmiko import ConnectHandler
import pprint
import concurrent.futures



######################################################################################
######################################################################################


def pause(user_prompt):
    choice = input(f'{user_prompt} COMPLETE. CONTINUE WITH THE SCRIPT? [Yn]: ')
    if choice == 'Y':
        pass
    elif choice == 'n':
        exit(1)
    else:
        pause(user_prompt)



######################################################################################
######################################################################################


async def show_command_async(hostname, device, cmds):

    print(f'CONNECTING: {hostname} @ {time.strftime("%X")}')

    try:

        driver = device.pop('driver')
        buffer = ''

        with open(cmds) as commands:
            async with driver(**device) as conn:
                for cmd in commands.readlines():
                    if str(cmd).startswith('term len 0'):
                        response = await conn.send_command(cmd)
                    elif str(cmd).startswith('## '):
                        buffer += cmd
                    elif str(cmd) == '\n':
                        pass
                    else:
                        response = await conn.send_command(cmd)
                        output_timestamp = '"' + cmd.replace('\n', '') + '"' + f' @ {date.today()} {time.strftime("%X")}\n'
                        buffer += output_timestamp
                        buffer += '='*len(output_timestamp)
                        buffer += '\n'
                        buffer += response.result
                        buffer += '\n'*9

            print(f'DISCONNECTED: {hostname} @ {time.strftime("%X")}')

            device['driver'] = driver

            return hostname, buffer


    except Exception as e:

        print(f'__ ERROR CONNECTING: {hostname} @ {time.strftime("%X")}')

        buffer += str(e)

        device['driver'] = driver

        return hostname, buffer



######################################################################################
######################################################################################


async def run_async(devices, cmds, folder):

    print()

    try:
        os.makedirs(folder)
    except FileExistsError:
        pass


    tasks = []

    for device in devices:
        for k, v in device.items():
            task = asyncio.create_task(show_command_async(k, v, cmds))
            tasks.append(task)

    results = await asyncio.gather(*tasks, return_exceptions=False)

    for result in results:
        output_file = os.path.join(folder, f'{result[0]}.txt')

        if os.path.exists(output_file) == False:
            pass
        else:
            os.remove(output_file)

        with open(output_file, 'a') as f:
            output = str(result[1])
            f.write(output)
            print(f'OUTPUT FILE CREATED: {result[0]}')

    print()



######################################################################################
######################################################################################



def show_commands_netmiko_sync(hostname, device, cmds):

    print(f'CONNECTING: {hostname} @ {time.strftime("%X")}')

    try:

        buffer = ''

        with open(cmds) as commands:
            with ConnectHandler(**device) as net_connect:
                for cmd in commands.readlines():
                    if str(cmd).startswith('term len 0'):
                        response = net_connect.send_command(cmd)
                    elif str(cmd).startswith('## '):
                        buffer += cmd
                    elif str(cmd) == '\n':
                        pass
                    else:
                        print(f'__ SENDING CMD >> {cmd}')
                        response = net_connect.send_command(cmd)
                        output_timestamp = '"' + cmd.replace('\n', '') + '"' + f' @ {date.today()} {time.strftime("%X")}\n'
                        buffer += output_timestamp
                        buffer += '='*len(output_timestamp)
                        buffer += '\n'
                        buffer += response
                        buffer += '\n'*9
                        print(f'__ CMD CAPTURED << {cmd}')

            print(f'DISCONNECTED: {hostname} @ {time.strftime("%X")}')

            return hostname, buffer


    except Exception as e:

        print(f'__ ERROR CONNECTING: {hostname} @ {time.strftime("%X")}')

        buffer += str(e)

        return hostname, buffer



######################################################################################
######################################################################################



def run_ios_sync(devices, cmds, folder):

    print()

    try:
        os.makedirs(folder)
    except FileExistsError:
        pass


    results = []

    for device in devices:
        for k, v in device.items():
            result = show_commands_netmiko_sync(k, v, cmds)
            results.append(result)


    for result in results:
        output_file = os.path.join(folder, f'{result[0]}.txt')

        if os.path.exists(output_file) == False:
            pass
        else:
            os.remove(output_file)

        with open(output_file, 'a') as f:
            output = str(result[1])
            f.write(output)
            print(f'OUTPUT FILE CREATED: {str(output_file)}')

    print()



######################################################################################
######################################################################################


def run_ios_mthread(devices, cmds, folder):

    print()

    try:
        os.makedirs(folder)
    except FileExistsError:
        pass


    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as ex:
        for device in devices:
            for k, v in device.items():
                results = ex.map(show_commands_netmiko_sync, k, v, cmds, timeout=60)


    for result in results:
        output_file = os.path.join(folder, f'{result[0]}.txt')

        if os.path.exists(output_file) == False:
            pass
        else:
            os.remove(output_file)

        with open(output_file, 'a') as f:
            output = str(result[1])
            f.write(output)
            print(f'OUTPUT FILE CREATED: {result[0]}')

    print()



##############################################################################################
# Run
##############################################################################################


if __name__ == '__main__':

    from devices import nxos_switches, iosxe_switches

    print()


##############################################################################################

    start = time.perf_counter()

    try:

        asyncio.get_event_loop().run_until_complete(run_async(nxos_switches, 'nxos/LN-RDC-ESV-1V_checks.txt', 'nxos/prechecks'))

        asyncio.get_event_loop().run_until_complete(run_async(iosxe_switches, 'iosxe/DB-BUR-11-CER-CORE-1_shows.txt', 'iosxe/prechecks'))

        asyncio.get_event_loop().run_until_complete(run_async(iosxe_switches, 'iosxe/DB-BUR-11-CER-CORE-1_pings.txt', 'iosxe/prechecks'))


        finish = time.perf_counter()
        print(f'CHECKS COMPLETE: @ {time.strftime("%X")} IN {round(finish-start, 2)} SECONDS !!!\n')

    except KeyboardInterrupt:
        print('QUITTING SCRIPT !!!')


##############################################################################################


    pause('PRE CHECKS')


##############################################################################################


    start = time.perf_counter()

    try:

        asyncio.get_event_loop().run_until_complete(run_async(nxos_switches, 'nxos/LN-RDC-ESV-1V_checks.txt', 'nxos/postchecks'))

        asyncio.get_event_loop().run_until_complete(run_async(iosxe_switches, 'iosxe/DB-BUR-11-CER-CORE-1_shows.txt', 'iosxe/postchecks'))

        asyncio.get_event_loop().run_until_complete(run_async(iosxe_switches, 'iosxe/DB-BUR-11-CER-CORE-1_pings.txt', 'iosxe/postchecks'))

        finish = time.perf_counter()
        print(f'CHECKS COMPLETE: @ {time.strftime("%X")} IN {round(finish-start, 2)} SECONDS !!!\n')

    except KeyboardInterrupt:
        print('QUITTING SCRIPT !!!')