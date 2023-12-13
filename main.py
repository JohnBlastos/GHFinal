# This file was created by John Blastos

import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 1025, 900
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 225)

# Game settings
FPS = 60
note_width, note_height = 50, 50
hit_bar_y = screen_height - 50  # Y position of the hit bar
hit_window = 100  # Increased window for hitting a note

# Additional settings for gradual speed increase
initial_spawn_interval = 60  # Initial spawn interval (in frames)
final_spawn_interval = 15    # Final spawn interval (in frames)
spawn_interval_decrement = (initial_spawn_interval - final_spawn_interval) / (FPS * 60 * 8.5)  # Gradual decrement over 8.5 minutes
current_spawn_interval = initial_spawn_interval

initial_note_speed = 5       # Initial note speed
final_note_speed = 10        # Final note speed
speed_increment = (final_note_speed - initial_note_speed) / (FPS * 60 * 8.5)  # Gradual increment over 8.5 minutes
notes_speed = initial_note_speed

# Load assets
note_image = pygame.image.load('Note.png') 
note_image = pygame.transform.scale(note_image, (note_width, note_height))
# set background------------------------------------------------------------------------------------------------------------------------------------
background_image = pygame.image.load('background.png') 
#---------------------------------------------------------------------------------------------------------------------------------------------------
pygame.mixer.music.load('master_of_puppets.mp3')
pygame.mixer.music.play(-1) 

# Note class
class Note:
    def __init__(self, x, y, column):
        self.x = x
        self.y = y
        self.column = column
        self.hit = False
        self.missed = False

    def draw(self, screen):
        if not self.hit and not self.missed:
            screen.blit(note_image, (self.x, self.y))

    def move(self):
        self.y += notes_speed

    def check_hit(self, hit_bar_y, hit_window):
        return hit_bar_y - hit_window <= self.y <= hit_bar_y + hit_window

    def check_missed(self, screen_height):
        if self.y > screen_height and not self.hit:
            self.missed = True
            return True
        return False

# Game initialization
clock = pygame.time.Clock()
notes = []
spawn_note_timer = 0
score = 0
notes_hit = 0
notes_missed = 0
current_streak = 0
highest_streak = 0

# Define note spawn positions
note_positions = [(320, 1), (447, 2), (575, 3), (700, 4)]  # (X position, Column number: 1, 2, 3, 4)

# 8:35 of song until end game
game_duration = 8 * 60 + 35  # 8 minutes and 35 seconds in seconds
start_time = pygame.time.get_ticks()  # Start time of the game


# DRAW MENU
def draw_menu(screen, selected_option):
    screen.fill(BLACK)
    font = pygame.font.SysFont(None, 48)

    # Menu options
    play_text = font.render('Play', True, WHITE if selected_option == 'play' else RED)
    tutorial_text = font.render('Tutorial', True, WHITE if selected_option == 'tutorial' else RED)

    # Arrow or pointer for the selected option
    arrow_font = pygame.font.SysFont(None, 60)
    arrow_text = arrow_font.render('->', True, WHITE)

    # Calculate positions
    play_text_pos = (screen_width // 2 - play_text.get_width() // 2, screen_height // 2 - 50)
    tutorial_text_pos = (screen_width // 2 - tutorial_text.get_width() // 2, screen_height // 2 + 50)
    arrow_pos = (play_text_pos[0] - 60, play_text_pos[1]) if selected_option == 'play' else (tutorial_text_pos[0] - 60, tutorial_text_pos[1])

    # Draw menu options and arrow
    screen.blit(play_text, play_text_pos)
    screen.blit(tutorial_text, tutorial_text_pos)
    screen.blit(arrow_text, arrow_pos)

    # Instructions for navigation and selection
    instructions_font = pygame.font.SysFont(None, 36)
    instructions_text = instructions_font.render('Use Arrow Keys to Navigate, Enter to Select', True, WHITE)
    screen.blit(instructions_text, (screen_width // 2 - instructions_text.get_width() // 2, screen_height - 40))

    pygame.display.flip()

def show_tutorial(screen):
    running = True
    while running:
        screen.fill(BLACK)
        font = pygame.font.SysFont(None, 28)
        tutorial_text = font.render('Tutorial: Press keys 1, 2, 3, 4 to hit notes when they hit the red line. Close this window to go to Menu', True, WHITE)
        screen.blit(tutorial_text, (50, screen_height // 2))
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

# Menu loop
menu_option = 'play'
in_menu = True
while in_menu:
    draw_menu(screen, menu_option)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                menu_option = 'tutorial' if menu_option == 'play' else 'play'
            elif event.key == pygame.K_RETURN:
                if menu_option == 'play':
                    pygame.mixer.music.play(-1)  # Start playing the music when the game starts
                    in_menu = False
                else:
                    show_tutorial(screen)

# Game loop
running = True
start_time = pygame.time.get_ticks()  # Start time of the game

while running:
    current_time = pygame.time.get_ticks()
    elapsed_time = (current_time - start_time) / 1000

    if elapsed_time > game_duration:
        break

    # Draw the background image
    screen.blit(background_image, (0, 0))

    # Calculate progress
    progress = elapsed_time / game_duration
    progress_bar_width = progress * screen_width

    # Draw hit bar
    pygame.draw.rect(screen, RED, (0, hit_bar_y, screen_width, 5))

    # Draw progress bar
    pygame.draw.rect(screen, BLUE, (0, 0, progress_bar_width, 20))

    # Spawn notes
    spawn_note_timer += 3.5 # number of notes per second spawned. Made 3.5 a second to match Master of Puppets 105 bpm
    if spawn_note_timer > current_spawn_interval:
        spawn_note_timer = 0
        x_pos, column = random.choice(note_positions)
        new_note = Note(x_pos, -note_height, column)
        notes.append(new_note)
        current_spawn_interval -= spawn_interval_decrement
        notes_speed += speed_increment

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key in [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4]:
                column = event.key - pygame.K_1 + 1
                note_hit = False
                for note in reversed(notes):  # Iterate in reverse order
                    if note.column == column and note.check_hit(hit_bar_y, hit_window) and not note.hit:
                        note.hit = True
                        score += 10
                        note_hit = True
                        break  # Stop after hitting the bottom-most note
                if not note_hit:  # Subtract points if no note is hit
                    score -= 15
                    notes_missed += 1
                    current_streak = 0

    # Update and check notes
    for note in notes:
        if not note.hit and not note.missed:
            note.move()
            if note.y > screen_height and not note.hit:
                note.missed = True
                score -= 5
                notes_missed += 1
                current_streak = 0
        if not note.missed:
            note.draw(screen)

        if note.hit:
            notes_hit += 1
            current_streak += 1
            highest_streak = max(highest_streak, current_streak)

    # Display score and counters
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    hit_text = font.render(f'Notes Hit: {notes_hit}', True, WHITE)
    missed_text = font.render(f'Notes Missed: {notes_missed}', True, WHITE)
    streak_text = font.render(f'Current Streak: {current_streak} (Best: {highest_streak})', True, BLACK)

    screen.blit(score_text, (10, 30))
    screen.blit(hit_text, (10, 70))
    screen.blit(missed_text, (10, 110))
    screen.blit(streak_text, (10, 150))

    # Remove missed and hit notes
    notes = [note for note in notes if not note.hit and not note.missed]

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Game End
print("Game Over")
print(f"Final Score: {score}")
print(f"Notes Hit: {notes_hit}")
print(f"Notes Missed: {notes_missed}")
print(f"Highest Streak: {highest_streak}")

# Quit the game
pygame.quit()