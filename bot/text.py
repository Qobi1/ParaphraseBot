def dictionary(user=None, language=None, action=None):
    dict = {
        '🇺🇿Uzb': {
            'greeting': f"Assalomu alaykum {user}, botimizga xush kelibsiz",
            'button': ['Matini taxrirlash', 'Plagiatni tekshirish', 'Google tarjimon', 'Valyuta kursi', 'Lotin->Kiril / Kiril->Lotin', '⚙Sozlamalar'],
            'menu': "Menudan brini tanlang!",
            'lotinkiril': ["Lotindan Kirilchaga", "Kirildan Lotinchaga"],
            'text': "Tekstni yuboring",
            'exchange-rate': ["Sotib olish", "Sotish"],
            'url': "https://nbu.uz/uz/exchange-rates/json/",
            'wrong': "Noto'g'ri malumot kritildi! Qaytadan urinib ko'ring",
            'back': "⬅Orqaga",
            'paraphrase': "Paraphrase qlish uchun tekstni jo'nating(Inglis tilida)",
            'wait': "Iltimos kuting..."
        },
        '🇷🇺Rus': {
            'greeting': "",
            'button': "",
            'menu': "",
            'lotinkiril': "",
            'text': "",
            'exchange-rate': "",
            'url': "https://nbu.uz/exchange-rates/json/",
            'wrong': "",
            'back': "",
            'paraphrase': "",
            'wait': "",
        },
        '🇺🇸Eng': {
            'greeting': f"Good day {user}, welcome to our telegram bot",
            'button': ['Paraphrase text', 'Check Plagiarism', 'Google translator', 'Exchange Rate', 'Lotin->Kiril / Kiril->Lotin', '⚙Settings'],
            'menu': "Choose one of them",
            'lotinkiril': ['From Lotin to Kiril', 'From Kiril to Lotin'],
            'text': "Send your text",
            'exchange-rate': ['Buy', 'Sell'],
            'url': "https://nbu.uz/uz/exchange-rates/json/",
            'wrong': "Bad request! Try again",
            'back': "⬅Back",
            'paraphrase': "Here you can paraphrase your English text",
            'wait': "Please wait...",
        }
    }
    return dict[language][action]