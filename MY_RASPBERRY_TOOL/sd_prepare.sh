#!/bin/bash
clear


echo "SD card path"
echo $1
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
1
2048
819199
t
b
a
n
p



w
EEOF


umount $1

ls -la /dev/mmcblk0*

echo "Enter the boot partition"

read Boot_Partition

umount $Boot_Partition

echo "mkfs.vfat $Boot_Partition -n boot"
su -c "mkfs.vfat $Boot_Partition -n boot"

echo "Enter the root partition"

read Root_Partition
umount $Root_Partition

echo "mkfs.ext4 $Root_Partition -L root"
su -c "mkfs.ext4 $Root_Partition -L root"

exit 0
