# Stephan Borzsonyi , Donald Kossmann , Konrad Stocker,
# The Skyline Operator, Proceedings of the 17th International Conference on Data Engineering,
# p.421-430, April 02-06, 2001

def cmpf(a, b, EPS = 1e-15):
    if a > b - EPS:
        if b > a - EPS:
            return 0
        else:
            return 1
    return -1

class RELATION:
        DOMINATED = 0
        DOMINATES = 1 
        INCOMPARABLE = 2
       
class SkylineBNL:
   
    def __init__(self):
        self.window = {}
        
    def addPoint(self, p):
        removeEntries = []
        notDominated = True
        for point in self.window:
            relation = self.__compare(p, self.window[point])
            if relation == RELATION.DOMINATED:
                notDominated = False
                break
            elif relation == RELATION.DOMINATES:
                removeEntries.append(point)
        
        for r in removeEntries:
            del self.window[r]
        
        if notDominated:
            self.window[p.rule] = p                
    
    def __compare(self, p1, p2):
        i = 0
        while i < p1.len() and cmpf(p1.value(i), p2.value(i)) == 0:
            i += 1
        
        if i == p1.len():
            return RELATION.INCOMPARABLE
        
        if cmpf(p1.value(i), p2.value(i)) < 0:
            for j in range(i+1, p1.len()):
                if cmpf(p1.value(j), p2.value(j)) > 0:
                    return RELATION.INCOMPARABLE 
            return RELATION.DOMINATED
        
        for j in range(i+1, p1.len()):
            if cmpf(p1.value(j), p2.value(j)) < 0:
                return RELATION.INCOMPARABLE 
        
        return RELATION.DOMINATES
        
        