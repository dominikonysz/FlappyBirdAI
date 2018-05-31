import entities

import pygame
from pygame import gfxdraw
import random as r

# pygame variables
screen = 0
screen_size = 300, 400

ticks_per_frame = 1

bird_color = (200, 200, 200)
obstacle_color = (255, 255, 255)

# game variabels
birds = []
dead_birds = []
obstacles = []

movement_speed = 3

# genetic algorithm variabels
num_gen = 0

def init():
    global screen

    pygame.init()
    screen = pygame.display.set_mode(screen_size)

    create_obstacle()
    birds.append(entities.Bird())


def main():
    global ticks_per_frame
    init()

    clock = pygame.time.Clock()

    running = True
    while running:
        clock.tick(60)  # limit fps
        # events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_SPACE:
                    print("change cycles")
                    if ticks_per_frame == 1:
                        ticks_per_frame = 10
                    elif ticks_per_frame == 10:
                        ticks_per_frame = 100
                    elif ticks_per_frame == 100:
                        ticks_per_frame = 1
                if event.key == pygame.K_s:
                    new_generation()
                if event.key == pygame.K_k:
                    kill_birds()
                if event.key == pygame.K_f:
                    show_fitness()


        screen.fill((15, 15, 15))

        update()
        draw()
        pygame.display.update()

    pygame.quit()

def draw():
    for bird in birds:
        #gfxdraw.filled_circle(screen, bird.x_pos, bird.y_pos, bird.radius, bird_color)
        gfxdraw.aacircle(screen, bird.x_pos, round(bird.y_pos), bird.radius, bird_color)
        #pygame.draw.circle(screen, bird_color, (bird.x_pos, bird.y_pos), bird.radius)

    for obs in obstacles:
        pygame.draw.rect(screen, obstacle_color, (obs.x_pos, 0, obs.width, obs.gap_y))
        pygame.draw.rect(screen, obstacle_color, (obs.x_pos, obs.gap_y + obs.gap_size, obs.width, screen_size[1] - obs.gap_y - obs.gap_size))


def update():
    for tick in range(ticks_per_frame):
        for obs in obstacles:
            obs.x_pos -= movement_speed
            if obs.x_pos + obs.width < 0:
                obstacles.remove(obs)

        if len(obstacles) == 1:
            if obstacles[0].x_pos + obstacles[0].width < entities.Bird.x_pos - entities.Bird.radius:
                create_obstacle()

        for bird in birds:
            bird.move(nextObstacle())
            check_bird_bounds(bird)
            bird.fitness += 1

        if len(birds) == 0:
            new_generation()

def check_bird_bounds(bird):
    if bird.y_pos < 0:
        kill(bird)
    if bird.y_pos > screen_size[1]:
        kill(bird)
    for obs in obstacles:
        if (bird.x_pos + entities.Bird.radius > obs.x_pos and bird.x_pos - entities.Bird.radius < obs.x_pos) \
            or (bird.x_pos - entities.Bird.radius < obs.x_pos + obs.width and bird.x_pos + entities.Bird.radius > obs.x_pos + obs.width):
            if bird.y_pos - entities.Bird.radius < obs.gap_y \
                or bird.y_pos + entities.Bird.radius > obs.gap_y + obs.gap_size:
                kill(bird)

def kill(bird):
    #print('Killed Bird')
    dead_birds.append(bird)
    try:
        birds.remove(bird)
    except Exception as e:
        pass

def kill_birds():
    for bird in birds:
        kill(bird)

def show_fitness():
    if len(birds) > 0:
        print('Fitness: {}'.format(birds[0].fitness))

def create_obstacle():
    obstacles.append(entities.Obstacle(r.randrange(10, screen_size[1]- 140), 120, screen_size[0]))

def nextObstacle():
    if len(obstacles) == 1:
        return obstacles[0]
    elif len(obstacles) == 2:
        return obstacles[1]

def reset():
    global obstacles
    obstacles = []
    create_obstacle()

def new_generation():
    global dead_birds, num_gen
    gen_size = 20

    # if it is the first generated generation
    if len(dead_birds) == 0:
        for i in range(gen_size):
            birds.append(entities.Bird())

    best_birds = sorted(dead_birds, key=lambda arw: arw.fitness, reverse=True)[:int(gen_size/4)]
    print([a.fitness for a in best_birds])
    best = best_birds[0]
    # copy the best arrow brains
    for b in best_birds:
        new = entities.Bird()
        new.brain = b.brain.copy()
        birds.append(new)
    for i in range(3):
        for b in best_birds:
            new = entities.Bird()
            new.brain = b.brain.copy()
            new.brain.mutate()
            birds.append(new)

    dead_birds = []
    print('Best Fitness: ', best.fitness)
    print('New Generation({}): '.format(num_gen), len(birds))
    num_gen += 1

    reset()


if __name__=='__main__':
    main()
