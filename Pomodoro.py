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
        # Schedule: List of tuples with (work_duration_in_minutes, break_duration_in_minutes)
        self.session_lengths = [(25, 5), (25, 5), (25, 5), (25, 15), (45, 15), (45, 15), (45, 25), (45, 25)]
        self.current_session = 0  # Index to track the current session
        self.time_left = self.session_lengths[self.current_session][0] * 60  # Start with the first work session

        # UI Components
        self.status_label = tk.Label(self.master, text="Press Start", font=("Calibri", self.current_font_size), bg="lightblue")
        self.status_label.pack(pady=20)

        self.timer_label = tk.Label(self.master, text=self.format_time(self.time_left), font=("Calibri", self.current_font_size), bg="lightblue")
        self.timer_label.pack(pady=10)

        self.start_button = tk.Button(self.master, text="Start", command=self.start_timer, font=("Calibri", self.current_font_size))
        self.start_button.pack(side=tk.LEFT, padx=20)

        self.pause_button = tk.Button(self.master, text="Pause/Continue", command=self.pause_timer, font=("Calibri", self.current_font_size))
        self.pause_button.pack(side=tk.RIGHT, padx=20)

        self.skip_button = tk.Button(self.master, text="Skip", command=self.skip_session, font=("Calibri", self.current_font_size))
        self.skip_button.pack(side=tk.BOTTOM, pady=10)

        self.master.bind("<MouseWheel>", self.zoom)  # Bind mousewheel to zoom in/out

        self.update_timer()  # Start the timer update loop

    def format_time(self, seconds):
        """Converts seconds into HH:MM:SS format."""
        return time.strftime('%H:%M:%S', time.gmtime(seconds))

    def update_timer(self):
        """Updates the timer every second."""
        if not self.is_paused:
            self.time_left -= 1
            if self.time_left <= 0:
                self.end_session()
            self.timer_label.config(text=self.format_time(self.time_left))
        self.master.after(1000, self.update_timer)  # Schedule next update

    def end_session(self):
        """Handles the transition between work and break sessions."""
        if self.current_session % 2 == 0:  # Work session just ended
            self.time_left = self.session_lengths[self.current_session][1] * 60  # Set time for break
            self.status_label.config(text="Breaking")
        else:  # Break session just ended
            self.current_session += 1
            if self.current_session >= len(self.session_lengths):  # Check if all sessions are complete
                messagebox.showinfo("Pomodoro Timer", "All sessions complete!")
                self.master.destroy()
                return
            self.time_left = self.session_lengths[self.current_session][0] * 60  # Set time for next work session
            self.status_label.config(text="Studying")

    def start_timer(self):
        """Starts or resumes the timer."""
        self.status_label.config(text="Studying" if self.current_session % 2 == 0 else "Breaking")
        self.is_paused = False

    def pause_timer(self):
        """Pauses or continues the timer."""
        self.is_paused = not self.is_paused

    def skip_session(self):
        """Skips the current session."""
        self.current_session += 1
        if self.current_session >= len(self.session_lengths):
            messagebox.showinfo("Pomodoro Timer", "All sessions complete!")
            self.master.destroy()
            return
        if self.current_session % 2 == 0:  # Next session is a work session
            self.time_left = self.session_lengths[self.current_session][0] * 60
            self.status_label.config(text="Studying")
        else:  # Next session is a break
            self.time_left = self.session_lengths[self.current_session][1] * 60
            self.status_label.config(text="Breaking")

    def zoom(self, event):
        """Zooms in or out the font size of UI components."""
        zoom_direction = event.delta
        if zoom_direction > 0 and self.current_font_size < 40:
            self.current_font_size += 2
        elif zoom_direction < 0 and self.current_font_size > 10:
            self.current_font_size -= 2

        # Update font size for all UI components
        self.status_label.config(font=("Calibri", self.current_font_size))
        self.timer_label.config(font=("Calibri", self.current_font_size))
        self.start_button.config(font=("Calibri", self.current_font_size))
        self.pause_button.config(font=("Calibri", self.current_font_size))
        self.skip_button.config(font=("Calibri", self.current_font_size))

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
