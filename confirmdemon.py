import sqlite3
from telegram import Bot
from bot import TOKEN
# Создаем объект бота
bot = Bot(token=TOKEN)

# Открываем соединение с базой данных
conn = sqlite3.connect('debptDB.db')

# Получаем объект-курсор для выполнения запросов к базе данных
cur = conn.cursor()

# Определяем функцию-обработчик для проверки записей в базе данных
def check_records():
    # Выполняем запрос к базе данных для получения записей с флагом "false"
    cur.execute('select * from debt_record where confirmation=0;')
    rows = cur.fetchall()
    
    # Если есть записи с флагом "false", отправляем сообщение пользователю
    if rows:
        for row in rows:
            user_id = row[1]  # Получаем ID пользователя
            message = 'Запись с ID {} помечена как "false".'.format(row[0])
            bot.send_message(chat_id=user_id, text=message)
    
    # Устанавливаем задержку и вызываем функцию-обработчик снова
    # через определенное время (например, 10 секунд)
    check_records()

# Запускаем функцию-обработчик
check_records()