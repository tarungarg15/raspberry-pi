echo "Main programme started"
sleep 20
echo "sleep is over"
sudo systemctl stop bluetooth.service
sudo systemctl disable bluetooth.service
echo "disable bluetooth"
sleep 3
#sudo python /home/pi/ble/bluez-5.44/start.py NO > /home/pi/ble/bluez-5.44/start_log.txt
echo "start script is over"
#sudo python trigger_ble.py /home/pi/ble/bluez-5.44/div/Python/1/ > /home/pi/ble/bluez-5.44/trigger_log.txt

