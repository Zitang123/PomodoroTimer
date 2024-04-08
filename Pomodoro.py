import tkinter as tk
from tkinter import messagebox
import time

class PomodoroTimer:
    def __init__(self, master):
        self.master = master
        self.master.title("Pomodoro Timer")
        self.master.configure(bg="lightblue")

        self.current_font_size = 20
        self.is_paused = True
        self.session_lengths = [(25, 5), (25, 5), (25, 5), (25, 5), (45, 15), (45, 15), (45, 25), (45, 25)]
        self.current_session = 0
        self.time_left = self.session_lengths[self.current_session][0] * 60

        self.status_label = tk.Label(self.master, text="Press Start", font=("Calibri", self.current_font_size), bg="lightblue")
        self.status_label.pack(pady=20)

        self.timer_label = tk.Label(self.master, text=self.format_time(self.time_left), font=("Calibri", self.current_font_size), bg="lightblue")
        self.timer_label.pack(pady=10)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer, font=("Calibri", self.current_font_size))
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.pause_button = tk.Button(self.master, text="Pause/Continue", command=self.pause_timer, font=("Calibri", self.current_font_size))
        self.pause_button.pack(side=tk.RIGHT, padx=20)

        self.update_timer()

        self.master.bind("<MouseWheel>", self.zoom)

    def format_time(self, seconds):
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

    def update_timer(self):
        if not self.is_paused:
            self.time_left -= 1
            if self.time_left <= 0:
                if self.current_session % 2 == 0:
                    self.time_left = self.session_lengths[self.current_session][1] * 60
                    self.status_label.config(text="Breaking")
                else:
                    self.current_session += 1
                    if self.current_session >= len(self.session_lengths):
                        messagebox.showinfo("Pomodoro Timer", "All sessions complete!")
                        self.master.destroy()
                        return
                    self.time_left = self.session_lengths[self.current_session][0] * 60
                    self.status_label.config(text="Studying")
            self.timer_label.config(text=self.format_time(self.time_left))
        self.master.after(1000, self.update_timer)

    def start_timer(self):
        if self.current_session % 2 == 0:
            self.status_label.config(text="Studying")
        else:
            self.status_label.config(text="Breaking")
        self.is_paused = False

    def pause_timer(self):
        self.is_paused = not self.is_paused

    def zoom(self, event):
        zoom_direction = event.delta
        if zoom_direction > 0:
            self.current_font_size += 2
        else:
            self.current_font_size -= 2

        self.status_label.config(font=("Calibri", self.current_font_size))
        self.timer_label.config(font=("Calibri", self.current_font_size))
        self.start_button.config(font=("Calibri", self.current_font_size))
        self.pause_button.config(font=("Calibri", self.current_font_size))


if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
