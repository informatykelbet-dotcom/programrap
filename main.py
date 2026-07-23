"""
=========================================================
Generator Raportu Nieobecności
Plik główny programu
=========================================================
"""

import threading
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from pathlib import Path

from report_engine import ReportEngine


class App:

    def __init__(self):

        self.window = tk.Tk()

        self.window.title("Generator raportu nieobecności")
        self.window.geometry("700x220")
        self.window.resizable(False, False)

        # ---------------------------------------
        # Zmienne
        # ---------------------------------------

        self.folder = tk.StringVar()
        self.status = tk.StringVar(value="Gotowy")

        # ---------------------------------------
        # Budowa okna
        # ---------------------------------------

        self.create_widgets()

    # =====================================================
    # Budowa interfejsu
    # =====================================================

    def create_widgets(self):

        frame = ttk.Frame(self.window, padding=15)
        frame.pack(fill="both", expand=True)

        ttk.Label(
            frame,
            text="Folder z kartami pracy:"
        ).pack(anchor="w")

        row = ttk.Frame(frame)
        row.pack(fill="x", pady=5)

        ttk.Entry(
            row,
            textvariable=self.folder
        ).pack(
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
        ).pack(pady=10)

        self.progress = ttk.Progressbar(
            frame,
            orient="horizontal",
            mode="determinate",
            maximum=100
        )

        self.progress.pack(fill="x")

        ttk.Label(
            frame,
            textvariable=self.status
        ).pack(anchor="w", pady=10)

    # =====================================================
    # Wybór folderu
    # =====================================================

    def choose_folder(self):

        folder = filedialog.askdirectory()

        if folder:
            self.folder.set(folder)

    # =====================================================
    # Aktualizacja paska postępu
    # =====================================================

    def update_progress(self, value):

        self.window.after(
            0,
            lambda: self.progress.configure(value=value)
        )

    # =====================================================
    # Aktualizacja statusu
    # =====================================================

    def update_status(self, text):

        self.window.after(
            0,
            lambda: self.status.set(text)
        )

    # =====================================================
    # Start programu
    # =====================================================

    def start(self):

        if not self.folder.get():

            messagebox.showwarning(
                "Brak folderu",
                "Wybierz folder z kartami pracy."
            )

            return

        threading.Thread(
            target=self.generate_report,
            daemon=True
        ).start()

    # =====================================================
    # Generowanie raportu
    # =====================================================

    def generate_report(self):

        try:

            engine = ReportEngine(
                folder=Path(self.folder.get()),
                progress_callback=self.update_progress,
                status_callback=self.update_status
            )

            report = engine.run()

            self.window.after(
                0,
                lambda: messagebox.showinfo(
                    "Gotowe",
                    f"Raport zapisano:\n\n{report}"
                )
            )

        except Exception as e:

            self.window.after(
                0,
                lambda: messagebox.showerror(
                    "Błąd",
                    str(e)
                )
            )

    # =====================================================
    # Uruchomienie programu
    # =====================================================

    def run(self):

        self.window.mainloop()


# =========================================================
# Start programu
# =========================================================

if __name__ == "__main__":

    App().run()
