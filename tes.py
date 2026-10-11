Import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton

# --- CONFIGURATION ---
TOKEN = "8962527584:AAHmESJgKKbNorU2x8fQr9DTp2rhRXFXxMs"  
bot = telebot.TeleBot(TOKEN)

# --- STYLE & CUSTOM EMOJI PATCH (InlineKeyboardButton) ---
_old_inline_dict = InlineKeyboardButton.to_dict
def _new_inline_dict(self):
    d = _old_inline_dict(self)
    style = getattr(self, 'style', None)
    if style:
        d['style'] = style
    emoji_id = getattr(self, 'icon_custom_emoji_id', None)
    if emoji_id:
        val = str(emoji_id).strip()
        if val:
            d['icon_custom_emoji_id'] = val
    return d
InlineKeyboardButton.to_dict = _new_inline_dict

# --- STYLE & CUSTOM EMOJI PATCH (KeyboardButton) ---
_old_reply_dict = KeyboardButton.to_dict
def _new_reply_dict(self):
    d = _old_reply_dict(self)
    style = getattr(self, 'style', None)
    if style:
        d['style'] = style
    emoji_id = getattr(self, 'icon_custom_emoji_id', None)
    if emoji_id:
        val = str(emoji_id).strip()
        if val:
            d['icon_custom_emoji_id'] = val
    return d
KeyboardButton.to_dict = _new_reply_dict

# Safe wrapper function with color support for Inline Buttons
def ibtn(text, callback_data=None, url=None, style=None, custom_emoji_id=None):
    kwargs = {'text': text}
    if callback_data: kwargs['callback_data'] = callback_data
    if url: kwargs['url'] = url

    b = InlineKeyboardButton(**kwargs)

    if style:
        try: b.style = style
        except AttributeError: pass

    emoji_val = str(custom_emoji_id).strip() if custom_emoji_id else None
    if emoji_val:
        try: b.icon_custom_emoji_id = emoji_val
        except AttributeError: pass

    return b

# Safe wrapper function with color support for Reply Buttons
def rbtn(text, style=None, custom_emoji_id=None):
    b = KeyboardButton(text=text)
    if style:
        try: b.style = style
        except AttributeError: pass
    emoji_val = str(custom_emoji_id).strip() if custom_emoji_id else None
    if emoji_val:
        try: b.icon_custom_emoji_id = emoji_val
        except AttributeError: pass
    return b

# Dummy load_data function to prevent NameError
def load_data():
    return {}


def get_main_menu(chat_id):
    data = load_data()
    texts = data.setdefault("texts", {})
    btn_get_number = texts.get("btn_get_number", "GET NUMBER")
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        rbtn(btn_get_number, style="success", custom_emoji_id="5251514997388897766"), 
        rbtn("Custom Number", style="danger", custom_emoji_id="5253737930727384427")  
    )
    markup.add(
        rbtn("PROFILE", style="primary", custom_emoji_id="5251671733630431622"),     
        rbtn("LEADERBOARD", style="success", custom_emoji_id="5282843764451195532")
    )
    return markup


# ============================================
# --- ADMIN PANEL & MAIN MENU HANDLER ---
# ============================================
@bot.message_handler(commands=['start', 'admin'])
def show_admin_panel(message):
    chat_id = message.chat.id
    
    text = (
        f"<b>RM-XEL BOT ADMIN PANEL</b>\n"
        f"Manage your bot with colored buttons.\n\n"
        f"<b>Status:</b> <code>Online 🚀</code>"
    )
    
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        ibtn("MANAGE SERVICES", callback_data="admin_services", style="primary", custom_emoji_id="5336814486701514414"), 
        ibtn("FORWARD GROUPS", callback_data="admin_groups", style="primary", custom_emoji_id="5337010556253543833")
    )
    markup.add(
        ibtn("RANG OTP GROUPS", callback_data="admin_rang_groups", style="danger", custom_emoji_id="5346042941196507141")
    )
    markup.add(
        ibtn("SEARCH USER DATA", callback_data="admin_search_user", style="success", custom_emoji_id="5335010201005231986"),  
        ibtn("MANAGE BALANCES", callback_data="admin_balance", style="success", custom_emoji_id="5348469219761626211")
    )
    markup.add(
        ibtn("BROADCAST", callback_data="admin_broadcast", style="primary", custom_emoji_id="5334807341109908955"), 
        ibtn("BAN / UNBAN USER", callback_data="admin_ban", style="danger", custom_emoji_id="5334868205091459431")
    )
    
    # Send main menu reply keyboard along with the admin message
    reply_markup = get_main_menu(chat_id)
    bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)
    bot.send_message(chat_id, "<b>Main Menu:</b>", parse_mode="HTML", reply_markup=reply_markup)

# --- HANDLER FOR GET NUMBER / SERVICES PAGING OR VIEW ---
@bot.message_handler(func=lambda message: message.text in ["GET NUMBER", "Custom Number"] or message.text == load_data().get("texts", {}).get("btn_get_number", "GET NUMBER"))
def show_services_menu(message):
    chat_id = message.chat.id
    text = "<b>Select a service below to proceed:</b>"
    
    markup = InlineKeyboardMarkup(row_width=2)
    for name, emoji_id, style in SERVICES_DATA:
        markup.add(ibtn(name, callback_data=f"srv_{name}", style=style, custom_emoji_id=emoji_id))
    
    bot.send_message(chat_id, text, parse_mode="HTML", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    if call.data.startswith("srv_"):
        service_name = call.data.replace("srv_", "")
        bot.answer_callback_query(call.id, f"Selected: {service_name}")
        bot.send_message(call.message.chat.id, f"You selected: <b>{service_name}</b>. Processing request...", parse_mode="HTML")
    else:
        bot.answer_callback_query(call.id, f"Action: {call.data}")

if __name__ == "__main__":
    print("Bot is running with colored buttons and all premium services integrated...")
    bot.infinity_polling()





