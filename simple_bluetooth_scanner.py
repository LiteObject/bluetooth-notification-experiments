#!/usr/bin/env python3
"""
Simple Bluetooth Device Scanner
A simplified version that focuses on basic device discovery.
"""

import asyncio
from bleak import BleakScanner
from datetime import datetime


async def simple_scan():
    """Simple scan for Bluetooth devices."""
    print("🔍 Scanning for Bluetooth devices...")
    print("=" * 50)

    try:
        # Discover devices
        devices = await BleakScanner.discover(timeout=10.0)

        if not devices:
            print("❌ No Bluetooth devices found.")
            print("Make sure Bluetooth is enabled and devices are discoverable.")
            return

        print(f"✅ Found {len(devices)} Bluetooth device(s):")
        print("=" * 50)

        for i, device in enumerate(devices, 1):
            print(f"Device #{i}:")
            print(f"  Name: {device.name or 'Unknown Device'}")
            print(f"  Address: {device.address}")
            print(
                f"  Details: {device.details if hasattr(device, 'details') else 'N/A'}")
            print("-" * 30)

    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure Bluetooth is enabled on your system.")


def main():
    """Main function."""
    print("🔵 Simple Bluetooth Scanner")
    print(f"⏰ Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    try:
        asyncio.run(simple_scan())
    except KeyboardInterrupt:
        print("\n❌ Scan interrupted by user.")


if __name__ == "__main__":
    main()
