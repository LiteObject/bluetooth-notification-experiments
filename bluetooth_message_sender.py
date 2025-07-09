#!/usr/bin/env python3
"""
Bluetooth Device Connector and Message Sender
Connects to Bluetooth devices and sends messages via characteristics.
"""

import asyncio
from bleak import BleakScanner, BleakClient
from datetime import datetime
import uuid
from typing import Optional, List


class BluetoothConnector:
    """Class to handle Bluetooth device connections and messaging."""

    def __init__(self):
        self.client: Optional[BleakClient] = None
        self.device_address: Optional[str] = None
        self.connected = False

    async def scan_for_devices(self, duration=10):
        """Scan for available Bluetooth devices."""
        print("🔍 Scanning for Bluetooth devices...")
        print("=" * 50)

        devices = await BleakScanner.discover(timeout=duration)

        if not devices:
            print("❌ No devices found.")
            return []

        print(f"✅ Found {len(devices)} device(s):")
        print("=" * 50)

        for i, device in enumerate(devices, 1):
            print(f"{i}. {device.name or 'Unknown Device'}")
            print(f"   Address: {device.address}")
            print(
                f"   Details: {device.details if hasattr(device, 'details') else 'N/A'}")
            print("-" * 30)

        return devices

    async def connect_to_device(self, device_address):
        """Connect to a specific Bluetooth device."""
        print(f"🔗 Connecting to device: {device_address}")

        try:
            self.client = BleakClient(device_address)
            await self.client.connect()

            if self.client.is_connected:
                self.device_address = device_address
                self.connected = True
                print(f"✅ Successfully connected to {device_address}")
                return True
            else:
                print(f"❌ Failed to connect to {device_address}")
                return False

        except Exception as e:
            print(f"❌ Connection error: {e}")
            return False

    async def discover_services(self):
        """Discover services and characteristics of the connected device."""
        if not self.connected or not self.client:
            print("❌ Not connected to any device.")
            return

        print("🔍 Discovering services and characteristics...")
        print("=" * 60)

        try:
            services = self.client.services

            for service in services:
                print(f"📋 Service: {service.uuid}")
                print(f"   Description: {service.description}")

                for char in service.characteristics:
                    print(f"   📝 Characteristic: {char.uuid}")
                    print(f"      Properties: {char.properties}")
                    print(f"      Description: {char.description}")

                    # Show descriptors if any
                    for desc in char.descriptors:
                        print(f"         📄 Descriptor: {desc.uuid}")

                print("-" * 40)

        except Exception as e:
            print(f"❌ Error discovering services: {e}")

    async def send_message(self, characteristic_uuid, message, message_type="string"):
        """Send a message to a specific characteristic."""
        if not self.connected or not self.client:
            print("❌ Not connected to any device.")
            return False

        try:
            # Convert message to bytes based on type
            if message_type == "string":
                data = message.encode('utf-8')
            elif message_type == "hex":
                data = bytes.fromhex(message)
            elif message_type == "bytes":
                data = message
            else:
                print(f"❌ Unsupported message type: {message_type}")
                return False

            print(f"📤 Sending message to characteristic {characteristic_uuid}")
            print(f"   Message: {message}")
            print(f"   Data: {data}")

            await self.client.write_gatt_char(characteristic_uuid, data)
            print("✅ Message sent successfully!")
            return True

        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False

    async def read_characteristic(self, characteristic_uuid):
        """Read data from a characteristic."""
        if not self.connected or not self.client:
            print("❌ Not connected to any device.")
            return None

        try:
            print(f"📥 Reading from characteristic {characteristic_uuid}")
            data = await self.client.read_gatt_char(characteristic_uuid)

            print(f"✅ Read data: {data}")
            print(f"   As string: {data.decode('utf-8', errors='ignore')}")
            print(f"   As hex: {data.hex()}")

            return data

        except Exception as e:
            print(f"❌ Error reading characteristic: {e}")
            return None

    async def subscribe_to_notifications(self, characteristic_uuid):
        """Subscribe to notifications from a characteristic."""
        if not self.connected or not self.client:
            print("❌ Not connected to any device.")
            return False

        def notification_handler(sender, data):
            """Handle incoming notifications."""
            print(f"📬 Notification from {sender}: {data}")
            print(f"   As string: {data.decode('utf-8', errors='ignore')}")
            print(f"   As hex: {data.hex()}")

        try:
            await self.client.start_notify(characteristic_uuid, notification_handler)
            print(f"✅ Subscribed to notifications from {characteristic_uuid}")
            return True

        except Exception as e:
            print(f"❌ Error subscribing to notifications: {e}")
            return False

    async def disconnect(self):
        """Disconnect from the current device."""
        if self.connected and self.client:
            await self.client.disconnect()
            self.connected = False
            print(f"✅ Disconnected from {self.device_address}")
        else:
            print("❌ Not connected to any device.")


