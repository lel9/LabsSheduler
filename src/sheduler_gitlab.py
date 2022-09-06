import traceback


def create_subgroup(gitlab, config, lab_num):
    try:
        subgroup = gitlab.groups.create({'name': config['Gitlab']['group_name_prefix'] + lab_num,
                                         'path': config['Gitlab']['group_name_prefix'] + lab_num,
                                         'parent_id': config['Gitlab']['group_parent_id']})
    except Exception as e:
        traceback.print_exc()
        return 1, None
    return 0, subgroup


def add_project_gitlab(gitlab, config, subgroup, student):
    try:
        # берем пользака
        user = gitlab.users.get(student['gitlab_id'])
        # создаем проект (репо)
        project = gitlab.projects.create({'name': student['stud_id'], 'namespace_id': subgroup.id})
        # наделяем пользака правами девелопера
        if 'project_access_expires_at' in config['Gitlab']:
            member = project.members.create({'user_id': user.id,
                                             'access_level': config['Gitlab']['project_access_level'],
                                             'expires_at': config['Gitlab']['project_access_expires_at']})
        else:
            member = project.members.create({'user_id': user.id,
                                             'access_level': config['Gitlab']['project_access_level']})
        # добавляем коммит, тк без него вообще ничего не работает
        data = {
            'branch': 'main',
            'commit_message': 'Initial commit',
            'actions': [
                {
                    'action': 'create',
                    'file_path': 'README.md',
                    'content': '',
                }
            ]
        }
        commit = project.commits.create(data)
        # добавляем метки в проект
        if 'project_labels' in config['Gitlab']:
            labels = config['Gitlab']['project_labels'].split(',')
            for label in labels:
                name_and_color = label.split(':')
                if len(name_and_color) == 2:
                    project.labels.create({'name': name_and_color[0], 'color': name_and_color[1]})

        # навешиваем веб-хук
        hook = project.hooks.create({'url': config['Gitlab']['hook_url'],
                                     'merge_requests_events': 1,
                                     'push_events': 0})
    except Exception as e:
        traceback.print_exc()
        return 1, None
    return 0, project
