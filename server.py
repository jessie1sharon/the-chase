# wrote by : Jessica Llanos 327083183 & Margarita Kaplan 321775579
import socket
import random
from _thread import *
import threading

print_lock = threading.Lock()


# a func to sent data to the client
def connection_cl(item):
    global conn
    msg1 = str(item)
    conn.send(msg1.encode())


# a func to close the connection to the client
def disconnect():
    global thread_num
    conn.close()
    thread_num -= 1


# with how many money the client will start
class Bank:
    def __init__(self, start):
        self.amount = int(start)

    def double(self):
        self.amount = int(self.amount * 2)

    def half(self):
        self.amount = int(self.amount / 2)


# setting the board
class Board:

    def __init__(self):
        self.saving_wheel = int(1)
        self.place = []
        self.chaser_place = int(0)
        self.player_place = int(0)
        self.there_is_a_winner = int(0)
        self.bank_amount = int(0)
        self.place.append(str('                '))
        self.place.append(str('                '))
        self.place.append(str('                '))
        self.place.append(str('                '))
        self.place.append(str('                '))
        self.place.append(str('                '))
        self.place.append(str('                '))
        self.print_b = '   stages  | progress board \n' + '           |' + self.place[1] + '\n' + '     1     |' + \
                       self.place[1] + '\n' + '     2     |' + self.place[2] + '\n' + '     3     |' + self.place[
                           3] + '\n' + '     4     |' + self.place[4] + '\n' + '     5     |' + self.place[
                           5] + '\n' + '     6     |' + self.place[6] + '\n' + '     7     |     Bank       \n' + '\n'

    def end_game(self, winner):
        if winner == 'player':
            self.print_b = 'The winner is the Player\n'
            self.there_is_a_winner = 1
        if winner == 'chaser':
            self.print_b = 'The winner is the Chaser\n'
            self.there_is_a_winner = 1

    def using_saving_wheel(self):
        self.saving_wheel = self.saving_wheel - 1

    def player_place_change(self):
        if self.player_place + 1 == 7:
            self.end_game('player')
        else:
            self.place[self.player_place + 1] = self.place[self.player_place]
            self.place[self.player_place] = str('                ')
            self.player_place = self.player_place + 1
            self.update_board()

    def chaser_place_change(self):
        if self.chaser_place + 1 == self.player_place:
            self.end_game('chaser')
        else:
            self.place[self.chaser_place + 1] = self.place[self.chaser_place]
            self.place[self.chaser_place] = str('                ')
            self.chaser_place = self.chaser_place + 1
            self.update_board()

    def update_board(self):
        self.print_b = '   stages  | progress board \n' + '           |' + self.place[0] + '\n' + '     1     |' + \
                       self.place[1] + '\n' + '     2     |' + self.place[2] + '\n' + '     3     |' + self.place[
                           3] + '\n' + '     4     |' + self.place[4] + '\n' + '     5     |' + self.place[
                           5] + '\n' + '     6     |' + self.place[6] + '\n' + '     7     |     Bank       \n' + '\n'

    def print_board(self):
        if self.there_is_a_winner == 1:
            msg3 = self.print_b
        else:
            msg3 = self.print_b + 'player bank amount is : ' + str(self.bank_amount) + '  saving wheel :' + str(
                self.saving_wheel) + '\n\n'
        connection_cl(msg3)

    def option_choice_for_start(self, bank_amount):
        self.place[0] = str('     Chaser     ')
        self.place[2] = str('     ' + str(bank_amount * 2))
        self.place[3] = str('     ' + str(bank_amount))
        self.place[4] = str('     ' + str(int(bank_amount / 2)))
        self.update_board()
        self.bank_amount = bank_amount

    def option_choose(self, option):
        if option == 1:
            self.place[0] = str('     Chaser     ')
            self.place[2] = str('                ')
            self.place[3] = str('     Player     ')
            self.place[4] = str('                ')
            self.player_place = 3

        if option == 2:
            self.place[0] = str('     Chaser     ')
            self.place[2] = str('     Player     ')
            self.place[3] = str('                ')
            self.place[4] = str('                ')
            self.bank_amount = self.bank_amount * 2
            self.player_place = 2
        if option == 3:
            self.place[0] = str('     Chaser     ')
            self.place[2] = str('                ')
            self.place[3] = str('                ')
            self.place[4] = str('     Player     ')
            self.bank_amount = int(self.bank_amount / 2)
            self.player_place = 4

        self.update_board()


# setting the questions & correct answers & other answers
class Question:
    def __init__(self, qa, correct_answer, other_answer):
        self.qa = qa
        self.corranswer = correct_answer
        self.othanswer = other_answer
        self.othanswer_short = other_answer[0]


