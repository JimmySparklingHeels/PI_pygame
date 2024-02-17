import pygame
import copy
pygame.init()
#Используемые цвета
white = (255, 255, 255)
gray = (128, 128, 128)
black = (0, 0, 0)
red = (255, 0, 0)
azure = (0, 128, 255)
#Разрешение окна
dis_width = 400
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))
#Заголовок окна
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()
fps = 10
#Шрифты
debug_font = pygame.font.SysFont("bahnschrift", 14)
message_font = pygame.font.SysFont("bahnschrift", 20)
#Функция для вывода номера хода
def print_turn(turn):
    value = debug_font.render("Время: " + str(turn), True, red)
    dis.blit(value, [0, 24])
#Функция для вывода уведомления о паузе
def print_pause():
    pygame.draw.rect(dis, black, [dis_width/2 - 130, 40, 280, 50])
    value = message_font.render("Игра на паузе", True, red)
    dis.blit(value, [dis_width/2 - 65, 40])
    value = message_font.render("Нажмите C чтобы продолжить", True, red)
    dis.blit(value, [dis_width/2 - 130, 70])
#Функция для вывода уведомления об окончании игры
def print_gameover():
    pygame.draw.rect(dis, black, [dis_width/2 - 130, 40, 280, 50])
    value = message_font.render("Игра окончена!", True, red)
    dis.blit(value, [dis_width/2 - 70, 40])
    value = message_font.render("Нажмите R чтобы переиграть", True, red)
    dis.blit(value, [dis_width/2 - 130, 70])
#Функция для вывода уведомления о зацикливании игры
def print_gamerepeat():
    value = message_font.render("Игра зациклилась!", True, red)
    dis.blit(value, [dis_width/2 - 85, 40])
    value = message_font.render("Нажмите R чтобы переиграть", True, red)
    dis.blit(value, [dis_width/2 - 130, 70])
#Функция для прорисовки фона
def draw_background():
    pygame.draw.rect(dis, gray, [100, 100, 200, 200], 2)
    value = message_font.render("Conway's Game of Life", True, azure)
    dis.blit(value, [dis_width/2 - 100, 305])
    value = message_font.render("Нажмите P для паузы", True, azure)
    dis.blit(value, [20, 330])
    value = message_font.render("Нажмите Q для выхода", True, azure)
    dis.blit(value, [20, 350])
    value = message_font.render("Нажмите R для перезапуска", True, azure)
    dis.blit(value, [20, 370])
#Функция для отрисовки клеток и вычисления идентификатора хода
def processCell(alive, x, y, gamestate):
    if alive == True:
        pygame.draw.rect(dis, white, [100 + 20 * x, 100 + 20 * y, 20, 20])
        gamestate = gamestate + "1"
    else:
        pygame.draw.rect(dis, black, [100 + 20 * x, 100 + 20 * y, 20, 20])
        gamestate = gamestate + "0"
    return gamestate

