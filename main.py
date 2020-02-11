import random
import time as tm
import string
import pygame
from pygame.locals import *
from textinput import TextInput as pygame_textinput

BLACK = (0,0,0)
RED = (220,0,5)
WHITEBLUE = (220,220,255)
BLUE = (20,20,255)
GREEN = (0,255,0)
YELLOW = (255,255,0)

pygame.init()
pygame.font.init()
pygame.display.set_caption("Typing speedtest".upper())
screen = pygame.display.set_mode((800,500))
clock = pygame.time.Clock()

headerFont = pygame.font.SysFont("poorrichard", 50)
typingFont = pygame.font.SysFont(None, 24)
timerFont = pygame.font.SysFont("berlinsansfb", 36)
finisedFont = pygame.font.SysFont("berlinsansfb", 40)

def load_sentence():
    with open("sentences.txt", "r", encoding='utf-8') as f:
        data = f.read().split("\n")
    sentence = random.choice(data)
    return sentence

def title_text():
    header = headerFont.render("TYPING SPEED TEST", True, RED)
    h_rect = header.get_rect()
    h_rect_c = pygame.Rect(h_rect).centerx
    screen.blit(header, (800/2-h_rect_c, 50))

def timer_start():
    t1 = tm.time()
    return t1

def timer(t1, go):
    if go:
        t2 = tm.time()
        return round(t2-t1,2)
    return 0

def sentence_box(sent, timer, sentPos=0):
    title_text()
    pygame.draw.rect(screen, (255,255,255),[45,130, 700, 50], 1)
    pygame.draw.rect(screen, (255,255,255),[45,250, 700, 50], 1)

    textToWrite = typingFont.render(sent, True, WHITEBLUE)
    screen.blit(textToWrite, (60, 145))

    textFill = typingFont.render(sent[:sentPos], True, YELLOW)
    screen.blit(textFill, (60, 145))

    textTimer = timerFont.render(str(timer), True, BLUE)
    screen.blit(textTimer, (370, 195))

def compare_texts(txt1, txt2):
    pos = len(txt2)
    txt1Letters = list(txt1)
    txt2Letters = list(txt2)
    return txt1Letters[:pos] == txt2Letters

def accuracy(qty, pos):
    x, y = 400, 250
    if pos > 0: perc = 100-(qty/pos*100)
    else: perc = 100.0
    percFails = str(round(perc, 1))+"%"
    headerPercFails = typingFont.render("% ACCURACY", True, (255,255,255))
    screen.blit(headerPercFails, (x-305, y+110))
    textPercFails = typingFont.render(percFails, True, (255,255,255))
    screen.blit(textPercFails, (x-270, y+150))
    if perc < 100:
        circFail = pygame.draw.circle(screen, RED, (150, 385), 70, 2)
    else:
        circFail = pygame.draw.circle(screen, GREEN, (150, 385), 70, 2)

def charmin(charminute=0):
    x, y = 400, 250
    headerCharmin = typingFont.render("CHARS/MIN", True, (255,255,255))
    screen.blit(headerCharmin, (x+162, y+110))
    textCharmin = typingFont.render(str(charminute), True, (255,255,255))
    screen.blit(textCharmin, (x+190, y+150))
    pygame.draw.circle(screen, GREEN, (x+210, y+135), 70, 2)

def difference(txt1, txt2, t):
    qty = 0
    qty_previous = 0
    pos = len(txt2)
    txt1Letters = list(txt1)
    txt2Letters = list(txt2)
    for idx in range(pos):
        if idx < len(txt1) and txt1[idx] != txt2[idx]:
            qty +=1
    accuracy(qty, pos)
    if pos > 0:
        try:
            typesPerMin = round(pos/(int(t)/60),2)
        except:
            typesPerMin = 0
        charmin(typesPerMin)
    else:
        charmin(0)
        t1 = timer_start()

while True:
    textinput = pygame_textinput()
    textinput.text_color = WHITEBLUE
    sentence = load_sentence()
    t1 = timer_start()
    writtenText = ""
    start = False
    finished = False

    while not finished:
        clock.tick(60)
        screen.fill(BLACK)
        events = pygame.event.get()
        if start and len(writtenText) == 0:
            t1 = timer_start()
            start = False
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                start = True
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_F2:
                    sentence = load_sentence()
        textinput.update(events)
        screen.blit(textinput.get_surface(), (60, 265))
        writtenText = textinput.get_text()
        difference(sentence, writtenText, timer(t1, start))
        if not compare_texts(sentence, writtenText):
            textinput.text_color = RED
        else:
            textinput.text_color = GREEN
        sentence_box(sentence, timer(t1, start), len(writtenText))
        if len(list(writtenText)) >= len(list(sentence)):
            finished = True
            rect = pygame.Rect(10, 10, 600, 400)
            screenFinish = screen.copy()
        pygame.display.flip()

    moveY=0
    while finished:
        if moveY > 500:
            moveY = 0
        moveY += 2
        clock.tick(30)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                if event.key == pygame.K_y:
                    finished = False

        screen.blit(screenFinish, (0,0))
        textFinished1 = finisedFont.render("TO RESTART PRESS Y", True, (255,255,0))
        screen.blit(textFinished1, (195, moveY))
        textFinished2 = finisedFont.render("ESC TO QUIT", True, (255,255,0))
        screen.blit(textFinished2, (265, moveY+40))

        pygame.display.flip()

pygame.quit()