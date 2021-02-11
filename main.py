from threading import Thread
from VkAdapter import start_longpoll
from TestAdapter import start_longpoll as test_start_longpoll
import multiprocessing


def new_message(event):
    print(event)


def main():
    # t = Thread(target=start_longpoll(new_message), daemon=True)
    # t2 = Thread(target=test_start_longpoll(new_message), daemon=True)
    # t.start()
    # t2.start()
    p1 = multiprocessing.Process(target=start_longpoll, args=(new_message,))
    p2 = multiprocessing.Process(target=test_start_longpoll, args=(new_message,))
    p1.start()
    p2.start()
    command = input()
    print(command)
    p1.join()
    p2.join()



if __name__ == '__main__':
    main()
