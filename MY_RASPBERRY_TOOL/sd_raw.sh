#!/bin/bash
clear


echo "SD card path"
echo
echo
echo $1
echo
echo
sudo fdisk $1 <<EEOF
p
d
1
d
2
w
EEOF

ls -la /dev/mmcblk0*

sudo fdisk $1 <<EEOF
p
n
p



w
EEOF


umount $1

ls -la /dev/mmcblk0*

echo "Enter the Partition"

read Root_Partition

umount $Root_Partition

echo "mkfs.ext4 $Root_Partition -n root"
su -c "mkfs.ext4 $Root_Partition -n root"

exit 0
