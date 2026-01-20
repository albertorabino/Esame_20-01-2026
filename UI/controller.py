import flet as ft
from UI.view import View
from model.model import Model

class Controller:
    def __init__(self, view: View, model: Model):
        self._view = view
        self._model = model
        self._num_nodi = 0

    def handle_create_graph(self, e):

        self._view.txt_result.clean()
        self._view.ddArtist.options = []
        self._num_nodi = 0
        try:
            numero = self._view.txtNumAlbumMin.value
            numero = int(numero)
            if numero>0:
                self._model.build_graph(numero)
                self._num_nodi,archi,nodi = self._model.dettagli_grafo()
                self._view.txt_result.controls.append(ft.Text(f"Grafo creato: {self._num_nodi} nodi (artisti), {archi} archi"))
                self._view.ddArtist.disabled = False
                self._view.txtMinDuration.disabled = False
                self._view.txtMaxArtists.disabled = False
                self._view.btnSearchArtists.disabled = False
                for nodo in nodi:
                    self._view.ddArtist.options.append(ft.dropdown.Option(key=nodo.id,text = f"{nodo.name}"))
            else:
                self._view.show_alert("Inserire un positivo")
                return
        except:
            self._view.show_alert("Inserire un valore intero positivo")
            return
        self._view.update_page()

    def handle_dd(self,e):
        self._view.btnArtistsConnected.disabled = False
        self._view.update_page()

    def handle_connected_artists(self, e):
        self._view.txt_result.clean()
        id = self._view.ddArtist.value
        risultato,artista = self._model.analizza_grafo(id)
        self._view.txt_result.controls.append(ft.Text(f"Artisti direttamente collegati all'artista {artista.id}, {artista.name}"))
        for r in risultato:
            self._view.txt_result.controls.append(
                ft.Text(f"{r[0].id}, {r[0].name} - Numero generi in comune: {r[1]}"))
        self._view.update_page()


    def handle_cammino(self,e):
        durata_minima = self._view.txtMinDuration.value
        lunghezza = self._view.txtMaxArtists.value
        self._view.txt_result.clean()

        try:
            durata_minima = float(durata_minima)
            lunghezza = int(lunghezza)
            start = self._view.ddArtist.value
            start = int(start)
            if durata_minima<0:
                self._view.show_alert("Inserire un valore durata (float) positivo")
            elif lunghezza<=0 or lunghezza>self._num_nodi:
                self._view.show_alert(f"Inserire un valore artista (int) tra 1 e {self._num_nodi}")
            else:
                best,peso = self._model.ricerca_cammino(durata_minima,lunghezza,start)
                k = 0
                for b in best:
                    print(b)
                    if k==0:
                        self._view.txt_result.controls.append(ft.Text(f"Cammino di peso massimo dell'artista {b.id}, {b.name}\nLunghezza: {len(best)}"))
                        self._view.txt_result.controls.append(ft.Text(f"{b.id}, {b.name}"))
                        k+=1
                    else:
                        self._view.txt_result.controls.append(ft.Text(f"{b.id}, {b.name}"))
                self._view.txt_result.controls.append(ft.Text(f"Peso massimo: {peso}"))

        except:
            self._view.show_alert("Inserire un valore positivo sia per durata(float) che per gli artisti(int), con anche l'artista")
            return


        self._view.update_page()


