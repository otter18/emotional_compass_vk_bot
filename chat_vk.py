from pd import get_imgs, get_table, get_history, add_result
from pd import *
from random import shuffle
from vk_api.keyboard import VkKeyboardColor


class Chat:
    def __init__(self):

        self.url = ['start']
        self.data = ''
        self.now = 0
        self.sequence = []
        self.score = 0
        self.name = ''
        self.other = []
        self.bnt = None
        self.hint = 0

    def answer(self, message, user_id):

        if message == '📊 История игр':
            get_history(user_id)
            self.url = ['start']
            return 'Вот история твоих игр', [[{'txt': '⏪ Выход', 'color': VkKeyboardColor.SECONDARY}]], str(user_id)
        if self.url == ['start'] or message == '/start':

            self.__init__()
            self.name = get_user_name_from_vk_id(user_id)
            self.data = get_table()
            self.other = list(self.data['ans'])
            self.sequence = list(range(len(self.data['img'])))
            shuffle(self.sequence)
            self.url = ['main']
            return '👋Привет! Давай сыграем. Буду показывать эмоцию, а ты угадай, какую именно.', [[{'txt': '▶️ Начать игру', 'color': VkKeyboardColor.SECONDARY}], [{'txt': '📊 История игр', 'color': VkKeyboardColor.SECONDARY}]], None

        if self.url == ['set name']:
            self.url = ['set name', 'save']
            return '✏️Введите ваше имя (название команды)', [], None
        if message == "🚫 Закончить игру":
            self.url = ["start"]
            add_result(user_id, int(self.score / (len(self.sequence) * 3) * 100))
            return '📌 Твой результат: ' + str(int(self.score / (len(self.sequence) * 3) * 100)) + "%.", [[{'txt': '📊 История игр', 'color': VkKeyboardColor.SECONDARY}], [{'txt': '⏩ В главное меню', 'color': VkKeyboardColor.SECONDARY}]], None  # str(self.name) + ': ' + str(self.score) + ' из ' + str(len(self.sequence) * 3) + '(not fully)'
        if self.url == ['set name', 'save']:
            self.name = message
            self.url = ['main']
        if self.url == ['main', 'check']:
            if message == self.data['ans'][self.sequence[self.now]]:
                if self.now < len(self.sequence) - 1:
                    self.score += (3 - self.hint)
                    self.now += 1

                    bnt = []
                    temp = self.other[:]
                    temp.pop(temp.index(self.data['ans'][self.sequence[self.now]]))
                    shuffle(temp)

                    temp2 = [self.data['ans'][self.sequence[self.now]]] + temp[-3:]
                    shuffle(temp2)

                    for i in range(0, len(temp2) - 1, 2):
                        bnt += [[{'txt': str(temp2[i]), 'color': VkKeyboardColor.SECONDARY},
                                 {'txt': str(temp2[i + 1]), 'color': VkKeyboardColor.SECONDARY}]]
                    bnt += [[{'txt': '🚫 Закончить игру', 'color': VkKeyboardColor.SECONDARY}]]
                    self.bnt = bnt
                    self.url = ['main', 'check']
                    self.hint = 0
                    return '✅Правильно! ' + self.name + ", какую эмоцию испытывает человек на картинке❓", bnt, str(self.data['ans'][self.sequence[self.now]])
                self.score += 3 - self.hint
                self.url = ['start']
                add_result(user_id, int(self.score / (len(self.sequence) * 3) * 100))
                return '📌 Твой результат: ' + str(int(self.score / (len(self.sequence) * 3) * 100)) + "%.", [
                    [{'txt': '📊 История игр', 'color': VkKeyboardColor.SECONDARY}], [{'txt': '⏩ В главное меню',
                                                                                     'color': VkKeyboardColor.SECONDARY}]], None  # str(self.name) + ': ' + str(self.score) + ' из ' + str(len(self.sequence) * 3) + '(not fully)'

            else:
                if self.hint < 2:
                    self.url = ['main', 'check']

                    self.hint += 1
                    # shuffle(self.bnt)
                    for row in range(len(self.bnt)):
                        for button in range(len(self.bnt[row])):
                            if self.bnt[row][button]['txt'] == message:
                                self.bnt[row][button]['color'] = VkKeyboardColor.NEGATIVE
                    return '❌ Упс. Неправильно!\nПодсказка:\n' + str(self.data['help' + str(self.hint)][self.sequence[self.now]]), self.bnt, str(self.data['ans'][self.sequence[self.now]])
                bnt = []
                temp = self.other[:]
                temp.pop(temp.index(self.data['ans'][self.sequence[self.now]]))

                shuffle(temp)
                temp2 = [self.data['ans'][self.sequence[self.now]]] + temp[-3:]
                shuffle(temp2)
                for i in range(0, len(temp2) - 1, 2):
                    bnt += [[{'txt': str(temp2[i]), 'color': VkKeyboardColor.SECONDARY},
                             {'txt': str(temp2[i + 1]), 'color': VkKeyboardColor.SECONDARY}]]
                bnt += [[{'txt': '🚫 Закончить игру', 'color': VkKeyboardColor.SECONDARY}]]
                self.bnt = bnt
                self.url = ['main', 'check']
                self.hint = 0
                self.now += 1
                if self.now < len(self.sequence):
                    return '❌ Упс. Неправильно!\n' + str(self.now + 1) + ') ' + self.name + ", какую эмоцию испытывает человек на картинке❓", bnt, str(self.data['ans'][self.sequence[self.now]])
                self.url = ['start']
                add_result(user_id, int(self.score / (len(self.sequence) * 3) * 100))
                return '📌 Твой результат: ' + str(int(self.score / (len(self.sequence) * 3) * 100)) + "%.", [
                    [{'txt': '📊 История игр', 'color': VkKeyboardColor.SECONDARY}], [{'txt': '⏩ В главное меню',
                                                                                     'color': VkKeyboardColor.SECONDARY}]], None  # str(self.name) + ': ' + str(self.score) + ' из ' + str(len(self.sequence) * 3) + '(not fully)'

        if self.url == ['main']:
            bnt = []
            temp = self.other[:]
            temp.pop(temp.index(self.data['ans'][self.sequence[self.now]]))
            shuffle(temp)
            temp2 = [self.data['ans'][self.sequence[self.now]]] + temp[-3:]
            shuffle(temp2)
            for i in range(0, len(temp2) - 1, 2):
                bnt += [[{'txt': str(temp2[i]), 'color': VkKeyboardColor.SECONDARY},
                         {'txt': str(temp2[i + 1]), 'color': VkKeyboardColor.SECONDARY}]]
            bnt += [[{'txt': '🚫 Закончить игру', 'color': VkKeyboardColor.SECONDARY}]]
            self.bnt = bnt
            self.url = ['main', 'check']
            return str(self.now + 1) + ') ' + self.name + ", какую эмоцию испытывает человек на картинке❓", bnt, str(self.data['ans'][self.sequence[self.now]])






