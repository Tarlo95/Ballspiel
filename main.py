import pygame
import random
import sys
import time
import numpy
import math

x = 1920
y = 1080
hand_x = int(x / 2)
hand_y = int(y / 2)
brad = 15
pygame.init()
screen = pygame.display.set_mode([x, y])
screen.fill((0, 0, 0))
zeit = time.time()
zeitBeginn = time.time()
zeitGriffbeginn = time.time()
ballRichtungsaenderung = time.time()
limitGreifen = 4
limitMissmatch = 8
cheat = 0
ballBreite = 15
ball_x = random.randint(ballBreite, x - ballBreite)
ball_y = random.randint(ballBreite, y - ballBreite)
pygame.mouse.set_visible(False)
missmatchvariablen = [-2, -1, -0.5, 0.5, 1, 2]
xMiss = 1
yMiss = 1
änderungszeitMissmatch = 3
änderungszeitMissmatchStart = änderungszeitMissmatch
schriftgroesse = 30
font = pygame.font.SysFont('Consolas', schriftgroesse)
restzeit = 100
trefferquote = 0.8
echteTrefferquote = 0
treffer = 0
laufendeNummerTa = 1
tarray = []
langeTarray = 20

buttonDark = (100, 100, 100)
buttonLight = (170, 170, 170)
farbeHand = (255, 255, 0)

modus = "start"
ersteMal = 1

einstellungenToggle = 0

richtungsAenderungsZeit = 2.5
ballgeschwindigkeit = 1

speedvariablen = [-1, -0.5, -0.25, 0.25, 0.5, 1]


def ballbewegung():
    global ball_x, ball_y, xSpeed, ySpeed, bewegungsCounter, dxSpeed, dySpeed, zielWinkel, aktuellerWinkel, ballgeschwindigkeit, rechts, links, außerhalb, rechts2, links2, außerhalb2, rechteSeite, linkeSeite

    while aktuellerWinkel > math.pi:
        aktuellerWinkel -= math.pi * 2
    while aktuellerWinkel < -math.pi:
        aktuellerWinkel += math.pi * 2
    while zielWinkel > math.pi:
        zielWinkel -= math.pi * 2
    while zielWinkel < -math.pi:
        zielWinkel += math.pi * 2

    if aktuellerWinkel <= 0:
        if aktuellerWinkel < zielWinkel <= aktuellerWinkel + math.pi:
            aktuellerWinkel += 0.25 * ballgeschwindigkeit * math.pi * 2 / 360
        else:
            aktuellerWinkel -= 0.25 * ballgeschwindigkeit * math.pi * 2 / 360
    if aktuellerWinkel >= 0:
        if aktuellerWinkel - math.pi < zielWinkel <= aktuellerWinkel:
            aktuellerWinkel -= 0.25 * ballgeschwindigkeit * math.pi * 2 / 360
        else:
            aktuellerWinkel += 0.25 * ballgeschwindigkeit * math.pi * 2 / 360

    if ball_x <= 10:
        zielWinkel = math.pi - zielWinkel
        aktuellerWinkel = math.pi - aktuellerWinkel
    if ball_x >= x - 10:
        zielWinkel = math.pi - zielWinkel
        aktuellerWinkel = math.pi - aktuellerWinkel
    if ball_y <= 10:
        zielWinkel = abs(zielWinkel)
        aktuellerWinkel = abs(aktuellerWinkel)
    if ball_y >= y - 10:
        zielWinkel = -abs(zielWinkel)
        aktuellerWinkel = -abs(aktuellerWinkel)

    xSpeed = ballgeschwindigkeit * math.cos(aktuellerWinkel)
    ySpeed = ballgeschwindigkeit * math.sin(aktuellerWinkel)
    ball_x += xSpeed
    ball_y += ySpeed


def ta(zahl):
    global laufendeNummerTa, echteTrefferquote, tarray
    if len(tarray) == langeTarray:
        tarray[laufendeNummerTa] = zahl
    else:
        tarray.append(zahl)
    laufendeNummerTa += 1
    if laufendeNummerTa == langeTarray:
        laufendeNummerTa = 1
    echteTrefferquote = numpy.mean(tarray)


