from django.shortcuts import render
import requests
from django.http import HttpResponse
import time

# Create your views here.
#   Возвращает список факультетов в формате json
#   С данными о наименованиях и коде факультетов
def get_faculties_data():
    resp = requests.get('http://mit-vs-t4.main.vsu.ru/attu_tst/hs/v1/faculty')
    faculties_data = resp.json()

    return faculties_data

#  Передаёт наименования факультетов в шаблон
def faculty_list(request):
    faculty_list = []
    for elem in get_faculties_data():
        faculty_list.append(elem['Наименование'])

    print(faculty_list)
    return render(request, 'sсhedule/faculty_list.html', context={'faculties':faculty_list})

#   Передаёт наименования групп в шаблон
def group_choise(request, faculty):
    faculty_code = ''
    for elem in get_faculties_data():
        if elem['Наименование'] == str(faculty):
            faculty_code = elem['Код']

    resp = requests.get('http://mit-vs-t4.main.vsu.ru/attu_tst/hs/v1/group/' + faculty_code)
    facutly_data = resp.json()
    group_list = []
    for elem in facutly_data:
        # print(elem)
        group_list.append(elem['Группа'])
    print(group_list)

    return render(request, 'schedule/group_list.html', context={'faculty': faculty, 'groups': group_list})


#   Передаёт в шаблон раписание определённой группы
def group_schedule(request, faculty, group):
    print(faculty)
    print(group)
    faculty_code = ''
    for elem in get_faculties_data():
        if elem['Наименование'] == str(faculty):
            faculty_code = elem['Код']

    resp = requests.get('http://mit-vs-t4.main.vsu.ru/attu_tst/hs/v1/group/' + faculty_code)
    facutly_data = resp.json()

    #   Получение id группы
    group_id = ''
    for elem in facutly_data:
        # print(elem)
        if elem['Группа'] == str(group):
            group_id = elem['Код']

    #   Получиение всех данных о расписании
    resp = requests.get('http://mit-vs-t4.main.vsu.ru/attu_tst/hs/v1/schedule/' + str(faculty_code) + '?groupID=' + str(group_id))
    schedule_data = resp.json()

    #   Сортировка данных
    day_number = []
    time_window = []
    type = []
    building = []
    subject = []
    room = []
    teacher = []

    for elem in schedule_data:
        day_number.append(elem['НомерДня'])
        time_window.append(elem['ВременноеОкно'])
        subject.append(elem['Дисциплина'])
        building.append(elem['Здание'])
        room.append(elem['Помещение'])
        teacher.append(elem['Преподаватель'])

    counter = range(len(day_number))
    return render(request, 'schedule/group_schedule.html', context={'day_number':day_number,'time_window':time_window,
                    'type':type, 'building':building, 'subject':subject, 'room':room, 'teacher': teacher, 'counter': counter})
