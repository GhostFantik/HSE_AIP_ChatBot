# HSE_AIP_ChatBot
Course work. 1 course. MIEM
# .ENV File
* DB = название базы данных (bot.db)
* FLASK_APP = server
* FLASK_ENV = development
* vk_token = токен Vk группы
* tg_token = токен Telegram
* server_message_url = http://server_url/message
# Запуск:
* Создадим виртуальное окружение VENV:
  >python -m venv venv
* Подключим виртуальное окружение
  - Linux:
    >source ./venv/Scripts/activate
  - Windows:
    >./venv/Scripts/activate
* Установим необходимые зависимости:
  >pip install -r ./requirements.txt
* Убедитесь, что файл .env создан и находится в корневой директории проекта
* Запустите сервер
  > flask run
* Запустите VkAdapter:
  > python ./VkAdapter.py
* Запустите TgAdapter.py
  > python ./TgAdapter.py
# Тестирование через терминал
  * Создайте виртуальное окружение и установите все зависимости из requirements.txt (см. Запуск)
  * Запустите main.py
    > python main.py
  * Для завершения работы напишите exit в терминал
# Логи
  * Логи расположены в файле logs.txt