def resetGriff():
    global ballRichtungsaenderung, xMiss, yMiss, ersteMal, ball_x, ball_y, limitGreifen, limitMissmatch, restzeit, zeitGriffbeginn, cheat, hand_x, hand_y, änderungszeitMissmatch, trefferquote, echteTrefferquote, treffer, versuche, farbeHand, xSpeed, ySpeed
    hand_x = int(x / 2)
    hand_y = int(y / 2)
    ball_x = random.randint(ballBreite, x - ballBreite)
    ball_y = random.randint(ballBreite, y - ballBreite)
    zeitGriffbeginn = time.time()
    ersteMal = 1
    xMiss=1
    yMiss=1
    Vektor()


def Restart():
    global modus, echteTrefferquote, treffer, laufendeNummerTa, tarray, langeTarray, xMiss, yMiss, ballgeschwindigkeit, änderungszeitMissmatch
    print("joo")
    resetGriff()
    modus = "start"
    echteTrefferquote = 0
    treffer = 0
    laufendeNummerTa = 1
    tarray = []
    langeTarray = 20
    xMiss = 1
    yMiss = 1
    ballgeschwindigkeit = 1
    änderungszeitMissmatch = änderungszeitMissmatchStart


def zeichnen():
    screen.fill((0, 0, 0))
    if modus != "Greifen ohne Zeit" and modus != "start" and modus != "esc":
        screen.blit(font.render(str(round(restzeit, 1)), True, (255, 255, 255)), (1200, 48))
    elif modus != "start" and modus != "esc":
        screen.blit(font.render("kein Zeitlimit", True, (255, 255, 255)), (1200, 48))
    if modus != "start" and modus != "esc":
        pygame.draw.circle(screen, (255, 0, 0), (ball_x, ball_y), brad, 0)
        screen.blit(font.render(str(treffer), True, (255, 255, 255)), (32, 48))
        screen.blit(font.render("Trefferquote: " + str(round(echteTrefferquote, 5)), True, (255, 255, 255)), (800, 48))
        if modus == "Missmatch":
            screen.blit(font.render("Änderungszeit: " + str(round(änderungszeitMissmatch, 2)), True, (255, 255, 255)),
                        (300, 48))
        if modus == "Missmatch mit Geschwindigkeitsanpassung" or modus == "Greifen mit Zeit":
            screen.blit(
                font.render("Ballgeschwindigkeit: " + str(round(ballgeschwindigkeit, 5)), True, (255, 255, 255)),
                (300, 48))
    if modus == "start":
        Button("Modus", x / 2, y / 5, 0)
        Button("Greifen ohne Zeitlimit", x / 4 + 100, y / 4 + 80, 1)
        Button("Greifen mit Zeitlimit und Geschwindigkeitsanpassung", x / 4 * 3 - 100, y / 4 + 80, 1)
        Button("Missmatch mit Missmatchanpassung", x / 4 + 100, y / 3 + 80, 1)
        Button("Missmatch mit Geschwindigkeitsanpassung", x / 4 * 3 - 100, y / 3 + 80, 1)
        Button("Einstellungen", x / 2, 2 * y / 3 - 80, 1)
        if einstellungenToggle:
            Einstellungsfelder("Ballgeschwindigkeit", x / 2, 720, ballgeschwindigkeit)
            Einstellungsfelder("Strecke bis Richtungsänderung", x / 2, 770, richtungsAenderungsZeit)
            Einstellungsfelder("Zeitlimit (Greifen mit Zeit)", x / 2, 820, limitGreifen)
            Einstellungsfelder("Zeitlimit (Missmatch)", x / 2, 870, limitMissmatch)
            Einstellungsfelder("Änderungszeit Missmatch (Anfang)", x / 2, 920, änderungszeitMissmatch)
            Einstellungsfelder("Zieltrefferquote", x / 2, 970, trefferquote)
    if modus == "esc":
        Button("Menü", x / 2, y / 2 - 40, 1)
        Button("Exit", x / 2, y / 2 + 40, 1)

    pygame.draw.circle(screen, farbeHand, (hand_x, hand_y), brad, 0)
    pygame.display.flip()


