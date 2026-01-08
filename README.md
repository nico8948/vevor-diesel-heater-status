# Vevor diesel heater control and status

This project provides a Python script for getting the control and status off a VEVOR diesel air heater.

## Description

The script is based on esp project: https://github.com/atholbro/esp32-vevor-ble
see also: https://github.com/spin877/Bruciatore_BLE

## Features

- Monitoring and displaying information received from the heater, such as temperature, ignition status, power, and more in json format.

## Requirements

- Python 3.x
- pip install bleak

## Usage

1. Ensure your Bluetooth device is enabled.
   - systemctl enable bluetooth
   - use bluetoothctl to scan for the mac addresses.
2. Run the Python script:  vevorheaterstatus.py


## Supported Commands

Available Commands:
Usage: vevorheatercontrol.py <mac address> command:

vevorheatercontrol.py <mac address> p1/p0 (On/Off)
vevorheatercontrol.py <mac address> l1 to t10 (Set heating level from 1 to 10)
vevorheatercontrol.py <mac address> s (Get status)
  
## Product Information

For more details about the VEVOR Diesel Air Heater, visit the [VEVOR product page](https://www.vevor.com/s/diesel-heater).

## Important Note

This project is created for educational purposes and automation of the VEVOR diesel air heater. Use the software at your own risk. The author is not responsible for any damage resulting from the improper use of the code.

