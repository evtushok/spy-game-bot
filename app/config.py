BOT_TOKEN = ""

MIN_PLAYERS = 3
MAX_PLAYERS = 10
DBG = "[DEBUG]"

MUSICIANS = [
    {"name": "Drake", "image": "images/musicians/drake.png"},
    {"name": "Travis Scott", "image": "images/musicians/travis.png"},
    {"name": "Kanye West", "image": "images/musicians/ye.png"}
]

FOOTBALLERS = [
    {"name": "Лионель Месси", "image": "images/footballers/messi.png"},
    {"name": "Криштиану Роналду", "image": "images/footballers/ronaldo.png"},
    {"name": "Неймар", "image": "images/footballers/neymar.png"}
]


BLOGGERS = [
    {"name": "IShowSpeed", "image": "images/bloggers/ishowspeed.png"},
    {"name": "Khaby Lame", "image": "images/bloggers/khaby.png"},
    {"name": "MrBeast", "image": "images/bloggers/mrbeast.png"}
]

CATEGORIES = {
    "music": {
        "label": "🎵 музыканты",
        "items": MUSICIANS
    },
    "football": {
        "label": "⚽ футболисты",
        "items": FOOTBALLERS
    },
    "bloggers": {
        "label": "🎥 блогеры",
        "items": BLOGGERS
    }
}