def Button(text, x, y, colorflip):
    breite = len(text) * 17
    if x - breite / 2 <= hand_x <= x + breite / 2 and y - schriftgroesse / 2 - 3 <= hand_y <= y + schriftgroesse / 2 - 3 and colorflip:
        farbe = buttonLight
    else:
        farbe = buttonDark
    pygame.draw.rect(screen, farbe, [x - breite / 2, y - schriftgroesse / 2 - 3, breite, schriftgroesse + 6])
    screen.blit(font.render(text, True, (255, 255, 255)), (x - breite / 2, y - schriftgroesse / 2))


def Einstellungsfelder(text, x, y, initialwert):
    breite = len(text + "     -  " + str(initialwert) + "  +") * 17
    screen.blit(font.render(text + "     -  " + str(initialwert) + "  +", True, (255, 255, 255)),
                (x - breite / 2, y - schriftgroesse / 2))


def EKLICK(text, x, y, initialwert, schrittgroeße=0.1):
    breite = len(text + "     -  " + str(initialwert) + "  +") * 17
    if x - breite / 2 + len(text + "    ") * 17 <= hand_x <= x - breite / 2 + len(
            text + "     -  ") * 17 and y - schriftgroesse / 2 - 3 <= hand_y <= y + schriftgroesse / 2 - 3:
        return round(initialwert - schrittgroeße, 1)
    elif x - breite / 2 + len(text + "     -  " + str(initialwert) + " ") * 17 <= hand_x <= x - breite / 2 + len(
            text + "     -  " + str(
                    initialwert) + "  +   ") * 17 and y - schriftgroesse / 2 - 3 <= hand_y <= y + schriftgroesse / 2 - 3:
        return round(initialwert + schrittgroeße, 1)
    return initialwert


def MKLICK(text, x, y):
    breite = len(text) * 17
    if x - breite / 2 <= hand_x <= x + breite / 2 and y - schriftgroesse / 2 - 3 <= hand_y <= y + schriftgroesse / 2 - 3:
        return 1
    else:
        return 0


def Vektor():
    global xSpeed, ySpeed, ballRichtungsaenderung, zielWinkel, aktuellerWinkel, ersteMal
    zielWinkel = random.randint(-179, 180) * 2 * math.pi / 360
    if ersteMal == 1:
        aktuellerWinkel = zielWinkel
        ersteMal = 0
        xSpeed = ballgeschwindigkeit * math.cos(zielWinkel)
        ySpeed = ballgeschwindigkeit * math.sin(zielWinkel)
    ballRichtungsaenderung = time.time()


