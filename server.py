import socket
from _thread import *
import pickle
from gameLogic import Game

SERVER = "192.168.1.6"
PORT = 5555

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER, PORT))
except socket.error as e:
    str(e)


s.listen(2)
print("Server Started...Waiting for Players to join..")

connected = set()
games = {}
idCount = 0


def handleConnection(con, p, gameId):
    global idCount
    con.send(str.encode(str(p)))

    reply = ""
    while True:
        try:
            data = con.recv(4096).decode()
            
            if gameId in games:
                game = games[gameId]

                if not data:
                    break
                else:
                    if data == "reset":
                        game.restGame()
                    elif data != "get":
                        game.play(p, data)

                    con.sendall(pickle.dump(game))
            else:
                break
        
        except:
            break

    
    print("Lost Connection")

    try:
        del games[gameId]
        print("Closing Game", gameId)
    except:
        pass

    idCount = -1
    con.close()

    
    
while True:
    con, addr = s.accept()
    print("Server is Connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount-1)//2

    if idCount%2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a New Game")
        
    else:
        games[gameId].ready = True
        p = 1

        
    start_new_thread(handleConnection, (con, p, gameId))
