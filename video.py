import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import mysql.connector
import io
import base64
import os
import time

class SlideshowApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Slideshow App")
        self.root.geometry("800x600")

        # Connect to MySQL database
        self.conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='MyNewPass',
            database='users'
        )
        self.cursor = self.conn.cursor()

        # Initialize variables
        self.photos = []
        self.music_files = []
        self.transitions = []
        self.current_photo_index = 0
        self.current_music_index = 0
        self.current_transition_index = 0

        # Load data from the database
        self.load_data()

        # Create GUI elements
        self.photo_label = ttk.Label(root)
        self.photo_label.pack(fill=tk.BOTH, expand=True)

        # Start the slideshow
        self.start_slideshow()

    def load_data(self):
        # Retrieve photos from the database
        self.cursor.execute("SELECT image_blob FROM photos")
        self.photos = self.cursor.fetchall()

        # Retrieve music files from the database
        self.cursor.execute("SELECT path FROM music")
        self.music_files = self.cursor.fetchall()

        # Retrieve transitions from the database
        self.cursor.execute("SELECT name FROM transitions")
        self.transitions = self.cursor.fetchall()

    def start_slideshow(self):
        # Initialize pygame for music playback
        pygame.mixer.init()

        # Play music
        if self.music_files:
            pygame.mixer.music.load(self.music_files[self.current_music_index][0])
            pygame.mixer.music.play(-1)  # Loop indefinitely

        # Display photos with transitions
        while True:
            photo_blob = self.photos[self.current_photo_index][0]
            photo = self.convert_blob_to_image(photo_blob)
            photo = photo.resize((800, 600), Image.ANTIALIAS)
            photo_tk = ImageTk.PhotoImage(photo)

            # Display photo with transition
            self.display_with_transition(photo_tk)

            # Move to the next photo
            self.current_photo_index = (self.current_photo_index + 1) % len(self.photos)

    def convert_blob_to_image(self, blob_data):
        # Convert BLOB data to Image object
        image_stream = io.BytesIO(blob_data)
        image = Image.open(image_stream)
        return image

    def display_with_transition(self, photo_tk):
        # Display photo with transition effect
        transition_name = self.transitions[self.current_transition_index][0]
        if transition_name == 'fade':
            self.fade_transition(photo_tk)
        elif transition_name == 'slide':
            self.slide_transition(photo_tk)
        elif transition_name == 'dissolve':
            self.dissolve_transition(photo_tk)

    def fade_transition(self, photo_tk):
        # Fade transition
        self.photo_label.config(image=photo_tk)
        self.photo_label.image = photo_tk
        for alpha in range(256):
            photo_tk.putalpha(alpha)
            time.sleep(0.01)
            self.root.update()

    def slide_transition(self, photo_tk):
        # Slide transition
        for x in range(-800, 0, 10):
            self.photo_label.place(x=x)
            self.photo_label.config(image=photo_tk)
            self.photo_label.image = photo_tk
            time.sleep(0.01)
            self.root.update()

    def dissolve_transition(self, photo_tk):
        # Dissolve transition
        for alpha in range(256):
            photo_tk.putalpha(alpha)
            self.photo_label.config(image=photo_tk)
            self.photo_label.image = photo_tk
            time.sleep(0.01)
            self.root.update()

    def stop_slideshow(self):
        # Stop music playback
        pygame.mixer.music.stop()

if __name__ == "__main__":
    root = tk.Tk()
    app = SlideshowApp(root)
    root.mainloop()
