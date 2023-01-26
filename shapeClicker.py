import pygame
import random
import time
import math
import sys

# Initialize pygame
pygame.init()

# Set the window size and caption
size_x = 1920
size_y = 1080
size = (size_x, size_y)
caption = "Pop the Shapes"
screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)  # | pygame.FULLSCREEN
pygame.display.set_caption(caption)


# TODO: Increase speed/size of already spawned shapes while the game is running

class Shape:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def move(self):
        pass

    def draw(self):
        pass

    def is_clicked(self, x, y):
        pass


class Circle(Shape):
    # Class variables
    radius_min = 10
    radius_max = 60
    speed_min = 0
    speed_max = 0.4

    def __init__(self, x, y, color, speed, angle, radius):
        super().__init__(x, y, color)
        self.angle = angle

        if radius > Circle.radius_max:
            self.radius = Circle.radius_max
        elif radius < Circle.radius_min:
            self.radius = Circle.radius_min
        else:
            self.radius = radius

        if speed > Circle.speed_max:
            self.speed = Circle.speed_max
        elif speed < Circle.speed_min:
            self.speed = Circle.speed_min
        else:
            self.speed = speed

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        if self.x < 0 + self.radius or self.x > size[0] - self.radius:
            self.angle = math.pi - self.angle
        if self.y < 0 + self.radius or self.y > size[1] - self.radius:
            self.angle = - self.angle

    def is_clicked(self, x, y):
        return (x - self.x) ** 2 + (y - self.y) ** 2 < self.radius ** 2


class Rectangle(Shape):
    # Class variables
    width_min = 10
    width_max = 60
    height_min = 10
    height_max = 60
    speed_min = 0
    speed_max = 0.4

    def __init__(self, x, y, color, speed, angle, width, height):
        super().__init__(x, y, color)
        self.angle = angle
        self.width = width
        self.height = height

        if width > Rectangle.width_max:
            self.width = Rectangle.width_max
        elif width < Rectangle.width_min:
            self.width = Rectangle.width_min
        else:
            self.width = width

        if height > Rectangle.height_max:
            self.height = Rectangle.height_max
        elif height < Rectangle.height_min:
            self.height = Rectangle.height_min
        else:
            self.height = height

        if speed > Rectangle.speed_max:
            self.speed = Rectangle.speed_max
        elif speed < Rectangle.speed_min:
            self.speed = Rectangle.speed_min
        else:
            self.speed = speed

    def draw(self):
        pygame.draw.rect(screen, self.color,
                         (self.x - self.width / 2, self.y - self.height / 2, self.width, self.height))

    def move(self):
        self.x += self.speed * math.cos(self.angle)
        self.y += self.speed * math.sin(self.angle)
        if self.x < 0 + self.width / 2 or self.x > size[0] - self.width / 2:
            self.angle = math.pi - self.angle
        if self.y < 0 + self.height / 2 or self.y > size[1] - self.height / 2:
            self.angle = - self.angle

    def is_clicked(self, x, y):
        return (self.x - self.width / 2 < x < self.x + self.width / 2) and (
                self.y - self.height / 2 < y < self.y + self.height / 2)


# Note: Minimum speed limit of shapes must be 0 to use "Stationary" mode
# TODO: Not randomized color option
def generate_random_shape(shape_list, shape_movement):
    # Randomly decide to spawn a circle or a rectangle
    shape_type = random.choice(shape_list)
    print(f"Generated shape_type: {shape_type}")

    # Since these are common attributes among shapes, generate them directly without checking type of shape
    x = random.randint(0, size[0])
    y = random.randint(0, size[1])
    color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    # Random shape color mustn't be equal to background color
    while color == background_color:
        print(f"Shape color is same as background color, regenerating color.")
        color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

    if shape_type == "circle":
        radius = random.randint(Circle.radius_min, Circle.radius_max)

        # Initialize movement speed/angle according to game mode
        if shape_movement == "Random":
            # Spawned circle will have the ability to move with a probability of 50%, 50% stationary circle
            can_move = random.randint(0, 1)
            if can_move:
                speed = random.uniform(Circle.speed_min, Circle.speed_max)
                angle = random.uniform(0, 2 * math.pi)
            else:
                speed = 0
                angle = 0
        elif shape_movement == "Stationary":
            speed = 0
            angle = 0
        elif shape_movement == "Movement":
            speed = random.uniform(Circle.speed_min, Circle.speed_max)
            angle = random.uniform(0, 2 * math.pi)

        shape = Circle(x, y, color, speed, angle, radius)

    elif shape_type == "rectangle":
        width = random.randint(Rectangle.width_min, Rectangle.width_max)
        height = random.randint(Rectangle.height_min, Rectangle.height_max)

        # Initialize movement speed/angle according to game mode
        if shape_movement == "Random":
            # Spawned circle will have the ability to move with a probability of 50%, 50% stationary circle
            can_move = random.randint(0, 1)
            if can_move:
                speed = random.uniform(Rectangle.speed_min, Rectangle.speed_max)
                angle = random.uniform(0, 2 * math.pi)
            else:
                speed = 0
                angle = 0
        elif shape_movement == "Stationary":
            speed = 0
            angle = 0
        elif shape_movement == "Movement":
            speed = random.uniform(Rectangle.speed_min, Rectangle.speed_max)
            angle = random.uniform(0, 2 * math.pi)

        shape = Rectangle(x, y, color, speed, angle, width, height)

    return shape