async def interactive_mode():
    """Interactive mode for connecting and messaging."""
    connector = BluetoothConnector()

    print("🔵 Bluetooth Device Connector")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    while True:
        print("\nOptions:")
        print("1. Scan for devices")
        print("2. Connect to device")
        print("3. Discover services")
        print("4. Send message")
        print("5. Read characteristic")
        print("6. Subscribe to notifications")
        print("7. Disconnect")
        print("8. Exit")

        try:
            choice = input("\nEnter your choice (1-8): ").strip()

            if choice == "1":
                await connector.scan_for_devices()

            elif choice == "2":
                address = input("Enter device address: ").strip()
                await connector.connect_to_device(address)

            elif choice == "3":
                await connector.discover_services()

            elif choice == "4":
                if not connector.connected:
                    print("❌ Please connect to a device first.")
                    continue

                char_uuid = input("Enter characteristic UUID: ").strip()
                message = input("Enter message: ").strip()
                message_type = input(
                    "Message type (string/hex/bytes) [string]: ").strip() or "string"

                await connector.send_message(char_uuid, message, message_type)

            elif choice == "5":
                if not connector.connected:
                    print("❌ Please connect to a device first.")
                    continue

                char_uuid = input("Enter characteristic UUID: ").strip()
                await connector.read_characteristic(char_uuid)

            elif choice == "6":
                if not connector.connected:
                    print("❌ Please connect to a device first.")
                    continue

                char_uuid = input("Enter characteristic UUID: ").strip()
                await connector.subscribe_to_notifications(char_uuid)

                print("Listening for notifications... Press Ctrl+C to stop.")
                try:
                    while True:
                        await asyncio.sleep(1)
                except KeyboardInterrupt:
                    print("\n📴 Stopped listening for notifications.")

            elif choice == "7":
                await connector.disconnect()

            elif choice == "8":
                await connector.disconnect()
                print("👋 Goodbye!")
                break

            else:
                print("❌ Invalid choice. Please try again.")

        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            await connector.disconnect()
            break
        except Exception as e:
            print(f"❌ Error: {e}")


async def example_usage():
    """Example of programmatic usage."""
    print("📋 Example Usage:")
    print("=" * 40)

    connector = BluetoothConnector()

    # Scan for devices
    devices = await connector.scan_for_devices(5)

    if devices:
        # Connect to first device (for demonstration)
        first_device = devices[0]
        connected = await connector.connect_to_device(first_device.address)

        if connected:
            # Discover services
            await connector.discover_services()

            # Example: Send a message (you'll need to replace with actual characteristic UUID)
            # await connector.send_message("12345678-1234-5678-9012-123456789abc", "Hello Device!")

            # Disconnect
            await connector.disconnect()


def main():
    """Main function."""
    print("🔵 Bluetooth Message Sender")
    print(f"⏰ Start time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    print("Choose mode:")
    print("1. Interactive mode")
    print("2. Example usage")

    try:
        choice = input("Enter your choice (1-2): ").strip()

        if choice == "1":
            asyncio.run(interactive_mode())
        elif choice == "2":
            asyncio.run(example_usage())
        else:
            print("❌ Invalid choice.")

    except KeyboardInterrupt:
        print("\n👋 Goodbye!")


if __name__ == "__main__":
    main()
