from django.shortcuts import render
from telegram.ext import CallbackContext
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from .models import User
from .text import dictionary
import requests
from fake_useragent import UserAgent
# Create your views here.
from selenium import webdriver
from selenium.webdriver.common.by import By


def start(update: Update, context: CallbackContext):
    user = update.effective_user
    client = User.objects.filter(user_id=user.id).first()
    if client is None:
        update.message.reply_text("🇺🇸 - Choose the language\n🇷🇺 - Выберите язык\n🇺🇿 - Tilni tanlang", reply_markup=buttons(type='lang', user=user))
        User.objects.create(user_id=user.id, state=1, log={'menu': '', 'type': ''}).save()

    elif client is not None and client.language is not None:
        update.message.reply_text(dictionary(language=client.language, action='menu'), reply_markup=buttons(type='menu', user=user))
        client.state = 2
        client.save()

    elif client.language is None:
        print('eqw')
        update.message.reply_text("🇺🇸 - Choose the language\n🇷🇺 - Выберите язык\n🇺🇿 - Tilni tanlang", reply_markup=buttons(type='lang', user=user))


def message_handler(update: Update, context: CallbackContext):
    user = update.effective_user
    msg = update.message.text

    client = User.objects.filter(user_id=user.id).first()
    try:
        if msg == dictionary(language=client.language, action='back'):
            client.state -= 2
            client.save()
    except:
        pass

    if client.state == 1 and msg in ['🇺🇿Uzb', '🇷🇺Rus', '🇺🇸Eng', '⬅Orqaga', '⬅Back']:
        if msg not in ['⬅Orqaga', '⬅Back']:
            client.language = msg
        client.state = 2
        client.save()
        update.message.reply_text(dictionary(user=user.first_name, language=client.language, action='greeting'))
        update.message.reply_text(dictionary(language=client.language, action='menu'), reply_markup=buttons(type='menu', user=user))
    elif client.state == 1 and msg not in ['🇺🇿Uzb', '🇷🇺Rus', '🇺🇸Eng']:
        update.message.reply_text("Error🚫", reply_markup=buttons(type='lang', user=user))
    elif client.state == 2 and msg == dictionary(language=client.language, action='button')[0]:# Matini taxrirlash
        update.message.reply_text(dictionary(language=client.language, action='paraphrase'))
        update.message.reply_text(dictionary(language=client.language, action='text'), reply_markup=buttons(type='back', user=user))
        client.state = 3
        client.log['menu'] = 'paraphrase'
    elif client.state == 2 and msg == dictionary(language=client.language, action='button')[1]:# Plagiatni tekshirish
        update.message.reply_text("Coming soon....")
    elif client.state == 2 and msg == dictionary(language=client.language, action='button')[2]:# Google tarjimon
        update.message.reply_text("Coming soon....")
    elif client.state == 2 and msg == dictionary(language=client.language, action='button')[3]:# Valyuta kursi
        url = dictionary(language=client.language, action='url')
        buy = ""
        sell = ""
        for i in requests.get(url).json():
            if i['nbu_buy_price'] != '':
                buy += f"1 {i['title']} = {i['nbu_buy_price']} so'm\n"
        for i in requests.get(url).json():
            if i['nbu_buy_price'] != '':
                sell += f"1 {i['title']} = {i['nbu_cell_price']} so'm\n"
        update.message.reply_text(f"<b>CBU bank</b>\n\n<i>{dictionary(language=client.language, action='exchange-rate')[0]}</i>\n\n{buy}\n<i>{dictionary(language=client.language, action='exchange-rate')[1]}</i>\n\n{sell}", parse_mode='HTML')
    elif client.state == 2 and msg == dictionary(language=client.language, action='button')[4] or msg in dictionary(language=client.language, action='back'):# Lotin Kiril
        update.message.reply_text(dictionary(language=client.language, action='menu'), reply_markup=buttons(type='lotinkiril', user=user))
        client.log['menu'] = 'lotinkiril'
        client.state = 3
    elif client.state == 2 and msg == dictionary(language=client.language, action='button')[5]:# Sozlamalar
        update.message.reply_text("🇺🇸 - Choose the language\n🇷🇺 - Выберите язык\n🇺🇿 - Tilni tanlang", reply_markup=buttons(type='lang', user=user))
        client.language = msg
        client.state = 1
    elif client.state == 3 and client.log['menu'] == 'lotinkiril' and (msg in dictionary(language=client.language, action='lotinkiril') or msg in dictionary(language=client.language, action='back')):
        update.message.reply_text(dictionary(language=client.language, action='text'), reply_markup=buttons(type='back', user=user))
        client.log['type'] = msg
        client.state = 4
    elif client.state == 3 and client.log['menu'] == 'lotinkiril' and msg not in dictionary(language=client.language, action='lotinkiril'):
        update.message.reply_text(dictionary(language=client.language, action='wrong'), reply_markup=buttons(type='lotinkiril', user=user))
    elif client.state == 4:
        update.message.reply_text(lotin_kiril(msg, client.log['type']), reply_markup=buttons(type='back', user=user))
    elif client.state == 3 and client.log['menu'] == 'paraphrase' and msg not in dictionary(language=client.language, action='menu'):
        update.message.reply_text(dictionary(language=client.language, action='wait'), reply_to_message_id=update.message.message_id)
        update.message.reply_text(f"<b>Result</b>\n\n{text_parapharaser(msg)}", parse_mode="HTML", reply_to_message_id=update.message.message_id, reply_markup=buttons(type='back', user=user))
    client.save()


