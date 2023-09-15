import math
import time
try: #logica de detecção da biblioteca turtle
    import turtle 
    turtleImported = True
except ModuleNotFoundError as err:
    turtleImported = False

filename = "steps.txt" 

#A* - Hugo Pina e Mariana Gurgel
#27 de Agosto de 2023

#----------------------------------------------Classes e Funcoes auxiliares----------------------------------------------
#Turt: Classe utilizada para o desenho gráfico do algoritmo em execução
class Turt():
    def __init__(self, world, open, closed, obstacles) -> None:
        turtle.hideturtle()
        turtle.tracer(0, 1000)
        turtle.setup(600,600)
        self.screen = turtle.getscreen()
        
        self.size = turtle.screensize()
        self.startPos = (-1*((self.size[0]/2)), (self.size[1]-30))
        self.world = world
        
        self.closed = [x.position for x in closed]
        self.open = [x.position for x in open]
        self.obs = obstacles
        self.path = []
        pass

    def update(self, open, closed, path = []):
        self.open = [x.position for x in open]
        self.closed = [x.position for x in closed]
        self.path = path
        turtle.clear()
        turtle.home()
        self.drawWorld()
        self.screen.update()
        pass

    def drawSquare(self, sqrSide, color='blue'):
        turtle.begin_fill()
        turtle.color('black', color)
        for _ in range(4):
            turtle.forward(sqrSide)
            turtle.right(90)
            
        turtle.end_fill()

    def drawWorld(self):
        turtle.penup()
        turtle.setpos(self.startPos)
        turtle.pendown()
        sqrSide = (self.size[0]-20)/self.world[0]
        for line in range(self.world[0]):
            for col in range(self.world[1]):
                color = 'white'
                if (line,col) in self.path:
                    color = 'green'
                elif(line,col) in self.closed:
                    color = 'red'
                elif (line,col) in self.open:
                    color = 'blue'
                elif (line,col) in self.obs:
                    color = 'black'

                self.drawSquare(sqrSide, color)
                turtle.forward(sqrSide)
            turtle.penup()
            turtle.setpos(self.startPos)
            turtle.right(90)
            for i in range(line+1):
                turtle.forward(sqrSide)
            turtle.left(90)
            turtle.pendown()

#Classe para abstração dos nós        
class Node():
    def __init__(self, position, parent=None, g=0, h=0, f=0) -> None:
        self.position = position
        self.parent = parent
        self.g = g
        self.h = h
        self.f = f
    
    def __eq__(self, __value) -> bool:
        return self.position == __value.position

class World():
    def __init__(self, size) -> None:
        self.size = size
        pass

    def manhattanHeuristics(self, end, actualPosition): #Definição da heuristica Manhattan
        sum = 0
        for i in range(9):
            sum += abs(end.position[i][1] - actualPosition[i][1]) + abs(end.position[i][0] - actualPosition[i][0])
        return sum
    
    def getNextCell(self, open): #Obter a proxima celula dado o conjunto de celulas abertas disponivel
        fValuesArr = [x.f for x in open]
        idxs = [i for i, v in enumerate(fValuesArr) if v == min(fValuesArr)]
        minCells = [open[i] for i in idxs]
        return minCells[0]
    def getNeighbours(self, cell,end,closed): #Funcao responsavel pela obtenção dos vizinhos para dado nó
        deltas = [(0,1),(0,-1),(1,0),(-1,0)]
        neighbours = []
        
        possibleMovingBlocks = [(cell.position[0][0] + delta[0],cell.position[0][1] + delta[1]) for delta in deltas]
        for pmb in possibleMovingBlocks:
            if pmb[0] >= 0 and pmb[0] < 3 and pmb[1] >= 0 and pmb[1] < 3:
                newPos = cell.position.copy()
                oldEmptyPos = newPos[0]
                newEmptyPos = pmb
                newPos[newPos.index(pmb)] = oldEmptyPos # pode estar errado
                newPos[0] = newEmptyPos
                g = cell.g+1
                h = self.manhattanHeuristics(end,newPos)
                f = h + g
                if newPos not in [c.position for c in closed]:
                    neighbours.append(Node(newPos,cell,g,h,f))
        return neighbours

def writeToFile(string): # Funcao de auxilio para a escria no arquivo steps.txt
    with open(filename, 'a') as f:
        f.write(string)

#----------------------------------------------Algoritmo A*----------------------------------------------

def aStar(start, end, world):
    
    open = [start]
    closed = []
    current = world.getNextCell(open)

    counter = 0 
    while current != end:
        closed.append(open.pop(open.index(current)))
        availableNeighbours = world.getNeighbours(current, end,closed) 
        for n in availableNeighbours:
            if n in open and n.f < open[open.index(n)].f:
                #parent already updated
                open[open.index(n)] = n
            if n not in open:
                open.append(n)
        current = world.getNextCell(open)
        print(current.position)

    closed.append(current)
    
    writeToFile(f'{counter} \n OpenCells: {[x.position for x in open]}\n ClosedCells: {[x.position for x in closed]}\n\n')

    path = []
    cell = closed[-1]
    while cell.parent:
        path.append(cell.position)
        cell = cell.parent
    path.append(cell.position)
    print("All closed cells:" + str([x.position for x in closed]))
    writeToFile(f'Path {path[::-1]}')
    return path[::-1]        


#----------------------------------------------Funcao main---------------------------------------------

if __name__ == "__main__":
    world = World((3,3)) #Tamanho do mundo
    start = Node([(1,1),(2,2),(0,1),(2,1),(0,2),(1,0),(1,2),(0,0),(2,0)]) #Posicao do nó inicial
    end = Node([(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]) #Posicao do nó final 

    path = aStar(start,end,world)