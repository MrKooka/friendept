
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import db
import datetime
import pytz


# Устанавливаем нужный часовой пояс
tz = pytz.timezone('America/Los_Angeles')
# Получаем текущую дату и время
now = datetime.datetime.now(tz)
# Преобразуем дату и время в строку с нужным форматом

TOKEN = "5852161421:AAHYOyVfbG5HwskQ0QMO5bBadsXs93KA_MU"


def make_reply_markup(last_row_id: int):
    button1 = InlineKeyboardButton('Подтвердить', callback_data=f'approve:{last_row_id}')
    button2 = InlineKeyboardButton('Отклонить', callback_data=f'decline:{last_row_id}')
    keyboard = [[button1, button2]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup


async def users(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    users = db.users()
    users = ",\n".join([item[0] for item in users])
    await update.message.reply_text(users)
    
    
async def confirm_debt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    # CallbackQueries need to be answered, even if no notification to the user is needed
    # Some clients may have trouble otherwise. See https://core.telegram.org/bots/api#callbackquery

    query = update.callback_query
    print(query.data)
    status, last_row_id = query.data.split(":")
    if status == 'approve':
        db.set_confirmation_status(last_row_id)
        await query.answer()
        await query.edit_message_text(text=f"Подтверждено ✅")
    else:
        await query.answer()
        await query.edit_message_text(text=f"Отклонено ❌")


    
async def debt(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    try:
        
        data = {
            "debtor": context.args[0].lower(),
            "creditor": context.args[1].lower(),
            "amount": context.args[2],
            "comment": ' '.join(context.args[3:])
        }
        if db.check_user_exist(data['creditor']):
            creditor_obj = db.check_user_exist(data['creditor'])
            data['creditor'] = creditor_obj.id
            print("creditor_obj => ", creditor_obj.tgId)
            
        else: 
            await update.message.reply_text(f'Пользователя с ником {data["creditor"]} нет в базе')
        
        if db.check_user_exist(data['debtor']):
            debtor_obj = db.check_user_exist(data['debtor'])
            print("debtor_obj => ", debtor_obj.tgId)
            data['debtor'] = debtor_obj.id
            
        else: 
            await update.message.reply_text(f'Пользователя с ником {data["debtor"]} нет в базе')

        data['author'] = update.message.from_user.first_name
        data['datetime'] = now.strftime('%Y-%m-%d %H:%M:%S %Z')
        data['author_id'] = update.message.chat_id
        # print(update.message.chat_id)
        print(data)
        
        last_inserted_row: db.DebtRow = db.insert_debt(data)
        reply_markup = make_reply_markup(last_inserted_row.id)
        await context.bot.send_message(
            chat_id=creditor_obj.tgId, 
            text=f'Долг => {last_inserted_row.author}  {last_inserted_row.amount}\nКомментарий: {last_inserted_row.comment}', 
            reply_markup=reply_markup
        )

    except ValueError:
        await update.message.reply_text(f'Неправильно!!: должник, кому должен, сколько, комментарий')



app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("debt", debt))
app.add_handler(CommandHandler("users", users))
app.add_handler(CallbackQueryHandler(confirm_debt))

app.run_polling()
