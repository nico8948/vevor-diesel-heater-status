#!/usr/bin/python3

import asyncio
from bleak import BleakClient
import sys
import json

SERVICE_UUID = "0000ffe0-0000-1000-8000-00805f9b34fb"
CHAR_UUID    = "0000ffe1-0000-1000-8000-00805f9b34fb"

XOR_KEY = b"password"


def checksum(*b):
    return sum(b) & 0xFF


def build_packet(passkey, cmd, d0=0x00, d1=0x00):
    hi = passkey // 100
    lo = passkey % 100
    return bytes([
        0xAA, 0x55,
        hi, lo,
        cmd, d0, d1,
        checksum(hi, lo, cmd, d0, d1)
    ])


def decrypt(raw: bytes):
    if len(raw) == 48 and raw[0] == 0xDA and raw[1] == 0x07:
        return bytes(raw[i] ^ XOR_KEY[i % 8] for i in range(len(raw)))
    return None


def s16(hi, lo):
    v = (hi << 8) | lo
    return v - 65536 if v > 32767 else v


def parse(frame: bytes):
    if frame[:2] != b"\xAA\x66":
        return None

    running_state_map = {
        0: "Uit",
        1: "Zelf test",
        2: "Onsteken",
        3: "Verwarmen",
        4: "Uitzetten",
        }
    heater_on_off = {
        0: "Uit",
        1: "Aan",
    }
#    heater_on_off {
#        0: "Off",
#        1: "On",

#    running_state_map = {
#        0x00: "Off",
#        0x01: "Self test running",
#        0x02: "Ignition",
#        0x03: "Heating",
#        0x04: "Shutting down",
#        }

    frames = { 
        "heater_on": heater_on_off[frame[3]],
        "error": frame[4],
        "step": running_state_map[frame[5]],
        "mode": frame[8],
        "run_temp": frame[9],
        "run_level": frame[10],
        "voltage": (256 * frame[11] + frame[12]) / 10,
        "shell_temp": s16(frame[13], frame[14]),
        "room_temp": s16(frame[32], frame[33]) / 10,
        "altitude_m": (256 * frame[6] + frame[7]) / 10,
    }

    status = json.dumps(frames)
    return status


class DieselHeater:
    def __init__(self, mac, passkey):
        self.client = BleakClient(mac)
        self.passkey = passkey

    async def connect(self):
        await self.client.connect()
        await self.client.start_notify(CHAR_UUID, self.on_notify)
#        print("✅ BLE connected")

    async def send(self, cmd, d0=0, d1=0):
        pkt = build_packet(self.passkey, cmd, d0, d1)
        await self.client.write_gatt_char(CHAR_UUID, pkt)

    async def poll(self):
        await self.send(0x01)

    async def power(self, on: bool):
        await self.send(0x03, 1 if on else 0)

    async def set_mode(self, auto: bool):
        await self.send(0x02, 0x02 if auto else 0x01)

    async def set_temp(self, celsius: int):
        await self.send(0x04, celsius)

    async def set_level(self, level: int):
        await self.send(0x04, level)

    def on_notify(self, _, data: bytearray):
        raw = bytes(data)
        dec = decrypt(raw)
        if not dec:
            return

        parsed = parse(dec)
        if parsed:
            print(parsed)


async def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <mac address> ")
        sys.exit(1)
    heater = DieselHeater(
        mac=str(sys.argv[1]),   # <-- your heater MAC
        passkey=1234               # <-- your passkey
    )

    await heater.connect()
    await heater.poll()
#    await asyncio.sleep(10)

#    while True:
#        await heater.poll()
#        await asyncio.sleep(10)


asyncio.run(main())
