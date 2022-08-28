import configparser, codecs
from redminelib import Redmine
from os import listdir
from os.path import isfile, join

def read_config():
    try:
        # загружаем настройки
        config = configparser.ConfigParser()  # создаём объекта парсера
        config.readfp(codecs.open("settings.ini", "r", "utf8")) # читаем конфиг

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
        if 'issue_subject_prefix' not in config['Redmine']:
            raise AttributeError('issue_subject_prefix not found')
        if 'issue_tracker_id' not in config['Redmine']:
            raise AttributeError('issue_tracker_id not found')
        if 'issue_descr_prefix' not in config['Redmine']:
            raise AttributeError('issue_descr_prefix not found')

        if 'Files' not in config:
            raise AttributeError('Files config not found')
        if 'students' not in config['Files']:
            raise AttributeError('students not found')
        if 'labs_dir' not in config['Files']:
            raise AttributeError('labs_dir not found')

    except AttributeError as ae:
        print('Config error: ')
        print(ae)
        return 1, ''
    except Exception as e:
        print('Unknown error')
        print(e)
        return 2, ''
    return 0, config

def get_redmine(config):
    return Redmine(config['Redmine']['redmine_host'],
             key = config['Redmine']['redmine_key'])

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
                    'gitlab_id': gl_id.strip(),
                    'eu_id': eu_id.strip()
            })
    except Exception as e:
        print(e)
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
        print(e)
        return 1, {}
    return 0, {'description': description,
               'num': lab_num,
               'files': addition_descr,
               'vars': vars}