# all of the questions
questions = [Question("When did the website 'Facebook' launch?\n", "2004", ["2003", "2006", "2001"]),
             Question("What is the true color of coca-cola?\n", "Green", ["Yellow", "White", "Black"]),
             Question("What is the sum of all the numbers on a roulette wheel?\n", "666", ["999", "700", "696"]),
             Question("Which of the below is not a vegetable?\n", "Eggplant", ["Cucumber", "Carrot", "Broccoli"]),
             Question("Which of the following is the world's best-selling book?\n", "The Lord of the Rings",
                      ["Harry potter", "The Da Vinci Code", "The Hobbit"]),
             Question("Who directed 'E.T. the Extra-Terrestrial' (1982)?\n", "Steven Spielberg",
                      ["Martin Scorsese", "Quentin Tarantino", "David Lynch"]),
             Question("What is the oldest Disney film?\n", "Snow White and the Seven Dwarfs",
                      ["Pinocchio", "Dumbo", "Bambi"]),
             Question("What's the name of the river that runs through Egypt?\n", "The Nile",
                      ["The Tanitic", "The Bolbitinic", "The Sebennytic"]),
             Question("What's the highest mountain in the world?\n", "Mount Everest",
                      ["Makalu", "Lhotse", "Nanda Devi"]),
             Question("What year did World War || ended?\n", "1945", ["1948", "1991", "1942"]),
             Question("What sport did Fred Perry play?\n", "Tennis", ["Football", "Golf", "Volleyball"]),
             Question("What is the capital of Spain?\n", "Madrid", ["Barcelona", "Seville", "Malaga"]),
             Question("Who is the lead singer of Coldplay?\n", "Chris Martin",
                      ["Guy Berryman", "David Guetta", "Adam Levine"]),
             Question("What is the largest muscle in the body?\n", "Gluteus maximus",
                      ["The stapedius", "Masseter", "The heart"]),
             Question("Which actor or actress is killed off in the opening scene of the movie Scream?\n",
                      "Drew Barrymore", ["Courtney Cox", "Neve Campbell", "Rose McGowan"])]


# setting the chaser as requested
class Chaser:
    def chaser_answer(self, correct_answer_index):
        if random.uniform(0, 1) < 0.75:   # the Chaser has a 0.75 probability to answer right
            return correct_answer_index
        if correct_answer_index == 0:
            ans = [1, 2, 3]
            random.shuffle(ans)
            return ans[0]
        if correct_answer_index == 1:
            ans = [0, 2, 3]
            random.shuffle(ans)
            return ans[0]
        if correct_answer_index == 2:
            ans = [0, 1, 3]
            random.shuffle(ans)
            return ans[0]
        if correct_answer_index == 3:
            ans = [0, 1, 2]
            random.shuffle(ans)
            return ans[0]


def saving_wheel(q):
    global board_game
    board_game.using_saving_wheel()
    chaser_p = Chaser()
    correct_answer_index = int(0)
    k = int(0)
    item = q.qa  # item = a question
    connection_cl(item)  # printing the question
    possible = [q.othanswer_short] + [q.corranswer]
    random.shuffle(possible)  # randomize the options

    while k < 2:
        if possible[k] == q.corranswer:
            correct_answer_index = k
        k = k + 1

    count = 0  # list indexes start at 0
    while count < len(possible):  # printing the options for an answer
        p_print = str(count + 1) + ": " + possible[count] + '       '
        connection_cl(p_print)
        count += 1
    connection_cl('\n')
    ans = 'Please enter the number of your answer :'
    connection_cl(ans)
    msg1 = conn.recv(1024)  # receiving the answer of the client = msg1
    msg1 = int(msg1)
    while not (0 < msg1 <= len(possible)):  # if the answer is not in the range
        wrong = "That number doesn't correspond to any answer. Please enter the number of your answer:"
        connection_cl(wrong)
        msg1 = conn.recv(1024)
    if possible[msg1 - 1] == q.corranswer:  # if the client is correct
        corr = 'Yes ! You are correct :)'
        connection_cl(corr)
        board_game.player_place_change()
        if board_game.there_is_a_winner != 1:
            answer_ch = int(chaser_p.chaser_answer(correct_answer_index))
            if possible[answer_ch] == q.corranswer:
                board_game.chaser_place_change()

        board_game.print_board()
    else:  # if the client is wrong
        wro = 'Your answer was wrong :(\n'
        connection_cl(wro)
        answer_ch = int(chaser_p.chaser_answer(correct_answer_index))
        if possible[answer_ch] == q.corranswer:
            board_game.chaser_place_change()
        wro = "Correct answer was: " + q.corranswer + '\n'
        connection_cl(wro)
        board_game.print_board()


