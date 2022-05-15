# draw board
import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((2000, 1000))
clock = pygame.time.Clock()
screenColor = pygame.Color("white")
screen.fill(screenColor)
is_running = True
x = 500
y = 500
square_width = 39 * 5 - 0.95
square_height = 39 - 0.95
tile_size = 39
square = pygame.Surface((square_width, square_height))
dragable = True


def within(mouse_x, mouse_y, x, y, width, height):
    return mouse_x > x and mouse_x < x + width and mouse_y > y and mouse_y < y + height


def change_color(surface, color):
    w, h = surface.get_size()
    r, g, b, _ = color
    for x in range(w):
        for y in range(h):
            a = surface.get_at((x, y))[3]
            if surface.get_at((x, y))[0] != 0:
                surface.set_at((x, y), pygame.Color(r, g, b, a))


def snap_to_grid(x, y):
    if x >= 890 or x <= 110 or y >= 890 or y <= 110:
        return x, y
    else:
        if (x - 110) % tile_size > tile_size / 2:
            x = x + tile_size - (x - 110) % tile_size
        else:
            x = x - ((x - 110) % tile_size)
        if (y - 110) % tile_size > tile_size / 2:
            y = y + tile_size - (y - 110) % tile_size
        else:
            y = y - ((y - 110) % tile_size)
    return min(x, 890 - 39), min(y, 890 - 39)


square.fill((255, 0, 0))
pygame.draw.line(square, (0, 0, 0), (0, 0), (square_width, 0))
pygame.draw.line(square, (0, 0, 0), (0, 0), (0, square_height))
pygame.draw.line(
    square, (0, 0, 0), (0, square_height - 1), (square_width - 1, square_height - 1)
)
pygame.draw.line(
    square, (0, 0, 0), (square_width - 1, 0), (square_width - 1, square_height - 1)
)
pygame.draw.line(square, (0, 0, 0), (38.05, 0), (38.05, square_height))
pygame.draw.line(square, (0, 0, 0), (38.05 + 39, 0), (38.05 + 39, square_height))
pygame.draw.line(
    square, (0, 0, 0), (38.05 + 39 * 2, 0), (38.05 + 39 * 2, square_height)
)
pygame.draw.line(
    square, (0, 0, 0), (38.05 + 39 * 3, 0), (38.05 + 39 * 3, square_height)
)
while is_running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            is_running = False
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not within(
            event.pos[0], event.pos[1], x, y, square_width, square_height
        ):
            dragable = False
        if event.type == pygame.MOUSEBUTTONUP:
            dragable = True
            x, y = snap_to_grid(x, y)
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            square = pygame.transform.rotate(square, 90)
            temp = square_width
            square_width = square_height
            square_height = temp

    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_q]:
        change_color(square, pygame.Color("lightblue"))
    if pressed[pygame.K_w]:
        change_color(square, pygame.Color("white"))
    if pressed[pygame.K_e]:
        change_color(square, pygame.Color("orange"))
    if pressed[pygame.K_r]:
        change_color(square, pygame.Color("red"))
    mouse_rel = pygame.mouse.get_rel()
    if pygame.mouse.get_pressed()[0] and dragable:
        x += mouse_rel[0]
        y += mouse_rel[1]

    screen.fill(screenColor)
    pygame.draw.rect(screen, (100, 100, 100), pygame.Rect(100, 100, 800, 800))
    for row in range(20):
        for col in range(20):
            pygame.draw.rect(
                screen,
                (200, 200, 200),
                pygame.Rect(110 + col * 39, 110 + row * 39, 38.05, 38.05),
            )
    screen.blit(square, (x, y))
    pygame.display.flip()
    clock.tick(60)
