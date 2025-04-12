from flask import Flask, render_template, request
import serial
import time
import os
import serial
import time
import threading
# Initialize Flask app and specify template folder
app = Flask(__name__, template_folder=os.path.join('web_portal', 'templates'))

ARDUINO_PORT = 'COM5'  # Using the specified COM5 port
BAUD_RATE = 9600

# Global variable to track Arduino connection status
arduino = None


def connect_to_arduino():
    """Attempt to connect to the Arduino"""
    global arduino
    try:
        arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)
        print(f"Connected to Arduino on {ARDUINO_PORT}")
        time.sleep(2)  # Give Arduino time to reset after connection
        return True
    except Exception as e:
        print(f"Failed to connect to Arduino: {e}")
        arduino = None
        return False


# Try to connect to Arduino when starting the server
connect_to_arduino()


@app.route('/signal_arduino', methods=['POST'])
def signal_arduino():
    """Send signal to Arduino to open the door"""
    global arduino

    # Get command from request
    data = request.get_json()
    command = data.get('command')

    if command != 'open_door':
        return jsonify({'success': False, 'message': 'Invalid command'})

    # Check if Arduino is connected
    if arduino is None:
        # Try to reconnect
        if not connect_to_arduino():
            return jsonify({'success': False, 'message': 'Arduino not connected'})

    try:
        # Send the 'o' character to trigger door opening in Arduino
        arduino.write(b'o')
        print("Signal sent to Arduino to open door")
        return jsonify({'success': True})
    except Exception as e:
        print(f"Error communicating with Arduino: {e}")
        # Connection might be lost, set to None to try reconnecting next time
        arduino = None
        return jsonify({'success': False, 'message': 'Failed to communicate with return system'})

@app.route('/')
def index():
    return render_template('ko.html')  # Flask should now look inside 'web_portal/templates/'

@app.route('/trigger-return', methods=['POST'])
def trigger_return():
    try:
        with serial.Serial(COM_PORT, BAUD_RATE, timeout=1) as arduino:
            time.sleep(2)  # Allow time for the connection to establish
            arduino.write(b'o')  # Send 'o' to Arduino to trigger door (from Confirm Return)
        return render_template('ko.html', status="Return initiated. Please insert the book.")
    except serial.SerialException as e:
        if "PermissionError" in str(e):
            return render_template('ko.html', status="Error: Access denied. Ensure the port is not in use by another application.")
        return render_template('ko.html', status=f"Serial error: {e}")
    except Exception as e:
        return render_template('ko.html', status=f"Error: {e}")
if __name__ == '__main__':
    app.run(debug=True)