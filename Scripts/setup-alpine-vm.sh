#!/bin/sh

#
#  setup-alpine-vm.sh
#  Progetto di Distributed Systems and Big Data
#  Anno Accademico 2024-25
#  (C) 2024 Luca Montera, Alessio Giordano
#
#  Created by Alessio Giordano on 21/11/24.
#

vi /etc/apk/repositories # Decomment community repo
apk update
apk upgrade
apk add docker docker-cli-compose
rc-update add docker boot
apk add open-vm-tools open-vm-tools-guestinfo open-vm-tools-deploypkg open-vm-tools-plugins-all
rc-update add open-vm-tools boot
mkdir shared
modprobe fuse
/usr/bin/vmhgfs-fuse .host:/shared /root/shared
apk add python3 py3-pip
apk add curl
vi /etc/inittab # tty1::respawn:/bin/sh
apk add vim
echo "#!/sbin/openrc-run" >> /etc/init.d/mount_shared
echo "start() {" >> /etc/init.d/mount_shared
echo "ebegin \"Mounting shared directory\"" >> /etc/init.d/mount_shared
echo "modprobe fuse" >> /etc/init.d/mount_shared
echo "/usr/bin/vmhgfs-fuse .host:/shared /root/shared" >> /etc/init.d/mount_shared
echo "eend $?" >> /etc/init.d/mount_shared
echo "}" >> /etc/init.d/mount_shared
chmod +x /etc/init.d/mount_shared
rc-update add mount_shared boot