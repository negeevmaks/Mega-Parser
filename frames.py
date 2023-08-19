import customtkinter as ctk
from spinbox import Spinbox
from math import ceil
from os import getcwd
from time import sleep
from datetime import datetime

def round_up(number, multiple):
    return int(ceil(number / multiple) * multiple)

class SiteChooseFrame(ctk.CTkFrame):
    def __init__(self, master, title, values, checkbox_frame):
        super().__init__(master)
        self.values = values
        self.title = title
        self.radiobuttons = []
        self.variable = ctk.StringVar(value="")

        self.title_label = ctk.CTkLabel(self, text=self.title, 
                                fg_color=("#C0C0C0","gray30"), corner_radius=6)
        self.title_label.grid(row=0, column=1, padx=10, pady=(10, 0), sticky="ew", columnspan=2)

        for i, value in enumerate(self.values):
            radiobutton = ctk.CTkRadioButton(self, text=value, value=value, variable=self.variable,
                                            command=lambda val=value: self.update_checkbox_frame(val, checkbox_frame))
            radiobutton.grid(row=1, column=i, padx=10, pady=(10, 10), sticky="w")
            self.radiobuttons.append(radiobutton)

    def get(self):
        return self.variable.get()

    def set(self, value):
        self.variable.set(value)

    def update_checkbox_frame(self, value, checkbox_frame):
        import main
        checkbox_frame.set(main.checks(value))

class MyScrollableCheckboxFrame(ctk.CTkScrollableFrame):
    def __init__(self, master, title, values):
        super().__init__(master, label_text=title)
        self.grid_columnconfigure(0, weight=1)
        self.values = values
        self.checkboxes = []
        self.create_label()

    def create_label(self):
        self.label = ctk.CTkLabel(self, text="Виберіть сайт")
        self.label.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="w")
        self.is_label = True

    def create_checkboxes(self):
        if self.is_label:
            self.label.grid_forget()
            self.label.destroy()
            self.is_label = False
        for i, value in enumerate(self.values):
            checkbox = ctk.CTkCheckBox(self, text=value)
            checkbox.grid(row=i+1, column=0, padx=10, pady=(10, 0), sticky="w")
            self.checkboxes.append(checkbox)

    def set(self, new_values):
        # Clear existing checkboxes
        for checkbox in self.checkboxes:
            checkbox.grid_forget()
            checkbox.destroy()
        self.checkboxes = []

        # Set new checkboxes
        self.values = new_values
        self.create_checkboxes()

    def get(self):
        checked_checkboxes = []
        for checkbox in self.checkboxes:
            if checkbox.get() == 1:
                checked_checkboxes.append(checkbox.cget("text"))
        return checked_checkboxes

class AmountChooseFrame(ctk.CTkFrame):
    def __init__(self, master, title, min_val, max_val):
        super().__init__(master)
        self.title = title
        self.max = max_val
        self.min = min_val
        
        self.title_label = ctk.CTkLabel(self, text=self.title,
                                        fg_color=("#C0C0C0", "gray30"), corner_radius=6)
        self.title_label.grid(row=0, column=0, 
                            padx=10, pady=10, 
                            sticky="w")

        self.amount = ctk.CTkSlider(self, from_=self.min, to=self.max,
                                    command=self.slider_event)
        self.amount.set(30)
        self.amount.grid(row=1, column=0, 
                        padx=10, pady=10, 
                        sticky="ew", columnspan=3)

        self.amount_label = ctk.CTkLabel(self, text=f"Поточне значення: {int(self.amount.get())}", corner_radius=6)
        self.amount_label.grid(row=0, column=2, 
                            padx=10, pady=10, 
                            sticky="w")

        self.grid_columnconfigure(1, weight=1)

    def slider_event(self, value):
        rounded_value = round_up(value, 10)
        self.amount_label.configure(text=f"Кількість машин: {rounded_value}")
    
    def get(self):
        return round_up(self.amount.get(), 10)

class YearChooseFrame(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        year = datetime.now().year
        
        self.year_main_title = ctk.CTkLabel(self, text="Рік", 
                                            fg_color=("#C0C0C0","gray30"), 
                                            corner_radius=6)
        self.year_main_title.grid(row=0, column=0, 
                                padx=10, pady=10, 
                                sticky="ew", rowspan=2)
        
        
        self.min_year_title = ctk.CTkLabel(self, text="Від:", corner_radius=6)
        self.min_year_title.grid(row=0, column=1, 
                                padx=10, pady=10, 
                                sticky="ew")
        
        self.min_year_spinbox = Spinbox(self, width=150, 
                                        min_value=0,
                                        max_value=year, 
                                        default_value = year)
        self.min_year_spinbox.grid(row=0, column=2)
        
        self.max_year_title = ctk.CTkLabel(self, text="До:", corner_radius=6)
        self.max_year_title.grid(row=1, column=1, 
                                padx=10, pady=10, 
                                sticky="ew")
        
        self.max_year_spinbox = Spinbox(self, width=150, 
                                        min_value=0, 
                                        max_value=year, 
                                        default_value = year)
        self.max_year_spinbox.grid(row=1, column=2, 
                                padx=10)
    
    def get_min(self):
        return self.min_year_spinbox.get()
    def get_max(self):
        return self.max_year_spinbox.get()

class PriceChooseFrame(ctk.CTkFrame):
    def __init__(self, master, text):
        super().__init__(master)
        
        self.price_main_title =  ctk.CTkLabel(self, text=text, 
                                            fg_color=("#C0C0C0","gray30"), 
                                            corner_radius=6)
        self.price_main_title.grid(row=0, column=0, 
                                padx=10, pady=10, 
                                sticky="ew", rowspan=2)
        
        
        self.min_price_title = ctk.CTkLabel(self, text="Від:", corner_radius=6)
        self.min_price_title.grid(row=0, column=1, 
                                padx=10, pady=10, 
                                sticky="ew")
        
        self.min_price_spinbox = Spinbox(self, width=150, 
                                        min_value=0, 
                                        default_value = 0)
        self.min_price_spinbox.grid(row=0, column=2)
        
        self.max_price_title = ctk.CTkLabel(self, text="До:", corner_radius=6)
        self.max_price_title.grid(row=1, column=1, 
                                padx=10, pady=10, 
                                sticky="ew")
        
        self.max_price_spinbox = Spinbox(self, width=150, 
                                        min_value=0, 
                                        default_value = 0)
        self.max_price_spinbox.grid(row=1, column=2, 
                                    padx=10)
    
    def get_min(self):
        return self.min_price_spinbox.get()
    def get_max(self):
        return self.max_price_spinbox.get()