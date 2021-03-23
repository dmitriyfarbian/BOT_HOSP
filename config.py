config_bot = '1572276926:AAG0yAnzeFLpQyl29YtujEpcrOWKfPG2TwQ'
db_file = 'database.vdb'

start_bot_message = r'Доброго дня! Для создания заявки нажмите'
helping_massage = 'Неверный формат входных данный'
success_message = 'Заявка отправлена! Спасибо!'


class States:
    St_START = '0'
    St_MO = '1'
    St_FIO = '2'
    St_AGE = '3'
    St_CONTACT = '4'
    St_EPICRISIS = '5'
    St_OUTPUT = '6'
