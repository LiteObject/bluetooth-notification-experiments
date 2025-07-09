# Bluetooth Notification Experiments

This project contains scripts to scan for Bluetooth devices, send messages to connected devices, and experiment with Bluetooth notifications.

## Features

- **Bluetooth Device Scanner**: Scan for available Bluetooth devices and display their information
- **Simple Scanner**: A simplified version for basic device discovery
- **Advertisement Data**: Option to view detailed advertisement data from devices
- **Message Sender**: Connect to devices and send messages via characteristics
- **Notification Sender**: Send notifications to connected Bluetooth devices
- **Interactive Mode**: User-friendly interface for device interaction

## Requirements

- Python 3.7+
- Windows 10/11 with Bluetooth support
- Virtual environment (recommended)

## Installation

1. Make sure you have Python installed
2. Clone this repository
3. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .venv\Scripts\Activate.ps1
   ```
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Usage

### Basic Bluetooth Scan

Run the simple scanner:
```powershell
python simple_bluetooth_scanner.py
```

### Advanced Bluetooth Scan

Run the advanced scanner with more options:
```powershell
python bluetooth_scanner.py
```

The advanced scanner offers two modes:
1. **Basic scan**: Shows device names and addresses
2. **Detailed scan**: Shows advertisement data including manufacturer data, service UUIDs, etc.

### Detailed Device Information

Get comprehensive device information:
```powershell
python detailed_bluetooth_info.py
```

### Send Messages to Devices

#### Simple Message Sender
```powershell
python simple_message_sender.py
```

Choose from:
1. **Simple example**: Auto-connects to first available device
2. **Interactive mode**: Select specific device and characteristic

#### Advanced Message Sender
```powershell
python bluetooth_message_sender.py
```

Features:
- Interactive device selection
- Service and characteristic discovery
- Send messages (string, hex, or bytes)
- Read from characteristics
- Subscribe to notifications
- Connection management

#### Send Notifications
```powershell
python notification_sender.py
```

Options:
1. **Custom notification**: Create your own notification
2. **System notification**: Send system-style notifications
3. **Alert notification**: Send high-priority alerts
4. **Test mode**: Test with specific device

## Output Information

The scanners will display:
- Device name (if available)
- Bluetooth address (MAC address)
- RSSI (signal strength) - in advanced mode
- Advertisement data (manufacturer data, service UUIDs, etc.) - in detailed mode

## Message Sending

### How It Works

1. **Scan for devices**: Discover available Bluetooth devices
2. **Connect to device**: Establish a connection using BleakClient
3. **Discover services**: Find available services and characteristics
4. **Send messages**: Write data to writable characteristics
5. **Read responses**: Read data from readable characteristics
6. **Handle notifications**: Subscribe to characteristic notifications

### Message Types

- **String messages**: Regular text messages
- **Hex messages**: Hexadecimal data
- **Bytes messages**: Raw byte data
- **JSON notifications**: Structured notification data

### Example Code

```python
import asyncio
from bleak import BleakClient

async def send_message():
    async with BleakClient("device_address") as client:
        if client.is_connected:
            message = "Hello Device!"
            await client.write_gatt_char("characteristic_uuid", message.encode('utf-8'))
            print("Message sent!")

asyncio.run(send_message())
```

## Troubleshooting

- **No devices found**: Make sure Bluetooth is enabled on your system and target devices are discoverable
- **Connection failed**: Ensure the device is in pairing/connectable mode
- **Permission errors**: Make sure you're running the script with appropriate permissions
- **Import errors**: Make sure all dependencies are installed in your virtual environment
- **Characteristic not found**: Use the service discovery feature to find the correct UUIDs

## Important Notes

- The scan duration is set to 10 seconds by default
- Some devices may only be discoverable for a limited time
- Different devices may provide different levels of information
- BLE (Bluetooth Low Energy) devices are the primary focus
- **Always use `python` command instead of `py` when virtual environment is activated**
- Not all devices support message sending - it depends on the device's services and characteristics
- Some characteristics may require authentication or pairing before writing

## Device-Specific Considerations

### Common Bluetooth Services

- **Generic Access Service**: Device information
- **Generic Attribute Service**: Service discovery
- **Device Information Service**: Manufacturer, model, etc.
- **Battery Service**: Battery level information
- **Custom Services**: Device-specific functionality

### Message Formats

Different devices expect different message formats:
- **Text devices**: UTF-8 encoded strings
- **IoT devices**: JSON or custom protocols
- **Audio devices**: Audio control commands
- **Health devices**: Health data formats

## Security Considerations

- Only send messages to devices you own or have permission to interact with
- Be cautious with unknown devices
- Some devices may require pairing or authentication
- Consider implementing message encryption for sensitive data