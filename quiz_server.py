import socket
from threading import Thread
import random

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip_address = '192.168.1.20'
port_number = 8000

server.bind((ip_address, port_number))
server.listen()
clients = []
nicknames = []
questions = ["What is the Italian word for PIE? \na.Mozarella\nb.Pasty\nc.Patty\nd.Pizza",
             "Which sea creature has three hearts? \na.Dolphin\nb.Octopus\nc.Walrus\nd.Seal"]
answers = ['d', 'b']


def clientthread(conn, nickname):
    score = 0
    conn.send("Welcome to this quiz game!".encode('utf-8'))
    conn.send("You'll will receive a question. The answer to that question should be one of a,b,c ord\n".encode('utf-8'))
    conn.send("Good Luck!\n\n".encode('utf-8'))
    index, question, answer = get_random_question_answer(conn)
    while True:
        try:
            message = conn.recv(2048).decode('utf-8')
            if message:
                if message.lower() == answer:
                    score += 1
                    conn.send("Right Answer! Your score: ",
                              score.encode('utf-8'))
                else:
                    conn.send("Incorrect Answer!".encode('utf-8'))
                    remove_questions(index)
                    index, question, answer = get_random_question_answer(conn)
            else:
                remove(conn)
                remove_nickname(nickname)
        except:
            continue


def remove(connection):
    if connection in clients:
        clients.remove(connection)


def remove_questions(i):
    questions.pop(i)
    answers.pop(i)


def remove_nickname(nickname):
    if nickname in nicknames:
        nickname.remove(nickname)


def get_random_question_answer(conn):
    index = random.randint(0, len(questions)-1)
    question = questions[index]
    answer = answers[index]
    conn.send(question.encode('utf-8'))
    return index, question, answer


while True:
    conn, addr = server.accept()
    conn.send('NICKNAME'.encode('utf-8'))
    nickname = conn.recv(2048).decode('utf-8')
    nicknames.append(nickname)
    clients.append(conn)
    print(nickname+" conncted!")
    new_thread = Thread(target=clientthread, args=(conn, nickname))
    new_thread.start()
