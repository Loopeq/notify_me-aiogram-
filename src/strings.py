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
        "not_list": {
            "add": 'Добавить напоминание',
            "all": 'Запустить из списка',
            "stop_current": "Остановить текущее напоминание",
            "no_current": "Нет напоминаний в работе"
        },
        "add_not": "Введите интервал в минутах (или нажмите на клавиатуре):",
        "add_not_expt": "Введите кол-во минут без дополнительных символов:",
        "add_not_interval": "Введите значение в пределе от 1мин до 500мин:",
        "add_not_ph": "Введите текст, который будет приходить в уведомлении:",
        "add_not_len_expt": "Ваше сообщение слишком длинное (>50 символов)",
        "not_ready": "Создано уведомление {} - {}m",
        'not_show': "Веберите нужное напоминание:",
        'no_in_run': "У вас не запущено ни одно напоминание.",
        'stop_not': "Напоминание [{}m - {}] остановлено."
    },
    Languages.EN.value: {
        "greeting": "create your first interval✏️",
        "not_list": {
            "add": 'Add reminder',
            "all": 'Run from list',
            "stop_current": "Stop the current reminder",
            "no_current": "No reminders in operation"
        },
        "add_not": "Enter the interval in minutes (or press the keyboard):",
        "add_not_expt": "Enter the number of minutes without any additional characters:",
        "add_not_interval": "Enter the value in the range from 1min to 500min:",
        "add_not_ph": "Enter the text that will be in the notification:",
        "add_not_len_expt": "Your message is too long (>50 characters)",
        "not_ready": "Created a notification {} - {}m",
        'not_show': "Capture the required reminder:",
        'no_in_run': "You have no reminders running.",
        'stop_not': "The [{}m - {}] reminder is stopped."
    }
}
