import socket
from threading import Thread
from threading import Lock
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
lock = Lock()

def handleConnection(lock, con, p, gameId):
    with lock:
        global idCount
        con.send(str.encode(str(p)))
        reply = ""
        while True:
            try:
                data = con.recv(4096).decode()
                
                if gameId in games:
                    game = games[gameId]

                    if not data:
                        if lock.locked():
                            lock.release()
                        break
                    else:
                        if data == "reset":
                            game.resetGame()
                        elif data != "get":
                            game.play(p, data)

                        con.sendall(pickle.dumps(game))
                        if lock.locked():
                            lock.release()
                else:
                    if lock.locked():
                        lock.release()
                    break
            
            except:
                if lock.locked():
                    lock.release()
                break

        
        print("Lost Connection")

        try:
            del games[gameId]
            print("Closing Game", gameId)
        except:
            pass

        idCount -= 1

        if lock.locked():
            lock.release()
        con.close()

    
    
while True:
    con, addr = s.accept()
    print("Server is Connected to: ", addr)

    idCount += 1
    p = 0
    gameId = (idCount - 1) // 2

    if idCount % 2 == 1:
        games[gameId] = Game(gameId)
        print("Creating a new Game...")
        
    else:
        games[gameId].ready = True
        p = 1

        
    Thread(target = handleConnection, args = (lock, con, p, gameId)).start()
