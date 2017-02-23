# chille-ding-sudoku-s-jwz
make chille ding great again

we got the best sudokus. they're great. it's true.

nodig:
def addToStatespaceList(een sudoku in de vorm rij van rijen, rij van StateSpaces):
   voegt de eerste input toe aan de tweede, maar op zo een manier dat op elk punt waar een 0 staat in de sudoku,
   er hierin een lijst staat met de mogelijkheden voor de situatie.


def getSafestOption(een StateSpace):
   return: A = een list met eerst de coördinaten x,y en daarna de lijst met mogelijkheden
   oftewel bijvoorbeeld [6,8,[1,2,3,6]] voor puzzle1.sudoku wanneer nog niets is ingevuld

def setFirstOfOptions(een sudoku in de vorm rij van rijen, A):
   return: een sudoku in de vorm rij van rijen zodat op de gegeven x,y positie de eerste waarde is ingevuld uit
           de bijgegeven list.

def removeFirstOfOptionsFromStateSpace(een statespace, A):
   return: een nieuwe StateSpace representatie op zo een wijze dat de lijst op positie x,y uit A zo is aangepast dat
           de eerste optie verwijdert is.

def checkStateSpaceValid(een StateSpace):
   return false als er een lijst is in de StateSpace die leeg is
          voorbeeld:
          dit is de eerste rij van een statespace representatie van een oningevulde puzzle1.sudoku
          [[7,9,[7,9,3,1,5,2,8][4,6],[7,9,3,1,6,4][2,5,8],[7,9,3,1,6][2,4,5,8],[7,9,3,1,6,5,8][2,4],





defenitielijst van waardes/vormen die vaker terugkomen:
A = een list met eerst de coördinaten x,y en daarna de lijst met mogelijkheden
   oftewel bijvoorbeeld [6,8,[1,2,3,6]] voor puzzle1.sudoku wanneer nog niets is ingevuld

