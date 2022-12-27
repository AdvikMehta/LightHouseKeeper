# Imports
import pygame
import math
import os
from pygame import mixer
from shapely.geometry import LineString
from shapely.geometry import Point

# Init
pygame.init()
os.environ["SDL_VIDEO_CENTERED"] = "1"
boundsX = 960
boundsY = 540
clock = pygame.time.Clock()
screen = pygame.display.set_mode((boundsX, boundsY))
pygame.display.set_caption("Lighthouse Keeper and the Shadow Pirates")
icon = pygame.image.load("LightHouse/Sprites/icon.png")
pygame.display.set_icon(icon)

# Images
gamebg = pygame.image.load("LightHouse/Backgrounds/sb2.png")
lighthouse = pygame.image.load("LightHouse/Lighthouse/0.png")
player_down_left = pygame.image.load("LightHouse/Player/ship_down_left.png")
player_down_right = pygame.image.load("LightHouse/Player/ship_down_right.png")
player_up_left = pygame.image.load("LightHouse/Player/ship_up_left.png")
player_up_right = pygame.image.load("LightHouse/Player/ship_up_right.png")
player = player_down_right
title = pygame.image.load("LightHouse/Sprites/title.png")
gameover = pygame.image.load("LightHouse/Sprites/gameover.png")
menubg = pygame.image.load("LightHouse/Backgrounds/menubg.png")
settingsbg = pygame.image.load("LightHouse/Backgrounds/settingsbg.png")
gameoverbg = pygame.image.load("LightHouse/Backgrounds/gameoverbg.png")
pausebg = pygame.image.load("LightHouse/Backgrounds/pausebg.png")
button = pygame.image.load("LightHouse/Sprites/0.png")
buttonsel = pygame.image.load("LightHouse/Sprites/1.png")
arrow = pygame.image.load("LightHouse/Player/arrow.png")
ball = pygame.image.load("LightHouse/Sprites/target.png")
invalidball = pygame.image.load("LightHouse/Sprites/invalidtarget.png")
tile = pygame.image.load("LightHouse/Sprites/10.png")
playerMap = pygame.image.load("LightHouse/Sprites/map.png").convert_alpha()
playerarrow = pygame.image.load("LightHouse/Sprites/arrow.png")

# Music and sounds
bgmusic = mixer.music.load("LightHouse/Music/menumusic.wav")  # using music and not sound
mixer.music.play(-1)
click = mixer.Sound("LightHouse/Music/click.wav")

# Variables
bgwidth = 6704
bgheight = 3944
targetX = -1
targetY = -1
mouseX = 0
mouseY = 0
mapX = 730
mapY = 370
arrowX = 820
arrowY = 435
lightX = 225
lightY = 218
spawnX = 460
spawnY = 250
playerX = spawnX
playerY = spawnY
pointX = 0
pointY = 0
bgX = -2875
bgY = -1700
m = False
s = False
transparency = 128
gamerunning = True
menurunning = True
settingsrunning = True
reached = True
last = 0
dec = False
inc = True
bg = 0
dx = 0
dy = 0
bgXCopy = 0
bgYCopy = 0
uplimit = False
downlimit = False
edgeleft = False
edgeright = False

def blitMenuButtons(x, y):
    if 407 < x < 576 and 248 < y < 312:
        screen.blit(buttonsel, (407, 248))
    else:
        screen.blit(button, (407, 248))
    if 407 < x < 576 and 323 < y < 390:
        screen.blit(buttonsel, (407, 323))
    else:
        screen.blit(button, (407, 323))
    screen.blit(title, (262, 28))
def showMenuText():
    font = pygame.font.Font("LightHouse/Fonts/slkscr.ttf", 32)
    play = font.render("Play", True, (255, 255, 255))
    settings = font.render("Settings", True, (255, 255, 255))
    screen.blit(play, (445, 260))
    screen.blit(settings, (410, 332))
