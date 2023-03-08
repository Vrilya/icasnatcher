import telebot
import os

# Hämta den absoluta sökvägen till den aktuella katalogen
script_dir = os.path.dirname(os.path.realpath(__file__))

# Läs in bot-token från textfilen
with open(os.path.join(script_dir, "telegram_credentials.txt"), "r") as f:
    bot_token = f.readline().strip()

# Läs in SKU och pris från values.txt och skapa en dictionary
sku_dict = {}
with open(os.path.join(script_dir, "values.txt"), "r", encoding="utf-8") as f:
    for line in f:
        sku, price = line.strip().split("\t")
        sku_dict[sku.lower()] = price

product_dict = {}
with open(os.path.join(script_dir, "pages.txt"), "r", encoding="utf-8") as f:
    for line in f:
        url, sku, name = line.strip().split("\t")
        product_dict[sku.lower()] = {"name": name, "url": url}


# Skapa en bot med det inlästa bot-token
bot = telebot.TeleBot(bot_token)

# Definiera en funktion som svarar på meddelanden
@bot.message_handler(func=lambda message: message.chat.id == <KANAL-ID HÄR>)
def handle_message(message):
    sku = message.text.strip().lower()
    if sku in sku_dict:
        price = sku_dict[sku]
        product_info = product_dict.get(sku)
        if product_info:
            name = product_info["name"]
            url = product_info["url"]
            message_text = f"{name}\n{price}"
            bot.reply_to(message, message_text)
        else:
            bot.reply_to(message, "Tyvärr, hittade ingen produktinformation.")
    else:
        bot.reply_to(message, "Tyvärr, hittade ingen produkt med det nyckelordet.")

# Funktion som hämtar den senaste kommentaren och hanterar den om den matchar en SKU i sku_dict
def handle_latest_comment(chat_id):
    latest_message = bot.get_chat(chat_id).recent_message
    if latest_message and latest_message.text.strip().lower() in sku_dict:
        handle_message(latest_message)

# Starta en "polling" för att lyssna på inkommande meddelanden
bot.polling()

# Hantera den senaste kommentaren om den matchar en SKU i sku_dict
chat_id = <KANAL-ID här>  # Byt ut detta mot den chatt-id som du vill hämta senaste kommentaren från
handle_latest_comment(chat_id)
