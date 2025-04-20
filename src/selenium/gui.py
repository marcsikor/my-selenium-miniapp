import tkinter as tk
import json
import pywinstyles, sys

import sv_ttk
import scraper

class UserInterface:
    def __init__(self):
        self.root = tk.Tk()
        self.username = tk.StringVar()
        self.password = tk.StringVar()

    def apply_theme_to_titlebar(self):
        version = sys.getwindowsversion()
        if version.major == 10 and version.build >= 22000:
            # Set the title bar color to the background color on Windows 11 for better appearance
            pywinstyles.change_header_color(self.root, "#1c1c1c")
        elif version.major == 10:
            pywinstyles.apply_style(root, "dark")
            # A hacky way to update the title bar's color on Windows 10 (it doesn't update instantly like on Windows 11)
            self.root.wm_attributes("-alpha", 0.99)
            self.root.wm_attributes("-alpha", 1)

    def configure_window(self):
        # Example usage (replace `root` with the reference to your main/Toplevel window) -- has to be under setting dark theme
        self.apply_theme_to_titlebar()
        # set app title
        self.root.title("USOS Bot")
        # change initial window size
        self.root.geometry("500x400")
        # set custom window icon
        photo = tk.PhotoImage(file = 'apprentice.png')
        self.root.wm_iconphoto(False, photo)
        # This is where the magic happens
        sv_ttk.set_theme("dark")

    def create_app(self):
        # set window & top bar properties properties
        self.configure_window()
        # place a label on the root window
        tk.Label(self.root, text="Aplikacja (raczej) nie będzie przechowywać twoich danych logowania do USOSa").pack()
        # getting username
        tk.Label(self.root, text="Podaj numer albumu").pack() 
        tk.ttk.Entry(self.root, textvariable=self.username).pack()
        # getting password
        tk.Label(self.root, text="Podaj hasło do USOSa").pack()
        tk.ttk.Entry(self.root, show="*", textvariable=self.password).pack()
        # submit button
        tk.ttk.Button(self.root, text="Pobierz średnią", command=self.handle_click).pack()
    
    def start_app(self):
        self.root.mainloop()

    def handle_click(self):
        with open('portal-paths.json') as paths:
            paths_dict = json.load(paths)

        sc = scraper.Scraper(True)

        sc.execute_login(self.username.get(), self.password.get(), paths_dict["login-page"])
        
        output = sc.get_grades(paths_dict["grades-page"])
        
        tk.Label(self.root, text="Wykaz średnich poniżej").pack()
        for period, grade in output.items():
           tk.Label(self.root, text=period + ': ' + str(round(grade,3))).pack()

if __name__ == "__main__":
    ui = UserInterface()
    ui.create_app()
    ui.start_app()
