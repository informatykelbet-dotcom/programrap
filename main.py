import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path
import threading

from report_engine import ReportEngine


class App:

    def __init__(self):

        self.window = tk.Tk()

        self.window.title("Generator raportu nieobecności")
        self.window.geometry("700x220")
        self.window.resizable(False, False)

        self.folder = tk.StringVar()
        self.status = tk.StringVar(value="Gotowy")

        self.create_widgets()

        self.window.mainloop()

    def create_widgets(self):

        frame = ttk.Frame(self.window, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Folder z kartami pracy:"
        ).pack(anchor="w")

        row = ttk.Frame(frame)
        row.pack(fill="x", pady=5)

        self.entry = ttk.Entry(
            row,
            textvariable=self.folder
        )

        self.entry.pack(
            side="left",
            fill="x",
            expand=True
        )

        ttk.Button(
            row,
            text="Przeglądaj...",
            command=self.choose_folder
        ).pack(side="left", padx=5)

        ttk.Button(
            frame,
            text="Generuj raport",
            command=self.start
        ).pack(pady=15)

        self.progress = ttk.Progressbar(
            frame,
            mode="determinate",
            length=600
        )

        self.progress.pack()

        ttk.Label(
            frame,
            textvariable=self.status
        ).pack(anchor="w", pady=10)

    def choose_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.folder.set(folder)

    def start(self):

        folder = self.folder.get()

        if not folder:

            messagebox.showwarning(
                "Uwaga",
                "Wybierz folder."
            )

            return

        threading.Thread(
            target=self.generate,
            daemon=True
        ).start()

    def generate(self):

        try:

            engine = ReportEngine(
                Path(self.folder.get()),
                self.progress,
                self.status
            )

            engine.run()

            messagebox.showinfo(
                "Gotowe",
                "Raport został wygenerowany."
            )

        except Exception as e:

            messagebox.showerror(
                "Błąd",
                str(e)
            )


if __name__ == "__main__":
    App()
