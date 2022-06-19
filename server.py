import socket
from threading import Thread
from threading import Lock
import pickle
from gameLogic import Game

"""
The SERVER stores the IPv4 Address of your system. 
You have to update this line once you clone my github repository. 
To do this, open command prompt in windows and type "ipconfig" without the quotation marks or in ubuntu you can refer the Network settings.
Then copy and paste the IPv4 Address provided there in Line 13 of this file and also in line 18 of client.py file
"""
SERVER = "PASTE YOUR IPv4 ADDRESS HERE"
PORT = 5555

#initialization of socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    s.bind((SERVER, PORT))
except socket.error as e:
    str(e)

#The server listens for 2 connection 
s.listen(2)
print("Server Started...Waiting for Players to join..")

games = {}
idCount = 0
#initializing the Mutex Lock from the python library threading
lock = Lock()

def handleConnection(lock, con, p, gameId):
    #Mutex lock has been activated here..
    with lock:
        global idCount
        con.send(str.encode(str(p)))
        while True:
            try:
                #The server receives data from the client at every stage of the game using the socket's function recv() and is decoded 
                #with the function decode()
                data = con.recv(4096).decode()
                
                if gameId in games:
                    game = games[gameId]

                    if not data:
                        if lock.locked():
                            lock.release()
                        break
                    else:
                        if data == "reset":
                            #this request to reset the game to initial position to get the players' move again
                            game.resetGame()
                        elif data != "get":
                            #This makes sure that the move of each player is accounted.
                            #This function makes the move that is sent to the server as "data" by the client and updates p1Gone or p2Gone 
                            game.play(p, data)

                        #The changed instance "game" is then sent to client by the function sendall() and using pickle library
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
        """
        It can be seen above that, the block:
            if lock.locked():
                lock.release()

        is used many times within this function. This is because at each stage of the game, the current thread has to wait for the next thread. 
        As it contains the game of the other player. So it is important to release the Mutex Lock whenever required.
        """
        if lock.locked():
            lock.release()
        #The connection is closed when the game is stopped
        con.close()

    
    
while True:
    con, addr = s.accept()
    print("Server is Connected to: ", addr)

    idCount += 1
    p = 0
    #gameId stores the id for each game. It is unique for every two players.
    gameId = (idCount - 1) // 2

    if idCount % 2 == 1:
        #if idCount is an odd number, only one of 2 players have joined and is waiting for the opponent to join. 
        #This step also requires the creation of a new instance of Game with gameId as it's parameter
        games[gameId] = Game(gameId)
        print("Creating a new Game...")
        
    else:
        #if idCount is even, then the second player has arrived to the lobby.
        games[gameId].ready = True
        p = 1

    #A new thread is created for each player using the threading library.
    Thread(target = handleConnection, args = (lock, con, p, gameId)).start()
