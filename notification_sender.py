#!/usr/bin/env python3
"""
Bluetooth Notification Sender
Demonstrates how to send notifications to connected Bluetooth devices.
"""

import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime
import json


async def send_notification_to_device(device_address, notification_data):
    """Send a notification to a specific device."""

    print(f"📱 Sending notification to {device_address}")
    print(f"   Data: {notification_data}")

    try:
        async with BleakClient(device_address) as client:
            if not client.is_connected:
                print("❌ Failed to connect to device.")
                return False

            print("✅ Connected to device")

            # Find a suitable characteristic for notifications
            # This varies by device - you'll need to know the specific UUIDs for your device
            services = client.services

            for service in services:
                for char in service.characteristics:
                    # Look for writable characteristics
                    if "write" in char.properties or "notify" in char.properties:
                        print(f"📝 Found suitable characteristic: {char.uuid}")

                        # Convert notification data to bytes
                        if isinstance(notification_data, str):
                            data = notification_data.encode('utf-8')
                        elif isinstance(notification_data, dict):
                            data = json.dumps(
                                notification_data).encode('utf-8')
                        else:
                            data = str(notification_data).encode('utf-8')

                        # Send the notification
                        await client.write_gatt_char(char.uuid, data)
                        print("✅ Notification sent successfully!")
                        return True

            print("❌ No suitable characteristics found for notifications.")
            return False

    except Exception as e:
        print(f"❌ Error sending notification: {e}")
        return False


async def broadcast_notification(notification_data):
    """Broadcast a notification to all discoverable devices."""

    print("📡 Broadcasting notification to all devices...")
    print(f"   Data: {notification_data}")

    # Discover devices
    devices = await BleakScanner.discover(timeout=5.0)

    if not devices:
        print("❌ No devices found.")
        return

    print(f"✅ Found {len(devices)} device(s)")

    # Send notification to each device
    successful_sends = 0

    for device in devices:
        print(f"\n🎯 Targeting: {device.name or 'Unknown'} ({device.address})")

        success = await send_notification_to_device(device.address, notification_data)
        if success:
            successful_sends += 1

    print(
        f"\n📊 Summary: {successful_sends}/{len(devices)} notifications sent successfully")


async def send_custom_notification():
    """Send a custom notification with user input."""

    print("✏️ Custom Notification Sender")
    print("=" * 40)

    # Get notification details from user
    title = input("Enter notification title: ").strip()
    message = input("Enter notification message: ").strip()

    # Create notification data
    notification_data = {
        "title": title,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "type": "custom"
    }

    print(f"\n📋 Notification Data:")
    print(json.dumps(notification_data, indent=2))

    # Ask for delivery method
    print("\nDelivery method:")
    print("1. Send to specific device")
    print("2. Broadcast to all devices")

    try:
        choice = input("Enter your choice (1-2): ").strip()

        if choice == "1":
            # Get device address
            device_address = input("Enter device address: ").strip()
            await send_notification_to_device(device_address, notification_data)

        elif choice == "2":
            await broadcast_notification(notification_data)

        else:
            print("❌ Invalid choice.")

    except KeyboardInterrupt:
        print("\n👋 Cancelled.")


async def send_system_notification():
    """Send a system-style notification."""

    notification_data = {
        "title": "System Notification",
        "message": "This is a test notification from your Python script",
        "timestamp": datetime.now().isoformat(),
        "type": "system",
        "priority": "normal"
    }

    print("🖥️ Sending system notification...")
    await broadcast_notification(notification_data)


async def send_alert_notification():
    """Send an alert-style notification."""

    notification_data = {
        "title": "⚠️ Alert",
        "message": "This is an important alert message",
        "timestamp": datetime.now().isoformat(),
        "type": "alert",
        "priority": "high"
    }

    print("🚨 Sending alert notification...")
    await broadcast_notification(notification_data)


def main():
    """Main function."""
    print("🔵 Bluetooth Notification Sender")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 50)

    print("Choose notification type:")
    print("1. Custom notification")
    print("2. System notification")
    print("3. Alert notification")
    print("4. Test with specific device")

    try:
        choice = input("Enter your choice (1-4): ").strip()

        if choice == "1":
            asyncio.run(send_custom_notification())
        elif choice == "2":
            asyncio.run(send_system_notification())
        elif choice == "3":
            asyncio.run(send_alert_notification())
        elif choice == "4":
            # Test mode - just try to connect and discover characteristics
            device_address = input("Enter device address: ").strip()
            test_data = "Test notification from Python"
            asyncio.run(send_notification_to_device(device_address, test_data))
        else:
            print("❌ Invalid choice.")

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
