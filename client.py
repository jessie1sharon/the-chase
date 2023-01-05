
import socket
global conn


def begin_play():
    maybe = []
    global conn
    n0 = 3

    while n0 > 0:                                 # phase 1 of the game
        msg1 = conn.recv(1024)
        print(msg1.decode())
        maybe.append(msg1.decode())               # if the first message is that we are the fourth client
        if maybe[0] == msg3:
            conn.close()
            quit()
        msg1 = input()
        conn.send(msg1.encode())
        n0 -= 1


try:
    HOST = '127.0.0.1'     # the IP & port of the server
    PORT = 7000
    conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    ADDR = HOST, PORT
    answer = []
    # maybe = []
    msg2 = 'failed : do you want to start again?'
    msg3 = 'No can do , try again later please:) \n '

    play = input("Do you want to play? ")       # the beginning of the game
    if play.upper() == 'NO':
        quit()
    elif play.upper() == 'YES':
        conn.connect(ADDR)

    begin_play()

    msg = conn.recv(1024)
    print(msg.decode())
    answer.append(msg.decode())

    if answer[0] == msg2:            # if the client failed all 3 questions
        msg = input()
        conn.send(msg.encode())
        if msg.upper() == 'NO':      # don't play again
            conn.close()
            quit()
        elif msg.upper() == 'YES':   # play again
            begin_play()

    while True:                       # phase 2 of the game
        msg4 = conn.recv(1024)
        print(msg4.decode())
        msg4 = input()
        conn.send(msg4.encode())
        if msg4.upper() == 'NO':      # after the has ended
            conn.close()
            quit()
        if msg4.upper() == 'YES':
            begin_play()

except OSError as error:
    print(error)
    conn.close()
    quit()
