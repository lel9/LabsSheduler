from sheduler_redmine import *
from sheduler_gitlab import *
import helpers as h

# mode = 1 -- только редмайн
# mode = 2 -- только гитлаб
# mode = 0 -- всё
def shedule_lab(lab_num, duration, mode):

    # читаем конфиги
    err_code, config = h.read_config()
    if err_code != 0:
        print('Ошибка чтения настроечного файла settings.ini!')
        exit(err_code)
    else:
        print('Настроечный файл успешно прочитан')
        #print(config)

    # читаем список студентов
    err_code, students = h.get_students(config)
    if err_code != 0:
        print('Ошибка получения списка студентов!')
        exit(err_code)
    else:
        print('Список студентов успешно прочитан...')
        #print(students)

    if mode == 0 or mode == 1:
        # читаем инфу о лабе (общее описание, доп.файлы, варианты)
        err_code, lab = h.get_lab(config, lab_num)
        if err_code != 0:
            print('Ошибка получения информации о лабораторной!')
            exit(err_code)
        else:
            print('Информация о лабораторной успешно прочитана...')
            #print(lab)
        lab['duration'] = duration # добавили срок в днях

        # создаем объект для работы с апи редмайна
        redmine = h.get_redmine(config)

        # создаем проект, один на каждую лабу, в описании проекта будет условие лабы
        # во вкладке файлов будут доп. файлы
        # внутри проекта будут задачи для каждого студента, в описании задачи -- вариант
        err_code, project_rm = create_project(redmine, config, lab)
        if err_code != 0:
            print('Ошибка создания проекта в Redmine!')
            exit(err_code)
        else:
            print('Проект в Redmine успешно создан...')
            #print(project)

    if mode == 0 or mode == 2:
        # создаем объект для работы с апи гитлаба
        gitlab = h.get_gitlab(config)

        # создаем подгруппу, одну на каждую лабу
        # внутри подгруппы будут репозитории для каждого студента
        err_code, subgroup = create_subgroup(gitlab, config, lab_num)
        if err_code != 0:
            print('Ошибка создания проекта в Gitlab!')
            exit(err_code)
        else:
            print('Проект в Gitlab успешно создан...')

    # каждому студенту назначаем лабу
    for student in students:
        if mode == 0 or mode == 1:
            # добавляем задачу в редмайн
            err_code, issue = add_task_redmine(redmine, config, project_rm, student, lab)
            if err_code != 0:
                print('Ошибка создания задачи в Redmine для студента с id=' + str(student['redmine_id']) + '!')
            else:
                print('Задача для студента с id=' + str(student['redmine_id']) + ' успешно добавлена...')
            # print(issue)

        if mode == 0 or mode == 2:
            # добавляем проект (репозиторий)
            err_code, project_gl = add_project_gitlab(gitlab, config, subgroup, student)
            if err_code != 0:
                print('Ошибка создания проекта (репо) Gitlab для студента с id=' + str(student['gitlab_id']) + '!')
            else:
                print('Проект (репо) для студента с id=' + str(student['gitlab_id']) + ' успешно добавлен...')
            # print(project_gl)