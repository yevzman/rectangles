'''
Чтобы решить эту задачу, используем алгоритм оптимизации - имитационный отжиг. (и chatGPT)

Имитационный отжиг - это вероятностный алгоритм оптимизации, который вдохновлен процессом отжига в металлургии.
Алгоритм начинает с начального решения, а затем итеративно генерирует новые решения путем внесения небольших случайных
изменений в текущее решение. Эти изменения могут быть приняты или отклонены на основе функции вероятности,
которая зависит от разницы в значении объективной функции между текущим решением и новым решением, а также
параметра температуры, который управляет вероятностью принятия худших решений.

В коде мы сначала считываем входные значения n, m и k, а затем считываем координаты k прямоугольников.
Затем мы используем имитационный отжиг для оптимизации расположения прямоугольников.

Функция `intersection_area` вычисляет площадь пересечения всех пар прямоугольников.
Функция `move_rectangles` генерирует случайные смещения для прямоугольников, случайным образом перемещая их по
горизонтали или вертикали. Перемещение принимается только в том случае, если полученное площадь пересечения
меньше текущего значения или соответствует определенному порогу вероятности, основанному на параметре температуры.

Цикл имитации отжига итеративно генерирует новые ходы и принимает или отвергает их на основе функции вероятности.
Цикл постепенно уменьшает параметр температуры с течением времени, что позволяет алгоритму сходиться к почти оптимальному
решению. Наконец, выводим новое расположение прямоугольников и минимальную область пересечения, найденную алгоритмом.
'''

import random
import math

# Define the function to calculate the intersection area of the rectangles
def intersection_area(rectangles):
    intersectionArea = 0
    for i in range(len(rectangles)):
        for j in range(i + 1, len(rectangles)):
            xOverlap = max(0, min(rectangles[i][2], rectangles[j][2]) - max(rectangles[i][0], rectangles[j][0]));
            yOverlap = max(0, min(rectangles[i][1], rectangles[j][1]) - max(rectangles[i][3], rectangles[j][3]));
            intersectionArea += xOverlap * yOverlap
    return intersectionArea

# Define the function to move the rectangles by a random distance
def move_rectangles(rectangles, n, m):
    moved_rectangles = []
    for rect in rectangles:
        moveX = random.randint(-rect[0], n - rect[2])
        moveY = random.randint(-rect[3], m - rect[1])
        # print(rect)
        # print(f"shift: {moveX}, {moveY}")
        x1 = rect[0] + moveX
        y1 = rect[1] + moveY
        x2 = rect[2] + moveX
        y2 = rect[3] + moveY
        moved_rectangles.append([x1, y1, x2, y2])
    return moved_rectangles

# Define the function to calculate the energy of a solution
def energy(solution):
    return -intersection_area(solution)

# Define the function to accept or reject a new solution
def accept_probability(delta_energy, temperature):
    if delta_energy < 0:
        return 1.0
    return math.exp(-delta_energy / temperature)

# Define the main function for simulated annealing
def simulated_annealing(rectangles, initial_temperature, cooling_rate, stopping_temperature):
    # Initialize the current solution
    current_solution = rectangles
    current_energy = energy(current_solution)
    if current_energy == 0:
        return current_energy

    # Initialize the best solution
    best_solution = current_solution
    best_energy = current_energy

    # Initialize the temperature
    temperature = initial_temperature

    # Iterate until the stopping temperature is reached
    while temperature > stopping_temperature:
        # Generate a new solution by moving the existing rectangles
        new_solution = move_rectangles(current_solution, n, m)
        new_energy = energy(new_solution)
        if new_energy == 0:
            return new_solution
        # Calculate the energy difference
        delta_energy = new_energy - current_energy

        # Decide whether to accept the new solution
        accept_probability_treshold = random.random()

        if accept_probability(delta_energy, temperature) >= accept_probability_treshold:
            current_solution = new_solution
            current_energy = new_energy

        # Update the best solution if necessary
        if current_energy < best_energy:
            best_solution = current_solution
            best_energy = current_energy

        # Cool the temperature
        temperature *= cooling_rate

    return best_solution


# Get the input from the user
k = int(input("Enter the number of rectangles: "))
n = int(input("Enter the height of the field: "))
m = int(input("Enter the width of the field: "))

initial_temperature = 500
cooling_rate = 0.99
stopping_temperature = 1

rectangles = []
for i in range(k):
    x1 = int(input("Enter the x-coordinate of the top-left corner of rectangle {}: ".format(i+1)))
    y1 = int(input("Enter the y-coordinate of the top-left corner of rectangle {}: ".format(i+1)))
    x2 = int(input("Enter the x-coordinate of the bottom-right corner of rectangle {}: ".format(i+1)))
    y2 = int(input("Enter the y-coordinate of the bottom-right corner of rectangle {}: ".format(i+1)))
    rectangles.append([x1, y1, x2, y2])

best_solution = simulated_annealing(rectangles, initial_temperature, cooling_rate, stopping_temperature)

print("The best solution found by simulated annealing is:")
for i, rect in enumerate(best_solution):
    print("Rectangle {}: ({}, {}) ({}, {})".format(i+1, rect[0], rect[1], rect[2], rect[3]))
print('Final intersection area:', intersection_area(best_solution))

'''
Test-1
2
6
6
2
3
4
1
3
4
5
2
'''