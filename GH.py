# This file was created by John Blastos

import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
screen_width, screen_height = 800, 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Game settings
FPS = 60
notes_speed = 5
note_width, note_height = 50, 50
re
# Load assets (replace 'note.png' and 'guitar_sound.mp3' with your own assets)
note_image = pygame.image.load('note.png')  # Replace with your note image
note_image = pygame.transform.scale(note_image, (note_width, note_height))
pygame.mixer.music.load('guitar_sound.mp3')  # Replace with your sound file

# Note class
class Note:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hit = False

    def draw(self, screen):
        screen.blit(note_image, (self.x, self.y))

    def move(self):
        self.y += notes_speed

# Game initialization
clock = pygame.time.Clock()
notes = []
spawn_note_timer = 0
score = 0

# Game loop
running = True
while running:
    screen.fill(BLACK)

    # Spawn notes
    spawn_note_timer += 1
    if spawn_note_timer > FPS:  # spawn a note every second
        spawn_note_timer = 0
        new_note = Note(random.randint(0, screen_width - note_width), -note_height)
        notes.append(new_note)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:  # Press space to simulate strumming
                for note in notes:
                    if note.y > screen_height - 100 and not note.hit:
                        note.hit = True
                        score += 1
                        pygame.mixer.music.play()

    # Update notes
    for note in notes:
        if not note.hit:
            note.move()
        note.draw(screen)

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