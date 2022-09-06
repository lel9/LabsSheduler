import sheduler as sh
import argparse
import helpers as h

# параметры:
# - номер лабы (обязательный)
# - длительность (необязательный)
# - id трекера в redmine
# - режим (1 -- только редмайн, 2 -- только гитлаб, 0 -- всё, по умолчанию)
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Параметры запуска:')
    parser.add_argument('num', type=str, help='ID лабораторной работы, например, 01')
    parser.add_argument('-d','--duration', type=int, default=14,
                        help='Длительность лабораторной работы, дни (по-умолчанию 14)')
    parser.add_argument('-t', '--tracker', type=int, default=1,
                        help='ID трекера задач в Redmine (по-умолчанию 1)')
    parser.add_argument('-m', '--mode', type=int, default=0,
                        help='Режим запуска:\n'
                             '1 -- выдача только в Redmine,\n'
                             '2 -- выдача только в Gitlab,\n'
                             '0 -- выдача во всех системах (по-умолчанию 0)')
    parser.add_argument('-s', '--settings', type=str, default='oii.ini',
                        help='Путь к настроечному файлу (по-умолчанию ./oii.ini)')
    ns = parser.parse_args()
    print(ns)

    # читаем конфиги
    err_code, config = h.read_config(ns.settings)
    if err_code != 0:
        print('Ошибка чтения настроечного файла oii.ini!')
        exit(err_code)
    else:
        print('Настроечный файл успешно прочитан...')
        sh.shedule_lab(ns.num, ns.duration, ns.tracker, ns.mode, config)
