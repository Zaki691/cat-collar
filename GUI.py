import tkinter as tk
from tkinter import ttk
import geocoder
import gmplot
import webbrowser
import os

class GPSDesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("GPS Tracker App")

        # Button to open the map in a web browser
        self.open_map_button = ttk.Button(root, text="Open Map in Browser", command=self.open_map)
        self.open_map_button.grid(row=0, column=0, padx=10, pady=5)

        # Get the current location based on the IP address
        location = geocoder.ip('me')
        if location.latlng:
            latitude, longitude = location.latlng
            # Generate the map with the current location
            self.generate_map(latitude, longitude)
        else:
            print("Location not found.")

    def generate_map(self, latitude, longitude):
        # Create a map centered at the current location
        gmap = gmplot.GoogleMapPlotter(latitude, longitude, 13)

        # Add a marker for the current location
        gmap.marker(latitude, longitude, "red")

        # Save the map to an HTML file
        gmap.draw("map.html")

    def open_map(self):
        # Open the map in the default web browser
        webbrowser.open_new_tab("file://" + os.path.realpath("map.html"))

# Adjust the main function to start the GUI application
def main():
    root = tk.Tk()
    app = GPSDesktopApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
