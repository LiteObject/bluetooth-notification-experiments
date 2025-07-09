#!/usr/bin/env python3
"""
Bluetooth Device Scanner
Scans for available Bluetooth devices and prints their information.
"""

import asyncio
import sys
from bleak import BleakScanner
from datetime import datetime


async def scan_bluetooth_devices(duration=10):
    """
    Scan for Bluetooth devices and print their information.

    Args:
        duration (int): Duration in seconds to scan for devices
    """
    print(f"🔍 Scanning for Bluetooth devices for {duration} seconds...")
    print("=" * 60)

    try:
        # Start scanning for devices
        devices = await BleakScanner.discover(timeout=duration)

        if not devices:
            print("❌ No Bluetooth devices found.")
            return

        print(f"✅ Found {len(devices)} Bluetooth device(s):")
        print("=" * 60)

        # Sort devices by name for better readability
        sorted_devices = sorted(devices, key=lambda x: x.name or "Unknown")

        for i, device in enumerate(sorted_devices, 1):
            print(f"📱 Device #{i}")
            print(f"   Name: {device.name or 'Unknown'}")
            print(f"   Address: {device.address}")

            # Print additional device information if available
            if hasattr(device, 'details') and device.details:
                print(f"   Details: {device.details}")

            print("-" * 40)

    except Exception as e:
        print(f"❌ Error scanning for devices: {e}")
        print("Make sure Bluetooth is enabled on your system.")


async def scan_with_advertisement_data():
    """
    Scan for devices with detailed advertisement data.
    """
    print("🔍 Scanning for Bluetooth devices with advertisement data...")
    print("=" * 60)

    devices_found = []

    def detection_callback(device, advertisement_data):
        """Callback function called when a device is detected."""
        devices_found.append((device, advertisement_data))

        print(f"📱 Device detected: {device.name or 'Unknown'}")
        print(f"   Address: {device.address}")
        print(f"   RSSI: {advertisement_data.rssi} dBm")

        # Print advertisement data
        if advertisement_data:
            print(f"   Local Name: {advertisement_data.local_name}")
            print(
                f"   Manufacturer Data: {advertisement_data.manufacturer_data}")
            print(f"   Service Data: {advertisement_data.service_data}")
            print(f"   Service UUIDs: {advertisement_data.service_uuids}")

        print("-" * 40)

    try:
        # Start scanning with callback
        scanner = BleakScanner(detection_callback)
        await scanner.start()

        # Scan for 10 seconds
        await asyncio.sleep(10)

        await scanner.stop()

        print(f"✅ Scan completed. Found {len(devices_found)} device(s).")

    except Exception as e:
        print(f"❌ Error during scanning: {e}")


def print_system_info():
    """Print system information."""
    print("🖥️  System Information:")
    print(f"   Python version: {sys.version}")
    print(f"   Platform: {sys.platform}")
    print(f"   Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)


async def main():
    """Main function to run the Bluetooth scanner."""
    print("🔵 Bluetooth Device Scanner")
    print("=" * 60)

    print_system_info()

    # Ask user for scan type
    print("\nChoose scan type:")
    print("1. Basic scan (default)")
    print("2. Detailed scan with advertisement data")

    try:
        choice = input("\nEnter your choice (1 or 2): ").strip()

        if choice == "2":
            await scan_with_advertisement_data()
        else:
            await scan_bluetooth_devices()

    except KeyboardInterrupt:
        print("\n❌ Scan interrupted by user.")
    except Exception as e:
        print(f"❌ Unexpected error: {e}")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
