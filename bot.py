from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from telegram import Update, Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import pickle

model = load_model('best_model.h5')


def predict_message(text):
    with open('tokenizer.pickle', 'rb') as handle:
        tokenizer = pickle.load(handle)
    sequence = tokenizer.texts_to_sequences([text])
    return model.predict(sequence)


def start(update: Update, context: CallbackContext):
    update.message.reply_text(text='Привет, давай пообщаемся?')


def help(update: Update, context: CallbackContext):
    update.message.reply_text(text='Мне нечем тебе помочь, извини(')


def echo(update: Update, context: CallbackContext):
    res = predict_message(update.message.text)
    if res[0][0] >= 0.5:
        ans ='Позитивное сообщение!\nточность = ' + str(res[0][0])
    else:
        ans ='Негативное сообщение!\nточность = ' + str(res[0][0])
    update.message.reply_text(text = ans)



def main():
    # привязываем token и создаём объект для работы бота
    updater = Updater("1989603124:AAGLtkds9Hn14eEGZq4ejZE_aMIJMuIAnek")
    dp = updater.dispatcher

    # добавляем два хэндлера для работы с двумя командами
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", help))

    # добавляем хэндлер для работы с текстовым сообщением
    dp.add_handler(MessageHandler(Filters.text, echo))

    # команда, с которой начинается работа бота
    updater.start_polling(drop_pending_updates=True)
    updater.idle()


if __name__ == '__main__':
    main()
