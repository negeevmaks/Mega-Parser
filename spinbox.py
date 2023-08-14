import customtkinter
from typing import Callable, Union
class Spinbox(customtkinter.CTkFrame):
    def __init__(self, *args,
                width: int = 100,
                height: int = 32,
                step_size: Union[int, float] = 1,
                command: Callable = None,
                min_value: int = 0,
                max_value: int = 9999,
                default_value: int = 5,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self.step_size = step_size
        self.command = command
        self.min_value = min_value
        self.max_value = max_value
        self.default_value = default_value

        self.configure(fg_color=("gray78", "gray28"))  # set frame color

        self.grid_columnconfigure((0, 2), weight=0)  # buttons don't expand
        self.grid_columnconfigure(1, weight=1)  # entry expands

        self.subtract_button = customtkinter.CTkButton(self, text="-", width=height-6, height=height-6,
                                                        command=self.subtract_button_callback)
        self.subtract_button.grid(row=0, column=0, padx=(3, 0), pady=3)

        self.entry = customtkinter.CTkEntry(self, width=width-(2*height), height=height-6, border_width=0, justify="center")
        self.entry.grid(row=0, column=1, columnspan=1, padx=3, pady=3, sticky="ew")

        self.add_button = customtkinter.CTkButton(self, text="+", width=height-6, height=height-6,
                                                    command=self.add_button_callback)
        self.add_button.grid(row=0, column=2, padx=(0, 3), pady=3)

        # default value
        self.entry.insert(0, self.default_value)

    def add_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) + self.step_size
            if value <= self.max_value:
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def subtract_button_callback(self):
        if self.command is not None:
            self.command()
        try:
            value = int(self.entry.get()) - self.step_size
            if value >= self.min_value:
                self.entry.delete(0, "end")
                self.entry.insert(0, value)
        except ValueError:
            return

    def get(self) -> Union[int, None]:
        try:
            return int(self.entry.get())
        except ValueError:
            return None

    def set(self, value: int):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(int(value)))

if __name__ == "__main__":
    app = customtkinter.CTk()
    customtkinter.set_appearance_mode("light")
    spinbox_1 = Spinbox(app, width=150, max_value=40, min_value=0)
    spinbox_1.grid(row=0, column=0)

    # spinbox_1.set(35)
    def button_callback():
        print(spinbox_1.get())
    button = customtkinter.CTkButton(app, text="my button", command=button_callback)
    button.grid(row=1, column=0)

    app.mainloop()