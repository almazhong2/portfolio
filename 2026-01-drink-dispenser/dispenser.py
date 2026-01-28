import tkinter as tk
from tkinter import font
import time
import serial


class Dispenser:
    def __init__(self, root, ser):
        self.root = root
        self.root.title("Dispenser")
        self.ser = ser

        #7" LCD display
        self.root.attributes("-fullscreen", True)
        self.root.configure(bg = "#000000")

        #escape full screen
        self.root.bind("<Escape>", lambda e: self.root.attributes("-fullscreen", False))
 
        #drinks
        self.options = [
            {"name": "Coffee", "color":"#8f693f", "code": 1},
            {"name": "Water", "color":"#73b6f0", "code": 2},
            {"name": "Soda", "color":"#5fc798", "code": 3},
            {"name": "Juice", "color":"#9261c9", "code": 4},
        ]

        self.display_selection()
    
    #exit fullscreen helper
    def exit_fullscreen(self):
        self.root.attributes("-fullscreen", False)

    #add an on-screen exit button (top-right)
    def add_exit_button(self):
        exit_btn = tk.Button(
            self.root,
            text="Exit",
            command=self.exit_fullscreen,
            bg="#333333",
            fg="white",
            font=font.Font(family="Helvetica", size=16, weight="bold"),
            bd=0,
            padx=10,
            pady=5,
            activebackground="#555555",
            activeforeground="white",
        )
        # top-right corner
        exit_btn.place(relx=0.98, rely=0.02, anchor="ne")

    def send_to_arduino(self, drink_code):
        # clear any leftover messages from previous runs
        self.ser.reset_input_buffer()

        message = f"{drink_code}\n"
        self.ser.write(message.encode())
        self.ser.flush()
        start = time.time()
        last_line = None
        
        while time.time() - start < 20:  
            line = self.ser.readline().decode("utf-8", errors="replace").strip()  
            if not line:
                continue
            print("arduino:", line)
            last_line = line

            if line.endswith("done"):
                return line
        
        return last_line or "Timed out"

    
    #clear the current screen
    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    #show selection screen
    def display_selection(self):
        self.clear()
        self.root.configure(bg = "#000000")

        #title
        title_font = font.Font(family = "Helvetica", size = 48, weight = "bold")
        title = tk.Label(
            self.root,
            text = "welcome to automatic dispenser",
            font = title_font,
            fg = "white",
            bg = "#000000"
        )
        title.pack(pady = 30)

        #subheadings
        sub_font = font.Font(family = "Helvetica", size = 24)
        subheading = tk.Label(
            self.root,
            text = "select a drink",
            font = sub_font,
            fg = "#fdb5ec",
            bg = "#000000"
        )
        subheading.pack(pady = 10)

        #button fomrat
        button = tk.Frame(self.root, bg = "#000000")
        button.pack(expand = True, fill = "both", padx = 40, pady = 20)

        for i in range(2):
            button.grid_rowconfigure(i, weight = 1)
            button.grid_columnconfigure(i, weight = 1)

        btn_font = font.Font(family = "Helvetica", size = 32, weight = "bold")
        for index, drink in enumerate(self.options):
            row = index//2
            col = index%2

            btn = tk.Button(
                button,
                text = drink["name"],
                font = btn_font,
                bg = drink["color"],
                fg = "white",
                activebackground = drink["color"],
                activeforeground = "white",
                relief = tk.RAISED,
                bd = 5,
                command = lambda d = drink: self.pour(d)
            )

            btn.grid(row = row, column = col, padx = 15, pady = 15, sticky = "nsew")
        
        self.add_exit_button()

    #switch to pour screen
    def pour(self, drink):
        self.clear()
        self.root.configure(bg = drink["color"])

        cup = tk.Frame(self.root, bg = drink["color"])
        cup.pack(expand = True)

        #text
        pour_font = font.Font(family = "Helvetica", size = 56, weight = "bold")
        pour_label = tk.Label(
            cup,
            text = "pouring...",
            font = pour_font,
            fg = "white",
            bg = drink["color"]
        )

        pour_label.pack(pady = 30)

        #drink name
        drink_font = font.Font(family = "Helvetica", size = 40)
        drink_label = tk.Label(
            cup,
            text = drink["name"],
            font = drink_font,
            fg = "white",
            bg = drink["color"]
        )
        drink_label.pack(pady = 20)

        # status from arduino
        status_label = tk.Label(
            cup,
            text="Preparing...",
            font=font.Font(family="Helvetica", size=28),
            fg="white",
            bg=drink["color"]
        )
        status_label.pack(pady=20)

        #loading
        dots_label = tk.Label(
            cup,
            text = "●  ●  ●",
            font = font.Font(family = "Helvetica", size = 36),
            fg = "white",
            bg = drink["color"]
        )
        dots_label.pack(pady = 30)

        self.animate(dots_label, 0)
         
        #update display and send drink to arduino
        self.root.update()
        arduino_msg = self.send_to_arduino(drink["code"])
        if arduino_msg:
            status_label.config(text=arduino_msg)

        #selection screen after done pouring, we can adjust depending on if we use weight or timer
        #trigger rspi here
        self.root.after(5000, self.display_selection) #5 seconds
    
    def animate(self, label, state):
        dots = ["●  ○  ○", "○  ●  ○", "○  ○  ●", "○  ●  ○"]
        if label.winfo_exists():
            label.config(text = dots[state % 4])
            self.root.after(300, lambda: self.animate(label, state + 1))
    
    def cleanup(self):
        try: 
            if self.ser and self.ser.is_open:
                self.ser.close()
        except Exception:
            pass

        self.root.destroy()


def main():
    ser = serial.Serial("/dev/ttyACM1", 115200, timeout=1) # this port name will change when we upload to arduino vs mac!
    ser.flushInput()
    ser.setDTR(True)
    time.sleep(2)
    print("Serial connection established")

    root = tk.Tk()
    app = Dispenser(root, ser)
        
    root.mainloop()

if __name__ == "__main__":
    main()
