IP_CHARS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', '.']

def create_server(current_dict, ip_dict, name, ip):
    accept = True
    # filters out cases in which ip has invalid charactars
    for char in ip:
        if char not in IP_CHARS:
            accept = False
    if accept:
        parts = ip.split('.')
        for i in range(len(parts)):
            parts[i] = int(parts[i])
        # rejects cases in which ip has incorrect bits
        if len(parts) != 4 or not(parts[0] in range(0, 256) and parts[1] in range(0, 256) and parts[2] in range(0, 256) and parts[3] in range(0, 256)):
            print('Unable to create server: invalid ip')
        # rejects duplicate ips
        elif ip in ip_dict.values():
            print('Unable to create serer: duplicate ip')
        else:
        # adds server to server dictionary and to ip dictionary to be used for transferring between ip and server
            current_dict[name] = {}
            ip_dict[name] = ip
            print(f'Success: A server with name {name} was created at ip {ip}')
    else:
        print('Unable to create server: invalid ip')

def create_connection(current_dict, server_one, server_two, time):
    # rejects cases in which one or two servers don't exist
    if server_one not in current_dict or server_two not in current_dict:
        print('Unable to create connection: one or more of the servers listed do not exist')
    # rejects cases in which connection exists already
    elif server_two in current_dict[server_one]:
        print('Unable to create connection: connection already exists')
    else:
        current_dict[server_one][server_two] = time
        current_dict[server_two][server_one] = time
        print(f'Success: A server with name {server_one} is now connected to {server_two}')

def trace_path(servers, current, final, visited):
    path = []
    # base case - reached the destination
    if current == final:
        return [final]
    visited[current] = True
    # goes through each possible path
    for server in servers[current]:
        if not visited[server]:
            # recursive case
            path = trace_path(servers, server, final, visited)
            if path:
                return [current] + path
    visited[current] = False
    return path

def path_ping(servers, path):
    # returns a list with the time it takes for each step in the path
    time_list = ['0']
    for i in range(len(path)-1):
        time_list.append(servers[path[i]][path[i+1]])
    return time_list

def start():
    command = input()
    servers = {}
    ips = {}
    current = ''
    # main loop starts
    while command != 'quit':
        cmd = command.split(' ')
        cmd_choice = cmd[0]
        if 'create-server' == cmd_choice:
            create_server(servers, ips, cmd[1], cmd[2])

        elif 'create-connection' == cmd_choice:
            create_connection(servers, cmd[1], cmd[2], cmd[3])

        elif 'set-server' == cmd_choice:
            choice = cmd[1]
            # rejects cases in which the ip or server does not exist
            if choice in servers:
                current = choice
            elif choice in ips.values():
                for server, ip in ips.items():
                    if ip == choice:
                        current = server
            if current:
                print(f'Server {choice} selected.')
            else:
                print('Unable to set server: server or ip not found')

        elif 'ping' == cmd_choice or 'traceroute' == cmd_choice or 'tracert' == cmd_choice:
            final = cmd[1]
            # rejects cases in which a server is not yet set
            if current:
                visited = {}
                for y in servers:
                    visited[y] = False
                path = []
                # rejects cases in which the server or ip address does not exist
                if final in servers:
                    path = trace_path(servers, current, final, visited)
                elif final in ips.values():
                    # inverts dictionary to convert ip to server
                    for server, ip in ips.items():
                        if ip == final:
                            new_final = server
                    path = trace_path(servers, current, new_final, visited)
                else:
                    print(f'Unable to trace: server or ip address does not exist')

                times = path_ping(servers, path)
                # rejects cases in which there is no path to the destination
        if path:
                    if 'ping' == cmd_choice:
                        # adds up total time of path
                        total = 0
                        for time in times:
                            total += int(time)
                        print(f'Reply from {ips.get(final, final)} time = {str(total)} ms.')
                    elif ('traceroute' == cmd_choice or 'tracert' == cmd_choice):
                        print(f'Tracing route to {path[len(path)-1]} [{final}]')
                        # prints out each iteration of the path
                        for i in range(len(path)):
                            print(f'\t{i}\t{times[i]}\t[{ips[path[i]]}]\t{path[i]}')
                        print('Trace complete')
                else:
                    print(f'Unable to find path to target system {final}')
            else:
                print('Unable to trace: current server is not set')

        elif command == 'display-servers':
            for serv in servers:
                print(f'\t{serv}\t{ips[serv]}')
                for connection in servers[serv]:
                    print(f'\t\t{connection}\t{ips[connection]}\t{servers[serv][connection]}')

        elif command == 'ip-config':
            print(current + ips[current])
        # rejects invalid commands
        else:
            print('Invalid command')
        command = input()

if __name__ == '__main__':
    start()
