from aiogram import Bot, Dispatcher

Bot_token = '5933923237:AAEjRD4ZWRq-4tUD3OoUiIV-ojrswsm-xHA'
test_key = '-4160869434'
GROUP_ID = -1001580602852
ADMIN_ID = [313157090, 694086094,1185602840]
tab_names = ['DB_image1.txt','DB_image2.txt']

names = """Агапов Арсений Александрович
Бальва Илья Владиславович
Бедрышева Мария Сергеевна
Белов Леонид Сергеевич
Голубцов Артём Андреевич
Гончаров Владислав Романович
Губарев Артём Максимович
Жукова Софья Владиславовна
Иржанов Самир Амангельдыевич
Катков Евгений Иннокентьевич
Кащаева Анна Витальевна
Королева Виктория Алексеевна
Крутьков Алексей Ростиславович
Лазейкина Екатерина Андреевна
Максимович Анастасия Викторовна
Малявина Ева Евгеньевна
Манякин Илья Антонович
Марцынкьян Валентин Сергеевич
Миннегалиев Тимур Дамирович
Муравкин Егор Всеволодович
Мурьянов Георгий Александрович
Орлов Артемий Сергеевич
Поротников Алексей Александрович
Савичев Дмитрий Николаевич
Сайтаков Айдар Маратович
Сиваков Тимофей Юрьевич
Сорокин Владислав Таирович
Сысоев Михаил Витальевич
Ушков Андрей Валерьевич
Халил Тауфик Абдулла""".split("\n")




surnames = []
for name in names:
    surnames.append(name.split()[0])

bot = Bot(token=Bot_token)

