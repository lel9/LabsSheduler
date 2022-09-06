import os
import datetime
import traceback


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
        traceback.print_exc()
        return 1, None
    return 0, project


def add_task_redmine(redmine, config, project, student, lab):
    try:
        issue = redmine.issue.create(
            project_id = project.identifier,
            subject = config['Redmine']['issue_subject_prefix'] + lab['num'],
            tracker_id = lab['tracker_id'],
            priority_id = config['Redmine']['issue_priority_id'],
            description = config['Redmine']['issue_descr_prefix'] + lab['vars'][student['num']] if lab['vars'] else '',
            assigned_to_id = student['redmine_id'],
            start_date = datetime.date.today(),
            due_date = datetime.date.today() + datetime.timedelta(days=lab['duration'])
        )
    except Exception as e:
        traceback.print_exc()
        return 1, None
    return 0, issue
