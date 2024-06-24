import requests
import bs4
import telebot
from telebot import types
import pandas as pd

score = 0
idProduct = 0
resultInfo = ''
headers = {
    'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 '
                  'Safari/537.36 Edg/122.0.0.0'}

dataMacs = []
dataIphones = []
dataAirpods = []

bot = telebot.TeleBot('YOUR BOTFATHER GENERATED TOKEN')

urlMacs = "shop/mac"
urlIphones = "shop/iphone"
urlAirpods = "shop/airpods"
main_url = "https://ipiter.ru/"


# Парсинг страницы и запись данных в CSV файл
def get_soup(url_):
    res = requests.get(url_, headers)
    return bs4.BeautifulSoup(res.text, 'html.parser')


categories_page = get_soup(main_url + urlMacs)
categories = categories_page.findAll('div', class_='nokolvo')

for cat in categories:
    url = cat.find('a', class_='ajax')['href']
    price = cat.find('span', class_='price').text.strip()
    img = cat.find('div', class_='covers')
    style_value = img.get('style')
    img_url = f"https://ipiter.ru{style_value.split('(')[1].split(')')[0]}"

    dataMacs.append([main_url + url, price, img_url])

    score += 1
    if score == 20:
        break

categories_page = get_soup(main_url + urlIphones)
categories = categories_page.findAll('div', class_='nokolvo')

for cat in categories:
    url = cat.find('a', class_='ajax')['href']
    price = cat.find('span', class_='price').text.strip()
    img = cat.find('div', class_='covers')
    style_value = img.get('style')
    img_url = f"https://ipiter.ru{style_value.split('(')[1].split(')')[0]}"

    dataIphones.append([main_url + url, price, img_url])

    score += 1
    if score == 20:
        break

categories_page = get_soup(main_url + urlAirpods)
categories = categories_page.findAll('div', class_='nokolvo')

for cat in categories:
    url = cat.find('a', class_='ajax')['href']
    price = cat.find('span', class_='price').text.strip()
    img = cat.find('div', class_='covers')
    style_value = img.get('style')
    img_url = f"https://ipiter.ru{style_value.split('(')[1].split(')')[0]}"

    dataAirpods.append([main_url + url, price, img_url])

    score += 1
    if score == 20:
        break

df = pd.DataFrame(dataMacs)
df.to_csv(r'macs.csv', index=False)

df = pd.DataFrame(dataIphones)
df.to_csv(r'iphones.csv', index=False)

df = pd.DataFrame(dataAirpods)
df.to_csv(r'airpods.csv', index=False)

newMacs = pd.read_csv('macs.csv')
newIphones = pd.read_csv('iphones.csv')
newAirpods = pd.read_csv('airpods.csv')


# Настройка бота и интерфейса
@bot.message_handler(commands=['start'])
def main(message):
    markup = types.InlineKeyboardMarkup()
    markup2 = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn1 = types.InlineKeyboardButton('Маки', callback_data='macs')
    btn2 = types.InlineKeyboardButton('Айфоны', callback_data='iphones')
    btn3 = types.InlineKeyboardButton('Эйрподсы', callback_data='airpods')
    markup2.add(types.KeyboardButton('Настройки'))
    markup.row(btn1, btn2, btn3)
    bot.send_message(message.chat.id, 'Поиск по магазину Ipiter\nКакой гаджет хотите найти?', reply_markup=markup)


@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(call):
    if call.data == 'macs':
        i = 0
        j = 5
        while i < j:
            # Кнопки
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Кнопка ссылки', url=newMacs.iloc[i]['0']))
            # Фотография
            photo_response = requests.get(newMacs.iloc[i]['2'])
            photo_response.raise_for_status()
            # Сообщение с ссылкой
            bot.send_photo(call.message.chat.id, photo_response.content, f'Цена: {newMacs.iloc[i]["1"]}',
                           reply_markup=markup)
            i += 1

    elif call.data == 'iphones':
        i = 0
        j = 5
        while i < j:
            # Кнопки
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Кнопка ссылки', url=newIphones.iloc[i]['0']))
            # Фотография
            photo_response = requests.get(newIphones.iloc[i]['2'])
            photo_response.raise_for_status()
            # Сообщение с ссылкой
            bot.send_photo(call.message.chat.id, photo_response.content, f'Цена: {newIphones.iloc[i]["1"]}',
                           reply_markup=markup)
            i += 1

    elif call.data == 'airpods':
        i = 0
        j = 5
        while i < j:
            # Кнопки
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton('Кнопка ссылки', url=newAirpods.iloc[i]['0']))
            # Фотография
            photo_response = requests.get(newAirpods.iloc[i]['2'])
            photo_response.raise_for_status()
            # Сообщение с ссылкой
            bot.send_photo(call.message.chat.id, photo_response.content, f'Цена: {newAirpods.iloc[i]["1"]}',
                           reply_markup=markup)
            i += 1


if __name__ == '__main__':
    bot.polling(none_stop=True)
