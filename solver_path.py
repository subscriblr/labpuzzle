from labrun import Lab, Prog, Run
from labrun import charToGo, match
from labrun import ALL_DIRS, ALL_TYPES
from tests import test_cases

class Path:
    def __init__(self):
        self.cells = []

class PathGenerator:
    def __init__(self, lab):
        self.lab = lab
        self.paths = []
        self.current_path = [lab.start]
        
        
    def generate(self):
        curpos = self.current_path[-1]
        if (curpos == self.lab.finish):
            self.paths.append(self.current_path.copy())
            return
        #print(self.current_path)
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if abs(dx) + abs(dy) != 1: continue
                if not self.lab.canGo(curpos[0] + dx, curpos[1] + dy): continue
                nextpos = (curpos[0] + dx, curpos[1] + dy)
                if nextpos in self.current_path: continue

                self.current_path.append(nextpos)
                self.generate()
                self.current_path.pop()

class PathSolver:
    def __init__(self, lab):
        self.lab = lab
        self.prog = Prog()
        

    def solvePath(self, path):
        actions = []
        for i in range(len(path) - 1):
            curaction = '!'
            for (c, dd) in charToGo.items():
                if path[i][0] + dd[0] == path[i + 1][0] and path[i][1] + dd[1] == path[i + 1][1]:
                    curaction = c
            assert curaction != '!'
            actions.append(curaction)
        covered = [False] * len(actions)

        #print("trying to solve path " + str(path))
        self.prog.lines.clear()
        while True:
            #print("iteration " + str(covered))
            #try add default
            action = '!'
            can_end = True
            for i in range(len(actions)):
                if covered[i]: continue
                if action == '!':
                    action = actions[i]
                elif action != actions[i]:
                    can_end = False
            if can_end:
                self.prog.default = action
                return True
            #try add a line
            added = False
            for d in ALL_DIRS:
                for t in ALL_TYPES:
                    for g in ALL_DIRS:
                        if added: break
                        line = ''.join([d, t, g])

                        matched_ids = []
                        have_bad_id = False
                        for i in range(len(actions)):
                            if (covered[i]): continue
                            if match(line, self.lab, path[i]):
                                if actions[i] == g:
                                    matched_ids.append(i)
                                else:
                                    have_bad_id = True
                                    break
                        if have_bad_id or len(matched_ids) == 0:
                            continue
                        self.prog.lines.append(line)
                        added = True
                        for id in matched_ids:
                            covered[id] = True
            if not added:
                return False

                


    def solve(self):
        g = PathGenerator(self.lab)
        g.generate()
        print("Generated " + str(len(g.paths)) + " paths")
        for path in g.paths:
            if self.solvePath(path):
                return True
        return False

test_id = [0, 1, 2]

for tid in test_id:
    print("Running solver on test " + str(tid))
    l = Lab(test_cases[tid])    
    ps = PathSolver(l)
    print(ps.solve())
    print(ps.prog.lines)
    print(ps.prog.default)
    Run(l, ps.prog).runCheck(display = True)