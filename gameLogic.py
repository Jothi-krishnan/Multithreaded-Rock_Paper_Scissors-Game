class Game:
    def __init__(self, id):
        self.p1Gone = False
        self.p2Gone = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    
    def isConnected(self):
        return self.ready
    
    def bothGone(self):
        return self.p1Gone and self.p2Gone

    def getPlayerMove(self, p):
        return self.moves[p]

    def play(self, player, move):
        self.moves[player] = move

        if player == 0:
            self.p1Gone = True
        else:
            self.p2Gone = True
        
    
    def findWinner(self):
        p1 = self.moves[0].upper()[0]
        p2 = self.moves[1].upper()[0]

        winner = -1

        if p1 == "R" and p2 == "P":
            winner = 1
        elif p1 == "R" and p2 == "S":
            winner = 0
        elif p1 =="P" and p2 == "R":
            winner = 0
        elif p1 == "P" and p2 == "S":
            winner = 1
        elif p1 == "S" and p2 == "R":
            winner = 1
        elif p1 == "S" and p2 == "P":
            winner = 0

        return winner

    def resetGame(self):
        self.p1Gone = False
        self.p2Gone = False
    