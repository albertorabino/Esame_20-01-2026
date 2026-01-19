import flet as ft
from UI.alert import AlertManager

class View:
    def __init__(self, page: ft.Page):
        # Page
        self.page = page
        self.page.title = "Programmazione Avanzata - Primo Appello - iTunes"
        self.page.horizontal_alignment = "center"
        self.page.theme_mode = ft.ThemeMode.LIGHT

        # Alert
        self.alert = AlertManager(page)

        # Controller
        self.controller = None

    def show_alert(self, messaggio):
        self.alert.show_alert(messaggio)

    def set_controller(self, controller):
        self.controller = controller

    def update(self):
        self.page.update()

    def load_interface(self):
        """ Crea e aggiunge gli elementi di UI alla pagina e la aggiorna. """
        # Intestazione
        self.txt_titolo = ft.Text(value="Gestione Artisti e Generi", size=30, weight=ft.FontWeight.BOLD)

        # RIEMPIRE !!!!

        # --- Layout della pagina ---
        self.page.add(
            self.txt_titolo
        )

        self.page.scroll = "adaptive"
        self.page.update()

