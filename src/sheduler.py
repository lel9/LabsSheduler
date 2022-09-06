from sheduler_redmine import *
from sheduler_gitlab import *
import helpers as h


# mode = 1 -- только редмайн
# mode = 2 -- только гитлаб
# mode = 0 -- всё
def shedule_lab(lab_num, duration, tracker_id, mode, config):

    # читаем список студентов
    err_code, students = h.get_students(config)
    if err_code != 0:
        print('Ошибка получения списка студентов!')
        exit(err_code)
    else:
        print('Список студентов успешно прочитан...')
        #print(students)

    redmine_success = 0
    if mode == 0 or mode == 1:
        # читаем инфу о лабе (общее описание, доп.файлы, варианты)
        err_code, lab = h.get_lab(config, lab_num)
        if err_code != 0:
            print('Ошибка получения информации о лабораторной!')
        else:
            print('Информация о лабораторной успешно прочитана...')
            lab['duration'] = duration # добавили срок в днях
            lab['tracker_id'] = tracker_id # добавили трекер в Redmine
            if len(lab['vars']) > 0:
                lab['vars'] *= (int(len(students) / len(lab['vars'])) + 1)  # вариантов м.б. меньше, чем студентов

            # создаем объект для работы с апи редмайна
            err_code, redmine = h.get_redmine(config)
            if err_code != 0:
                print('Ошибка доступа к Redmine!')
            else:
                # создаем проект, один на каждую лабу, в описании проекта будет условие лабы
                # во вкладке файлов будут доп. файлы
                # внутри проекта будут задачи для каждого студента, в описании задачи -- вариант
                err_code, project_rm = create_project(redmine, config, lab)
                if err_code != 0:
                    print('Ошибка создания проекта в Redmine!')
                else:
                    redmine_success = 1
                    print('Проект в Redmine успешно создан...')

    gitlab_success = 0
    if mode == 0 or mode == 2:
        # создаем объект для работы с апи гитлаба
        err_code, gitlab = h.get_gitlab(config)
        if err_code != 0:
            print('Ошибка доступа к Gitlab!')
        else:
            # создаем подгруппу, одну на каждую лабу
            # внутри подгруппы будут репозитории для каждого студента
            err_code, subgroup = create_subgroup(gitlab, config, lab_num)
            if err_code != 0:
                print('Ошибка создания подгруппы в Gitlab!')
            else:
                gitlab_success = 1
                print('Подгруппа в Gitlab успешно создана...')

    # каждому студенту назначаем лабу
    for student in students:
        if redmine_success:
            # добавляем задачу в редмайн
            err_code, issue = add_task_redmine(redmine, config, project_rm, student, lab)
            if err_code != 0:
                print('Ошибка создания задачи в Redmine для студента с id=' +
                      str(student['redmine_id']) + '!')
            else:
                print('Задача для студента с id=' +
                      str(student['redmine_id']) + ' успешно добавлена...')

        if gitlab_success:
            # добавляем проект (репозиторий)
            err_code, project_gl = add_project_gitlab(gitlab, config, subgroup, student)
            if err_code != 0:
                print('Ошибка создания проекта (репозитория) Gitlab для студента с id=' +
                      str(student['gitlab_id']) + '!')
            else:
                print('Проект (репозиторий) для студента с id=' +
                      str(student['gitlab_id']) + ' успешно добавлен...')