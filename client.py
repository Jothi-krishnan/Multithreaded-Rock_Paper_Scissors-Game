import pygame
import socket
import pickle
pygame.font.init()

#This class called Network is responsible for connecting to the server with the necessary information for each game.
#It send and receives information to the server at each stage of each game that is being played.
class Network:
    #initializing the instance with the server and port. 
    """
    The self.server stores the IPv4 Address of your system. 
    You have to update this line once you clone my github repository. 
    To do this, open command prompt in windows and type "ipconfig" without the quotation marks or in ubuntu you can refer the Network settings.
    Then copy and paste the IPv4 Address provided there in Line 18 of this file and also in line 13 of server.py file
    """
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "PASTE YOUR IPv4 ADDRESS HERE"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()

    #This function finds out which player is making or sending the requests to the server at a point.
    def getPlayer(self):
        return self.p

    #This function connects with the servers and it returns the decoded version of the received set of bits.
    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()

        except:
            pass
        
    #This function is responsible for sending the request of each player after every move or after completion of game.
    #This is very important because, it is by this method we would know the status of each game at a particular time.
    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096))

        except socket.error as e:
            print(e)


#This is the width and height of the pygame window and the window is called as "win"
WIDTH =  400
HEIGHT = 400
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")

#This class called Button represents the button that appears on the pygame window after the game starts. i.e Rock Paper and Scissors Buttons.
#This class has it's methods to draw button in a pygame window and each instances of it stores various properties of the button like x and y 
#coordinates, color , text on the button etc.
class Button:
    #Initialization of various properties of the button
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 100
        self.height = 50

    #this function allows us to draw a button with the properties of the current instance on a pygame window
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 20)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x+round(self.width/2)-round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))
    
    #This function determines if the mouse has clicked the button or not.
    def click(self, pos):
        x1 = pos[0] 
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <=self.y + self.height:
            return True
        else:
            return False


#This function is responsible for updating the scores of players that is stored in a list called "scores" for each player in a game called "game"   
def scoreUpdate(game, p, scores):
    if game.findWinner() == -1: #The game is draw if the findWinner() function returns -1
        scores[2] += 1
    else:
        if game.findWinner() == p: #The current player has won the match
            scores[0] += 1
        else:   #The current player has lost the match
            scores[1] += 1

    

#This function is to draw a pygame window "win" for a particular game "game" and a particular player "p" 
def redrawWindow(win, game, p, scores):  
    win.fill((255, 255, 255))

    if not(game.isConnected()): #If the function .isConnected() is false, then there is only one player who has joined the lobby.
        #Printing a text in the lobby of Pygame window until the opponent arrives.
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Waiting for opponent...", 1, (0, 0, 0))
        win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    
    else:
        #Displaying the moves of both the players and their status of their choice(locked in or waiting)
        font = pygame.font.SysFont("comicsans", 30)
        text = font.render("Your Move", 1, (0, 255, 255))
        win.blit(text, (30, 50))

        text = font.render("Opponent's", 1, (0, 255, 255))
        win.blit(text, (200, 50))

        move1 = game.getPlayerMove(0)
        move2 = game.getPlayerMove(1)

        if game.bothGone():
            text1 = font.render(move1, 1, (0, 0, 0))
            text2 = font.render(move2, 1, (0, 0, 0))

        else:
            if game.p1Gone and p == 0:
                text1 = font.render(move1, 1, (0, 0, 0))
            elif game.p1Gone:
                text1 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text1 = font.render("Waiting...", 1, (0, 0, 0))


            if game.p2Gone and p == 1:
                text2 = font.render(move2, 1, (0, 0, 0))
            elif game.p2Gone:
                text2 = font.render("Locked In", 1, (0, 0, 0))
            else:
                text2 = font.render("Waiting...", 1, (0, 0, 0))

        #This makes sure that the oppoent cannot see the move we make but we can see the move we made.
        #For the opponent, status of our move should be displayed as "waiting" or "Locked in" depending on whether we have made our choice or not.
        if p == 1: 
            win.blit(text2, (30, 120))
            win.blit(text1, (200, 120))
        else:
            win.blit(text1, (30, 120))
            win.blit(text2, (200, 120))

        #This block prints the number of wins, losses and ties for each player that is stored in the list "scores"
        f = pygame.font.SysFont("comicsans", 30)
        w1 = f.render("Wins: " + str(scores[0]), 1, (0, 255, 0))
        l1 = f.render("Loses: " + str(scores[1]), 1, (255, 0, 0))
        t1 = f.render("Ties: " + str(scores[2]), 1, (0, 0, 0))

        w2 = f.render("Wins: " + str(scores[0]), 1, (0, 255, 0))
        l2 = f.render("Loses: " + str(scores[1]), 1, (255, 0, 0))
        t2 = f.render("Ties: " + str(scores[2]), 1, (0, 0, 0))

        if p == 0:
            win.blit(w1, (20, 350))
            win.blit(t1, (150, 350))
            win.blit(l1, (270, 350))
        else:
            win.blit(w2, (20, 350))
            win.blit(t2, (150, 350))
            win.blit(l2, (270, 350))

        #This draws every button that is initialized in the window "win"
        for btn in btns:
            btn.draw(win)

    #Updates the pygame window after changes. 
    pygame.display.update()

