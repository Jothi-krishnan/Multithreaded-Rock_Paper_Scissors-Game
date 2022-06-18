#This python file contains a class named "Game" which is imported into client.py file. 
#This Game class is very imporant because, it is necessary to create a different instance for each game and this servers to that purpose.

class Game:
    def __init__(self, id):
        #initializing the variables on creation of the instance with a particular gameId.
        self.p1Gone = False
        self.p2Gone = False
        self.ready = False
        self.id = id
        self.moves = [None, None]

    #this function returns if both the players are still connected to the server or not
    def isConnected(self):
        return self.ready
    
    #this function determines if both the players have locked in their choices for the game or not.
    def bothGone(self):
        return self.p1Gone and self.p2Gone

    #The purpose of this function is to get a specific player "p" 's move
    def getPlayerMove(self, p):
        return self.moves[p]

    #this function acconts for the move made by the player. Each move is given as argument which is sent from h
    def play(self, player, move):
        self.moves[player] = move

        if player == 0:
            self.p1Gone = True
        else:
            self.p2Gone = True
        
    
    #This function determines the winner by comparing the moves which are sent from the Buttons in the client.py to the server.
    #This returs -1 if the game is drawn, 0 if player 1 wins and 1 if player 2 wins the current game.
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

    #The below function is called to reset the game when a round is completed. This function resets the variables p1Gone and p2Gone, 
    #which will be altered again if one of them makes a move.
    def resetGame(self):
        self.p1Gone = False
        self.p2Gone = False
    