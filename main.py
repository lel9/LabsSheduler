import sheduler as sh
import argparse

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
    ns = parser.parse_args()
    print(ns)

    sh.shedule_lab(ns.num, ns.duration, ns.tracker, ns.mode)
