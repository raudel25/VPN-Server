from vpn import VPN, UserClient
from udp import UDP
from tcp import TCP
from rules import RestrictUser, RestrictVLAN
import threading


def help():
    print("help: Show the commands")
    print("create_user <user> <password> <id_vlan>: Create a new user")
    print('remove_user <id>: Remove a user')
    print('show_users: Show all users')
    print("start <protocol>: Start the VPN")
    print("stop: Stop the VPN")
    print("restrict_user <rule_name> <id_user> <dest_ip> <dest_port>: Restrict a user to sent data")
    print("restrict_vlan <rule_name> <id_vlan> <dest_ip> <dest_port>: Restrict a vlan to sent data")
    print("show_rules: Show all rules")
    print("exit: Exit the program\n")


ip = 'localhost'
port = 5001

udp = UDP(ip, port)
tcp = TCP(ip, port)

vpn = VPN(tcp)
vpn_thread = None

print("Welcome to the VPN")
print(f"Running on {ip}:{port} \n")
help()

while True:
    command = input()
    command = command.split(' ')

    if len(command) == 0:
        print("Invalid command\n")

    if command[0] == "create_user" and len(command) == 4 and str.isdigit(command[3]):
        user = command[1]
        password = command[2]
        id_vlan = int(command[3])
        vpn.create_user(UserClient(user, password, id_vlan))

    elif command[0] == "remove_user" and len(command) == 2 and str.isdigit(command[1]):
        vpn.remove_user(int(command[1]))

    elif command[0] == "show_users":
        vpn.show_users()

    elif command[0] == "start" and len(command) == 2:
        if (vpn_thread is not None):
            print("VPN already started\n")
            continue

        if command[1] == "tcp":
            vpn.protocol = tcp
        elif command[1] == "udp":
            vpn.protocol = udp
        else:
            print("Invalid command\n")
            continue

        vpn_thread = threading.Thread(target=vpn.run)
        vpn_thread.start()

    elif command[0] == "stop":
        if (vpn_thread is None):
            print("VPN not started\n")
            continue
        vpn.stop()
        vpn_thread.join()
        vpn_thread = None

    elif command[0] == 'restrict_vlan' and len(command) == 5 and str.isdigit(command[2]) and str.isdigit(command[4]):
        rule = RestrictVLAN(command[1], command[3],
                            int(command[4]), int(command[2]))
        vpn.add_rule(rule)

    elif command[0] == 'restrict_user' and len(command) == 5 and str.isdigit(command[2]) and str.isdigit(command[4]):
        rule = RestrictUser(command[1], command[3],
                            int(command[4]), int(command[2]))
        vpn.add_rule(rule)

    elif command[0] == "show_rules":
        vpn.show_rules()

    elif command[0] == "remove_rule" and len(command) == 2 and str.isdigit(command[1]):
        vpn.remove_rule(int(command[1]))

    elif command[0] == "exit":
        if (vpn_thread is not None):
            vpn.stop()
            vpn_thread.join()
        break

    elif command[0] == "help":
        help()
    else:
        print("Invalid command\n")
