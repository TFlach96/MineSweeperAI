import pygame
import sys
import time
import ttf_opensans
import random
import copy
from minesweeper import Minesweeper, MinesweeperAI

HEIGHT = 8
WIDTH = 8
MINES = 8
population_size = 5
child = []
offspring = []
generationsCounter = 1
initial_solve = True
initial_knowledge = []
mine_first = True

# Colors
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

# Create game
pygame.init()
size = width, height = 600, 400
screen = pygame.display.set_mode(size)

# Fonts
OPEN_SANS = "assets/fonts/OpenSans-Regular.ttf"
smallFont = pygame.font.Font(OPEN_SANS, 20)
mediumFont = pygame.font.Font(OPEN_SANS, 28)
largeFont = pygame.font.Font(OPEN_SANS, 40)

# Compute board size
BOARD_PADDING = 20

board_width = width - (BOARD_PADDING * 2)
board_height = height - (BOARD_PADDING * 2)
cell_size = int(min(board_width / WIDTH, board_height / HEIGHT))
board_origin = (BOARD_PADDING, BOARD_PADDING)

# Add images
flag = pygame.image.load("assets/images/flag.png")
flag = pygame.transform.scale(flag, (cell_size, cell_size))
mine = pygame.image.load("assets/images/mine.png")
mine = pygame.transform.scale(mine, (cell_size, cell_size))

# Create game and AI agent
game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)

# Keep track of revealed cells, flagged cells, and if a mine was hit
revealed = set()
flags = set()
unsolved = True

