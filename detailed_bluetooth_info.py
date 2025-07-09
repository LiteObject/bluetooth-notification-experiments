#!/usr/bin/env python3
"""
Bluetooth Device Information Extractor
Gets detailed information about discovered Bluetooth devices.
"""

import asyncio
from bleak import BleakScanner
from datetime import datetime


async def get_device_info():
    """Get detailed information about Bluetooth devices."""
    print("🔍 Scanning for Bluetooth devices with detailed information...")
    print("=" * 70)

    try:
        # Use the detection callback to get real-time data
        devices_data = []

        def device_callback(device, advertisement_data):
            """Callback for when a device is discovered."""
            devices_data.append((device, advertisement_data))

        # Start scanning
        scanner = BleakScanner(detection_callback=device_callback)
        await scanner.start()

        # Scan for 10 seconds
        print("⏳ Scanning for 10 seconds...")
        await asyncio.sleep(10)

        await scanner.stop()

        if not devices_data:
            print("❌ No devices found.")
            return

        print(
            f"✅ Found {len(devices_data)} device(s) with advertisement data:")
        print("=" * 70)

        # Sort by device name
        devices_data.sort(key=lambda x: x[0].name or "Unknown")

        for i, (device, adv_data) in enumerate(devices_data, 1):
            print(f"📱 Device #{i}: {device.name or 'Unknown Device'}")
            print(f"   🔗 Address: {device.address}")
            print(f"   📡 RSSI: {adv_data.rssi} dBm")
            print(f"   🔋 TX Power: {adv_data.tx_power}")

            # Local name
            if adv_data.local_name:
                print(f"   📝 Local Name: {adv_data.local_name}")

            # Manufacturer data
            if adv_data.manufacturer_data:
                print(f"   🏭 Manufacturer Data:")
                for company_id, data in adv_data.manufacturer_data.items():
                    print(f"      Company ID {company_id}: {data.hex()}")

            # Service UUIDs
            if adv_data.service_uuids:
                print(f"   🔧 Service UUIDs:")
                for uuid in adv_data.service_uuids:
                    print(f"      {uuid}")

            # Service data
            if adv_data.service_data:
                print(f"   📊 Service Data:")
                for uuid, data in adv_data.service_data.items():
                    print(f"      {uuid}: {data.hex()}")

            # Platform specific data
            if hasattr(adv_data, 'platform_data'):
                print(f"   💻 Platform Data: {adv_data.platform_data}")

            print("-" * 50)

    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main function."""
    print("🔵 Bluetooth Device Information Extractor")
    print(f"⏰ Scan time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)

    try:
        asyncio.run(get_device_info())
    except KeyboardInterrupt:
        print("\n❌ Scan interrupted by user.")


if __name__ == "__main__":
    main()
