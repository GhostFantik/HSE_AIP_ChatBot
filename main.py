from BotLogic import message_handle
import db


def main():
    db.connect()
    s = ''
    while s != 'exit':
        s = input()
        print(message_handle('n', 'terminal', s))
    db.disconnect()


if __name__ == '__main__':
    main()
