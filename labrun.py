ALL_DIRS = ['U', 'D', 'L', 'R']
ALL_TYPES = ['#', '.']

charToGo = {'U' : (-1, 0),
            'D' : (1, 0), 
            'L' : (0, -1), 
            'R' : (0, 1),
            'H' : (0, 0)} 

class Lab:
    def __init__(self, cells):
        self.cells = cells
        self.n = len(cells)
        self.m = len(cells[0])
        for i in range(self.n):
            for j in range(self.m):
                if (cells[i][j] == 'S'):
                    self.start = (i, j)
                if (cells[i][j] == 'F'):
                    self.finish = (i, j)

    def cellAt(self, x, y):
        return self.cells[x][y]

    def canGo(self, x, y):
        return x >= 0 and x < self.n and y >= 0 and y < self.m and self.cells[x][y] != '#'


def match(line, lab, pos):
    go = charToGo[line[0]]
    x = pos[0] + go[0]
    y = pos[1] + go[1]
    if x < 0 or x >= lab.n or y < 0 or y >= lab.m:
        return False
    if line[1] == '#':
        return lab.cellAt(x, y) == '#'
    if line[1] == '.':
        return lab.cellAt(x, y) == '.' or lab.cellAt(x, y) == 'S' or lab.cellAt(x, y) == 'F'
    return False


class Prog:
    def __init__(self, lines = [], default = '!'):
        self.lines = lines
        self.default = default

    def runInPos(self, lab, pos):
        for line in self.lines:
            if match(line, lab, pos):
                return line[-1]
        return self.default

    def runIn(self, run):
        return self.runInPos(run.lab, run.pos) 

def overChar(strp, pos, val):
    sli = list(strp)
    sli[pos] = val
    return ''.join(sli)


class Run:
    def __init__(self, lab, prog):
        self.lab = lab
        self.prog = prog
        self.pos = lab.start

    def printState(self, wait = False):
        cp = self.lab.cells.copy()
        for i in range(len(cp)):
            for j in range(len(cp[0])):
                if cp[i][j] == 'S':
                    cp[i] = overChar(cp[i], j, '.')
                if i == self.pos[0] and j == self.pos[1]:
                    cp[i] = overChar(cp[i], j, '@')
        for i in range(len(cp)):
            print(cp[i])
        if wait:
            #input("press to conitinue")
            input()

    def runCheck(self, display = False):
        self.visited = set()
        while True:
            if self.pos == self.lab.finish:
                return True
            if self.pos in self.visited:
                print("Going in cycle")
                return False
            if display:
                self.printState(wait = True)

            self.visited.add(self.pos)
            action = self.prog.runIn(self)
            #print("go with action " + action)
            go = charToGo[action]
            self.pos = (self.pos[0] + go[0], self.pos[1] + go[1])

            if not self.lab.canGo(self.pos[0], self.pos[1]):
                print("Go into a wall")
                return False
            

            

"""
l = Lab(["#F##",
         "#..#",
         "##.#",
         "#..#",
         "#S##"])
"""

l = Lab(["#F######",
         "#..#...#",
         "##...#.#",
         "######.#",
         "##.....#",
         "#.....##",
         "#S######"])


p = Prog(["U.U",
          "L.L",
          "U#R"],
          'D')

#res = Run(l, p).runCheck(display = True)
#print(res)

