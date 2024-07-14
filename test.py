import tkinter as tk
from tkVideoPlayer import TkinterVideo

root = tk.Tk()
root.attributes("-fullscreen", True)

videoplayer = TkinterVideo(master=root, scaled=True)
videoplayer.load(r"sample-5s.mp4")
videoplayer.pack(expand=True, fill="both")

videoplayer.play() # play the video

root.mainloop()