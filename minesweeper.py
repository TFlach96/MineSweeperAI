import itertools
import random
import copy
import time


class Minesweeper:
    """
    Minesweeper 
    ame representation
    """

    def __init__(self, height, width, mines):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:

            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class MinesweeperAI:
    """
    Minesweeper game player
    """

    def __init__(self, height, width, kb=()):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of moves about the game known to be true
        self.knowledge = kb
        if len(self.knowledge) != 0:
            for knowledge in kb:
                if knowledge[1] == 'safe':
                    self.mark_safe(knowledge[0])
                elif knowledge[1] == 'mine':
                    self.mark_mine(knowledge[0])
        random.seed(time.time())

    def mark_mine(self, cell):
        """
        Marks a cell as a mine
        """
        self.mines.add(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe
        """
        self.safes.add(cell)

    def mark_move(self, cell):
        """
        Marks a cell as safe
        """
        self.moves_made.add(cell)

    def add_knowledge(self, cell, status):
        self.knowledge.append([cell, status])
        self.mark_move(cell)
        if status == 'safe':
            self.mark_safe(cell)
        elif status == 'mine':
            self.mark_mine(cell)

    def make_safe_move(self):
        # return a safe cell to choose on minesweeper board.
        for cell in self.safes:
            if cell not in self.moves_made:
                return cell
        return None

    def make_random_move(self):
        good_move = False
        board_values = []
        for x in range(self.height):
            row = []
            for y in range(self.width):
                row.append(1)
            board_values.append(row)
        while sum(row.count(1) for row in board_values) > 0:
            num1 = random.randint(0, self.height - 1)
            num2 = random.randint(0, self.width - 1)
            cell = (num1, num2)
            if (cell not in self.moves_made) and (cell not in self.mines):
                good_move = True
                break
            else:
                board_values[num1][num2] = 0
        if good_move:
            return cell
        else:
            return None
