import telebot
import os
import sys

# Hämta den absoluta sökvägen till den aktuella katalogen
script_dir = os.path.dirname(os.path.realpath(__file__))

# Läs in bot-token från textfilen
with open(os.path.join(script_dir, "telegram_credentials.txt"), "r") as f:
    bot_token = f.readline().strip()

# Skapa en bot med det inlästa bot-token
bot = telebot.TeleBot(bot_token)

# Läs in data från values.txt
values = []
with open(os.path.join(script_dir, "values.txt"), "r", encoding="utf-8") as f:
    for line in f:
        values.append(line.strip().split("\t"))

# Läs in data från old_values.txt
old_values = []
with open(os.path.join(script_dir, "old_values.txt"), "r", encoding="utf-8") as f:
    for line in f:
        old_values.append(line.strip().split("\t"))

# Läs in data från pages.txt
products = []
with open(os.path.join(script_dir, "pages.txt"), "r", encoding="utf-8") as f:
    for line in f:
        fields = line.strip().split("\t")
        url = fields[0]
        sku = fields[1]
        name = fields[2]

        # Lägg till produkt i listan
        products.append({"sku": sku, "name": name})

# Skapa en boolean-variabel för att hålla reda på om ett meddelande har skickats
message_sent = False

# Jämför values och old_values och skicka meddelanden till Telegram om det har gjorts några ändringar
for value in values:
    sku = value[0]
    price = float(value[1].strip("kr").replace(",", "."))

    for old_value in old_values:
        old_sku = old_value[0]
        old_price = float(old_value[1].strip("kr").replace(",", "."))

        if sku == old_sku:
            # Hitta namnet för SKU
            try:
                product = next(product for product in products if product["sku"] == sku)
                name = product["name"]
            except StopIteration:
                name = ""
                pass

            if price > old_price:
                message = "!!! VARNING !!!\n" + name + " har ökat i pris!"
                message += "\n" + str(old_price) + " kr ---> " + str(price) + " kr"
                bot.send_message(<KANAL-ID HÄR>, message)  # byt ut <chat_id> mot en giltig chat-id
                message_sent = True
            elif price < old_price:
                message = "!!! LYSTRING !!!\n" + name + " har gått ned i pris!"
                message += "\n" + str(old_price) + " kr ---> " + str(price) + " kr"
                bot.send_message(<KANAL-ID HÄR>, message)  # byt ut <chat_id> mot en giltig chat-id
                message_sent = True

# Uppdatera old_values.txt med de aktuella värdena
with open(os.path.join(script_dir, "old_values.txt"), "w") as f:
    for value in values:
        f.write(value[0] + "\t" + value[1] + "\n")

# Kontrollera om ett meddelande har skickats. Om det har gjorts, avsluta skriptet
if message_sent:
    sys.exit()
else:
    print("Inga prisförändringar att rapportera.")
    sys.exit()