# TODO: Settings menu for shape customization, movement mode, input mode etc.
def settings_menu():
    global screen
    global size
    while True:
        for event1 in pygame.event.get():
            if event1.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        screen.fill(background_color)

        # Create the restart button
        button = pygame.Rect(size[0] // 2 - 50, size[1] // 2 + 50, 90, 30)
        pygame.draw.rect(screen, (255, 0, 0), button)
        button_text = font.render("Start", True, white_color)
        screen.blit(button_text, (size[0] // 2 - 35, size[1] // 2 + 55))

        # Draw the settings menu options on the screen
        pygame.display.update()
        # Check for user input
        for event2 in pygame.event.get():
            # Click button to skip settings menu and start game
            if event2.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event2.pos):
                    return

            if event2.type == pygame.KEYDOWN:
                if event2.key == pygame.K_1:
                    # Change screen size to 800x600
                    size = (800, 600)
                    screen = pygame.display.set_mode(size)
                if event2.key == pygame.K_2:
                    # Change screen size to 1024x768
                    size = (1024, 768)
                    screen = pygame.display.set_mode(size)
                if event2.key == pygame.K_3:
                    # Return to the main menu
                    return
                # Exit
                if event2.key == pygame.K_4:
                    sys.exit(0)


def increase_size_of_shape(shape, size_increase):
    if isinstance(shape, Circle):
        shape.radius += size_increase
    elif isinstance(shape, Rectangle):
        shape.width += size_increase
        shape.height += size_increase
    print(f"Size of spawned shapes increased")


def increase_speed_of_shape(shape, speed_increase):
    shape.speed += speed_increase
    print(f"Speed of spawned shapes increased")


# Fonts/Size of the texts
font = pygame.font.Font(None, 30)

# Set the initial score and spawn time
score = 0
spawn_time = 0.3  # time in seconds
game_time = 10  # time in seconds
endless_game = False
# start_time = time.time()

# Shapes to spawn in game
shapes_to_spawn = ["circle"]  # ["circle"]  # ["circle", "rectangle"]

# Generate a list of circles and rectangles
shapes = []

shape_movement = "Random"  # "Random", "Stationary", "Movement"
input_mode = "Click"  # Move, Click
freeze_when_no_mouse_movement = False
size_increase = 2
speed_increase = 0.2

black_color = (0, 0, 0)
white_color = (255, 255, 255)
red_color = (255, 0, 0)
blue_color = (0, 0, 255)
background_color = black_color

running = True
paused = False
paused_time = 0
end_game_screen = False

settings_menu()

# Set the game timer after the settings menu
start_time = time.time()
last_spawn_time = start_time

# Game loop
while running:
    # Clear the screen
    screen.fill(background_color)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            paused = False
        # Pause game with P key
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                paused = not paused
                # Workaround for stopping timer and spawn timer when game is paused
                if paused:
                    paused_time = time.time()
                else:
                    start_time += (time.time() - paused_time)
                    last_spawn_time -= paused_time

            if running and not paused and not end_game_screen:
                # Increase speed of all spawned shapes
                if event.key == pygame.K_6:
                    for shape in shapes:
                        increase_speed_of_shape(shape, speed_increase)
                # Increase size of all spawned shapes
                elif event.key == pygame.K_7:
                    for shape in shapes:
                        increase_size_of_shape(shape, size_increase)

        # Resize game window
        if event.type == pygame.VIDEORESIZE:
            size = event.size
            screen = pygame.display.set_mode(size, pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)

        # Click or move on shapes to get points
        if input_mode == "Click":
            if event.type == pygame.MOUSEBUTTONDOWN:
                # Get the mouse click coordinates
                x, y = pygame.mouse.get_pos()
                for shape in shapes:
                    if shape.is_clicked(x, y):  # check if the shape was clicked
                        shapes.remove(shape)
                        score += 1
        elif input_mode == "Move":
            # Get the mouse coordinates
            x, y = pygame.mouse.get_pos()
            for shape in shapes:
                if shape.is_clicked(x, y):  # check if the shape was clicked
                    shapes.remove(shape)
                    score += 1

    # End game screen with restart button
    if end_game_screen:
        text = font.render(f"Time's up! Your score is: {score}", True, white_color)
        screen.blit(text, (size[0] // 2 - 130, size[1] // 2))

        # Create the restart button
        restart_button = pygame.Rect(size[0] // 2 - 50, size[1] // 2 + 50, 100, 30)
        pygame.draw.rect(screen, (255, 0, 0), restart_button)
        text_restart = font.render("Restart", True, white_color)
        screen.blit(text_restart, (size[0] // 2 - 35, size[1] // 2 + 55))

        # Reset game attributes
        if event.type == pygame.MOUSEBUTTONDOWN:
            if restart_button.collidepoint(event.pos):
                score = 0
                start_time = time.time()
                shapes = []
                end_game_screen = False
        pygame.display.update()
        continue

    # Show "Paused" message when paused
    if paused:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                paused = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = not paused
        # Display "Paused"
        text = font.render("Paused", True, blue_color)
        screen.blit(text, (size[0] // 2, size[1] // 2))
        pygame.display.update()
        continue

    # # Remove 1 random shape when right mouse button is clicked
    # # TODO: Fix, why this runs multiple times
    # if event.type == pygame.MOUSEBUTTONDOWN:
    #     if event.button == 3:
    #         print(f"AA")
    #         if shapes:
    #             random_circle = random.choice(shapes)
    #             shapes.remove(random_circle)
    #             font = pygame.font.Font(None, 20)
    #             message = font.render("Circle removed", True, (0, 0, 0))
    #             screen.blit(message, (size[0] // 2, 10))
    #         # shapes = []

    if freeze_when_no_mouse_movement:
        for circle in shapes:
            circle.draw()

        if pygame.mouse.get_rel() != (0, 0):
            # Spawn a new shape every x seconds
            if time.time() - last_spawn_time > spawn_time:
                last_spawn_time = time.time()
                shape = generate_random_shape(shapes_to_spawn, shape_movement)
                shapes.append(shape)

            # Move and draw circles and make them bounce on the edges of the screen
            for circle in shapes:
                circle.move()
                # print(f"Circle {circle.x}, {circle.y}")
                if not 0 < circle.x < size_x:
                    circle.angle = math.pi - circle.angle
                if not 0 < circle.y < size_y:
                    circle.angle = - circle.angle
    else:
        # Spawn a new shape every x seconds
        if time.time() - last_spawn_time > spawn_time:
            last_spawn_time = time.time()
            shape = generate_random_shape(shapes_to_spawn, shape_movement)
            shapes.append(shape)

        # Move and draw circles and make them bounce on the edges of the screen
        for circle in shapes:
            circle.move()
            circle.draw()
            # print(f"Circle {circle.x}, {circle.y}")
            if not 0 < circle.x < size_x:
                circle.angle = math.pi - circle.angle
            if not 0 < circle.y < size_y:
                circle.angle = - circle.angle

    # Draw the score
    font = pygame.font.Font(None, 30)
    text = font.render("Score: " + str(score), True, white_color)
    screen.blit(text, (10, 10))

    if endless_game:
        # Draw timer
        text = font.render("Timer: " + str(int((time.time() - start_time))), True, white_color)
        screen.blit(text, (size[0] - 200, 10))
    else:
        # Draw the countdown timer
        remaining_time = game_time - (time.time() - start_time)
        text = font.render("Time remaining: " + str(int(remaining_time)), True, white_color)
        screen.blit(text, (size[0] - 200, 10))

        # Check if game time is up when its not already up
        if not end_game_screen:
            if time.time() - start_time > game_time:
                end_game_screen = True
                print(f"End Game")

    # Update the display
    pygame.display.update()