#Цикл для запуска игры
def gameLoop():
    shutdown = False #Выход из игры
    pause = True #Пауза
    pause_message = False
    gameover = False #Конец игры
    gameover_message = False
    gamerepeat = False #Игра зациклилась
    fieldlen = 10 #Размер поля
    cells = [[False] * fieldlen for i in range (fieldlen)] #Массив состояния клеток
    nextcells = [[False] * fieldlen for i in range (fieldlen)] #Массив состояния клеток на следующий ход
    gamestate = [] #Идентификатор хода
    turn = 1 #Номер хода
    #Считывание начальной позиции клеток из файла
    with open(r"conway_input.txt") as input_file:
        j = 0
        for line in input_file:
            for i in range(0, fieldlen):
                cells[i][j] = bool(int(line[i]))
            j += 1
            if j>fieldlen-1:
                break
    #Заливаем черный фон
    dis.fill(black)
    #Добавляем пустую строку для дальнейшего заполнения
    gamestate.append("")
    
    #Рисуем клетки и просчитываем идентификатор хода
    for i in range(fieldlen):
        for j in range(fieldlen):
            if cells[i][j] == True:
                gamestate[0] = processCell(True, i, j, gamestate[0])
            else:
                gamestate[0] = processCell(False, i, j, gamestate[0])
    #Рисуем фон
    draw_background()
    #Рисуем номер хода
    print_turn(0)
    #Выводим на экран отрисованные элементы
    pygame.display.update()

    #Основной цикл игры
    while not shutdown:
        #Считываем нажатия клавиш
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        shutdown = True
                    elif event.key == pygame.K_p:
                        pause = True
                        pause_message = False
                    elif event.key == pygame.K_r:
                        gameLoop()
                if event.type == pygame.QUIT: #При нажатии на крестик в углу окна происходит выход из игры
                    shutdown = True
        
        #Останавливаемся в новом цикле при завершении игры
        while gameover:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        shutdown = True
                        gameover = False
                        pause = False
                    elif event.key == pygame.K_r:
                        gameLoop()
                if event.type == pygame.QUIT:
                    shutdown = True
                    gameover = False
                    pause = False
            if not gameover_message: #Один раз выводим сообщение об окончании игры
                print_gameover()
                gameover_message = True
            pygame.display.update()
            clock.tick(fps)
        
        #Останавливаемся в новом цикле при паузе
        while pause:        
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        shutdown = True
                        pause = False
                    elif event.key == pygame.K_c:
                        pause = False
                if event.type == pygame.QUIT:
                    shutdown = True
                    pause = False
            if not pause_message: #Один раз выводим сообщение о паузе
                print_pause()
                pause_message = True
            pygame.display.update()
            clock.tick(fps)
        
        dis.fill(black)
        gamestate.append("")
        #Просчитываем состояния клеток на следующий ход
        for i in range(fieldlen):
            for j in range(fieldlen):
                alivenum = 0 #Количество живых соседей
                #Считаем, сколько у клетки живых соседей
                for a in range(-1, 2):
                    for b in range(-1, 2):
                        if a == b == 0: continue
                        c = i + a
                        v = j + b
                        if c < 0: c = fieldlen-1
                        if c > fieldlen-1: c = 0
                        if v < 0: v = fieldlen-1
                        if v > fieldlen-1: v = 0
                        if cells[c][v] == True:
                            alivenum = alivenum + 1

                #Если клетка мертвая
                if cells[i][j] == False:
                    if alivenum == 3: #Если три соседа, клетка живёт
                        nextcells[i][j] = True
                        gamestate[turn] = processCell(True, i, j, gamestate[turn])
                    else: #Иначе, клетка умирает
                        nextcells[i][j] = False
                        gamestate[turn] = processCell(False, i, j, gamestate[turn])
                else: #Если клетка живая
                    if alivenum < 2: #Если у неё меньше двух живых соседей, она умирает
                        nextcells[i][j] = False
                        gamestate[turn] = processCell(False, i, j, gamestate[turn])
                    elif alivenum > 3: #Если у неё больше трех живых соседей, она умирает
                        nextcells[i][j] = False
                        gamestate[turn] = processCell(False, i, j, gamestate[turn])
                    else: #Если 2 или 3 соседа, клетка остаётся жить
                        nextcells[i][j] = True
                        gamestate[turn] = processCell(True, i, j, gamestate[turn])
        cur = len(gamestate)-1 #Номер последнего хода
        
        #Если идентификатор равен нулю (все клетки мертвые), игра окончена
        if int(gamestate[cur]) == 0: gameover = True
        #Если идентификатор повторился, игра зациклилась
        for n in range(cur):
            if gamestate[n] == gamestate[cur]:
                gamerepeat = True
        #Копируем массив клеток следующего хода в массив клеток данного хода
        cells = copy.deepcopy(nextcells)
        #draw_background()
        #Если игра зациклилась, вывести сообщение
        if gamerepeat == True:
            print_gamerepeat()
        print_turn(turn) #Выводим номер хода
        pygame.display.update()
        turn += 1 #Прибавляем единицу к счетчику хода
        clock.tick(fps)
    #Если shutdown = true, выходим из игры
    pygame.quit()
    quit()

#Вызываем функцию для запуска игры
gameLoop()