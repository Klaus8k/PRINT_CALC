from tkinter import *
from tkinter.ttk import Combobox
from tkinter import messagebox
import Image_sum_CMYK as color_s


# Калькуляция печати без бумги
def print_calc():
    global coverage_k, coverage_cmy
    toner_price_k = 6600 / 3  # Цена банки черного (3 картриджа)
    toner_price_cmy = 8000 * 3 / 3  # Цена 3х банок цветных (по 3 картриджа)

    drum_price = 15750  # цена драма
    fuser_price = 17170  # цена печки
    belt_price = 17170  # цена ремня

    # плотности красок
    color_sum = color_s.sum_cmyk()
    coverage_k = color_sum[3]
    coverage_cmy = sum(color_sum[:-1])

    # Коэффициент плотности носителя 80-130 - 1, 150-250 - 0.75, 300-400 - 0.5
    if int(choise_media.get()) < 150:
        coefficient_media = 1
    elif int(choise_media.get()) < 300:
        coefficient_media = 0.75
    else:
        coefficient_media = 0.5

    # Общая фрмула расчета цены печати
    # цена отпечатка А4 цена тонера/ресурс * на покрытие / 5% + 4 драма + печка + ремень / коэффициент плотности

    print_oki_calc = 2 * ((toner_price_k / 22000) * (coverage_k / 5) + (toner_price_cmy / 22000) * (coverage_cmy / 5) +
                          (4 * drum_price / 30000 + fuser_price / 100000 + belt_price / 100000) / coefficient_media)

    return print_oki_calc


# Цены на бумагу
def paper_price():
    if int(choise_media.get()) < 150:
        return 3
    elif int(choise_media.get()) < 300:
        return 5
    else:
        return 10


# вывод результата с проверкой на 0
def finish():
    lists = int(pressrun.get()) // sum_on_list()  # Листов в тираже

    try:
        result = f'Размер изделия {int(width_suit.get()) + 4}x{int(height_suit.get()) + 4}\n' \
                 f'На 1 листе SRA3 {sum_on_list()} изделий.\n' \
                 f'необходимо {lists} листов, на сумму {lists * paper_price()}руб.\n' \
                 f'Цена тиража: {int(print_calc()) * lists + paper_price() * lists} руб.\n'\
                 f'Заливка страницы CMYK {color_s.sum_cmyk()}'
        label_finish['text'] = result
        return result

    except ZeroDivisionError:
        messagebox.showinfo('Error', 'Что то не так!')


# Количество изделий на листе
def sum_on_list() -> object:
    label_finish['text'] = ''
    x = int(width_suit.get()) + 4
    y = int(height_suit.get()) + 4
    free_space = 5  # поля
    w_list = 320 - 2 * free_space  # размеры для SRA3
    h_list = 450 - 2 * free_space
    sum_list = max((w_list // x) * (h_list // y), (w_list // y) * (h_list // x))



    return sum_list


# UI программы
window = Tk()
window.title('Калькулятор печати OKI9655')
window.geometry('300x200+150+300')  # геометрия окна
txt_format_suit = Label(window, text='Формат изделия  ').grid(column=0, row=1)
txt_width_suit = Label(window, text='Width').grid(column=1, row=0, padx=5)
txt_height_suit = Label(window, text='Height').grid(column=2, row=0)
width_suit = Entry(window, width=11)  # ввод ширины изделия
width_suit.grid(column=1, row=1)
height_suit = Entry(window, width=11)  # ввод высоты изделия
height_suit.grid(column=2, row=1)
# Выбор бумаги
txt_media = Label(window, text='Выбери бумагу  ').grid(column=0, row=2, pady=5)
choise_media = Combobox(window)
choise_media['values'] = (80, 130, 200, 350)
choise_media.current(0)
choise_media.grid(column=1, row=2, columnspan=2)
# Тираж
pressrun_txt = Label(window, text='Тираж').grid(column=0, row=3, pady=5)
pressrun = Entry(window, width=5)
pressrun.grid(column=1, row=3, padx=5)

# Кнопка ФИНИШ
finish_b = Button(window, text='START', command=finish).grid(column=1, row=19, pady=5)
# вывод результата
label_finish = Label()
label_finish.grid(column=0, columnspan=3, row=20)

window.mainloop()
