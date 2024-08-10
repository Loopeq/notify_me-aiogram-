import enum


class Languages(enum.Enum):
    RU = "ru"
    EN = "en"


strings = {
    "common": {
        "select_lang": "Select the language:",
        "stop_notification": 'Stop🛑'
    },
    Languages.RU.value: {
        "greeting": "создай свое первое напоминани ✏️, ",
        "add_not": "Введите интервал минут (или нажмите на клавиатуре):",
        "add_not_expt": "Введите кол-во минут без дополнительных символов:",
        "add_not_interval": "Введите значение в пределе от 1мин до 500мин:",
        "add_not_ph": "Введите текст, который будет приходить в уведомлении:",
        "add_not_len_expt": "Ваше сообщение слишком длинное (>50 символов)",
        "not_ready": "Создано уведомление {} - {}m",
        'not_show': "Веберите нужное напоминание:",
        'no_in_run': "У вас не запущено ни одно напоминание.",
        'stop_not': "Напоминание [{}m - {}] остановлено.",
        'cancel': "Отменить❌",
        'nothing_to_launch': "🧐 Запускать нечего, сначала создайте напоминание, ",
        'min_placeholder': 'Только число минут без доп. символов',
        'text_placeholder': 'Например: "Хватит работать!"',
    },
    Languages.EN.value: {
        "greeting": "create your first reminder✏️, ",
        "add_not": "Enter the interval of minutes (or press the keyboard):",        "add_not_expt": "Enter the number of minutes without any additional characters:",
        "add_not_interval": "Enter the value in the range from 1min to 500min:",
        "add_not_ph": "Enter the text that will be in the notification:",
        "add_not_len_expt": "Your message is too long (>50 characters)",
        "not_ready": "Created a notification {} - {}m",
        'not_show': "Capture the required reminder:",
        'no_in_run': "You have no reminders running.",
        'stop_not': "The [{}m - {}] reminder is stopped.",
        'cancel': "Cancel❌",
        'nothing_to_launch': "🧐 Nothing to run, first create a reminder, ",
        'min_placeholder': 'Only number of minutes without add. characters',
        'text_placeholder': 'For example: "Stop working!"',
    }
}


