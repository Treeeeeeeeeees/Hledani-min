from types import NoneType
from data.parameters import *

def draw_button(display, pos_x, pos_y, size_x, size_y, size_text, text = str()):
    pygame.draw.rect(display, (66, 47, 23), pygame.Rect(pos_x, pos_y, size_x, size_y), 0)
    pygame.draw.rect(display, "white", pygame.Rect(pos_x, pos_y, size_x, size_y), 2)
    font = pygame.font.Font("freesansbold.ttf", size_text)
    text_surface = font.render(text, True, "white")
    textRect = text_surface.get_rect()
    textRect.center = (pos_x + (size_x // 2), pos_y + (size_y // 2))
    display.blit(text_surface, textRect)

def draw_title_screen(display):
        title_text = "Hledání min"
        font = pygame.font.Font("freesansbold.ttf", 4 * w_size)
        text = font.render(title_text, True, "white")
        textRect = text.get_rect()
        textRect.center = (x // 2, 100)
        display.blit(text, textRect)
        draw_button(display, x // 2 - 4 * w_size, y // 2, 8 * w_size, 2 * w_size, w_size, "Nová hra")
        draw_button(display, x // 2 - 4 * w_size, y // 2 + 3 * w_size, 8 * w_size, 2 * w_size, w_size, "Žebříček")
        draw_button(display, x // 2 - 4 * w_size, y // 2 + 6 * w_size, 8 * w_size, 2 * w_size, w_size, "Jak hrát")
        draw_button(display, x // 2 - 4 * w_size, y // 2 + 9 * w_size, 8 * w_size, 2 * w_size, w_size, "Konec")

def draw_other_screens(display):
        pygame.draw.rect(display, (112, 88, 57), pygame.Rect(100, 100, x - 200, y - 200), 0)
        pygame.draw.rect(display, "white", pygame.Rect(100, 100, x - 200, y - 200), 2)
        draw_button(display, 50, 50, 2 * w_size, 2 * w_size, w_size, "<")

def draw_grid(display, rows, columns, start_pos_x, start_pos_y, window_size):
    pygame.draw.rect(display, (66, 47, 23), pygame.Rect(start_pos_x, start_pos_y - 3 * window_size, columns * window_size, 3 * window_size), 0)
    pygame.draw.line(display, (255, 255, 255),(start_pos_x, start_pos_y),(start_pos_x, start_pos_y - 3 * window_size))
    pygame.draw.line(display, (255, 255, 255),(start_pos_x + window_size * columns, start_pos_y),(start_pos_x + window_size * columns, start_pos_y - 3 * window_size))
    pygame.draw.line(display, (255, 255, 255),(start_pos_x, start_pos_y - 3 * window_size),(start_pos_x + window_size * columns, start_pos_y - 3 * window_size))
    
    for i in range(rows + 1):
        pygame.draw.line(display, (255, 255, 255),(start_pos_x, start_pos_y + window_size * i),(start_pos_x + columns * window_size, start_pos_y + window_size * i))
    
    for j in range(columns + 1):
        pygame.draw.line(display, (255, 255, 255),(start_pos_x + window_size * j, start_pos_y),(start_pos_x + window_size * j, start_pos_y + rows * window_size))

def draw_clock(display, isPlaying, time, display_time, start_x, start_y, timing):
    display_time = draw_clock_display(isPlaying, time, display_time, timing)
    font = pygame.font.Font("freesansbold.ttf", w_size)
    text = font.render(display_time, True, "white")
    textRect = text.get_rect()
    textRect.topleft = (start_x + w_size, start_y - 2 * w_size)
    display.blit(text, textRect)

def draw_clock_time(isPlaying, time, timing):

    if isPlaying == True:
        time = time + timing

    return time

def draw_clock_display(isPlaying, time, display_time, timing):
    time_seconds = 0
    time_minutes = 0

    time = draw_clock_time(isPlaying, time, timing)

    time_seconds = int(time)

    if time_seconds >= 60:
        time_minutes = time_seconds // 60 #převod jednotek času z sekund na minuty

        if time_minutes >= 99: #strop minut
            time_minutes = 99
            time_seconds = time_seconds - time_minutes * 60

            if time_seconds >= 60: #strop sekund
                time_seconds = 60
        else:
            time_seconds = time_seconds - time_minutes * 60

    time_minutes = str(time_minutes) #formátování a vykreslení času
    time_seconds = str(time_seconds)
    display_time = time_minutes + " : " + time_seconds
    return display_time

def draw_remaining_bombs(display, start_x, start_y, columns, flagged): #počet zbývajících vlaječek
    flagged_str = str(flagged)
    font = pygame.font.Font("freesansbold.ttf", w_size)
    text = font.render(flagged_str, True, "white")
    textRect = text.get_rect()
    textRect.topleft = (start_x + w_size * (columns - 2), start_y - 2 * w_size)
    display.blit(text, textRect)

def draw_restart(display, gameOverType):
    pygame.draw.rect(display, (112, 88, 57), pygame.Rect(x // 2 - 8 * w_size, y // 2 - 4 * w_size, 16 * w_size, 8 * w_size), 0) #restart okénko
    pygame.draw.rect(display, "white", pygame.Rect(x // 2 - 8 * w_size, y // 2 - 4 * w_size, 16 * w_size, 8 * w_size), 2)
    font = pygame.font.Font("freesansbold.ttf", 2 * w_size)
    text_restart = "Restart"

    if gameOverType == "Win":
        result = "Vyhrál jsi!"
        draw_button(display, x // 2 - 7 * w_size, y // 2 + w_size, 6 * w_size, 2 * w_size, w_size, text_restart)
        draw_button(display, x // 2 + w_size, y // 2 + w_size, 6 * w_size, 2 * w_size, w_size, "Uložit")
    elif gameOverType == "Loss":
        result = "Prohrál jsi!"
        draw_button(display, x // 2 - 3 * w_size, y // 2 + w_size, 6 * w_size, 2 * w_size, w_size, text_restart)

    text = font.render(result, True, "white")
    textRect = text.get_rect()
    textRect.center = (x // 2, y // 2 - 2 * w_size)
    display.blit(text, textRect)

def draw_leaderboard_save(display, name):
    pygame.draw.rect(display, (112, 88, 57), pygame.Rect(x // 2 - 8 * w_size, y // 2 - 4 * w_size, 16 * w_size, 8 * w_size))
    pygame.draw.rect(display, "white", pygame.Rect(x // 2 - 8 * w_size, y // 2 - 4 * w_size, 16 * w_size, 8 * w_size), 2)
    draw_button(display, x // 2 - 7 * w_size, y // 2 + w_size, 6 * w_size, 2 * w_size, w_size, "Zpět")
    draw_button(display, x // 2 + w_size, y // 2 + w_size, 6 * w_size, 2 * w_size, w_size, "Uložit")
    draw_button(display, x // 2 - 7 * w_size, y // 2 - w_size, 14 * w_size, w_size, w_size, name)
    font = pygame.font.Font("freesansbold.ttf", w_size)
    text = font.render("Jméno (max. 20 znaků):", True, "white")
    textRect = text.get_rect()
    textRect.topleft = (x // 2 - 7 * w_size, y // 2 - 2 * w_size)
    display.blit(text, textRect)


def draw_leaderboard_full(display):
    pygame.draw.rect(display, (66, 47, 23), pygame.Rect(150, 120 , x - 2 * 150, 240), 0)
    pygame.draw.rect(display, "white", pygame.Rect(150, 120 , x - 2 * 150, 240), 2)
    pygame.draw.line(display, (255, 255, 255),(x - 226, 120),(x - 226, 360))
    draw_button(display, x / 2 - 4 * w_size ,y - 150 - 2 * w_size, 8 * w_size, 2 * w_size, w_size, "Vyčistit")
    file = open("data/leaderboard.json")
    data = json.load(file)
    current_leaderboard = data["Leaderboard"]
    font = pygame.font.Font("freesansbold.ttf", w_size)

    for i in range(12):

        if i != 11:
            pygame.draw.line(display, (255, 255, 255),(150, 140 + i * w_size),(x - 151, 140 + i * w_size))

        try:
            current_point = current_leaderboard[i]
            current_name = current_point["name"]
            current_display_time = current_point["display_time"]
            text_name = font.render(current_name, True, "white")
            text_display_time = font.render(current_display_time, True, "white")
            textRect_name = text_name.get_rect()
            textRect_name.topleft = (160, 120 + i * w_size)
            textRect_display_time = text_display_time.get_rect()
            textRect_display_time.topleft = (x - 216, 120 + i * w_size)
            display.blit(text_name, textRect_name)
            display.blit(text_display_time, textRect_display_time)

        except IndexError:
            pass

def draw_parameters(display, num_input, difficulty):
    parameters = ["Řádky (10-23):", "Sloupce (10-30):", "Počet Bomb:"]

    for i in range(3):
        font = pygame.font.Font("freesansbold.ttf", w_size)
        text = font.render(parameters[i], True, "white")
        textRect = text.get_rect()
        textRect.topleft = (x // 2 - 5 * w_size, y // 2 - w_size + (3 * i - 2) * w_size - 4 * w_size)
        display.blit(text, textRect)
        if i == 2:
            difficulties = ["Lehké:", "Střední:", "Těžké:"]
            for j in range(3):
                text = font.render(difficulties[j], True, "white")
                textRect.topleft = (x // 2 - (10 - 7 * j) * w_size, y // 2 - w_size + (3 * i) * w_size - 4 * w_size)
                display.blit(text, textRect)
                draw_button(display, x // 2 - (10 - 7 * j) * w_size, y // 2 - w_size + (3 * i + 1) * w_size - 4 * w_size, 6 * w_size,2 * w_size, w_size, str(difficulty[j]))
        else:
            draw_button(display, x // 2 - 5 * w_size, y // 2 - w_size + (3 * i - 1) * w_size - 4 * w_size, 10 * w_size, w_size, w_size, num_input[i])

def calculate_difficulty(rows, columns):
    difficulty = []

    for i in range(3):
        current_difficulty = int(rows * columns * (1 / (10 - 2 * i)))
        difficulty.append(current_difficulty)
    
    return difficulty