import warnings

import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model

    def connessa(self,e):
        connessa = self._model.getComponenteConnessa()
        self._view.txtOut.controls.append(
            ft.Text(f"Ci sono {connessa} componenti connesse"))
        self._view.update_page()

    def maxGrade(self, e):
        nN, nE = self._model.getGraphSize()
        if nN == 0:
            self._view.create_alert("Bisogna prima creare il grafo")
            return

        maxGrade, v = self._model.getMaxGrade()
        self._view.txtOut.controls.append(ft.Text(f"Giocatore con grafo massimo: {v.playerID}-{v.nameFirst} {v.nameLast} con grado {maxGrade} "))
        self._view.update_page()

    def handle_graph(self, e):
        try:
            anno = int(self._view.txt_year.value)
            salario = int(self._view.txt_salario.value) * (10**6)

        except ValueError:
            self._view.create_alert("Inserire due valori interi")
            return

        self._model.loadYears()
        if not self._model.tryAnno(anno):
            self._view.create_alert("L'anno inserito non è valido")
            return
        else:
            self._model.buildGraph(anno, salario)
            nN, nE = self._model.getGraphSize()
            self._view.txtOut.clean()
            self._view.txtOut.controls.append(ft.Text(f"Grafo creato con {nN} nodi e {nE} archi"))

        self._view.update_page()

    def handle_search(self, e):
        nN, nE = self._model.getGraphSize()
        if nN == 0:
            self._view.create_alert("Crea il grafo strunz")
            return

        anno = int(self._view.txt_year.value)
        bestPath, bestScore = self._model.getBestPath(anno)
        print(len(bestPath))
        print(bestPath)
        print(bestScore)

        self._view.txtOut2.clean()
        self._view.txtOut2.controls.append(ft.Text(f"Best path ottenuto con {len(bestPath)} squadre"))
        self._view.txtOut2.controls.append(ft.Text(f"Salario cumulativo: {bestScore}"))
        self._view.txtOut2.controls.append(ft.Text(f"Lista giocatori: "))
        for i in bestPath:
            self._view.txtOut2.controls.append(ft.Text(f"{i.playerID}"))
        self._view.update_page()
