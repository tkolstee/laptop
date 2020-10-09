#!/bin/bash

dpkg -l avahi-daemon || apt-get install avahi-daemon
systemctl enable avahi-daemon

for directive in HandleLidSwitch HandleLidSwitchExternalPower HandleLidSwitchDocked; do
  egrep -q "^\s*${directive}\s*=" /etc/systemd/login.conf
  if [ $? == 0 ]; then
    sed -i -e 's/^\s*${directive}\s*=.*$/${directive}=lock/' /etc/systemd/logind.conf
  else
    echo "${directive}=lock" >> /etc/systemd/logind.conf
  fi
done
systemctl restart systemd-logind.service

install -o root -g root -m 0755 backlightd /usr/local/bin/backlightd
install -o root -g root -m 0644 backlightd.service /lib/systemd/system/backlightd.service

systemctl enable backlightd.service
systemctl start backlightd.service