def blitSettingsButtons(x, y):
    if 406 < x < 575 and 209 < y < 259:
        screen.blit(buttonsel, (406, 209))
    else:
        screen.blit(button, (406, 209))
    if 406 < x < 575 and 267 < y < 317:
        screen.blit(buttonsel, (406, 267))
    else:
        screen.blit(button, (406, 267))
    if 406 < x < 575 and 473 < y < 523:
        screen.blit(buttonsel, (406, 473))
    else:
        screen.blit(button, (406, 473))
def showSettingsText():
    font = pygame.font.Font("LightHouse/Fonts/slkscr.ttf", 32)
    if m:
        music = font.render("Music", True, (63, 51, 51))
    else:
        music = font.render("Music", True, (255, 255, 255))
    if s:
        soundfx = font.render("Soundfx", True, (63, 51, 51))
    else:
        soundfx = font.render("Soundfx", True, (255, 255, 255))
    settings = font.render("Settings", True, (255, 255, 255))
    back = font.render("Back", True, (255, 255, 255))
    screen.blit(music, (435, 220))
    screen.blit(soundfx, (410, 280))
    screen.blit(settings, (410, 50))
    screen.blit(back, (448, 483))
def rotateShip():
    global player, last, dec, inc
    if last > 10:
        dec = True
        inc = False
    elif last < -5:
        inc = True
        dec = False

    if inc:
        last += 0.3
    elif dec:
        last -= 0.3
    player = pygame.transform.rotate(player, last)
    return player
