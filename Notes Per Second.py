import sys
from pythonosc import udp_client
import mido
import time
import os
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QCheckBox
from PyQt5.QtCore import QTimer, QObject, pyqtSignal
from PyQt5.QtGui import QFont, QPalette, QKeySequence
from PyQt5.QtCore import QThread, Qt
from pynput import keyboard
from pynput.keyboard import Key

# Initialize a UDP client to send messages
udpClient = udp_client.SimpleUDPClient("127.0.0.1", 9000)

# Global variables to keep track of notes and time
notes_played = 0
start_time = 0
highest_nps = 0  # Initialize the highest NPS variable

class MidiInput(QObject):
    message_received = pyqtSignal(object)

    def run(self):
        with mido.open_input() as port:
            for msg in port:
                if msg.type == 'note_on':
                    self.message_received.emit(msg)

def update_notes_per_second():
    global notes_played, start_time, highest_nps
    current_time = time.time()
    elapsed_time = current_time - start_time

    if elapsed_time > 0:
        nps = notes_played / elapsed_time
        rounded_nps = round(nps, 2)  # Round to two decimal places
        notes_per_second_label.setText(f"Notes Per Second: {rounded_nps:.2f}")

        # Update the highest NPS if necessary
        if rounded_nps > highest_nps:
            highest_nps = rounded_nps
            highest_nps_label.setText(f"Highest NPS: {highest_nps:.2f}")

        # Send the message via UDP every 2 seconds if NPS is not zero
        if rounded_nps > 0 and int(time.time()) % 2 == 0:
            message = f"Notes Per Second: {rounded_nps:.2f}"
            udpClient.send_message("/chatbox/input", [f"Current NPS: {rounded_nps:.2f}\vMax NPS: {highest_nps:.2f}", True, False])

    # Reset notes and time
    notes_played = 0
    start_time = current_time

# Create the PyQt5 application
app = QApplication(sys.argv)
app.setStyle("Windows")  # Set a Windows style for better text visibility

window = QWidget()
window.setWindowTitle("MIDI NPS")

# Set window flags to make it not clickable
window.setWindowFlags(
   Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.WindowDoesNotAcceptFocus
)
window.setAttribute(Qt.WA_TranslucentBackground)

layout = QVBoxLayout()

notes_per_second_label = QLabel("NPS: 0.00", window)
font = QFont()
font.setBold(True)
font.setPointSize(2 * font.pointSize())  # Make the text 2x bigger
notes_per_second_label.setFont(font)
notes_per_second_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
notes_per_second_label.setPalette(QPalette(Qt.white))

# Remove the border and set the text color to white
notes_per_second_label.setStyleSheet("QLabel { color: white; }")
layout.addWidget(notes_per_second_label)

highest_nps_label = QLabel("Highest NPS: 0.00", window)  # Add a label for highest NPS
highest_nps_label.setFont(font)
highest_nps_label.setAlignment(Qt.AlignTop | Qt.AlignLeft)
highest_nps_label.setPalette(QPalette(Qt.white))
highest_nps_label.setStyleSheet("QLabel { color: white; }")
layout.addWidget(highest_nps_label)

window.setLayout(layout)
window.show()

# Create a MIDI input thread and start it
midi_input_thread = QThread()
midi_input = MidiInput()
midi_input.moveToThread(midi_input_thread)
midi_input_thread.started.connect(midi_input.run)
midi_input.message_received.connect(lambda msg: notes_played_increment())

# Start the MIDI input thread
midi_input_thread.start()

# Start the notes per second update timer
start_time = time.time()
timer = QTimer()
timer.timeout.connect(update_notes_per_second)
timer.start(1000)  # Update every 1 second

def notes_played_increment():
    global notes_played
    notes_played += 1

def close_window():
    window.close()

# Move the window to the top-left corner
window.setGeometry(200, 200, 200, 100)  # Increased the window height
window.move(0, 0)

# Move the window down by 100 pixels
# window.move(window.pos().x() + 40, window.pos().y() + 150)

# Close Window
def on_key_release(key):
    if key == keyboard.Key.num_lock:
        close_window()

with keyboard.Listener(on_release=on_key_release) as listener:
    sys.exit(app.exec_())
