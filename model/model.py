import copy
import networkx as nx
from database.DAO import DAO


class Model:
    def __init__(self):
        self.listYears = []

        self.graph = nx.Graph()
        self.nodes = []
        self.edges = []
        self.idMap = {}

        self.bestPath = []
        self.bestScore = 0

    def getBestPath(self, anno):
        self.bestScore = 0
        self.bestPath = []

        for n in self.nodes:
            parziale = [n]
            squadre = []
            s = DAO.getPlayerTeamsInYear(anno, n.playerID)
            squadre.extend(s)
            tmp = copy.deepcopy(self.nodes)
            tmp = sorted(tmp, key=lambda x: x.salary, reverse=True)

            self._ricorsione(anno, squadre, parziale, tmp)

            return self.bestPath, self.bestScore

    def _ricorsione(self, anno, squadre, parziale, tmp):
        tmp.remove(parziale[-1])
        if len(tmp) == 0:
            salario = self.getSalary(parziale)
            if len(parziale) >= len(self.bestPath) and salario > self.bestScore:
                self.bestScore = salario
                self.bestPath = copy.deepcopy(parziale)

        """if len(parziale) > self.bestScore:
            self.bestScore = len(parziale)
            self.bestPath = copy.deepcopy(parziale)"""

        for nodo in tmp:
            if nodo not in parziale:
                conditio, squadre_appartenenza = self.checkSquadre(anno, nodo.playerID, squadre)
                if conditio:
                    parziale.append(nodo)
                    squadre.extend(squadre_appartenenza)
                    self._ricorsione(anno, squadre, parziale, tmp)
                    parziale.pop()
                    for i in squadre_appartenenza:
                        squadre.remove(i)

                else:
                    tmp.remove(nodo)

    def checkSquadre(self, anno, nodo, squadre):
        squadre_appartenenza = DAO.getPlayerTeamsInYear(anno, nodo)
        check = True
        for s in squadre_appartenenza:
            if s in squadre:
                check = False

        return check, squadre_appartenenza

    def getSalary(self, squadra):
        salario = 0
        for i in squadra:
            salario += i.salary

        return salario

    def loadYears(self):
        self.listYears = DAO.getYears()

    def tryAnno(self, anno):
        if anno in self.listYears:
            return True
        else:
            return False

    def buildGraph(self, anno, salario):
        self.graph.clear()
        self.nodes = DAO.getNodes(anno, salario)
        self.graph.add_nodes_from(self.nodes)

        for n in self.nodes:
            self.idMap[n.playerID] = n

        self.edges = DAO.getEdge(anno, salario, self.idMap)
        self.graph.add_edges_from(self.edges)

    def getGraphSize(self):
        return len(self.nodes), len(self.edges)

    def getMaxGrade(self):
        maxGrado = 0
        v = ""
        for n in self.nodes:
            grado = len(list(self.graph[n]))
            if grado > maxGrado:
                maxGrado = grado
                v = n
        return maxGrado, v

    def getComponenteConnessa(self):
        connessa = list(nx.connected_components(self.graph))
        return len(connessa)
