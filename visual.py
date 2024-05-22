import pygame
import sys

# Инициализация Pygame
pygame.init()

# Константы для цветов и размеров
FPS = 6
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRID_SIZE = 100
ROWS = 5
COLS = 5
WINDOW_SIZE = (ROWS * GRID_SIZE, COLS * GRID_SIZE)
k = 0

# Создание окна
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Visualization of the SWARM system")
pygame.display.set_icon(pygame.image.load("bee.bmp"))

# Загрузка изображений
background_image = pygame.image.load("forest.png")
background_image = pygame.transform.scale(background_image, WINDOW_SIZE)
scout_image = pygame.image.load("dron.png")
scout_image = pygame.transform.scale(scout_image, (GRID_SIZE, GRID_SIZE))
inspector_image = pygame.image.load("dron_1.png")
inspector_image = pygame.transform.scale(inspector_image, (GRID_SIZE, GRID_SIZE))
base_image = pygame.image.load("dron_base.png")
base_image = pygame.transform.scale(base_image, (GRID_SIZE, GRID_SIZE))
fire_image = pygame.image.load("fire.png")
fire_image = pygame.transform.scale(fire_image, (GRID_SIZE // 2, GRID_SIZE // 2))  # Изменение размера изображения
station_image = pygame.image.load("charger.png")
station_image = pygame.transform.scale(station_image, (GRID_SIZE // 1.5, GRID_SIZE // 1.5))


# Функция отрисовки сетки
def draw_grid():
    for x in range(0, WINDOW_SIZE[0] + 1, GRID_SIZE):
        pygame.draw.line(window, WHITE, (x, 0), (x, max(WINDOW_SIZE)))
    for y in range(0, WINDOW_SIZE[1] + 1, GRID_SIZE):
        pygame.draw.line(window, WHITE, (0, y), (max(WINDOW_SIZE), y))


# Функция для закраски клетки
def fill_cell(row, col, color):
    cell_rect = pygame.Rect(col * GRID_SIZE, row * GRID_SIZE, GRID_SIZE, GRID_SIZE)
    pygame.draw.rect(window, color, cell_rect)


# Класс для разведчика
class Scout(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.image = scout_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * GRID_SIZE, row * GRID_SIZE)
        self.start_x = col * GRID_SIZE  # Начальная координата X
        self.start_y = row * GRID_SIZE  # Начальная координата Y
        self.directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]   # Порядок движения
        self.current_direction = 1  # Изначальное направление
        self.move_allowed = True  # Флаг разрешения движения
        self.on_station = False
        self.battery_charge = 100  # Заряд батареи
        self.nick = [k]

    def move(self):
        if self.move_allowed and self.battery_charge > 0:
            dx, dy = self.directions[self.current_direction]
            self.rect.x += dx * GRID_SIZE
            self.rect.y += dy * GRID_SIZE
            self.decrease_battery_charge()  # Уменьшение заряда батареи при каждом движении

    def decrease_battery_charge(self):
        self.battery_charge -= 5  # Уменьшаем заряд на 2 единиц

    def increase_battery_charge(self):
        self.battery_charge += 5  # Увеличиваем заряд на 2 единиц

    def stop_movement(self):
        self.move_allowed = False  # Остановка разведчика

    def start_movement(self):
        self.move_allowed = True  # Начало движения разведчика

    def check_fire(self):
        row = self.rect.y // GRID_SIZE
        col = self.rect.x // GRID_SIZE
        if isinstance(grid[row][col], Fire):
            return True
        else:
            return False

    def check_station(self):
        row = self.rect.y // GRID_SIZE
        col = self.rect.x // GRID_SIZE
        if isinstance(grid[row][col], Station):
            return True
        else:
            return False


# Класс для базы
class Base(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.image = base_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * GRID_SIZE, row * GRID_SIZE)

    def give_direction(self, scout_first):
        if scout_first.check_fire():  # Если огонь обнаружен
            # scout_first.stop_movement()  # Остановка разведчика
            print("Scout № ", scout_first.nick, ": FIRE DETECTED!!!\t Location: X = ",
                  scout_first.rect.x // GRID_SIZE + 1, "\t Y = ", scout_first.rect.y // GRID_SIZE + 1)

        if scout_first.battery_charge < 25:  # Если заряд батареи меньше 20%
            if scout_first.rect.left > 0:  # Если разведчик не в крайней левой колонке
                scout_first.current_direction = 3  # Направление влево
            else:
                if scout_first.check_station():
                    if not scout_first.on_station:
                        scout_first.stop_movement()
                        print("Scout № ", scout_first.nick, " Прибыл на станцию")
                        scout_first.on_station = True
                    station.charge_scout(scout_first)
                else:
                    scout_first.current_direction = 0  # Направление вниз

        elif scout_first.check_station() and scout_first.battery_charge < 100:
            station.charge_scout(scout_first)

        else:  # Если огня нет и заряд батареи нормальный
            dx, dy = scout_first.directions[scout_first.current_direction]
            next_x = scout_first.rect.x + dx * GRID_SIZE
            next_y = scout_first.rect.y + dy * GRID_SIZE
            # Можно оставить только if 0 <= next_x < WINDOW_SIZE[0]:
            if 0 <= next_x < WINDOW_SIZE[0] and 0 <= next_y < WINDOW_SIZE[1]:
                scout_first.current_direction = scout_first.current_direction
            else:
                # Если разведчик достиг границы, меняем направление движения
                if scout_first.current_direction == 1:  # Если он шел вправо
                    scout_first.current_direction = 3  # Направление влево
                elif scout_first.current_direction == 3:  # Если он шел влево
                    scout_first.current_direction = 1  # Направление вправо

        if scout_first.battery_charge <= 0:
            all_sprites.remove(scout_first)
            grid[scout_first.rect.y // GRID_SIZE][scout_first.rect.x // GRID_SIZE] = BLACK

    def call_inspector(self, scout_check):
        if scout_check.check_fire():
            inspector_called = Inspector(scout_check.rect.y // GRID_SIZE, scout_check.rect.x // GRID_SIZE)
            return inspector_called


# Класс для дрона-смотрителя
class Inspector(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.image = inspector_image
        self.rect = self.image.get_rect()
        self.rect.topleft = (col * GRID_SIZE, row * GRID_SIZE)


# Класс для огня
class Fire(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.image = fire_image
        self.rect = self.image.get_rect()
        # self.rect.topleft = (col * GRID_SIZE, row * GRID_SIZE)
        self.rect.centerx = col * GRID_SIZE + GRID_SIZE // 2  # Устанавливаем центр по горизонтали
        self.rect.bottom = row * GRID_SIZE + GRID_SIZE  # Устанавливаем нижнюю границу


# Класс станции подзарядки(станции для дронов)
class Station(pygame.sprite.Sprite):
    def __init__(self, row, col):
        super().__init__()
        self.image = station_image
        # self.image = pygame.Surface((GRID_SIZE, GRID_SIZE))
        # self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect()
        # self.rect.topleft = (col * GRID_SIZE, row * GRID_SIZE)
        self.rect.left = col * GRID_SIZE  # Устанавливаем левую границу
        self.rect.bottom = row * GRID_SIZE + GRID_SIZE  # Устанавливаем нижнюю границу

    def charge_scout(self, scout):
        row = self.rect.y // GRID_SIZE
        col = self.rect.x // GRID_SIZE
        if (scout.rect.y == row * GRID_SIZE and scout.rect.x == col * GRID_SIZE) and \
                (scout.start_y != row * GRID_SIZE or scout.start_x != col * GRID_SIZE):
            if scout.battery_charge <= 100:
                scout.increase_battery_charge()
                if scout.battery_charge > 100:
                    scout.battery_charge = 100
                print("Scout № ", scout.nick, ": Current battery charge = ", scout.battery_charge)


# Создание сетки и размещение разведчика, огня и базы
grid = [[BLACK for _ in range(ROWS)] for _ in range(COLS)]

scout_0 = Scout(0, 0)  # Разведчик в левом верхнем углу
# grid[0][0] = scout_0   # Непонятно зачем ???
k += 1
scout_1 = Scout(2, 0)
k += 1
scout_2 = Scout(1, 0)
k += 1
scout_3 = Scout(3, 0)
k += 1

base = Base(COLS - 1, ROWS - 1)  # База в правом нижнем углу
grid[COLS - 1][ROWS - 1] = base

station = Station(COLS - 1, 0)  # Станция дронов
grid[COLS - 1][0] = station

# Группировка спрайтов для удобства управления
all_scouts = pygame.sprite.Group()
all_scouts.add(scout_0, scout_1, scout_2, scout_3)
all_sprites = pygame.sprite.Group()
all_sprites.add(all_scouts, base, station)

# Основной игровой цикл
clock = pygame.time.Clock()
running = True
while running:
    window.fill(BLACK)  # Отображение фона
    window.blit(background_image, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()  # Получаем координаты клика мыши
            col_new = mouse_x // GRID_SIZE  # Определяем колонку в сетке
            row_new = mouse_y // GRID_SIZE  # Определяем строку в сетке
            new_fire = Fire(row_new, col_new)  # Создаем объект огня
            grid[row_new][col_new] = new_fire  # Заполняем ячейку объектом огня
            all_sprites.add(new_fire)  # Добавляем объект огня в группу спрайтов

    for scout in all_scouts:
        base.give_direction(scout)
        scout.move()
        if scout.on_station and scout.battery_charge == 100:
            x_new = scout.start_x // GRID_SIZE
            y_new = scout.start_y // GRID_SIZE
            nick_new = scout.nick
            all_scouts.remove(scout)
            all_sprites.remove(scout, station)
            scout = Scout(y_new, x_new)
            scout.nick = nick_new
            all_scouts.add(scout)
            all_sprites.add(scout, station)
        if scout.check_fire():
            inspector = base.call_inspector(scout)
            all_sprites.add(inspector)  # Добавляем объект в группу спрайтов

    # Отрисовка сетки
    draw_grid()

    # Закрашиваем клетку в белый цвет
    fill_cell(4, 0, WHITE)

    # Отрисовка всех спрайтов
    all_sprites.draw(window)

    pygame.display.update()
    clock.tick(FPS)  # FPS для наглядности

pygame.quit()
sys.exit()