while True:
    pygame.time.wait(1)
    if modus != "start" and modus != "esc":
        ballbewegung()
    zeichnen()
    if modus == "Greifen mit Zeit":
        restzeit = limitGreifen - time.time() + zeitGriffbeginn
    elif modus == "Missmatch" or modus == "Missmatch mit Geschwindigkeitsanpassung":
        restzeit = limitMissmatch - time.time() + zeitGriffbeginn
    else:
        restzeit = 10

    if time.time() - ballRichtungsaenderung > richtungsAenderungsZeit / ballgeschwindigkeit:
        Vektor()

    # Missmatchänderung
    if time.time() - zeit > änderungszeitMissmatch and modus == "Missmatch":
        xMiss = random.choice(missmatchvariablen)
        yMiss = random.choice(missmatchvariablen)
        zeit = time.time()

    if modus == "Missmatch mit Geschwindigkeitsanpassung" and xMiss == 1 and yMiss == 1:
        xMiss = random.choice(missmatchvariablen)
        yMiss = random.choice(missmatchvariablen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and modus != "start" and modus != "esc":
            if abs(hand_x - ball_x) <= 30 and abs(hand_y - ball_y) <= 30:  # man klickt den Ball
                ta(1)
                resetGriff()
                treffer += 1
                if echteTrefferquote > trefferquote:
                    if modus == "Missmatch":
                        if änderungszeitMissmatch >= 0.5:
                            änderungszeitMissmatch -= 0.1
                        elif änderungszeitMissmatch > 0.25:
                            änderungszeitMissmatch -= 0.05
                        elif änderungszeitMissmatch > 0.2:
                            änderungszeitMissmatch -= 0.025
                        else:
                            änderungszeitMissmatch = 0.2
                    if modus == "Missmatch mit Geschwindigkeitsanpassung" and änderungszeitMissmatch > 2:
                        änderungszeitMissmatch -= 0.1
                    if modus == "Missmatch mit Geschwindigkeitsanpassung" or modus == "Greifen mit Zeit":
                        ballgeschwindigkeit += 0.1
        if event.type == pygame.MOUSEBUTTONUP:
            if modus == "start":
                if MKLICK("Menü", x - 50, 30):
                    Restart()
                if MKLICK("Greifen ohne Zeitlimit", x / 4 + 100, y / 4 + 80):
                    modus = "Greifen ohne Zeit"
                    resetGriff()
                if MKLICK("Greifen mit Zeitlimit und Geschwindigkeitsanpassung", x / 4 * 3 - 100, y / 4 + 80):
                    modus = "Greifen mit Zeit"
                    resetGriff()
                if MKLICK("Missmatch mit Missmatchanpassung", x / 4 + 100, y / 3 + 80):
                    modus = "Missmatch"
                    änderungszeitMissmatchStart = änderungszeitMissmatch
                    resetGriff()
                if MKLICK("Missmatch mit Geschwindigkeitsanpassung", x / 4 * 3 - 100, y / 3 + 80):
                    modus = "Missmatch mit Geschwindigkeitsanpassung"
                    resetGriff()
                if MKLICK("Einstellungen", x / 2, 2 * y / 3 - 80):
                    einstellungenToggle = 1
                ballgeschwindigkeit = EKLICK("Ballgeschwindigkeit", x / 2, 720, ballgeschwindigkeit)
                richtungsAenderungsZeit = EKLICK("Strecke bis Richtungsänderung", x / 2, 770, richtungsAenderungsZeit)
                limitGreifen = EKLICK("Zeitlimit (Greifen mit Zeit)", x / 2, 820, limitGreifen)
                limitMissmatch = EKLICK("Zeitlimit (Missmatch)", x / 2, 870, limitMissmatch)
                änderungszeitMissmatch = EKLICK("Änderungszeit Missmatch (Anfang)", x / 2, 920, änderungszeitMissmatch)
                trefferquote = EKLICK("Zieltrefferquote", x / 2, 970, trefferquote)
                xMiss = 1
                yMiss = 1
            if modus == "esc":
                if MKLICK("Menü", x / 2, y / 2 - 40):
                    Restart()
                if MKLICK("Exit", x / 2, y / 2 + 40):
                    sys.exit()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE:
                modus = "esc"
                xMiss = 1
                yMiss = 1

        if event.type == pygame.MOUSEMOTION:
            move = pygame.mouse.get_rel()
            if cheat:
                move = pygame.mouse.get_rel()
                cheat = 0
            if hand_x != 0 or hand_x != x:
                hand_x += move[0] * xMiss
                if hand_x < 0:
                    hand_x = 0
                if hand_x > x:
                    hand_x = x
            if hand_y != 0 or hand_y != y:
                hand_y += move[1] * yMiss
                if hand_y < 0:
                    hand_y = 0
                if hand_y > y:
                    hand_y = y
            mPosition = pygame.mouse.get_pos()
            if abs(hand_x - ball_x) <= 30 and abs(hand_y - ball_y) <= 30:  # Bälle berühren sich
                farbeHand = (0, 255, 0)
            else:
                farbeHand = (255, 255, 20)
            if mPosition[0] <= 50 or mPosition[0] >= x - 50 or mPosition[1] <= 50 or mPosition[
                1] >= y - 50:  # Maus is aus dem bildschirm
                pygame.mouse.set_pos(int(x / 2), int(y / 2))
                cheat = 1
    if restzeit <= 0 and modus != "start" and modus != "Greifen ohne Zeit" and modus != "esc":
        ta(0)
        resetGriff()
        if echteTrefferquote < trefferquote:
            if modus == "Missmatch":
                änderungszeitMissmatch += 0.1
            if modus == "Missmatch mit Geschwindigkeitsanpassung" or modus == "Greifen mit Zeit":
                ballgeschwindigkeit -= 0.1