def play_game():
    global conn
    global board_game
    # get a question from the list of questions
    random.shuffle(questions)                        # randomize the questions
    chaser_p = Chaser()
    correct_answer_index = int(0)

    for q in questions:
        if board_game.there_is_a_winner == 1:
            break
        k = int(0)
        item = q.qa                                  # item = a question
        connection_cl(item)                          # printing the question
        possible = q.othanswer + [q.corranswer]
        random.shuffle(possible)                     # randomize the options

        while k < 4:
            if possible[k] == q.corranswer:
                correct_answer_index = k
            k = k + 1

        count = 0                                   # list indexes start at 0
        while count < len(possible):                # printing the options for an answer
            p_print = str(count + 1) + ": " + possible[count] + '       '
            connection_cl(p_print)
            count += 1
        connection_cl('\n')
        if board_game.saving_wheel > 0:
            ans = 'Please enter the number of your answer or H for saving wheel:'
        else:
            ans = 'Please enter the number of your answer:'
        connection_cl(ans)
        msg1 = conn.recv(1024)                     # receiving the answer of the client = msg1
        check_h = msg1.decode()           # ***********************
        if check_h == 'H':
            if board_game.saving_wheel > 0:
                saving_wheel(q)
            continue                               # skip to next question
        msg1 = int(msg1)
        while not (0 < msg1 <= len(possible)):     # if the answer is not in the range
            wrong = "That number doesn't correspond to any answer. Please enter the number of your answer:"
            connection_cl(wrong)
            msg1 = conn.recv(1024)
        if possible[msg1 - 1] == q.corranswer:     # if the client is correct
            corr = 'Yes ! You are correct :)'
            connection_cl(corr)
            board_game.player_place_change()
            if board_game.there_is_a_winner != 1:
                answer_ch = int(chaser_p.chaser_answer(correct_answer_index))
                if possible[answer_ch] == q.corranswer:
                    board_game.chaser_place_change()

            board_game.print_board()
        else:                                       # if the client is wrong
            wro = 'Your answer was wrong :(\n'
            connection_cl(wro)
            answer_ch = int(chaser_p.chaser_answer(correct_answer_index))
            if possible[answer_ch] == q.corranswer:
                board_game.chaser_place_change()
            wro = "Correct answer was: " + q.corranswer + '\n'
            connection_cl(wro)
            board_game.print_board()


# setting all we need for the game & playing the game
def begin_play(conn):
    global board_game
    # part 1 : answering 3 questions

    n0 = 3  # num of questions
    i = 0  # index for msg
    answer = []  # array of the answers
    correct = 0  # num of correct answers

    while n0 > 0:  # 3 first questions
        msg = ['How many strings do a guitar have?', 'How many colors a Rubics cube has?', 'Where is the Eiffel tower?']
        conn.send(msg[i].encode())
        msg = conn.recv(1024)  # print('answer: ' + msg.decode())
        answer.append(msg.decode())  # putting the answers in an array
        i += 1
        n0 -= 1

    if answer[0] == '6':  # counting the correct answers
        correct += 1
    if answer[1] == '6':
        correct += 1
    if answer[2] == 'paris':
        correct += 1

    if correct == 0:  # if the client failed all 3 start questions
        msg = 'failed : do you want to start again?'
        connection_cl(msg)
        msg = conn.recv(1024)
        answer.append(msg.decode())
        if answer[3].upper() == 'NO':
            print_lock.release()
            disconnect()  # close connection cuz the client failed
            return
        elif answer[3].upper() == 'YES':
            begin_play(conn)   # try again

    start1 = int(0)                       # the starting money

    if correct == 1:
        start1 = 5000

    if correct == 2:
        start1 = 10000

    if correct == 3:
        start1 = 15000

    playerbank = Bank(start1)            # setting the starting money
    msg = 'you have 3 choices where to start, with different amount of money in the bank for each choice\n' + '1 : start in stage 3 with the amount you earned\n' + '2 : start in stage 2 with double the amount you earned\n' + '3 : start in stage 4 with half the amount you earned'
    connection_cl(msg)
    board_game = Board()
    board_game.option_choice_for_start(playerbank.amount)     # the client decides if he want double or half the amount
    board_game.print_board()

    choice = conn.recv(1024)             # reciving the answer of the client = msg1
    choice = int(choice.decode())          # ***************

    board_game.option_choose(choice)     # sending the answer of the client to the func
    board_game.print_board()             # printing the board

    msg = 'The chase begins\n'           # sending that we are about to start the game
    connection_cl(msg)

    play_game()                          # playing the game
    connection_cl('The game is overrr\n')  # finished the game

    msg6 = 'Do you want to play again ?\n'    # if the client wants to play again
    connection_cl(msg6)
    msg6 = conn.recv(1024)
    answer.append(msg6.decode())
    if answer[3].upper() == 'NO':
        print_lock.release()
        disconnect()                        # disconnecting the client
    if answer[3].upper() == 'YES':
        answer = []
        begin_play(conn)  # try again


HOST = '127.0.0.1'
PORT = 7000
global board_game
if __name__ == '__main__':
    num_players = 3
    thread_num = 0
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)        # creating the socket
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))                                         # binding the socket
    try:
        while True:
            s.listen()
            conn, addr = s.accept()                              # accepting a client
            if thread_num == num_players:  # accepting a client (up to 3 clients that plays & the fourth is thrown out)
                msg5 = 'No can do , try again later please:) \n '
                connection_cl(msg5)
                print_lock.release()
                disconnect()                                     # disconnecting the client cuz he is the fourth
                continue
            thread_num += 1
            print("thread count : " + str(thread_num))           # just for us to see how many client do we have
            print_lock.acquire()
            start_new_thread(begin_play, (conn,))
        s.close()
    except OSError as error1:
        print(error1)
