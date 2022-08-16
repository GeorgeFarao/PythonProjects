import sounddevice as sd
from tkinter import *
import queue
import soundfile as sf
import threading
from tkinter import messagebox

# UI
voice_rec = Tk()
voice_rec.geometry("360x200")
voice_rec.title("My Voice Recorder")
voice_rec.config(bg="#107dc2")

q = queue.Queue()

recording = False
file_exists = False


def enqueue(indata, frames, time, status):
    q.put(indata.copy())


def threading_rec(action):
    if action == 1:
        # If recording is selected, then the thread is activated
        t1 = threading.Thread(target=record_audio)
        t1.start()
    elif action == 2:
        # To stop, set the flag to false
        global recording
        recording = False
        messagebox.showinfo(message="Recording finished")
    elif action == 3:
        # To play a recording, it must exist.
        if file_exists:
            # Read the recording if it exists and play it
            data, fs = sf.read("trial.wav", dtype='float32')
            sd.play(data, fs)
            sd.wait()
        else:
            # Display and error if none is found
            messagebox.showerror(message="Record something to play")


# Recording function
def record_audio():
    # Declare global variables
    global recording
    # Set to True to record
    recording = True
    global file_exists
    # Create a file to save the audio
    messagebox.showinfo(
        message="Recording Audio after pressing OK. Speak into the mic. Press \"Stop Recording\" when you are finished.")
    with sf.SoundFile("trial.wav", mode='w', samplerate=44100,
                      channels=2) as file:
        # Create an input stream to record audio without a preset time
        with sd.InputStream(samplerate=44100, channels=2, callback=enqueue):
            while recording:
                # Set the variable to True to allow playing the audio later
                file_exists = True
                # write into file
                file.write(q.get())


title_lbl = Label(voice_rec, text="My Voice Recorder", bg="#107dc2").grid(row=0, column=0, columnspan=3)

# Button to record audio
record_btn = Button(voice_rec, text="Record Audio", command=lambda m=1: threading_rec(m))
# Stop button
stop_btn = Button(voice_rec, text="Stop Recording", command=lambda m=2: threading_rec(m))
# Play button
play_btn = Button(voice_rec, text="Play Recording", command=lambda m=3: threading_rec(m))

# Position buttons
record_btn.grid(row=1, column=1)
stop_btn.grid(row=1, column=0)
play_btn.grid(row=1, column=2)
voice_rec.mainloop()