def buttons(type=None, user=None):
    btn = []
    client = User.objects.filter(user_id=user.id).first()
    if type == "menu":
        for i in range(0, len(dictionary(language=client.language, action='button')), 2):
            btn.append([KeyboardButton(dictionary(language=client.language, action='button')[i]), KeyboardButton(dictionary(language=client.language, action='button')[i + 1])])
        if len(dictionary(language=client.language, action='button')) % 2 != 0:
            btn.append([KeyboardButton(dictionary(language=client.language, action='button')[-1])])
    elif type == 'lang':
        btn = [[KeyboardButton("🇺🇸Eng"), KeyboardButton("🇷🇺Rus")], [KeyboardButton("🇺🇿Uzb")]]
    elif type == 'lotinkiril':
        for i in dictionary(language=client.language, action='lotinkiril'):
            btn.append([KeyboardButton(i)])
        btn.append([KeyboardButton(dictionary(language=client.language, action='back'))])
    elif type == 'back':
        btn.append([KeyboardButton(dictionary(language=client.language, action='back'))])
    return ReplyKeyboardMarkup(btn, resize_keyboard=True)


def lotin_kiril(sentence, action=None):
    uzb_letter = {
        'A': 'А',
        'B': 'Б',
        'D': 'Д',
        'E': 'Е',
        'F': 'Ф',
        'G': 'Г',
        'H': 'Х',
        'I': 'И',
        'J': 'Ж',
        'K': 'К',
        'L': 'Л',
        'M': 'М',
        'N': 'Н',
        'O': 'О',
        'P': 'П',
        'Q': 'Қ',
        'R': 'Р',
        'S': 'С',
        'T': 'Т',
        'U': 'У',
        'V': 'В',
        'X': 'Х',
        'Y': 'Й',
        'Z': 'З',
        "Ch": 'Ч',
        "Sh": 'Ш',
        "O'": 'О',
        "G'": 'Г',
        "W": 'Ш',
        'a': 'а',
        'b': 'б',
        'd': 'д',
        'e': 'е',
        'f': 'ф',
        'g': 'г',
        'h': 'х',
        'i': 'и',
        'j': 'ж',
        'k': 'к',
        'l': 'л',
        'm': 'м',
        'n': 'н',
        'o': 'о',
        'p': 'п',
        'q': 'қ',
        'r': 'р',
        's': 'с',
        't': 'т',
        'u': 'у',
        'v': 'в',
        'x': 'х',
        'y': 'й',
        'z': 'з',
        "o'": 'о',
        "g'": 'г',
        "w": 'ш',
        "ch": 'ч',
        "sh": 'ш',
        "'": "",
        ' ': ' '
    }
    rus_letter = {
        "А": "A",
        "Б": "B",
        "В": "V",
        "Г": "G",
        "Д": "D",
        "Е": "E",
        "Ё": "Yo",
        "Ж": "J",
        "З": "Z",
        "И": "I",
        "Й": "Y",
        "К": "K",
        "Л": "L",
        "М": "M",
        "Н": "N",
        "О": "O",
        "П": "P",
        "Р": "R",
        "С": "S",
        "Т": "T",
        "У": "U",
        "Ф": "F",
        "Х": "X",
        "Ц": "S",
        "Ч": "Ch",
        "Ш": "Sh",
        "Щ": "Sh",
        "Ъ": "",
        "Ы": "",
        "Ь": "I",
        "Э": "E",
        "Ю": "Yu",
        "Я": "Ya",
        "Қ": "Q",
        "қ": "q",
        "а": "a",
        "б": "b",
        "в": "v",
        "г": "g",
        "д": "d",
        "е": "e",
        "ё": "yo",
        "ж": "j",
        "з": "z",
        "и": "i",
        "й": "y",
        "к": "k",
        "л": "l",
        "м": "m",
        "н": "n",
        "о": "o",
        "п": "p",
        "р": "r",
        "с": "s",
        "т": "t",
        "у": "u",
        "ф": "f",
        "х": "x",
        "ц": "s",
        "ч": "ch",
        "ш": "sh",
        "щ": "sh",
        "ъ": "",
        "ы": "i",
        "ь": "",
        "э": "e",
        "ю": "yu",
        "я": "ya",
    }
    reply = ""
    changes = ['c', 'C', 's', 'S']
    if action in ['Lotindan Kirilchaga', 'From Lotin to Kiril']:
        try:
            for i in range(0, len(sentence)):
                if sentence[i] in changes and (sentence[i + 1] == 'h' or sentence[i + 1] == 'H'):
                    reply += uzb_letter[sentence[i] + sentence[i + 1]]
                elif (sentence[i] == 'h' or sentence[i] == 'H') and sentence[i - 1] in changes:
                    pass
                elif sentence[i] in uzb_letter.keys():
                    reply += uzb_letter[sentence[i]]
                elif sentence[i] not in uzb_letter.keys():
                    reply += sentence[i]
        except Exception as e:
            print(e)
    elif action in ['Kirildan Lotinchaga', 'From Kiril to Lotin']:
        try:
            for i in range(0, len(sentence)):
                if sentence[i] in rus_letter.keys():
                    reply += rus_letter[sentence[i]]
                elif sentence[i] not in rus_letter.keys():
                    reply += sentence[i]
        except Exception as e:
            print(e)
    return reply


def text_parapharaser(sentence):
    url = 'https://www.paraphrase-online.com/'
    useragent = UserAgent()
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    options.add_argument(f'user-agent={useragent.random}')
    # options.add_argument("--proxy-server=138.128.91.65:8000")
    driver = webdriver.Chrome(executable_path="chromedriver\\chromedriver.exe",
                              options=options)
    output = 'Error'
    try:
        driver.get(url=url)
        # time.sleep(1)
        text = driver.find_element(By.ID, 'field1')
        text.send_keys(sentence)
        # time.sleep(1)
        driver.find_element(By.ID, 'synonym').click()
        # time.sleep(1)
        output = driver.find_element(By.ID, "field2").text
    except Exception as e:
        print(e)
    finally:
        driver.close()
        driver.quit()
    return output
