import tkinter as tk
from tkinter import messagebox
import serial
import requests

# RFID Scanner (Adjust COM port for Windows or /dev/ttyUSB0 for Linux)
rfid_reader = serial.Serial('COM3', 9600)

def rfid_login():
    if rfid_reader.in_waiting > 0:
        rfid_number = rfid_reader.readline().decode('utf-8').strip()
        response = requests.post("http://127.0.0.1:5000/login_rfid", json={"rfid_number": rfid_number})
        data = response.json()
        
        if response.status_code == 200:
            messagebox.showinfo("Login Successful", f"Welcome {data['user']['name']}!")
        else:
            messagebox.showerror("Login Failed", "Invalid RFID Card")

# Create Tkinter Window
root = tk.Tk()
root.title("Library Kiosk Login")
root.geometry("400x300")

btn_login = tk.Button(root, text="Tap RFID to Login", command=rfid_login, font=("Arial", 16))
btn_login.pack(pady=50)

root.mainloop()
