import tkinter as tk
from tkinter import ttk
import geocoder
import gmplot
import webbrowser
import os
import paho.mqtt.client as mqtt

class GPSDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPS Tracker App")

        # MQTT settings
        self.broker_address = "broker.hivemq.com"
        self.port = 1883
        self.topic = "gps/tracker"

        # Button to open the map in a web browser
        self.open_map_button = ttk.Button(root, text="Open Map in Browser", command=self.open_map)
        self.open_map_button.grid(row=0, column=0, padx=10, pady=5)

        # Initial location
        self.latitude = None
        self.longitude = None

        # Setup MQTT client
        self.client = mqtt.Client("GPS_Tracker_Client")
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect(self.broker_address, self.port, 60)
        self.client.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code " + str(rc))
        # Subscribing to the GPS topic
        self.client.subscribe(self.topic)

    def on_message(self, client, userdata, msg):
        print("Message received: " + msg.topic + " " + str(msg.payload))
        # Assume the payload is in the format "latitude,longitude"
        try:
            latitude, longitude = map(float, msg.payload.decode().split(','))
            self.update_location(latitude, longitude)
        except ValueError:
            print("Invalid GPS data received.")

    def update_location(self, latitude, longitude):
        self.latitude = latitude
        self.longitude = longitude
        # Generate the map with the new location
        self.generate_map(latitude, longitude)

    def generate_map(self, latitude, longitude):
        # Create a map centered at the current location
        gmap = gmplot.GoogleMapPlotter(latitude, longitude, 13)

        # Add a marker for the current location
        gmap.marker(latitude, longitude, "red")

        # Save the map to an HTML file
        gmap.draw("map.html")

    def open_map(self):
        # Open the map in the default web browser
        if self.latitude and self.longitude:
            webbrowser.open_new_tab("file://" + os.path.realpath("map.html"))
        else:
            print("No GPS data available to display the map.")

# Adjust the main function to start the GUI application
def main():
    root = tk.Tk()
    app = GPSDesktopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
