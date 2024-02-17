import pygame
import copy
pygame.init()
white = (255, 255, 255)
gray = (128, 128, 128)
black = (0, 0, 0)
red = (255, 0, 0)
azure = (0, 128, 255)
dis_width = 400
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Conway's Game of Life")
clock = pygame.time.Clock()
fps = 10
debug_font = pygame.font.SysFont("bahnschrift", 14)
message_font = pygame.font.SysFont("bahnschrift", 20)
def print_turn(turn):
    value = debug_font.render("Время: " + str(turn), True, red)
    dis.blit(value, [0, 24])
def processCell(alive, x, y, gamestate):
    if alive == True:
        pygame.draw.rect(dis, white, [100 + 20 * x, 100 + 20 * y, 20, 20])
        gamestate = gamestate + "1"
    else:
        pygame.draw.rect(dis, black, [100 + 20 * x, 100 + 20 * y, 20, 20])
        gamestate = gamestate + "0"
    return gamestate
def gameLoop():
    shutdown = False
    pause = True
    gameover = False
    fieldlen = 10
    cells = [[False] * fieldlen for i in range (fieldlen)]
    nextcells = [[False] * fieldlen for i in range (fieldlen)]
    gamestate = []
    turn = 1
    with open(r"conway_input.txt") as input_file:
        j = 0
        for line in input_file:
            for i in range(0, fieldlen):
                cells[i][j] = bool(int(line[i]))
            j += 1
            if j>fieldlen-1:
                break
    dis.fill(black)
    gamestate.append("")
    for i in range(fieldlen):
        for j in range(fieldlen):
            if cells[i][j] == True:
                gamestate[0] = processCell(True, i, j, gamestate[0])
            else:
                gamestate[0] = processCell(False, i, j, gamestate[0])
    print_turn(0)
    pygame.display.update()
    while not shutdown:
        for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        shutdown = True
                    elif event.key == pygame.K_p:
                        pause = True
                    elif event.key == pygame.K_r:
                        gameLoop()
                if event.type == pygame.QUIT:
                    shutdown = True
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
            pygame.display.update()
            clock.tick(fps)
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
            pygame.display.update()
            clock.tick(fps)
        dis.fill(black)
        gamestate.append("")
        for i in range(fieldlen):
            for j in range(fieldlen):
                alivenum = 0
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
                if cells[i][j] == False:
                    if alivenum == 3: 
                        nextcells[i][j] = True
                        gamestate[turn] = processCell(True, i, j, gamestate[turn])
                    else:
                        nextcells[i][j] = False
                        gamestate[turn] = processCell(False, i, j, gamestate[turn])
                else:
                    if alivenum < 2: 
                        nextcells[i][j] = False
                        gamestate[turn] = processCell(False, i, j, gamestate[turn])
                    elif alivenum > 3: 
                        nextcells[i][j] = False
                        gamestate[turn] = processCell(False, i, j, gamestate[turn])
                    else: 
                        nextcells[i][j] = True
                        gamestate[turn] = processCell(True, i, j, gamestate[turn])
        cur = len(gamestate)-1
        if int(gamestate[cur]) == 0: gameover = True
        for n in range(cur):
            if gamestate[n] == gamestate[cur]:
                gamerepeat = True
        cells = copy.deepcopy(nextcells)
        print_turn(turn)
        pygame.display.update()
        turn += 1
        clock.tick(fps)
    pygame.quit()
    quit()
gameLoop()