def create_subgroup(gitlab, config, lab_num):
    try:
        subgroup = gitlab.groups.create({'name': config['Gitlab']['group_name_prefix'] + lab_num,
                                         'path': config['Gitlab']['group_name_prefix'] + lab_num,
                                         'parent_id': config['Gitlab']['group_parent_id']})
    except Exception as e:
        print(e)
        return 1, None
    return 0, subgroup


def add_project_gitlab(gitlab, config, subgroup, student):
    try:
        # берем пользака
        user = gitlab.users.list(username=student['gitlab_id'])[0]
        # создаем проект (репо)
        project = gitlab.projects.create({'name': student['stud_id'], 'namespace_id': subgroup.id})
        # наделяем пользака правами девелопера
        member = project.members.create({'user_id': user.id, 'access_level': 30})
        # навешиваем веб-хук
        hook = project.hooks.create({'url': config['Gitlab']['hook_url'],
                                     'merge_requests_events': 1,
                                     'push_events': 0})
    except Exception as e:
        print(e)
        return 1, None
    return 0, project
