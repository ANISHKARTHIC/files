import serial
import binascii
import time
import json
import requests
import sys

# --- CONFIGURATION ---
# 1. HARDWARE SETTINGS
# Check Device Manager to confirm your LoRa E5 is on COM13
SERIAL_PORT = 'COM13'   
BAUD_RATE = 9600        # Standard baud rate for LoRa-E5

# 2. FIREBASE SETTINGS
# I have inserted your specific DB link here.
# The ".json" extension is REQUIRED for the Python code to work.
FIREBASE_URL = "https://cloudburst-c8d32-default-rtdb.asia-southeast1.firebasedatabase.app/sensor_readings.json"

def send_at_command(ser, cmd):
    """Sends a command to the LoRa module and waits briefly."""
    ser.write(f"{cmd}\r\n".encode())
    time.sleep(0.2)
    ser.reset_input_buffer() # Clear response to avoid cluttering the buffer

try:
    print(f"🔌 Connecting to LoRa-E5 on {SERIAL_PORT}...")
    ser = serial.Serial(SERIAL_PORT, BAUD_RATE, timeout=1)
    
    # --- AUTO-CONFIGURATION (Ensure E5 is in Receiver Mode) ---
    print("⚙  Configuring Radio...")
    send_at_command(ser, "AT+MODE=TEST")
    send_at_command(ser, "AT+TEST=RFCFG,433,SF9,125,8,8,14")
    send_at_command(ser, "AT+TEST=RXLRPKT")
    print("✅ Listening for Sensor Data & Ready to Upload to Firebase...")
    print(f"📡 Target Database: {FIREBASE_URL}")

    while True:
        # Check if there is data waiting in the serial buffer
        if ser.in_waiting > 0:
            try:
                line = ser.readline().decode('utf-8', errors='ignore').strip()
                
                # Check if the line is a Data Packet
                if line.startswith("+TEST: RX"):
                    # Format received is usually: +TEST: RX "7B2274..."
                    parts = line.split('"')
                    
                    if len(parts) > 1:
                        hex_data = parts[1]
                        
                        # STEP 1: DECODE HEX TO TEXT
                        # Converts robot hex code back into readable JSON text
                        ascii_json = binascii.unhexlify(hex_data).decode('utf-8')
                        print(f"\n📥 RECEIVED RAW DATA: {ascii_json}")
                        
                        # STEP 2: PARSE JSON
                        # Converts text into a Python Dictionary so we can use it
                        try:
                            sensor_data = json.loads(ascii_json)
                        except json.JSONDecodeError:
                            print("⚠ Error: Received data is not valid JSON. Skipping.")
                            continue

                        # Optional: Add a server-side timestamp
                        # This helps you know exactly when the cloud received the data
                        if "timestamp" not in sensor_data:
                            sensor_data["server_timestamp"] = time.time()
                        
                        # STEP 3: UPLOAD TO FIREBASE
                        try:
                            # We use .post() to create a new entry with a unique ID every time
                            response = requests.post(FIREBASE_URL, json=sensor_data)
                            
                            if response.status_code == 200:
                                # Success!
                                print(f"☁  Uploaded to Firebase! ID: {response.json().get('name')}")
                            else:
                                # Failure
                                print(f"⚠ Firebase Rejected: {response.status_code} - {response.text}")
                        except Exception as e:
                            print(f"❌ Upload Failed: Check Internet Connection. {e}")

            except Exception as e:
                print(f"Error processing line: {e}")

except serial.SerialException:
    print(f"❌ Critical Error: Could not open {SERIAL_PORT}.")
    print("1. Check if the LoRa dongle is plugged in.")
    print("2. Make sure the Arduino IDE Serial Monitor is CLOSED.")
except KeyboardInterrupt:
    print("\nStopped by user.")
