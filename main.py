# This file was created by John Blastos

import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 1000, 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

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

# Load assets (replace 'note.jpg' and 'master_of_puppets.mp3' with your own assets)
note_image = pygame.image.load('note.jpg')  # Replace with your note image
note_image = pygame.transform.scale(note_image, (note_width, note_height))
pygame.mixer.music.load('master_of_puppets.mp3')  # Replace with your music file
pygame.mixer.music.play(-1)  # Play the music indefinitely

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

# Define note spawn positions
note_positions = [(100, 1), (300, 2), (500, 3), (700, 4)]  # (X position, Column number: 1, 2, 3, 4)

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Draw hit bar
    pygame.draw.rect(screen, RED, (0, hit_bar_y, screen_width, 5))

    # Spawn notes
    spawn_note_timer += 3
    if spawn_note_timer > current_spawn_interval:  # Gradually decrease spawn interval
        spawn_note_timer = 0
        x_pos, column = random.choice(note_positions)
        new_note = Note(x_pos, -note_height, column)
        notes.append(new_note)
        current_spawn_interval -= spawn_interval_decrement  # Decrement spawn interval
        notes_speed += speed_increment  # Increment note speed

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

    # Update and check notes
    for note in notes:
        if not note.hit and not note.missed:
            note.move()
            if note.y > screen_height and not note.hit:
                note.missed = True
                score -= 5
        if not note.missed:
            note.draw(screen)

    # Remove missed and hit notes
    notes = [note for note in notes if not note.hit and not note.missed]

    # Display score
    font = pygame.font.SysFont(None, 36)
    score_text = font.render(f'Score: {score}', True, WHITE)
    screen.blit(score_text, (10, 10))

    # Update display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(FPS)

# Quit the game
pygame.quit()