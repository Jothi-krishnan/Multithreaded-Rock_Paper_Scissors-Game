from turtle import width
import pygame
import socket
import pickle
pygame.font.init()

class Network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "192.168.1.6"
        self.port = 5555
        self.addr = (self.server, self.port)
        self.p = self.connect()


    def getPlayer(self):
        return self.p

    def connect(self):
        try:
            self.client.connect(self.addr)
            return self.client.recv(2048).decode()

        except:
            pass
        

    def send(self, data):
        try:
            self.client.send(str.encode(data))
            return pickle.loads(self.client.recv(4096))

        except socket.error as e:
            print(e)


WIDTH =  700
HEIGHT = 700
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Client")


class Button:
    def __init__(self, text, x, y, color):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = 150
        self.height = 100

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont("comicsans", 40)
        text = font.render(self.text, 1, (255, 255, 255))
        win.blit(text, (self.x+round(self.width/2)-round(text.get_width()/2), self.y + round(self.height/2) - round(text.get_height()/2)))
    
    def click(self, pos):
        x1 = pos[0] 
        y1 = pos[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <=self.y + self.height:
            return True
        else:
            return False
    

def redrawWindow(win, game, p):
    win.fill((128, 128, 128))

    if not(game.isConnected()):
        font = pygame.font.SysFont("comicsans", 80)
        text = font.render("Waiting for player...", 1, (255, 0, 0), True)
        win.blit(text, (WIDTH/2 - text.get_width()/2, HEIGHT/2 - text.get_height()/2))
    
    else:
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Your Move", 1, (0, 255, 255))
        win.blit(text, (80, 200))

        text = font.render("Opponent's", 1, (0, 255, 255))
        win.blit(text, (380, 200))

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
        
        if p == 1:
            win.blit(text2, (100, 350))
            win.blit(text1, (400, 350))
        else:
            win.blit(text1, (100, 350))
            win.blit(text2, (400, 350))

        for btn in btns:
            btn.draw(win)

    pygame.display.update()


btns = [Button("Rock", 50, 500, (0, 0, 0)), Button("Paper", 250, 500, (255, 0, 0)), Button("Scissors", 450, 500, (0, 255, 0))]


def main():
    run = True
    clock = pygame.time.Clock()

    n = Network()
    player = int(n.getPlayer())
    print("You are Player ", player)

    while run:
        clock.tick(60)
        try:
            game = n.send("get")
        except:
            run = False
            print("Couldn't get Game")
            break

        if game.bothGone():
            redrawWindow(win, game, player)
            pygame.time.delay(500)

            try:
                game = n.send("reset")
            except:
                run = False
                print("Couldn't get game")
                break

            font = pygame.font.SysFont("comicsans", 90)
            if (game.findWinner() == 1 and player == 1) or (game.findWinner() == 0 and player == 0):
                text = font.render("You Won!!!", 1, (255, 0, 0))
            elif game.findWinner() == -1:
                text = font.render("Game Tied", 1, (255, 0, 0))
            else:
                text = font.render("You Lost..", 1, (255, 0, 0))
            
            win.blit(text, (WIDTH/2 -text.get_width()/2, HEIGHT/2 - text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(2000)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for btn in btns:
                    if btn.click(pos) and game.isConnected():
                        if player == 0:
                            if not game.p1Gone:
                                n.send(btn.text)
                        
                        else:
                            if not game.p2Gone:
                                n.send(btn.text)

        redrawWindow(win, game, player) 

def menu():
    run = True
    clock = pygame.time.Clock()

    while run:
        clock.tick(60)
        win.fill((128, 128, 128))
        font = pygame.font.SysFont("comicsans", 60)
        text = font.render("Click to Play!!!", 1, (255, 0, 0))
        win.blit(text, (100, 200))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                run = False

    main()


while True:
    menu()                      


