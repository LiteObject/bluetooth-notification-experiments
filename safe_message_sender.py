#!/usr/bin/env python3
"""
Safe Bluetooth Message Sender
A safer version that handles connection failures gracefully.
"""

import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime


async def find_connectable_devices():
    """Find devices that are actually connectable."""

    print("🔍 Scanning for connectable devices...")
    devices = await BleakScanner.discover(timeout=10.0)

    if not devices:
        print("❌ No devices found.")
        return []

    print(f"✅ Found {len(devices)} device(s), testing connectivity...")

    connectable_devices = []

    for device in devices:
        print(
            f"🔗 Testing connection to {device.name or 'Unknown'} ({device.address})...")

        try:
            # Try to connect with a short timeout
            async with BleakClient(device.address, timeout=5.0) as client:
                if client.is_connected:
                    print(
                        f"   ✅ Successfully connected to {device.name or 'Unknown'}")
                    connectable_devices.append(device)
                else:
                    print(
                        f"   ❌ Failed to connect to {device.name or 'Unknown'}")

        except Exception as e:
            print(f"   ❌ Connection failed: {str(e)[:50]}...")

    return connectable_devices


async def safe_send_message():
    """Safely send a message to a connectable device."""

    print("🔵 Safe Bluetooth Message Sender")
    print("=" * 50)

    # Find connectable devices
    connectable_devices = await find_connectable_devices()

    if not connectable_devices:
        print("❌ No connectable devices found.")
        print("💡 Make sure devices are:")
        print("   - Powered on")
        print("   - In pairing/discoverable mode")
        print("   - Close to your computer")
        return

    print(f"\n📱 Found {len(connectable_devices)} connectable device(s):")
    for i, device in enumerate(connectable_devices):
        print(f"{i+1}. {device.name or 'Unknown Device'} - {device.address}")

    # Let user select device
    try:
        if len(connectable_devices) == 1:
            choice = 0
            print(
                f"\n🎯 Auto-selecting: {connectable_devices[0].name or 'Unknown'}")
        else:
            choice = int(
                input(f"\nSelect device (1-{len(connectable_devices)}): ")) - 1
            if choice < 0 or choice >= len(connectable_devices):
                print("❌ Invalid selection.")
                return

        target_device = connectable_devices[choice]

    except ValueError:
        print("❌ Invalid input.")
        return

    # Connect and send message
    print(
        f"\n🔗 Connecting to {target_device.name or 'Unknown'} ({target_device.address})...")

    try:
        async with BleakClient(target_device.address, timeout=10.0) as client:
            if not client.is_connected:
                print("❌ Failed to establish connection.")
                return

            print("✅ Connected successfully!")

            # Discover services
            print("\n🔍 Discovering services and characteristics...")
            services = client.services

            if not services:
                print("❌ No services found on device.")
                return

            # Find writable characteristics
            writable_chars = []
            for service in services:
                print(f"📋 Service: {service.uuid}")
                for char in service.characteristics:
                    print(f"   📝 Characteristic: {char.uuid}")
                    print(f"      Properties: {char.properties}")

                    if "write" in char.properties or "write-without-response" in char.properties:
                        writable_chars.append(char)
                        print(f"      ✅ Writable!")

            if not writable_chars:
                print("\n❌ No writable characteristics found.")
                print("💡 This device may not support message sending.")
                return

            # Select characteristic
            print(
                f"\n📝 Found {len(writable_chars)} writable characteristic(s):")
            for i, char in enumerate(writable_chars):
                print(f"{i+1}. {char.uuid}")

            if len(writable_chars) == 1:
                char_choice = 0
                print(f"\n🎯 Auto-selecting: {writable_chars[0].uuid}")
            else:
                try:
                    char_choice = int(
                        input(f"\nSelect characteristic (1-{len(writable_chars)}): ")) - 1
                    if char_choice < 0 or char_choice >= len(writable_chars):
                        print("❌ Invalid selection.")
                        return
                except ValueError:
                    print("❌ Invalid input.")
                    return

            target_char = writable_chars[char_choice]

            # Get message from user
            message = input("\n✏️ Enter message to send: ").strip()
            if not message:
                message = "Hello from Python!"
                print(f"Using default message: {message}")

            # Send message
            print(f"\n📤 Sending message...")
            print(f"   To: {target_char.uuid}")
            print(f"   Message: {message}")

            try:
                data = message.encode('utf-8')
                await client.write_gatt_char(target_char.uuid, data)
                print("✅ Message sent successfully!")

                # Try to read response if the characteristic supports it
                if "read" in target_char.properties:
                    print("\n📥 Checking for response...")
                    try:
                        response = await client.read_gatt_char(target_char.uuid)
                        print(f"✅ Response received: {response}")
                        print(
                            f"   As string: {response.decode('utf-8', errors='ignore')}")
                    except Exception as e:
                        print(f"❌ Could not read response: {e}")

            except Exception as e:
                print(f"❌ Error sending message: {e}")

    except Exception as e:
        print(f"❌ Connection error: {e}")


async def demo_message_types():
    """Demonstrate different message types."""

    print("🔵 Message Types Demo")
    print("=" * 30)

    # Find connectable devices
    connectable_devices = await find_connectable_devices()

    if not connectable_devices:
        print("❌ No connectable devices found for demo.")
        return

    target_device = connectable_devices[0]
    print(
        f"\n🎯 Using device: {target_device.name or 'Unknown'} ({target_device.address})")

    try:
        async with BleakClient(target_device.address, timeout=10.0) as client:
            if not client.is_connected:
                print("❌ Failed to connect.")
                return

            # Find writable characteristics
            writable_chars = []
            for service in client.services:
                for char in service.characteristics:
                    if "write" in char.properties or "write-without-response" in char.properties:
                        writable_chars.append(char)

            if not writable_chars:
                print("❌ No writable characteristics found.")
                return

            target_char = writable_chars[0]
            print(f"📝 Using characteristic: {target_char.uuid}")

            # Demo different message types
            messages = [
                ("String message", "Hello Device!", "utf-8"),
                ("JSON message",
                 '{"type": "greeting", "message": "Hello from Python"}', "utf-8"),
                # "Hello World" in hex
                ("Hex message", "48656c6c6f20576f726c64", "hex"),
                ("Number message", "42", "utf-8"),
            ]

            for msg_type, message, encoding in messages:
                print(f"\n📤 Sending {msg_type}...")
                print(f"   Content: {message}")

                try:
                    if encoding == "hex":
                        data = bytes.fromhex(message)
                    else:
                        data = message.encode(encoding)

                    await client.write_gatt_char(target_char.uuid, data)
                    print("   ✅ Sent successfully!")

                    # Small delay between messages
                    await asyncio.sleep(1)

                except Exception as e:
                    print(f"   ❌ Error: {e}")

    except Exception as e:
        print(f"❌ Connection error: {e}")


def main():
    """Main function."""
    print("🔵 Safe Bluetooth Message Sender")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    print("Choose mode:")
    print("1. Safe message sender")
    print("2. Message types demo")
    print("3. Just find connectable devices")

    try:
        choice = input("Enter your choice (1-3): ").strip()

        if choice == "1":
            asyncio.run(safe_send_message())
        elif choice == "2":
            asyncio.run(demo_message_types())
        elif choice == "3":
            asyncio.run(find_connectable_devices())
        else:
            print("❌ Invalid choice.")

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
