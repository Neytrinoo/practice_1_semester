from math import cos, sin, sqrt, radians

x, y = 200, 0  # координаты коляски
point_of_intersection = [100, 100]  # координаты пересечения с линиями площадки
time_of_intersection = -1  # время пересечения площадки после старта
max_distance = 0  # максимальное расстояние удаления от ворот
all_distance = 0  # общее пройденное расстояние


def get_vector_length(x1, y1, x2, y2):  # получение длины вектора
    return sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


# функция проверки пересечения с границами площадки. x1, y1 - координаты до перемещения, x2, y2 - после
def check_intersection(x1, y1, x2, y2, t1, speed):
    displacement_vector_x, displacement_vector_y = x2 - x1, y2 - y1

    if displacement_vector_x != 0:
        # проверка пересечения с левой стенкой
        y = displacement_vector_y * (-x1 / displacement_vector_x) + y1
        if 0 <= y <= 200 and x2 <= 0 <= x1 and min(y2, y1) <= y <= max(y2, y1):
            distance_to_intersection = get_vector_length(x1, y1, 0, y)
            return [0, y, t1 + (distance_to_intersection / speed)]  # возвращаем координату пересечения с левой стенкой и время пересечения

        # проверка пересечения с правой стенкой
        y = displacement_vector_y * ((400 - x1) / displacement_vector_x) + y1
        if 0 <= y <= 200 and x1 <= 400 <= x2 and min(y2, y1) <= y <= max(y2, y1):
            distance_to_intersection = get_vector_length(x1, y1, 400, y)
            return [400, y, t1 + (distance_to_intersection / speed)]  # возвращаем координату пересечения с правой стенкой и время пересечения

    if displacement_vector_y != 0:
        # проверка пересечения с нижней стенкой
        x = displacement_vector_x * (-y1 / displacement_vector_y) + x1
        if 0 <= x <= 400 and y2 <= 0 <= y1 and min(x1, x2) <= x <= max(x1, x2):
            distance_to_intersection = get_vector_length(x1, y1, x, 0)
            return [x, 0, t1 + (distance_to_intersection / speed)]  # возвращаем координату пересечения с нижней стенкой и время пересечения

        # проверка пересечения с верхней стенкой
        x = displacement_vector_x * ((200 - y1) / displacement_vector_y) + x1
        if 0 <= x <= 400 and y1 <= 200 <= y2 and min(x1, x2) <= x <= max(x1, x2):
            distance_to_intersection = get_vector_length(x1, y1, x, 200)
            return [x, 200, t1 + (distance_to_intersection / speed)]  # возвращаем координату пересечения с верхней стенкой
    return False


def get_max_distance(x2, y2):
    global max_distance
    distance = get_vector_length(200, 0, x2, y2)
    if distance > max_distance:
        max_distance = distance


def moving(t1, t2, speed, direction):  # функция перемещения коляски
    global x, y, point_of_intersection, time_of_intersection, all_distance
    distance = (t2 - t1) * speed
    x += sin(radians(direction)) * distance
    y += cos(radians(direction)) * distance
    if time_of_intersection == -1:
        intersection = check_intersection(x - sin(radians(direction)) * distance, y - cos(radians(direction)) * distance, x, y, t1, speed)
        if intersection:
            point_of_intersection = intersection[:2]
            time_of_intersection = intersection[-1]
        else:
            get_max_distance(x, y)  # если нет пересечения, проверяем расстояние от ворот
    all_distance += get_vector_length(x - sin(radians(direction)) * distance, y - cos(radians(direction)) * distance, x, y)


def main():
    global x, y, point_of_intersection, time_of_intersection, max_distance, all_distance
    data = open('data.txt', 'r', encoding='utf-8').read().split('\n')  # считываем из файла входные данные
    for i in range(len(data)):
        if len(data[i].split()) == 1:
            data[i] = int(data[i])
        else:
            data[i] = list(map(float, data[i].split()))

    event_number = 0
    for i in range(len(data)):
        if type(data[i]) is int:
            if i != 0:
                print('Случай номер {}.'.format(event_number))
                if time_of_intersection == -1:
                    print('Коляска не покидала ограниченную площадку.')
                else:
                    print('Коляска покинула ограниченную площадку в точке ({:.2f}, {:.2f}) спустя {:.1f} '
                          'секунды после старта.'.format(point_of_intersection[0], point_of_intersection[1], time_of_intersection))
                print('Общий пройденный путь равен {:.1f} фута.'.format(all_distance))
            event_number += 1
            x, y = 200, 0
            point_of_intersection = [100, 100]
            time_of_intersection = -1
            max_distance = 0
            all_distance = 0
        else:
            moving(*data[i])


if __name__ == '__main__':
    main()
