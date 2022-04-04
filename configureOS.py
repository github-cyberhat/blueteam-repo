import os
import subprocess
import secrets
import string

from io import StringIO
from sys import stderr, stdin

RHEL_COMMANDS = [
    "sudo yum update",
    "yum install -y epel-release"
    "yum -y install clamav-server clamav-data clamav-update clamav-filesystem clamav clamav-scanner-systemd clamav-devel clamav-lib clamav-server-systemd",
    "yum install Fail2ban",
    "yum remove liblog4j-java"
]

DEBIAN_COMMANDS = [
    "apt-get update",
    "apt-get upgrade",
    "apt-get install clamav",
    "systemctl stop clamav-freshclam",
    "freshclam",
    "systemctl start clamav-freshclam",
    "apt install build-essential libpcap-dev libpcre3-dev libnet1-dev zlib1g-dev luajit hwloc libdnet-dev libdumbnet-dev bison flex liblzma-dev openssl libssl-dev pkg-config libhwloc-dev cmake cpputest libsqlite3-dev uuid-dev libcmocka-dev libnetfilter-queue-dev libmnl-dev autotools-dev libluajit-5.1-dev libunwind-dev",
    "apt install Fail2ban",
    "apt purge liblog4j-java"
]


def main():
    distro = input("Please enter your Linux distribution (Debian\\RHEL):\n ")
    commands = RHEL_COMMANDS if distro == "RHEL" else DEBIAN_COMMANDS

    for command in commands:
        print(f"[x] Running '{command}'.......\n")
        with subprocess.Popen("/bin/bash", stdin=subprocess.PIPE) as process:
            process.communicate(("yes |" + command).encode("utf-8"))
            print("\n")

    configure_firewall()
    secure_passwords_change_usernames()
    set_directory_permissions()


def secure_passwords_change_usernames():
    print("[x] Securing passwords...\n")
    secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(20)))
    password = ''.join((secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20)))

    with open("/etc/passwd", "r") as users_file:
        for line in users_file.readlines():
            user_name, _ = line.split(":", 1)
            secure_str = ''.join((secrets.choice(string.ascii_letters) for i in range(20)))
            password = ''.join(
                (secrets.choice(string.ascii_letters + string.digits + string.punctuation) for i in range(20)))
            if user_name not in ["root", "cyberuser2", "www-data", "apache"]:
                print(f"[x] Securing password of user '{user_name}'\n")
                subprocess.run(["passwd", user_name], input=f"{password}\n{password}".encode("utf-8"))
                print(f"[x] Changing username of user '{user_name}'\n")
                subprocess.run(f"usermod -l {user_name} {user_name + '1'}")


def configure_firewall():
    print("[x] Configuring IP tables rules...\n")
    commands = [
        "iptables -A INPUT -p tcp -s {ip}/24 --dport {port} -m conntrack --ctstate NEW,ESTABLISHED -j ACCEPT",
        "iptables -A OUTPUT -p tcp --sport 22 -m conntrack --ctstate ESTABLISHED -j ACCEPT",
        "iptables -A INPUT -i eth1 -s 0.0.0.0/0 -j LOG --log-prefix \"IP_SPOOF A: \"",
        "iptables -A INPUT -i eth1 -s 0.0.0.0/0 -j DROP"
    ]
    subnet = input("- Please enter your subnet (format x.x.x.0):\n")
    port = int(input("- Please enter the defined SSH port:\n"))

    with subprocess.Popen("/bin/bash", stdin=subprocess.PIPE) as popen:
        popen.communicate(commands[0].format(ip=subnet, port=port).encode("utf-8"))
    for command in commands[1:]:
        with subprocess.Popen("/bin/bash", stdin=subprocess.PIPE) as popen:
            popen.communicate(command.encode("utf-8"))


def set_directory_permissions():
    print("[x] Setting strict directory permissions...\n")
    directories = ["tmp", "snap", "root", "home"]
    for directory in directories:
        with subprocess.Popen("/bin/bash", stdin=subprocess.PIPE) as popen:
            print(f"[x] Changing permissions for {directory} \n")
            popen.communicate(f"chmod -R 744 xyz /{directory}".encode("utf-8"))


if __name__ == "__main__":
    main()
