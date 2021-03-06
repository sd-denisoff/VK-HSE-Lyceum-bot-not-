from config import *
from models import *
from actions import default_keyboard
from ElJurAPI.ElJurRequest import ElJurRequest
from ElJurAPI.AbstractState import AbstractState


class ScheduleState(AbstractState):
    def kind_of(self, id):
        keyboard = VkKeyboard(one_time=True)
        keyboard.add_button(label='Сегодня', color=VkKeyboardColor.DEFAULT, payload={'action': 'kind'})
        keyboard.add_button(label='Завтра', color=VkKeyboardColor.DEFAULT, payload={'action': 'kind'})
        keyboard.add_line()
        keyboard.add_button(label='Дата', color=VkKeyboardColor.DEFAULT, payload={'action': 'kind'})
        keyboard.add_button(label='На неделю', color=VkKeyboardColor.DEFAULT, payload={'action': 'kind'})
        vk.messages.send(user_id=id, message='Какое расписание Вам нужно?', keyboard=keyboard.get_keyboard())

    def get(self, id):
        user = User.get(User.id == id)
        r = ElJurRequest('/getschedule?auth_token=' + user.token + '&days=' + user.date)
        if not r.is_valid:
            vk.messages.send(user_id=id, message=r.query, keyboard=default_keyboard)
            return None
        if not r.query:
            vk.messages.send(user_id=id, message='Занятий в этот день нет! Ну, или же Вы указали некорректную дату',
                             keyboard=default_keyboard)
            return None
        schedule = r.query.get('students', {})
        schedule = schedule[user.eljur_id].get('days', {})
        return schedule

    def send(self, id, schedule):
        day_temp = '{title} ({date})\n'
        subj_temp = '{num}. {name} {room}\n'
        for day in sorted(schedule.keys(), key=lambda d: len(d)):
            date = '.'.join([day[6:], day[4:6], day[:4]])
            response = day_temp.format(title=schedule[day]['title'], date=date)
            subjects = schedule[day].get('items', {})
            for subj in sorted(subjects.keys(), key=lambda s: len(s)):
                response += subj_temp.format(num=subj, name=subjects[subj]['name'], room=subjects[subj].get('room', ''))
            vk.messages.send(user_id=id, message=response, keyboard=default_keyboard)