#This btns is a list containing the instances of the class "Button" with the specific property of each button given as parameter
btns = [Button("Rock", 25, 300, (0, 0, 0)), Button("Paper", 150, 300, (255, 0, 0)), Button("Scissors", 275, 300, (0, 255, 0))]


#This function "main" is called once a player has entered the game and the main logic starts here.
def main():
    run = True
    clock = pygame.time.Clock()

    n = Network()
    player = int(n.getPlayer()) #gets the player from the server. This player is 0 for Player1 and is 1 for Player2
    print("You are Player ", player)

    #This stores the resutls of every game(for a particular player) that is played between two players. 
    #This stores the info as [wins, loses, ties] in a game.
    scores = [0, 0, 0]

    while run:
        clock.tick(60)
        try:
            game = n.send("get") #sends a request "get" to the server. Then the server returns a game using connection.sendall() method.
        except:
            run = False
            print("Couldn't get Game")
            break

        if game.bothGone():
            scoreUpdate(game, player, scores) #If both players have made their moves, calculate the score and update in the list "scores"
            redrawWindow(win, game, player, scores) #Redraw the updated window
            pygame.time.delay(500)

            try:
                game = n.send("reset") #This request is sent to get to the starting point of the game to start a new game.
            except:
                run = False
                print("Couldn't get game")
                break

            #Declaration of the results in the center of the window after a delay of 1s.
            font = pygame.font.SysFont("comicsans", 60)
            if (game.findWinner() == 1 and player == 1) or (game.findWinner() == 0 and player == 0):
                text = font.render("You Won!!!", 1, (0, 255, 0))
            elif game.findWinner() == -1:
                text = font.render("Game Tied", 1, (0, 0, 0))
            else:
                text = font.render("You Lost...", 1, (255, 0, 0))
            
            win.blit(text, (WIDTH/2 -text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(1000)    #delay of 1000ms


        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quits the pygame window if its been quitted.
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos() #gets the position of mouse-click
                for btn in btns:
                    if btn.click(pos) and game.isConnected(): #Checks if the mouse has clicked the button and if the game is connected
                        #If above condition is met, send the text of the button to the server to make the move of a player.
                        if player == 0:
                            if not game.p1Gone:  
                                n.send(btn.text) 
                        
                        else:
                            if not game.p2Gone:
                                n.send(btn.text)
        
        #redrawing the pygame window with the updated scores
        redrawWindow(win, game, player, scores) 


#This function Menu is a landing page on starting the client. The user is asked to click the window to enter the game.
def menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font1 = pygame.font.SysFont("comicsans", 40)
        text1 = font1.render("Rock Paper Scissors", 1, (0, 0, 0))
        text2 = font1.render("Game", 1, (0, 0, 0))
        win.blit(text1, (WIDTH/2 -text1.get_width()/2, HEIGHT/2 - text1.get_height()/2 - 100))
        win.blit(text2, (WIDTH/2 - text2.get_width()/2, HEIGHT/2 - text2.get_height()/2 - 50))

        font = pygame.font.SysFont("comicsans", 50)
        text = font.render("Click to Play!!!", 1, (255, 0, 0))
        win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2 + 50))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT: #quits pygame window if the event is quit.
                pygame.quit()
                run = False

            #If mouse button is pressed, the player is entered into a game or will be waiting for the opponent. Thus obtained "Click to play" feature
            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    #Once the player enters the game, start the game by calling the function main()
    main()


while True:  #this redirects to the menu-screen if the opponent quits the game.
    menu()                      


