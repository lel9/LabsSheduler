import sys
import sheduler as sh

if __name__ == "__main__":
    lab_num = None
    duration = None
    # узнаем номер лабы, которую надо выдать, и её срок в днях
    # либо они переданы как параметры
    if len(sys.argv) == 3:
        lab_num = sys.argv[1]
        if sys.argv[2].isdigit() and int(sys.argv[2]) > 0:
            duration = int(sys.argv[2])
        else:
            print('Неверно указан срок выдаваемой лабораторной: это должно быть положительное число!')
    # либо надо посмотреть расписание выдачи лаб и понять,
    # нужно ли выдать лабу и если нужно, то какую
    else:
        print('Нужно указать номер выдаваемой лабораторной и её срок в днях, например, 01 и 28')
        # lab_num = get_current_lab_num()
        # TODO запуск по расписанию

    if lab_num is not None and duration is not None:
        sh.shedule_lab(lab_num, duration)




