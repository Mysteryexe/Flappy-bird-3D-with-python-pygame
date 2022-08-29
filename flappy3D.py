import pygame
import random
import sys
import shelve
import os
import math

# by Mystery.exe#5099 on discord.
pygame.init()
icon = pygame.image.load(r"images/bird (6).png")
pygame.display.set_caption("FlappyBird3D-Pourmehdi")
pygame.display.set_icon(icon)
pygame.mixer.set_num_channels(3)
# music
pygame.mixer.music.load(r"sounds/StardewValleyOverture.mp3")
pygame.mixer.music.play(-1)


def game():
    background = (38, 78, 174)

    # window setting
    w = 500
    h = 700
    window = pygame.display.set_mode((w, h), 8)
    # images
    birdImages = [r"images/bird (1).png", r"images/bird (2).png", r"images/bird (3).png",
                  r"images/bird (4).png", r"images/bird (5).png", r"images/bird (6).png"]

    wallimgR = pygame.image.load(r"images/wallRight.png").convert()
    wallimgRC = pygame.image.load(r"images/wallRightCap2.png").convert()
    wallimgRCU = pygame.image.load(r"images/wallRightCap.png").convert()
    wallimgL = pygame.image.load(r"images/wallLeft.png").convert()
    wallimgLC = pygame.image.load(r"images/wallLeftCap2.png").convert()
    wallimgLCU = pygame.image.load(r"images/wallLeftCap.png").convert()
    gradient = pygame.image.load(r"images/gradient.png").convert()
    lizardS1 = pygame.image.load(r"images/lizardShadow1.png").convert_alpha()
    lizardS2 = pygame.image.load(r"images/lizardShadow2.png").convert_alpha()
    birdFrames = []
    pauseImg = pygame.image.load(
        r"images/pause.png").convert_alpha()
    gradient = pygame.transform.scale(
        gradient, (w, h/3))

    # variables
    leftSpace = w
    viewPers = 1
    movement = 5
    rotateB = 0
    frame = 0

    # space between 2 walls, always stays the same
    space = h * 0.20

    clk = pygame.time.Clock()

    fallShetab = 0.5
    lastI = 0
    # gotPoint - to see if the player got the point of 2 walls showing in the screen already
    gotPoint = False
    # passedHiPoint - did player made a new hiscore?
    passedHiPoint = False
    paused = False

    # points
    point = "0"
    hipoint = 0
    file_path = r'score.dat'
    # if the score file doesnt exist, it makes one. otherwise it gets the current hiscore
    d = shelve.open(r'score')
    if os.stat(file_path).st_size == 0:
        d['score'] = 0
    else:
        hipoint = d['score']
    d.close()
    # rects
    wallup = pygame.Rect(0, 0, w*0.1, 0)
    wallupL = pygame.Rect(0, 0, (wallup.w*0.6), 0)
    wallupLC = pygame.Rect(0, 0, wallupL.w, 10)
    wallupR = pygame.Rect(0, 0, (wallup.w*0.4), 0)
    wallupRC = pygame.Rect(0, 0, wallupR.w, 10)

    walldown = pygame.Rect(0, 0, w*0.1, 0)
    walldownL = pygame.Rect(0, 0, (walldown.w*0.6), 0)
    walldownR = pygame.Rect(0, 0, (walldown.w*0.4), 0)

    bird = pygame.Rect((w/2)-(w/5), h/2, w/8, w/8)
    birdCollide = pygame.Rect((w/2)-(w/5), h/2, w/15, w/15)

    lizardRect = pygame.Rect(0, 0, wallupR.w, 25)

    backgroundRect = pygame.Rect(0, (h/3)*2, w, (h/3))
    # txt/fonts
    font = pygame.font.Font("fonts/pixel.ttf", 20)
    Pfont = pygame.font.Font("fonts/pixel.ttf", 30)
    bigFont = pygame.font.Font("fonts/pixel.ttf", 60)
    bigTxt = bigFont.render("Ready?!", True, (0, 0, 0))
    startTxt = font.render("Press SPACE!", True, (0, 0, 0))
    pointTxt = Pfont.render(point, True, (0, 0, 0))
    pointTxt.set_alpha(128)
    highPTxt = Pfont.render(
        ("highscore: " + str(hipoint)), True, (28, 68, 164))
    startRect = startTxt.get_rect()
    pointRect = pointTxt.get_rect()
    bigTxtRect = bigTxt.get_rect()
    highPRect = highPTxt.get_rect()
    # position text rects
    pointRect.center = (w-pointRect.w, pointRect.h)
    bigTxtRect.center = (w // 2, h // 2)
    startRect.center = (w // 2, (bigTxtRect.h + bigTxtRect.y + startRect.h))
    highPRect.center = (w//2, bigTxtRect.y - highPRect.h)
    # set bird frames sizes to the BirdRect(bird)
    for i in birdImages:
        birdFrames.append(pygame.transform.scale(
            pygame.image.load(i).convert_alpha(), (bird.w, bird.h)))

    # starting frame for bird animation
    i = 0

    # functions
    def genWall():
        # generates new walls
        offset = random.randint(math.trunc(h*0.1), math.trunc(h*0.55))
        wallup.h = offset
        wallupL.h = offset
        wallupR.h = offset

        walldown.h = h - (offset+space)
        walldown.y = offset + space
        walldownL.h = walldown.h
        walldownL.y = walldown.y
        walldownR.h = walldown.h
        walldownR.y = walldown.y

        # lizard
        if random.randint(1, 4) == 1:
            lizardRect.y = walldown.y + \
                random.randint(math.trunc(walldown.h*0.1),
                               math.trunc(walldown.h*0.5))
            lizardRect.h = 28
        else:
            lizardRect.h = 0

    def drawWall():
        # up
        window.blit(pygame.transform.scale(
            wallimgL, (wallupL.w, wallup.h)), wallupL)
        window.blit(pygame.transform.scale(
            wallimgLCU, (wallupLC.w, wallupLC.h)), wallupLC)
        window.blit(pygame.transform.scale(
            wallimgR, (wallupR.w, wallup.h)), wallupR)
        window.blit(pygame.transform.scale(
            wallimgRCU, (wallupRC.w, wallupRC.h)), wallupRC)

        # down
        window.blit(pygame.transform.scale(
            wallimgL, (walldownL.w, walldown.h)), walldownL)
        window.blit(pygame.transform.scale(
            pygame.transform.flip(wallimgLC, False, True), (walldownL.w, 10)), walldownL)

        window.blit(pygame.transform.scale(
            wallimgR, (walldownR.w, walldown.h)), walldownR)
        window.blit(pygame.transform.scale(
            pygame.transform.flip(wallimgRC, False, True), (walldownR.w, 10)), walldownR)
        # lizard
        if frame % 2 == 1:
            lizardRect.y += math.trunc(random.randint(0, 5))
        if frame % 50 >= 25:
            window.blit(pygame.transform.scale(
                lizardS1, (lizardRect.w, lizardRect.h)), lizardRect)
        else:
            window.blit(pygame.transform.scale(
                lizardS2, (lizardRect.w, lizardRect.h)), lizardRect)

    def setGradient():
        backgroundRect.h = math.trunc(h/3 + bird.y*0.5)
        backgroundRect.y = h - backgroundRect.h
    # menu
    while pygame.key.get_pressed()[pygame.K_SPACE] == False:
        setGradient()
        if bird.y < h/5 or bird.y > (h/5) * 4:
            movement = - movement
        bird.y = bird.y + (movement/2)

        window.fill(background)
        window.blit(pygame.transform.scale(
            gradient, (w, backgroundRect.h)), backgroundRect)

        window.blit(highPTxt, highPRect)
        window.blit(startTxt, startRect)
        window.blit(bigTxt, bigTxtRect)

        if i % 5 == 0:
            lastI = int(i/5)
        if i >= (5*(len(birdImages)-1)):
            i = 0
        else:
            i = i + 1

        window.blit(birdFrames[lastI], bird)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        pygame.display.update()
        clk.tick(60)
        pygame.event.pump()

    genWall()

    # literally changes the whole game move speed
    movement = 5
    # main game
    while 1:
        frame += 1
        if leftSpace >= -60:
            leftSpace = leftSpace - movement
            wallup.x = leftSpace
            walldown.x = leftSpace
        else:
            genWall()
            gotPoint = False
            leftSpace = w

        if leftSpace > 0:
            viewPers = (w/leftSpace)

        # up
        wallupL.x = leftSpace
        wallupL.w = math.trunc(wallup.w / viewPers*0.7)
        wallupLC.w = wallupL.w
        wallupLC.x = wallupL.x
        wallupLC.y = wallup.h - wallupLC.h
        # ----
        wallupR.x = leftSpace + wallupL.w
        wallupR.w = wallup.w - wallupL.w
        wallupRC.w = wallupR.w
        wallupRC.x = wallupR.x
        wallupRC.y = wallup.h - wallupRC.h
        # down
        walldownL.x = wallupL.x
        walldownL.w = wallupL.w
        # ----
        walldownR.x = wallupR.x
        walldownR.w = wallupR.w
        # lizard
        lizardRect.x = wallupR.x
        lizardRect.w = wallupR.w
        # gradient effect
        setGradient()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                mousePos = pygame.mouse.get_pos()
                if 5 < mousePos[0] < pointRect.h + 5 and 5 < mousePos[1] < pointRect.h + 5:
                    paused = True
                    reLoop = 1
                    currentMusicPos = int((pygame.mixer.music.get_pos())*2)
                    pygame.mixer.music.unload()
                    pygame.mixer.music.load(
                        r"sounds/StardewValleyOvertureSlow.mp3")
                    pygame.mixer.music.rewind()
                    pygame.mixer.music.play(-1)
                    pygame.mixer.music.set_pos(currentMusicPos/1000)
                    pygame.mixer.Channel(2).play(
                        pygame.mixer.Sound(r"sounds/toolCharge.wav"))
                    while paused == True:
                        if reLoop == 1:
                            window.fill(background)
                            window.blit(pygame.transform.scale(
                                gradient, (w, backgroundRect.h)), backgroundRect)

                            # walls
                            drawWall()
                            # paused text
                            bigTxt = bigFont.render("Paused!", True, (0, 0, 0))
                            bigTxtRect = bigTxt.get_rect()
                            bigTxtRect.center = (w // 2, h // 2)
                            window.blit(bigTxt, bigTxtRect)

                            window.blit(pointTxt, pointRect)
                            # pause icon
                            window.blit(pygame.transform.scale(
                                pauseImg, (pointRect.h, pointRect.h)), (5, h/40))

                            # set bird image
                            window.blit(pygame.transform.rotate(
                                birdFrames[lastI], rotateB), bird)
                            pygame.display.update()
                            reLoop = 2
                        clk.tick(60)
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                pygame.quit()
                                sys.exit()
                            if event.type == pygame.MOUSEBUTTONDOWN:
                                mousePos = pygame.mouse.get_pos()
                                if 5 < mousePos[0] < pointRect.h + 5 and 5 < mousePos[1] < pointRect.h + 5:
                                    bigTxtRect.x = -bigTxtRect.w
                                    currentMusicPos = int((
                                        pygame.mixer.music.get_pos())/2)
                                    pygame.mixer.music.unload()
                                    pygame.mixer.music.rewind()
                                    pygame.mixer.music.load(
                                        r"sounds/StardewValleyOverture.mp3")
                                    pygame.mixer.music.play(-1)
                                    pygame.mixer.music.set_pos(
                                        random.randint(1, 150))
                                    pygame.mixer.Channel(2).play(
                                        pygame.mixer.Sound(r"sounds/toolCharge.wav"))
                                    paused = False

        if pygame.key.get_pressed()[pygame.K_SPACE]:
            # move bird(jump-fly) if space is down
            if bird.y > 0:
                # if the bird is not literally connected to the top side of the screen
                bird.y = math.trunc(bird.y - movement)
                fallShetab = 0
            # bird images
            if i % 5 == 0:
                lastI = int(i/5)
            if i >= (5*(len(birdImages)-1)):
                i = 0
            else:
                i = i + 1
            # rotate bird back to normal
            if rotateB <= 0:
                rotateB += 10
        else:
            # else bird will fall
            fallShetab += 0.25
            bird.y += fallShetab - movement
            # changes the active image of the bird to image[1], it looks better.
            if lastI != 1:
                if i % 5 == 0:
                    lastI = int(i/5)
                if i >= (5*(len(birdImages)-1)):
                    i = 0
                else:
                    i = i + 1
            # rotate bird to down until -90deg
            if rotateB > -90:
                rotateB -= 1

        if bird.x > leftSpace and gotPoint == False:
            # give point for passing the walls
            gotPoint = True
            point = int(point)+1
            pointTxt = Pfont.render(str(point), True, (0, 0, 0))
            pointTxt.set_alpha(128)
            pointRect = pointTxt.get_rect()
            pointRect.center = (w-pointRect.w, pointRect.h)
            # checks current points and hiscore to play a sound for passing hiscore
            if point > hipoint and passedHiPoint == False and hipoint != 0:
                passedHiPoint = True
                pygame.mixer.Channel(1).play(
                    pygame.mixer.Sound(r"sounds/harpsichord_note.wav"))

        # sets collide box for bird to correct location
        birdCollide.center = (bird.x + (bird.w / 2), bird.y + (bird.h / 2))

        # gradient
        window.fill(background)
        window.blit(pygame.transform.scale(
            gradient, (w, backgroundRect.h)), backgroundRect)
        # random parrot sound, 0.2% chance
        if random.randint(1, 500) == 1 and gotPoint == True:
            pygame.mixer.Channel(2).play(
                pygame.mixer.Sound(r"sounds/parrot.wav"))
        # walls
        drawWall()
        if bigTxtRect.x > -bigTxtRect.w:
            # moves texts to left, only runs once pergame on startup
            startRect.x = startRect.x - movement
            bigTxtRect.x = bigTxtRect.x - movement
            highPRect.x = highPRect.x - movement
            window.blit(highPTxt, highPRect)
            window.blit(startTxt, startRect)
            window.blit(bigTxt, bigTxtRect)

        # points
        window.blit(pointTxt, pointRect)
        # pause icon
        window.blit(pygame.transform.scale(
            pauseImg, (pointRect.h, pointRect.h)), (5, h/40))

        # set bird image
        window.blit(pygame.transform.rotate(birdFrames[lastI], rotateB), bird)

        pygame.display.update()
        clk.tick(60)
        pygame.event.pump()
        # see if u touched anythin on touched the floor
        if pygame.Rect.colliderect(birdCollide, walldown) or pygame.Rect.colliderect(birdCollide, wallup) or bird.y > h:
            break  # died here

    # die sfx
    pygame.mixer.Channel(1).play(pygame.mixer.Sound(r"sounds/crit.wav"))

    # loads and sets the hiscore if its passed
    d = shelve.open(r'score')
    if int(point) > int(hipoint):
        d['score'] = point
    d.close()
    while 1:
        frame += 1
        # bird falls down to out of the screen
        if bird.y < h:
            bird.y += fallShetab - movement
            fallShetab += 0.25

        # gameover and stuff
        bigTxt = bigFont.render("GameOver!", True, (215, 56, 14))
        startTxt = font.render("Press R to play again", True, (0, 0, 0))
        highPTxt = Pfont.render(
            ("Score: " + str(point)), True, (0, 0, 0))
        startRect = startTxt.get_rect()
        bigTxtRect = bigTxt.get_rect()
        highPRect = highPTxt.get_rect()

        window.fill(background)
        window.blit(pygame.transform.scale(
            gradient, (w, backgroundRect.h)), backgroundRect)

        drawWall()

        # rotates bird while falling down until -90deg
        if rotateB > -90:
            rotateB -= 1
        # render bird image
        window.blit(pygame.transform.rotate(birdFrames[lastI], rotateB), bird)

        # render gameover and stuff
        bigTxtRect.center = (w // 2, h // 2)
        startRect.center = (
            w // 2, (bigTxtRect.h + bigTxtRect.y + startRect.h))
        highPRect.center = (w//2, bigTxtRect.y - highPRect.h)

        window.blit(startTxt, startRect)
        window.blit(bigTxt, bigTxtRect)
        window.blit(highPTxt, highPRect)

        pygame.display.update()

        # checks R keydown to restart the entire game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    pygame.mixer.Channel(1).play(
                        # restart sound
                        pygame.mixer.Sound(r"sounds/ghost.wav"))
                    # restarting
                    game()
                    return
        clk.tick(60)


game()
