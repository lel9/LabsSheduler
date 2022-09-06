import configparser, codecs
import traceback

from redminelib import Redmine
import gitlab
from os import listdir
from os.path import isfile, join


def read_config(path):
    try:
        # загружаем настройки
        config = configparser.ConfigParser()  # создаём объекта парсера
        config.readfp(codecs.open(path, "r", "utf8")) # читаем конфиг

        if 'Redmine' not in config:
            raise AttributeError('Redmine config not found')
        if 'redmine_host' not in config['Redmine']:
            raise AttributeError('redmine_host not found')
        if 'redmine_key' not in config['Redmine']:
            raise AttributeError('redmine_key not found')
        if 'project_name_prefix' not in config['Redmine']:
            raise AttributeError('project_name_prefix not found')
        if 'project_parent_id' not in config['Redmine']:
            raise AttributeError('project_parent_id not found')
        if 'project_member_group_id' not in config['Redmine']:
            raise AttributeError('project_member_group_id not found')
        if 'project_member_role_id' not in config['Redmine']:
            raise AttributeError('project_member_role_id not found')
        if 'issue_priority_id' not in config['Redmine']:
            raise AttributeError('issue_priority_id not found')
        if 'issue_subject_prefix' not in config['Redmine']:
            raise AttributeError('issue_subject_prefix not found')
        if 'issue_descr_prefix' not in config['Redmine']:
            raise AttributeError('issue_descr_prefix not found')

        if 'Gitlab' not in config:
            raise AttributeError('Gitlab config not found')
        if 'gitlab_host' not in config['Gitlab']:
            raise AttributeError('gitlab_host not found')
        if 'gitlab_token' not in config['Gitlab']:
            raise AttributeError('gitlab_token not found')
        if 'group_parent_id' not in config['Gitlab']:
            raise AttributeError('group_parent_id not found')
        if 'group_name_prefix' not in config['Gitlab']:
            raise AttributeError('group_name_prefix not found')
        if 'project_access_level' not in config['Gitlab']:
            raise AttributeError('project_access_level not found')
        if 'hook_url' not in config['Gitlab']:
            raise AttributeError('hook_url not found')

        if 'Files' not in config:
            raise AttributeError('Files config not found')
        if 'students' not in config['Files']:
            raise AttributeError('students not found')
        if 'labs_dir' not in config['Files']:
            raise AttributeError('labs_dir not found')

    except AttributeError as ae:
        print('Config error: ')
        print(ae)
        return 1, None
    except Exception as e:
        traceback.print_exc()
        return 2, None
    return 0, config


def get_redmine(config):
    try:
        return 0, Redmine(config['Redmine']['redmine_host'],
                          key = config['Redmine']['redmine_key'])
    except Exception as e:
        traceback.print_exc()
        return 1, None


def get_gitlab(config):
    try:
        # private token or personal token authentication (self-hosted GitLab instance)
        gl = gitlab.Gitlab(url=config['Gitlab']['gitlab_host'],
                           private_token=config['Gitlab']['gitlab_token'])

        # make an API request to create the gl.user object. This is not required but may be useful
        # to validate your token authentication. Note that this will not work with job tokens.
        gl.auth()
    except Exception as e:
        traceback.print_exc()
        return 1, None
    return 0, gl


def get_students(config):
    students = []
    file = config['Files']['students']
    try:
        with open(file) as f:
            f.readline() # пропускаем заголовок
            for count, line in enumerate(f.readlines()):
                stud_id, mail, tg_id, rc_id, rm_id, gl_id, eu_id = line.split('\t')
                students.append({
                    'num': count,
                    'stud_id': stud_id.strip(),
                    'telegram_id': tg_id.strip(),
                    'rocketchat_id': rc_id.strip(),
                    'redmine_id': int(rm_id.strip()),
                    'gitlab_id': int(gl_id.strip()),
                    'eu_id': eu_id.strip()
            })
    except Exception as e:
        traceback.print_exc()
        return 1, []
    return 0, students


def get_lab(config, lab_num):
    labs_dir = config['Files']['labs_dir']
    curr_lab_dir = labs_dir + '/' + lab_num
    curr_lab_descr_dir = curr_lab_dir + '/descr'
    try:
        # читаем условие лабы
        with open(curr_lab_descr_dir + '/description.txt', encoding='UTF-8') as f:
            description = f.read()
        # собираем доп.файлы
        addition_descr = []
        for f in listdir(curr_lab_descr_dir):
            if isfile(join(curr_lab_descr_dir, f)) and f != 'description.txt':
                addition_descr.append(curr_lab_descr_dir + '/' + f)
        # читаем варианты
        vars = []
        vars_file = curr_lab_dir + '/variants.txt'
        if isfile(vars_file):
            with open(vars_file, encoding='UTF-8') as f:
                for line in f.readlines():
                    vars.append(line.strip())
    except Exception as e:
        traceback.print_exc()
        return 1, {}
    return 0, {'description': description,
               'num': lab_num,
               'files': addition_descr,
               'vars': vars}