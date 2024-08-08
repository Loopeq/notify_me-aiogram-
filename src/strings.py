import enum


class Languages(enum.Enum):
    RU = "ru"
    EN = "en"


strings = {
    "common": {
        "select_lang": "Select the language:"
    },
    Languages.RU.value: {
        "greeting": "создайте свой первый интервал✏️",
        "main": {
            "add": 'Добавить напоминание',
            "all": 'Запустить из списка',
            "stop_current": "Остановить текущее напоминание",
            "no_current": "Нет напоминаний в работе"
        },
        "add_not": "Введите интервал в минутах (или нажмите на клавиатуре):"
    },
    Languages.EN.value: {
        "greeting": "create your first interval✏️",
        "main": {
            "add": 'Add reminder',
            "all": 'Run from list',
            "stop_current": "Stop the current reminder",
            "no_current": "No reminders in operation"
        },
        "add_not": "Enter the interval in minutes (or press the keyboard):"
    }
}