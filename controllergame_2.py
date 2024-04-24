import pygame
import sys
import serial
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Set colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
GOLD = (255, 215, 0)

# Define constants
COIN_SIZE = 30
NUM_COINS = 10
COIN_SPEED = 5

# Define Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((COIN_SIZE, COIN_SIZE))
        self.image.fill(GOLD)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - COIN_SIZE)
        self.rect.y = random.randint(0, SCREEN_HEIGHT - COIN_SIZE)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Moving Robot")

clock = pygame.time.Clock()

# Load background image
background_image = pygame.image.load("background_image.jpg").convert()

# Load robot image
robot_image = pygame.image.load("robot_image.png").convert_alpha()
robot_image = pygame.transform.scale(robot_image, (150, 175))  # Scale the robot image
robot_rect = robot_image.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Center the robot
robot_speed = 15

# configure the serial port
ser = serial.Serial(
port='COM10',
baudrate=115200,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_TWO,
bytesize=serial.EIGHTBITS
)
ser.isOpen()


# Loading screen
loading_screen = False
game_running = False

# Define direction constants
DIRECTION_STILL = 0
DIRECTION_FORWARD = 1
DIRECTION_BACKWARD = 2
DIRECTION_RIGHT = 3
DIRECTION_LEFT = 4

# Initialize direction flag
current_direction = DIRECTION_STILL

# Initialize score
score = 0

# Create coins
coins = pygame.sprite.Group()
for _ in range(NUM_COINS):
    coin = Coin()
    coins.add(coin)
    
# Function to interpret instructions and update robot position
def interpret_instructions(instruction):
    global current_direction
    # Split the instruction string by space and extract x and y coordinates
    coordinates = instruction.split()
    if len(coordinates) < 2:
        print("Error: Insufficient coordinates in the instruction:", instruction)
        return  # Exit the function if there are not enough coordinates
    x, y = map(float, coordinates)  
    # Update robot position based on the received coordinates
    if (x, y) == (16, 16):  # Standing still
        current_direction = DIRECTION_STILL
    elif (x, y) == (33, 16):  # Going forward
        current_direction = DIRECTION_FORWARD
    elif (x, y) == (0, 16):  # Going backward
        current_direction = DIRECTION_BACKWARD
    elif (x, y) == (16, 33):  # Going right
        current_direction = DIRECTION_RIGHT
    elif (x, y) == (16, 0):  # Going left
        current_direction = DIRECTION_LEFT

# Game loop
while not game_running:
    # Display "Press SPACEBAR to Start" text on the loading screen
    screen.fill(BLACK)  # Clear the screen before drawing text
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Press SPACEBAR to Start", True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            loading_screen = True
            game_running = True
    pygame.display.flip()  # Update the display

# Loading screen
if loading_screen:
    screen.fill(BLACK)
    # Display "Loading..." text on the loading screen
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Loading...", True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
    # Wait for 3 seconds before starting the game
    pygame.time.wait(3000)

# Game loop
while game_running:
    screen.blit(background_image, (0, 0))  # Show background image

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_running = False

    # Move the robot based on the current direction
    if current_direction == DIRECTION_FORWARD:
        if robot_rect.y - robot_speed >= 0:  # Check if moving forward will keep the robot inside the screen
            robot_rect.y -= robot_speed
    elif current_direction == DIRECTION_BACKWARD:
        if robot_rect.y + robot_speed <= SCREEN_HEIGHT - robot_rect.height:  # Check if moving backward will keep the robot inside the screen
            robot_rect.y += robot_speed
    elif current_direction == DIRECTION_RIGHT:
        if robot_rect.x + robot_speed <= SCREEN_WIDTH - robot_rect.width:  # Check if moving right will keep the robot inside the screen
            robot_rect.x += robot_speed
    elif current_direction == DIRECTION_LEFT:
        if robot_rect.x - robot_speed >= 0:  # Check if moving left will keep the robot inside the screen
            robot_rect.x -= robot_speed

    # Check for collisions with coins
    for coin in coins:
        if robot_rect.colliderect(coin.rect): 
            coins.remove(coin)
            score += 1
            if score >= 10:
                game_running = False

    # Draw the coins
    coins.draw(screen)

    # Read data from serial port
    instruction = ser.readline().decode().strip()
    if instruction:
        interpret_instructions(instruction)

    # Draw the robot
    screen.blit(robot_image, robot_rect)

    pygame.display.flip()
    clock.tick(60)

# Close serial port
ser.close()

# Quit Pygame
pygame.quit()
sys.exit()