running = True
while True:

    # Check if game quit
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # Draw board
    cells = []
    for i in range(HEIGHT):
        row = []
        for j in range(WIDTH):
            # Draw rectangle for cell
            rect = pygame.Rect(
                board_origin[0] + j * cell_size,
                board_origin[1] + i * cell_size,
                cell_size, cell_size
            )
            pygame.draw.rect(screen, GRAY, rect)
            pygame.draw.rect(screen, WHITE, rect, 3)

            # Add a mine, flag, or number if needed
            if game.is_mine((i, j)) and not unsolved:
                screen.blit(mine, rect)
            elif (i, j) in flags:
                screen.blit(flag, rect)
            elif (i, j) in revealed:
                neighbors = smallFont.render(
                    str(game.nearby_mines((i, j))),
                    True, BLACK
                )
                neighborsTextRect = neighbors.get_rect()
                neighborsTextRect.center = rect.center
                screen.blit(neighbors, neighborsTextRect)
            row.append(rect)
        cells.append(row)

    # Initial Solve
    if initial_solve:
        ai = MinesweeperAI(height=HEIGHT, width=WIDTH, kb=child)
        move = (0, 0)
        if move:
            while mine_first:
                if game.is_mine(move):
                    game = Minesweeper(height=HEIGHT, width=WIDTH, mines=MINES)
                    print("Mine in first box, creating new game.")
                else:
                    mine_first = False
                    break
            else:
                nearby = game.nearby_mines(move)
                revealed.add(move)
                ai.add_knowledge(move, 'safe')
                if nearby == 0:
                    moveStack = [move, (move[0] + 1, move[1]), (move[0] + 1, move[1] + 1), (move[0], move[1] + 1)]
                    while len(moveStack) != 0:
                        move = moveStack[-1]
                        nearby = game.nearby_mines(move)
                        revealed.add(move)
                        ai.add_knowledge(move, 'safe')
                        if nearby == 0:
                            # If within range of board, append
                            if move[0] + 1 < HEIGHT:
                                # Down
                                moveStack.append((move[0] + 1, move[1]))
                                if move[1] + 1 < WIDTH:
                                    # Diagonal Bottom Right
                                    moveStack.append((move[0] + 1, move[1] + 1))
                                if move[1] - 1 >= 0:
                                    # Diagonal Bottom Left
                                    moveStack.append((move[0] + 1, move[1] - 1))
                            if move[0] - 1 >= 0:
                                # Up
                                moveStack.append((move[0] + 1, move[1]))
                                if move[1] + 1 < WIDTH:
                                    # Diagonal Top Right
                                    moveStack.append((move[0] - 1, move[1] + 1))
                                if move[1] - 1 >= 0:
                                    # Diagonal Top Left
                                    moveStack.append((move[0] - 1, move[1] - 1))
                            if move[1] + 1 < WIDTH:
                                # Right
                                moveStack.append((move[0] + 1, move[1]))
                            if move[1] - 1 >= 0:
                                # Left
                                moveStack.append((move[0], move[1] - 1))

                            # Using set to remove duplicates
                            remove_dupes = set(moveStack)

                            # If element in moves_made, append to already_made
                            already_made = set()
                            for element in moveStack:
                                if element in ai.moves_made:
                                    already_made.add(element)

                            # Using set function difference_update() removes the items that exist in both sets from
                            # remove_dupes
                            remove_dupes.difference_update(already_made)
                            moveStack = list(remove_dupes)
                        else:
                            moveStack.pop()
        initial_solve = False
        initial_knowledge = ai.knowledge
        offspring = list(initial_knowledge)
    while unsolved:
        print("The current generation is", generationsCounter)
        AINumber = 0
        population = []
        fitness_scores = []
        while AINumber < population_size:
            if flags == game.mines:
                unsolved = False
                break
            print('AI #', AINumber + 1)
            child = list(offspring)
            ai = MinesweeperAI(height=HEIGHT, width=WIDTH, kb=child)
            revealed = set()
            flags = set()
            lose = False

            while not lose:
                move = None
                move = ai.make_safe_move()
                if move is None:
                    move = ai.make_random_move()
                    if move is None:
                        flags = ai.mines.copy()
                        if flags == game.mines:
                            break
                        print("No more moves to make.")
                    else:
                        print("No known safe moves, AI making random move.")
                else:
                    print("AI making safe move.")
                if flags == game.mines:
                    print("Win")
                    unsolved = False
                    break
                else:
                    if move:
                        if game.is_mine(move):
                            ai.add_knowledge(move, 'mine')
                            population.append(ai.knowledge)
                            fitness_scores.append(len(ai.knowledge))
                            AINumber += 1
                            print("Lost")
                            lose = True
                        else:
                            revealed.add(move)
                            ai.add_knowledge(move, 'safe')
        if flags == game.mines:
            unsolved = False
            break

        # Selection
        max_value = max(fitness_scores)
        max_index = fitness_scores.index(max_value)
        fitness_scores.pop(max_index)
        parent1 = population.pop(max_index)

        max_value2 = max(fitness_scores)
        max_index2 = fitness_scores.index(max_value2)
        fitness_scores.pop(max_index2)
        parent2 = population.pop(max_index2)

        # Crossover + Mutation
        offspring = []
        parentSize = len(parent1)

        parent1Mine = []
        for mc in parent1:
            if mc[1] == 'mine':
                parent1Mine.append(mc)

        parent2Mine = []
        for mc2 in parent2:
            if mc2[1] == 'mine':
                parent2Mine.append(mc2)

        # Checking for non dupes and adding
        for dupes in parent2Mine:
            if dupes not in parent1Mine:
                parent1Mine.append(dupes)
        for contents in parent1Mine:
            offspring.append(parent1Mine.pop())

        for breed in range(0, parentSize):
            if (breed + 1 % 2) != 0:
                rand = random.randint(0, len(parent1) - 1)
                offspring.append(parent1.pop(rand))
            else:
                if len(parent2) != 0:
                    rand = random.randint(0, len(parent2) - 1)
                    offspring.append(parent2.pop(rand))
                else:
                    rand = random.randint(0, len(parent1) - 1)
                    offspring.append(parent1.pop(rand))
        generationsCounter += 1
    pygame.display.flip()
