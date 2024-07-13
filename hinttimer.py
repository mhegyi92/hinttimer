import tkinter as tk
from PIL import Image, ImageTk, ImageFont, ImageDraw

class CountdownTimer:
    def __init__(self, window, seconds):
        # Init
        self.initial_time = seconds
        self.time_left = seconds
        self.timer_id = None
        self.paused = False

        # Window
        self.window = window
        self.window.configure(background='black')
        self.window.attributes("-fullscreen", True)
        
        # Get screen dimensions
        self.screen_width = window.winfo_screenwidth()
        self.screen_height = window.winfo_screenheight()

        # Calculate font sizes
        self.timer_font_size = self.screen_height // 5
        self.hint_font_size = self.screen_height // 25

        # Widgets
        self.timer = tk.Label(window, borderwidth=0, background='black')
        self.hint = tk.Label(window, borderwidth=0, background='black')

        self.timer.pack(expand=True, fill='both')
        
        self.update_timer()

        # Events
        self.window.bind('<space>', self.toggle_timer)
        self.window.bind('<plus>', self.add_time)
        self.window.bind('<minus>', self.subtract_time)
        self.window.bind('<r>', self.restart_timer)
        self.window.bind('<Escape>', self.quit)
        self.window.bind('<c>', lambda event: self.hint.pack_forget())
        hinttext = "Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged."
        self.window.bind('<h>', lambda event: self.show_hint(hinttext))

    def show_hint(self, hinttext):
        self.hint.pack(expand=True, fill='both')
        self.draw_label(self.hint, hinttext, 'BloodyTerror-GOW9Z.ttf', self.hint_font_size, 30, wrap=True)

    def draw_label(self, label_widget, text, font_path, font_size, padding, fill_color = "red", wrap=False, line_spacing = 4):
        font = ImageFont.truetype(font_path, font_size)
        max_width = self.screen_width - 2 * padding

        if wrap:
            # Split text into lines
            lines = self.wrap_text(text, font, max_width - 2 * padding)
        else:
            lines = [text]

        # Calculate text dimensions using get_text_dimensions
        line_height = self.get_text_dimensions(font, "Tg")[1]  # Using get_text_dimensions for line height
        text_height = line_height * len(lines)
        text_width = max(self.get_text_dimensions(font, line)[0] for line in lines)  # Using get_text_dimensions for text width

        # Create image with padding
        image_width = text_width + padding
        if wrap:
            image_height = text_height + padding + len(lines) * line_spacing
        else:
            image_height = text_height + padding
        image = Image.new('RGB', (image_width, image_height), "black")
        draw = ImageDraw.Draw(image)

        # Draw text
        text_y = padding // 2
        for line in lines:
            text_x = (image_width - self.get_text_dimensions(font, line)[0]) // 2  # Using get_text_dimensions for text x position
            draw.text((text_x, text_y), line, font=font, fill=fill_color)
            text_y += line_height + line_spacing  # Add line spacing here

        # Convert to PhotoImage and set to label
        image = ImageTk.PhotoImage(image)
        label_widget.configure(image = image)
        label_widget.image = image

        # Resize label widget to fit the image
        label_widget.config(width = image_width, height = image_height)

    def get_text_dimensions(self, font, text):
        bbox = font.getbbox(text)

        if bbox:
            left, top, right, bottom = bbox
            width = right - left
            height = bottom - top
            return width, height
        else:
            return 0, 0

    def wrap_text(self, text, font, max_width):
        words = text.split()
        lines = []
        current_line = ""
        for word in words:
            test_line = f"{current_line} {word}".strip()
            if self.get_text_dimensions(font, test_line)[0] <= max_width:
                current_line = test_line
            else:
                lines.append(current_line)
                current_line = word
        lines.append(current_line)
        return lines
    
    def format_time(self):
        hours, remainder = divmod(self.time_left, 3600)
        mins, secs = divmod(remainder, 60)
        return f"{hours:02}:{mins:02}:{secs:02}"

    def update_timer(self):
        if self.time_left > 0:
            self.time_left -= 1
            self.draw_label(self.timer, self.format_time(), 'digital-7-mono.ttf', self.timer_font_size, 30)
            self.timer_id = self.window.after(1000, self.update_timer)
        else:
            self.draw_label(self.timer, 'Time is up!', 'digital-7-mono.ttf', self.timer_font_size, 30)
            self.timer_id = None

    def add_time(self, event=None):
        self.time_left += 5 * 60
        if not self.paused:
            if self.timer_id is not None:
                self.window.after_cancel(self.timer_id)
                self.timer_id = None
            self.update_timer()
        else:
            self.draw_time()

    def subtract_time(self, event=None):
        self.time_left = max(0, self.time_left - 5 * 60)
        if not self.paused:
            if self.timer_id is not None:
                self.window.after_cancel(self.timer_id)
                self.timer_id = None
            self.update_timer()
        else:
            self.draw_time()

    def toggle_timer(self, event=None):
        if self.paused:
            self.start_timer()
        else:
            self.pause_timer()

    def pause_timer(self, event=None):
        if not self.paused:
            self.paused = True
            if self.timer_id is not None:
                self.window.after_cancel(self.timer_id)
                self.timer_id = None

    def start_timer(self, event=None):
        if self.paused:
            self.paused = False
            self.update_timer()
            
    def restart_timer(self, event=None):
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)
            self.timer_id = None
        self.time_left = self.initial_time
        self.update_timer()

    def quit(self, event=None):
        if self.timer_id is not None:
            self.window.after_cancel(self.timer_id)
        self.window.quit()    

def main():
    window = tk.Tk()
    CountdownTimer(window, 10)
    window.mainloop()

if __name__ == "__main__":
    main()
