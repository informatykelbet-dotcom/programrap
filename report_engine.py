"""
=========================================================
Generator Raportu Nieobecności
Silnik programu
=========================================================

Autor: ChatGPT + Użytkownik
Wersja: 1.0
"""

from pathlib import Path
from openpyxl import load_workbook, Workbook
from datetime import date, datetime, timedelta
import calendar
import re


class ReportEngine:
    """
    Główna klasa programu.

    Odpowiada za:
        • wyszukanie wszystkich plików
        • analizę obecności
        • wygenerowanie raportu Excel
    """

    # =====================================================
    # Konstruktor klasy
    # =====================================================

    def __init__(self, folder, progress_callback=None, status_callback=None):

        # Folder wybrany przez użytkownika
        self.folder = Path(folder)

        # Funkcje aktualizacji GUI
        self.progress_callback = progress_callback
        self.status_callback = status_callback

        # Lista znalezionych plików
        self.files = []

        # Wyniki końcowe
        self.results = []

        # Miesiąc raportu
        self.report_month = None

        # Rok raportu
        self.report_year = None

    # =====================================================
    # Aktualizacja statusu
    # =====================================================

    def set_status(self, text):

        """
        Aktualizuje napis widoczny w oknie programu.
        """

        if self.status_callback:
            self.status_callback(text)

    # =====================================================
    # Aktualizacja paska postępu
    # =====================================================

    def set_progress(self, value):

        """
        Aktualizuje pasek postępu.
        """

        if self.progress_callback:
            self.progress_callback(value)

    # =====================================================
    # Wyszukiwanie plików Excel
    # =====================================================

    def scan_files(self):

        """
        Wyszukuje wszystkie pliki .xlsx
        również w podfolderach.

        Przykład:

        Czerwiec 2026
            |
            |-- Kowalski.xlsx
            |
            |-- Ukraina
                    |
                    |-- Iwan.xlsx

        Zostaną znalezione oba pliki.
        """

        self.files.clear()

        # rglob() przeszukuje wszystkie podfoldery
        for file in self.folder.rglob("*.xlsx"):

            # Pomijamy wygenerowane wcześniej raporty
            if file.name.lower().startswith("raport_nieobecności"):
                continue

            # Pomijamy pliki tymczasowe Excela
            if file.name.startswith("~$"):
                continue

            self.files.append(file)

        # Sortujemy alfabetycznie
        self.files.sort()

        return self.files

    # =====================================================
    # Wyciąganie nazwiska i imienia z nazwy pliku
    # =====================================================

    @staticmethod
    def get_employee_name(file_path):

        """
        Z:

            BORÓWKA PIOTR 168.xlsx

        otrzymujemy:

            BORÓWKA PIOTR

        Z:

            NOWAK JAN 232,5 delegacja.xlsx

        otrzymujemy:

            NOWAK JAN
        """

        name = Path(file_path).stem

        match = re.search(r"\s+\d", name)

        if match:
            return name[:match.start()].strip()

        return name.strip()
