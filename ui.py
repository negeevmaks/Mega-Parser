from frames import *
from tkinter import messagebox, filedialog

folderpath = ""
def get_folderpath():
    global folderpath
    folderpath = filedialog.askdirectory(initialdir=getcwd(), 
                                        mustexist=True, 
                                        title = "Виберіть папку, в яку збережений результат")

class App(ctk.CTk):
    app_instance = None  # Global variable within the App class

    def __init__(self):
        super().__init__()

        self.title("Multi-parser")
        self.iconbitmap('parsing.ico')
        self.resizable(False, False)

        self.radiobutton_frame = MyScrollableCheckboxFrame(self, "Категории", values=[])
        self.radiobutton_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew", rowspan=3)
        
        self.checkbox_frame = SiteChooseFrame(self, "Сайти", values=["AUTO.RIA", "Machineryline", "Autoline", "Agriline"], checkbox_frame=self.radiobutton_frame)
        self.checkbox_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew", columnspan=3)
        
        self.price_frame = PriceChooseFrame(self)
        self.price_frame.grid(row=1, column=1, padx=10, pady=10, sticky="nsew", columnspan=2)
        
        self.save_button = ctk.CTkButton(self, text="Вибрати папку", command=get_folderpath)
        self.save_button.grid(row=3, column=1, padx=10, pady=10, sticky="ew", columnspan=2)
        
        self.amount_frame = AmountChooseFrame(self, "Кількість машин", 30, 30000)
        self.amount_frame.grid(row=6, column=0, padx=10, pady=10, sticky="nsew", columnspan=5)

        self.button = ctk.CTkButton(self, text="Почати", command=self.button_callback)
        self.button.grid(row=2, column=1, padx=10, pady=10, sticky="ew", columnspan=2)
        
        self.bar = ctk.CTkProgressBar(self, orientation='horizontal', mode='determinate')
        self.bar.set(0)
        
    def button_callback(self):
        self.data = {
            "site": self.checkbox_frame.get(), 
            "options": self.radiobutton_frame.get(),
            "min_price": self.price_frame.get_min(),
            "max_price": self.price_frame.get_max(),
            "amount": self.amount_frame.get(),
            "folderpath": folderpath,
            "window": self
        }
        if any(value == "" or value is None or value == [] for value in self.data.values()):
            messagebox.showerror('Помилка данних', 'Перевірте, що всі дані введено!')
        else:
            self.bar.grid(row=8, column=0, pady=10, padx=10, sticky="ew", columnspan=3)
            self.bar.start()
            self.button.configure(state="disabled")
            self.update()
            import main
            main.result(self.data)

    def ui_update(self, amount, progress):
        n = amount
        iter_step = 1 / n
        progress_step = iter_step * progress
        self.bar.set(progress_step)
        self.update()
        if amount == progress:
            self.bar.stop()
            messagebox.showinfo(title="Успіх!", message="Вся інформація успішно випарсена!")
            self.destroy()

def start():
    app = App()
    App.app_instance = app  # Assign the App instance to the app_instance variable
    app.mainloop()

def ui_update(amount, progress):
    app = App.app_instance  # Access the App instance through the app_instance variable
    if app is None:
        messagebox.showerror("Error", "UI is not initialized.")
        return

    app.ui_update(amount, progress)