def showMenu():
    global menurunning, targetX, targetY, gamerunning, settingsrunning
    while menurunning:
        screen.blit(menubg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                menurunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    menurunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and 407 < targetX < 576 and 248 < targetY < 312:
                    gamerunning = True
                    targetX = -1
                    targetY = -1
                    showGame()
                if event.button == 1 and 407 < targetX < 576 and 323 < targetY < 390:
                    settingsrunning = True
                    showSettings()

        targetX, targetY = pygame.mouse.get_pos()

        blitMenuButtons(targetX, targetY)
        showMenuText()
        pygame.display.update()
def redrawGameWindow():
    global player, reached, last
    # Direction
    if math.sqrt(((targetX - playerX) ** 2) + ((targetY - playerY) ** 2)) < 10:
        if targetX < playerX:
            player = player_down_left
        else:
            player = player_down_right
        reached = True
        rotateShip()
    else:
        reached = False
        last = 0
        if targetX > playerX and targetY < playerY:
            player = player_up_right
        elif targetX < playerX and targetY < playerY:
            player = player_up_left
        elif targetX > playerX and targetY > playerY:
            player = player_down_right
        elif targetX < playerX and targetY > playerY:
            player = player_down_left

    blitArrow()
    screen.blit(player, (int(playerX), int(playerY)))


    clock.tick(60)
    pygame.display.update()
def blitArrow():
    global pointX, pointY
    # Finding point
    point = Point(int(playerX + 12), int(playerY + 15))
    circle = point.buffer(20).boundary
    line = LineString([(mouseX, mouseY), (int(playerX + 12), int(playerY + 15))])
    intersect = circle.intersection(line)

    try:
        pointX = intersect.x
        pointY = intersect.y
    except AttributeError:
        pass

    # Rotation
    arrow_copy = arrow.copy()
    playerarrow_copy = playerarrow.copy()
    rel_x, rel_y = mouseX - pointX, mouseY - pointY
    angle = (180 / math.pi) * -math.atan2(rel_y, rel_x)
    arrow_copy = pygame.transform.rotate(arrow_copy, angle)
    playerarrow_copy = pygame.transform.rotate(playerarrow_copy, angle - 90)

    screen.blit(playerMap, (mapX, mapY))
    screen.blit(playerarrow_copy, (int(arrowX), int(arrowY)))

    if angle > 90:
        angle = 180 - angle
    rad = angle * math.pi / 180
    perp = abs(41 * math.sin(rad))
    base = abs(41 * math.cos(rad))

    if mouseX < pointX and mouseY < pointY:
        screen.blit(arrow_copy, (int(pointX - base), int(pointY - perp)))
    elif mouseX < pointX and mouseY > pointY:
        screen.blit(arrow_copy, (int(pointX - base), int(pointY)))
    elif mouseX > pointX and mouseY < pointY:
        screen.blit(arrow_copy, (int(pointX), int(pointY - perp)))
    else:
        screen.blit(arrow_copy, (int(pointX), int(pointY)))
def checkBounds():
    global playerX, bgX, bgY, targetX, targetY, bgXCopy, bgYCopy, uplimit, downlimit, edgeleft, edgeright
    # Background Bounds
    if bgX > 0:
        bgX = 0
        edgeleft = True
    if bgY > 0:
        bgY = 0
        uplimit = True
    if bgX < -(bgwidth - boundsX):
        bgX = -(bgwidth - boundsX)
        edgeright = True
    if bgY < -(bgheight - boundsY):
        bgY = -(bgheight - boundsY)
        downlimit = True
    '''# Player Bounds
    distance = math.sqrt((((spawnX + 2875) - (playerX + abs(bgX))) ** 2) + (((spawnY + 1575) - (playerY + abs(bgY))) ** 2))
    print(distance)
    if distance > 2500:
        print("Out of bounds")
        if abs(bgX) > 2875:
            edgeright = True
        else:
            edgeleft = True
        # bgX = bgXCopy
        # bgY = bgYCopy
    # bgXCopy = bgX
    # bgYCopy = bgY'''

    moveShip()
def moveShip():
    global reached, targetX, targetY, bgX, bgY, dx, dy, uplimit, downlimit, edgeleft, edgeright, arrowX, arrowY
    if not reached and targetX >= 0 and targetY >= 0:
        radians = math.atan2(targetY - playerY, targetX - playerX)
        dx = math.cos(radians)
        dy = math.sin(radians)
        bgXChange = dx * 10
        bgYChange = dy * 10
        if not (uplimit or downlimit or edgeleft or edgeright):
            bgX -= bgXChange
            bgY -= bgYChange
            targetX -= bgXChange
            targetY -= bgYChange
            arrowX += dx * 0.29
            arrowY += dy * 0.35
            screen.blit(ball, (int(targetX) - 13, int(targetY) - 12))
        else:
            screen.blit(invalidball, (int(targetX) - 13, int(targetY) - 12))
        if uplimit and targetY - 12 > playerY:
            uplimit = False
        if downlimit and targetY - 12 < playerY:
            downlimit = False
        if edgeleft and targetX - 13 > playerX:
            edgeleft = False
        if edgeright and targetX - 13 < playerX:
            edgeright = False
def showGame():
    global gamerunning, menurunning, settingsrunning, reached, lightX, lightY, playerX, playerY, player, last, targetX, targetY, pointX, pointY, bg,\
        boundsX, boundsY, bgX, bgY, mouseX, mouseY
    while gamerunning:
        screen.blit(gamebg, (int(bgX), int(bgY)))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gamerunning = False
                menurunning = False
                settingsrunning = False
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    gamerunning = False
                    menurunning = False
                    settingsrunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    targetX, targetY = pygame.mouse.get_pos()

        mouseX, mouseY = pygame.mouse.get_pos()

        checkBounds()
        redrawGameWindow()
def showSettings():
    global settingsrunning, menurunning, gamerunning, targetX, targetY, s, m

    while settingsrunning:
        screen.blit(settingsbg, (0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                settingsrunning = False
                menurunning = False
                gamerunning = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    settingsrunning = False
                    menurunning = False
                    gamerunning = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and 406 < targetX < 575 and 209 < targetY < 259:
                    if m:
                        m = False
                        pygame.mixer.music.unpause()
                    else:
                        m = True
                        pygame.mixer.music.pause()
                if event.button == 1 and 406 < targetX < 575 and 267 < targetY < 317:
                    if s:
                        s = False
                        click.play()
                    else:
                        s = True
                if event.button == 1 and 406 < targetX < 575 and 473 < targetY < 523:
                    settingsrunning = False

        targetX, targetY = pygame.mouse.get_pos()
        blitSettingsButtons(targetX, targetY)
        showSettingsText()
        pygame.display.update()

showMenu()
