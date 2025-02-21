from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from random import *
from time import *
from main_window import *
from menu_window import *

lb_time = QLabel()
btn_skip = QPushButton("Пропустити")

global timeLeft
timeLeft = sp_rest.value()


class Question():
    def __init__(self, question, answer, wrong_ans1, wrong_ans2, wrong_ans3):
        self.question = question
        self.wrong_ans1 = wrong_ans1
        self.wrong_ans2 = wrong_ans2
        self.wrong_ans3 = wrong_ans3
        self.answer = answer
        self.isAsking = True
        self.count_ask = 0
        self.count_right = 0
    
    def got_right(self):
        self.count_ask += 1
        self.count_right += 1
    
    def got_wrong(self):
        self.count_ask += 1

q1 = Question("Яблуко", "Apple", "Iphone", "Cock", "Accomodation")
q2 = Question("Підлога", "Floor", "Roof", "Door", "Beer")
q3 = Question("Ковер", "Rug", "Mug", "Fuck", "Suck")
q4 = Question("Вікно", "Window", "Linux", "MacOS", "Windows")

radio_buttons = [rb_ans1, rb_ans2, rb_ans3, rb_ans4]

questions = [q1, q2, q3, q4]

def new_question():
    global cur_q
    cur_q = choice(questions)
    lb_question.setText(cur_q.question)
    lb_right_answer.setText(cur_q.answer)
    shuffle(radio_buttons)
    radio_buttons[0].setText(cur_q.wrong_ans1)
    radio_buttons[1].setText(cur_q.wrong_ans2)
    radio_buttons[2].setText(cur_q.wrong_ans3)
    radio_buttons[3].setText(cur_q.answer)

new_question()

def check():
    RadioGroup.setExclusive(False)
    for answer in radio_buttons:
        if answer.isChecked():
            if answer.text() == lb_right_answer.text():
                cur_q.got_right()
                lb_result.setText('перемога (win)')
                answer.setChecked(False)
                break
    else:
        lb_result.setText('фу боже')
        cur_q.got_wrong()
    for answer in radio_buttons:
        answer.setChecked(False)
    RadioGroup.setExclusive(True)

def click_ok():
    if btn_next.text() == "Відповісти":
        check()
        gb_question.hide()
        gb_answer.show()
        btn_next.setText('Наступне запитання')

    else:
        new_question()
        gb_answer.hide()
        gb_question.show()
        btn_next.setText('Відповісти')

btn_next.clicked.connect(click_ok)

new_question()

def skip():
    gb_question.show()
    lb_question.show()
    btn_next.show()
    sp_rest.show()
    btn_rest.show()
    lb_rest.show()
    lb_time.hide()
    btn_skip.hide()

def rest():
    if sp_rest.value() != 0:
        global timeLeft
        timeLeft = sp_rest.value()
        gb_answer.hide()
        gb_question.hide()
        lb_question.hide()
        btn_next.hide()
        sp_rest.hide()
        btn_rest.hide()
        lb_rest.hide()

        if timeLeft < 60:
            lb_time.setText(f"Відпочинок: {timeLeft} хв")
        elif timeLeft == 60:
            lb_time.setText(f"Відпочинок: 1 год")
        elif timeLeft > 60:
            lb_time.setText(f"Відпочинок: {timeLeft // 60} год {timeLeft - 60} хв")

        h2_main.addWidget(lb_time, alignment=Qt.AlignCenter)
        h1_main.addWidget(btn_skip)
        lb_time.show()
        btn_skip.show()
        QTimer.singleShot(timeLeft * 60000, skip)
    else:
        pass

def openMenu():
    total_ask = sum(q.count_ask for q in questions)
    total_right = sum(q.count_right for q in questions)
    if cur_q.count_ask == 0:
        c = 0
    else:
        c = (total_right / total_ask) * 100
    text = f"Разів відповіли: {total_ask}" \
           f"Вірних відповідей: {total_right}" \
           f"Успішність: {round(c, 2)}%"
    lb_statistic.setText(text)
    menu_win.show()
    window.hide()

def back_menu():
    menu_win.hide()
    window.show()

def clear():
    le_question.clear()
    le_right_ans.clear()
    le_wrong_ans1.clear()
    le_wrong_ans2.clear()
    le_wrong_ans3.clear()

def add_question():
    new_q = Question(le_question.text(), le_right_ans.text(), le_wrong_ans1.text(), le_wrong_ans2.text(), le_wrong_ans3.text())
    questions.append(new_q)
    clear()

btn_add_question.clicked.connect(add_question)

btn_back.clicked.connect(back_menu)

btn_skip.clicked.connect(skip)

btn_clear.clicked.connect(clear)

btn_rest.clicked.connect(rest)

btn_menu.clicked.connect(openMenu)

window.show()

app.exec_()