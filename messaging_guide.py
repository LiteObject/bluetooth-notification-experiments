#!/usr/bin/env python3
"""
Bluetooth Messaging Guide
A comprehensive guide showing how to send messages to Bluetooth devices.
"""

import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime
import json


# Example 1: Basic message sending
async def basic_message_example():
    """Basic example of sending a message to a Bluetooth device."""

    print("📝 Basic Message Example")
    print("=" * 30)

    # Replace with your device's address
    DEVICE_ADDRESS = "XX:XX:XX:XX:XX:XX"

    # Replace with your device's characteristic UUID
    CHARACTERISTIC_UUID = "12345678-1234-5678-9012-123456789abc"

    message = "Hello from Python!"

    try:
        async with BleakClient(DEVICE_ADDRESS) as client:
            if client.is_connected:
                # Send message
                await client.write_gatt_char(CHARACTERISTIC_UUID, message.encode('utf-8'))
                print(f"✅ Sent: {message}")
            else:
                print("❌ Failed to connect")

    except Exception as e:
        print(f"❌ Error: {e}")


# Example 2: Discovery and sending
async def discovery_and_send_example():
    """Example that discovers devices and sends messages."""

    print("🔍 Discovery and Send Example")
    print("=" * 35)

    # Step 1: Scan for devices
    print("Scanning for devices...")
    devices = await BleakScanner.discover(timeout=5.0)

    if not devices:
        print("No devices found")
        return

    # Step 2: Try to connect to first device
    device = devices[0]
    print(f"Trying to connect to: {device.name or 'Unknown'}")

    try:
        async with BleakClient(device.address) as client:
            if not client.is_connected:
                print("Failed to connect")
                return

            print("Connected successfully!")

            # Step 3: Find writable characteristics
            for service in client.services:
                for char in service.characteristics:
                    if "write" in char.properties:
                        print(f"Found writable characteristic: {char.uuid}")

                        # Step 4: Send message
                        message = "Test message"
                        await client.write_gatt_char(char.uuid, message.encode('utf-8'))
                        print(f"Sent: {message}")
                        break

    except Exception as e:
        print(f"Error: {e}")


# Example 3: Notification sending
async def notification_example():
    """Example of sending structured notifications."""

    print("📱 Notification Example")
    print("=" * 25)

    # Create notification data
    notification = {
        "title": "Python Notification",
        "message": "This is a test notification",
        "timestamp": datetime.now().isoformat(),
        "priority": "normal"
    }

    # Convert to JSON
    notification_json = json.dumps(notification)

    # Scan for devices
    devices = await BleakScanner.discover(timeout=3.0)

    for device in devices:
        print(f"Trying to send notification to: {device.name or 'Unknown'}")

        try:
            async with BleakClient(device.address, timeout=5.0) as client:
                if client.is_connected:
                    # Find suitable characteristic
                    for service in client.services:
                        for char in service.characteristics:
                            if "write" in char.properties:
                                await client.write_gatt_char(char.uuid, notification_json.encode('utf-8'))
                                print(
                                    f"✅ Notification sent to {device.name or 'Unknown'}")
                                break
                        break

        except Exception as e:
            print(
                f"❌ Failed to send to {device.name or 'Unknown'}: {str(e)[:30]}...")


# Example 4: Interactive messaging
async def interactive_messaging():
    """Interactive example where user chooses device and message."""

    print("💬 Interactive Messaging")
    print("=" * 25)

    # Scan for devices
    print("Scanning for devices...")
    devices = await BleakScanner.discover(timeout=5.0)

    if not devices:
        print("No devices found")
        return

    # Display devices
    print("Available devices:")
    for i, device in enumerate(devices):
        print(f"{i+1}. {device.name or 'Unknown'} ({device.address})")

    # User selects device
    try:
        choice = int(input("Select device: ")) - 1
        selected_device = devices[choice]
    except (ValueError, IndexError):
        print("Invalid selection")
        return

    # User enters message
    message = input("Enter message: ")

    # Send message
    print(f"Sending to {selected_device.name or 'Unknown'}...")

    try:
        async with BleakClient(selected_device.address) as client:
            if client.is_connected:
                # Find first writable characteristic
                for service in client.services:
                    for char in service.characteristics:
                        if "write" in char.properties:
                            await client.write_gatt_char(char.uuid, message.encode('utf-8'))
                            print("✅ Message sent!")
                            return

                print("❌ No writable characteristics found")
            else:
                print("❌ Failed to connect")

    except Exception as e:
        print(f"❌ Error: {e}")


# Example 5: Common device types
async def device_specific_examples():
    """Examples for specific device types."""

    print("🔧 Device-Specific Examples")
    print("=" * 30)

    # Example for Arduino/ESP32 devices
    print("Arduino/ESP32 Example:")
    print("- Characteristic UUID: 6E400002-B5A3-F393-E0A9-E50E24DCCA9E (Nordic UART TX)")
    print("- Message format: Plain text")
    print("- Example: 'LED_ON' or 'LED_OFF'")
    print()

    # Example for phone notifications
    print("Phone Notification Example:")
    notification = {
        "app": "MyApp",
        "title": "New Message",
        "body": "You have a new notification",
        "timestamp": datetime.now().isoformat()
    }
    print(f"- Message format: {json.dumps(notification, indent=2)}")
    print()

    # Example for IoT devices
    print("IoT Device Example:")
    iot_command = {
        "command": "set_temperature",
        "value": 22.5,
        "unit": "celsius"
    }
    print(f"- Command format: {json.dumps(iot_command, indent=2)}")


def main():
    """Main function with examples."""

    print("🔵 Bluetooth Messaging Guide")
    print(f"⏰ Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    examples = [
        ("Basic message sending", basic_message_example),
        ("Discovery and send", discovery_and_send_example),
        ("Notification example", notification_example),
        ("Interactive messaging", interactive_messaging),
        ("Device-specific examples", device_specific_examples),
    ]

    print("Choose an example:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")

    try:
        choice = int(input("Enter choice (1-5): ")) - 1
        if 0 <= choice < len(examples):
            name, func = examples[choice]
            print(f"\n🚀 Running: {name}")
            print("=" * 40)
            asyncio.run(func())
        else:
            print("❌ Invalid choice")

    except (ValueError, KeyboardInterrupt):
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
