#!/usr/bin/env python3
"""
Simple Bluetooth Message Sender
A simplified example showing how to send messages to Bluetooth devices.
"""

import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime


async def send_message_example():
    """Example of how to send a message to a Bluetooth device."""

    print("🔵 Simple Bluetooth Message Sender")
    print("=" * 50)

    # Step 1: Scan for devices
    print("🔍 Scanning for devices...")
    devices = await BleakScanner.discover(timeout=5.0)

    if not devices:
        print("❌ No devices found.")
        return

    print(f"✅ Found {len(devices)} device(s):")
    for i, device in enumerate(devices):
        print(f"{i+1}. {device.name or 'Unknown'} - {device.address}")

    # Step 2: Select a device (for demo, we'll use the first one)
    if not devices:
        return

    # You can change this to select a specific device
    target_device = devices[0]
    print(
        f"\n🎯 Targeting device: {target_device.name or 'Unknown'} ({target_device.address})")

    # Step 3: Connect to the device
    print(f"\n🔗 Connecting to {target_device.address}...")

    async with BleakClient(target_device.address) as client:
        if client.is_connected:
            print("✅ Connected successfully!")

            # Step 4: Discover services and characteristics
            print("\n🔍 Discovering services...")
            services = client.services

            writable_chars = []
            for service in services:
                print(f"📋 Service: {service.uuid}")
                for char in service.characteristics:
                    print(f"   📝 Characteristic: {char.uuid}")
                    print(f"      Properties: {char.properties}")

                    # Check if characteristic is writable
                    if "write" in char.properties or "write-without-response" in char.properties:
                        writable_chars.append(char)
                        print(f"      ✅ This characteristic is writable!")

            # Step 5: Send a message (if we found writable characteristics)
            if writable_chars:
                print(
                    f"\n📤 Found {len(writable_chars)} writable characteristic(s)")

                # Example: Send to the first writable characteristic
                target_char = writable_chars[0]
                message = "Hello from Python!"

                print(f"📤 Sending message to {target_char.uuid}...")
                print(f"   Message: {message}")

                try:
                    await client.write_gatt_char(target_char.uuid, message.encode('utf-8'))
                    print("✅ Message sent successfully!")

                except Exception as e:
                    print(f"❌ Error sending message: {e}")

            else:
                print("❌ No writable characteristics found on this device.")

        else:
            print("❌ Failed to connect to device.")


async def interactive_sender():
    """Interactive version where user can select device and characteristic."""

    print("🔵 Interactive Bluetooth Message Sender")
    print("=" * 50)

    # Scan for devices
    print("🔍 Scanning for devices...")
    devices = await BleakScanner.discover(timeout=10.0)

    if not devices:
        print("❌ No devices found.")
        return

    # Display devices
    print(f"✅ Found {len(devices)} device(s):")
    for i, device in enumerate(devices):
        print(f"{i+1}. {device.name or 'Unknown Device'} - {device.address}")

    # Let user select device
    try:
        choice = int(input(f"\nSelect device (1-{len(devices)}): ")) - 1
        if choice < 0 or choice >= len(devices):
            print("❌ Invalid selection.")
            return

        target_device = devices[choice]
        print(
            f"\n🎯 Selected: {target_device.name or 'Unknown'} ({target_device.address})")

    except ValueError:
        print("❌ Invalid input.")
        return

    # Connect to device
    print(f"\n🔗 Connecting to {target_device.address}...")

    async with BleakClient(target_device.address) as client:
        if not client.is_connected:
            print("❌ Failed to connect to device.")
            return

        print("✅ Connected successfully!")

        # Discover services and find writable characteristics
        print("\n🔍 Discovering services...")
        services = client.services

        writable_chars = []
        for service in services:
            for char in service.characteristics:
                if "write" in char.properties or "write-without-response" in char.properties:
                    writable_chars.append(char)

        if not writable_chars:
            print("❌ No writable characteristics found on this device.")
            return

        # Display writable characteristics
        print(f"\n📝 Found {len(writable_chars)} writable characteristic(s):")
        for i, char in enumerate(writable_chars):
            print(f"{i+1}. {char.uuid} (Properties: {char.properties})")

        # Let user select characteristic
        try:
            choice = int(
                input(f"\nSelect characteristic (1-{len(writable_chars)}): ")) - 1
            if choice < 0 or choice >= len(writable_chars):
                print("❌ Invalid selection.")
                return

            target_char = writable_chars[choice]
            print(f"\n🎯 Selected characteristic: {target_char.uuid}")

        except ValueError:
            print("❌ Invalid input.")
            return

        # Get message from user
        message = input("\nEnter message to send: ")

        # Send message
        print(f"\n📤 Sending message...")
        print(f"   To: {target_char.uuid}")
        print(f"   Message: {message}")

        try:
            await client.write_gatt_char(target_char.uuid, message.encode('utf-8'))
            print("✅ Message sent successfully!")

        except Exception as e:
            print(f"❌ Error sending message: {e}")


def main():
    """Main function."""
    print("🔵 Bluetooth Message Sender")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    print("Choose mode:")
    print("1. Simple example (auto-select first device)")
    print("2. Interactive mode (select device and characteristic)")

    try:
        choice = input("Enter your choice (1-2): ").strip()

        if choice == "1":
            asyncio.run(send_message_example())
        elif choice == "2":
            asyncio.run(interactive_sender())
        else:
            print("❌ Invalid choice.")

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
