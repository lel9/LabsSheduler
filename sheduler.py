import helpers as h
import os
import datetime

def create_project(redmine, config, lab):
    name = config['Redmine']['project_name_prefix'] + lab['num']
    description = lab['description']
    parent_id = config['Redmine']['project_parent_id']

    try:
        # берем родительский проект (нам нужен его id -- это число)
        parent_project = redmine.project.get(parent_id)

        # создаем проект лабы
        # в описании -- условие лабы
        project = redmine.project.create(
            name = name,
            identifier = name.lower(),
            description = description,
            parent_id = parent_project.id,
            is_public = False
        )

        # добавляем участников -- нашу группу
        redmine.project_membership.create(
            project_id = project.id,
            user_id = config['Redmine']['project_member_group_id'],
            role_ids = [config['Redmine']['project_member_role_id']]
        )

        # добавляем в проект доп. файлы с условием лабы
        for file in lab['files']:
            redmine.file.create(
                project_id = project.id,
                path = file,
                filename = os.path.basename(file)
            )
    except Exception as e:
        print(e)
        return 1, None
    return 0, project


def add_task_redmine(redmine, config, project, student, lab):
    if len(lab['vars']) > 0:
        vars = lab['vars'] * (int(len(student) / len(lab['vars'])) + 1) # вариантов м.б. меньше, чем студентов
    else:
        vars = []
    try:
        issue = redmine.issue.create(
            project_id = project.identifier,
            subject = config['Redmine']['issue_subject_prefix'] + lab['num'],
            tracker_id = config['Redmine']['issue_tracker_id'],
            description = config['Redmine']['issue_descr_prefix'] + vars[student['num']] if vars else '',
            assigned_to_id = student['redmine_id'],
            start_date = datetime.date.today(),
            due_date = datetime.date.today() + datetime.timedelta(days=lab['duration'])
        )
    except Exception as e:
        print(e)
        return 1, None
    return 0, issue


def shedule_lab(lab_num, duration):

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

    # читаем инфу о лабе (общее описание, доп.файлы, варианты)
    err_code, lab = h.get_lab(config, lab_num)
    if err_code != 0:
        print('Ошибка получения информации о лабораторной!')
        exit(err_code)
    else:
        print('Информация о лабораторной успешно прочитана...')
        #print(lab)
    lab['duration'] = duration # добавили срок в днях

    # содаем объект для работы с апи редмайна
    redmine = h.get_redmine(config)

    # создаем проект, один на каждую лабу, в описании проекта будет условие лабы
    # во вкладке файлов будут доп. файлы
    # внутри проекта будут задачи для каждого студента, в описании задачи -- вариант
    err_code, project = create_project(redmine, config, lab)
    if err_code != 0:
        print('Ошибка создания проекта в Redmine!')
        exit(err_code)
    else:
        print('Проект в Redmine успешно создан...')
        #print(project)

    # каждому студенту назначаем лабу
    for student in students:

        # добавляем задачу в редмайн
        err_code, issue = add_task_redmine(redmine, config, project, student, lab)
        if err_code != 0:
            print('Ошибка создания задачи в Redmine для студента с id=' + str(student['redmine_id']) + '!')
        else:
            print('Задача для студента с id=' + str(student['redmine_id']) + ' успешно добавлена...')
            # print(issue)

        # создаем проект в гитлабе
        # TODO

        # создаем канал в рокетчате
        # TODO