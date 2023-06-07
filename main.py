import os
import random
import time
import numpy as np
from termcolor import colored
from collections import defaultdict
from typing import NamedTuple


class Player:
    def __init__(self):
        self.name = input("Please enter your name: ").title()
        self.score = 0
        self.sym = None
        self.opposite = None

        self.choice = None #Tic_Tac_Toe
        self.guess = None #H/T

    def get_opposite(self):
         self.opposite = " O " if self.sym == " X " else " X "
    def get_choice(self, board):
        clear_con()
    
        #Finds next available starting position
        avail = [(i, j) for i in range(3) for j in range(3)]
        for pos in avail:
            tile = board[pos]
            if tile.free == True:
                pos = tile.pos
                break

    
        choice = ""
        while choice != "Y":
            #----------------------------------------
            # Initialising
            #----------------------------------------
            if board[pos].free == True:
                board[pos].sym = self.sym
                board[pos].colour = "green"

            #----------------------------------------
            # Valid Directions
            #----------------------------------------
            choice = ""
            valid_directions = ['Y', 'W', 'A', 'S', 'D']
            while choice not in valid_directions:
            
                print(board)
                cardinals = [
                    ["","W",""],
                    ["A","","D"],
                    ["","S",""]]

                title_display("Options", False)
                for r in cardinals:
                    for card in r:
                        if card:     
                            print(f"\t  {card}  ", end="")
                        else:
                            print("\t    ", end="")
                    print("")


                #----------------------------------------
                # Get a valid choice
                #----------------------------------------
                print("-------------------------------------------")
                print("\t     Y - Confirm ")

                choice = input(f"\t   {self.name}'s choice : ").upper()
                
                new_pos = board.get_new_pos(pos, choice)

                if (choice == "Y" and board[new_pos].free == False) or not new_pos:
                    choice = ""

            #----------------------------------------
            # Update old and new positions
            #----------------------------------------
            prev = board[pos]
            new  = board[new_pos]

            if new.free == True:
                new.sym = self.sym
                new.colour = "green"
            else:
                new.colour = "yellow"
                
            if prev.free == True:
                prev.free = True
                prev.sym = '   '
                prev.colour = None
            else:
                prev.colour = "red"
            pos = new.pos

        #----------------------------------------
        # Position choosen ('Y')
        #----------------------------------------
        board[pos].sym = self.sym
        board[pos].free = False
        board[pos].colour = "red"
        board.total += 1
    
    def coin_flip(self):
        
        while self.guess not in ("H", "T"):
            title_display("Coin Flip!", True)
            self.guess = input(f"{self.name}, Heads or Tails? (H/T) \nInput : ").upper()
            
        self.guess = "Heads" if self.guess == "H" else "Tails"

      
        H_T = ["Tails", "Heads"][random.randint(0, 1)] #0 Tails, 1#Heads

        title_display("Flipping", True)
        for i in f"{('Heads Tails ' * 10 + H_T)}".split():
            title_display("Flipping", True)
            print(f"""Your choice : {self.guess} \nOutcome     : {i}""")
            time.sleep(0.1)
        print()
 
        if self.guess == H_T:
            print(f"{H_T} is correct!")
            self.sym = " X "
        else:           
            print(f"Unlucky, {self.guess} was wrong.")
            self.sym = " O "
        time.sleep(2)
            
 
class Ai(Player):
    def __init__(self):
        self.name = "Computer"
        self.score = 0
        self.sym = None
        self.opposite = None
    def __str__(self):
        return f"{self.name:>10} : {self.score:>10}"

    def get_choice(self, board):
        
        #beginner level
        #pos = (random.randint(0, 2), random.randint(0, 2))

        #while board[pos].free == False:
        #    pos = (random.randint(0, 2), random.randint(0, 2))
        
        #please note that the Ai should always set its position to the center IF it is playing second

        #Hard level
        win = []       
        block = []

        for s in board.get_slices():
 
            values = [tile.sym for tile in s]
            positions = [tile.pos for tile in s]

            #Try to make a winning move
            #Block a players winning move
            #Go to try instead sides, corners or center
            #Respectively
            self_count = values.count(self.sym)
            enemy_count = values.count(self.opposite)

            
            #Ensure winning always takes precedence over blocking
            if (self_count == 2 and enemy_count == 0): 
                win.append(positions[values.index('   ')])
                
            elif (self_count == 0 and enemy_count == 2):
                block.append(positions[values.index('   ')])
                
            else:
                corner = [(0, 0), (0, 2), (2, 0), (2, 2)]
                center = [(1, 1)]
                side = [(0, 1), (1, 0), (2, 1), (1, 2)]

                random.shuffle(corner)
                random.shuffle(side)

                for pos in (corner + center + side):
                    if board[pos].free:
                        pos = pos
                        break
    
        if win:
            pos = win[0]
        elif block: 
            pos = block[0]
        
        board[pos].sym =  self.sym
        board[pos].colour =  "red"
        board[pos].free = False
        board.total += 1

class Tile():
    def __init__(self, pos):
        self.pos = pos
        self.free = True
        self.sym = "   "
        self.colour = None


class Board:

    def __init__(self):
        self.board = np.array([[Tile((0, 0)), Tile((0, 1)), Tile((0, 2))],
                               [Tile((1, 0)), Tile((1, 1)), Tile((1, 2))],
                               [Tile((2, 0)), Tile((2, 1)), Tile((2, 2))]]) 
        self.total = 0
    def __str__(self):
        title_display("Tic Tac Toe!", True)
        print("\n")
        for row in self.board:
            for tile in row:
                print(colored(f'\t  {tile.sym}  ', tile.colour, attrs=["reverse", "blink"]),  end="")
            print("\n")
        return "" 
    def __getitem__(self, pos):
        return self.board[pos]  
    def __setitem__(self, pos, value):
        board[pos].sym = value 

    def get_new_pos(self, pos, choice):
            choice.upper()
            x, y = pos

            new_pos = defaultdict(lambda: False)
            new_pos["Y"] = pos
            new_pos["W"] = self.verify_boundary((x-1, y))
            new_pos["A"] = self.verify_boundary((x, y-1))
            new_pos["S"] = self.verify_boundary((x+1, y))
            new_pos["D"] = self.verify_boundary((x, y+1))

            return new_pos[choice]
    def get_slices(self):
        d1 = [board[0,0], board[1,1], board[2,2]]
        d2 = [board[2,0], board[1,1], board[0,2]]
        slices = [d1, d2]

        for i in range(3):
            slices.append(board[:, i])
            slices.append(board[i, :])

        #returns all row, column and diagonal slices withs its (symbol, position)
        return slices
    
    def verify_boundary(self, pos):
        if not pos: return False

        for coord in pos:
            if not (0 <= coord <= 2): 
                return False 
        return pos 

    def winner(self, players):

        if self.total == 9:
            return "DRAW"

        for s in self.get_slices():
            values = [tile.sym for tile in s]
            
            if (len(set(values)) == 1) and "   " not in values:
                
                tile_sym = values[0]
                winner = players[0] if tile_sym == " X " else players[1]
                winner.score += 1

                for r in board:
                    for tile in r:
                        tile.colour = "white"

                for tile in s:
                    tile.colour = "light_yellow"

                return True
        return False
        

class Menu:

    def __init__(self): 
        self.choice = None
    def __str__(self):
        self.choice = ""

        while self.choice not in ("1", "2", "3", "Q"):
            clear_con()
            print("""
        
            Ｔｉｃ－Ｔａｃ－Ｔｏｅ

            Which would you like to play?

            1: Player VS Player
            2: Player VS Computer
            3: Score 
            Q: Quit
            """)    
            self.choice = input("\t    Choice : ").upper()
        
        return ""

    def get_players(self):
        clear_con()

        title_display("Player 1", True)
        p1 = Player()
        p1.coin_flip()
        p1.get_opposite()

        time.sleep(2)  

        if menu.choice == '1':
            title_display("Player 2", True)
            p2 = Player() 
        else:
            p2 = Ai()

        p2.sym      = p1.opposite
        p2.opposite = p1.sym

        return (p1, p2) if p1.sym == " X " else (p2, p1)

    def show_score(self, players):
        clear_con()

        if players:
            title_display("Score", True)
            data_display([(p.name, p.score) for p in players])
            time.sleep(3)
        else:
            title_display("There are no existing players", True)
            time.sleep(2)


def title_display(title, clear):
    if clear:
        clear_con()
    print(f"""-------------------------------------------
{title}
-------------------------------------------""")           
def data_display(data):
    #Data must be tuple array
    for tup in data:
        print(f" {' | '.join([f' {item : <20}' for item in tup])}")
    print("-------------------------------------------")
def clear_con():
    clear = lambda: os.system('clear')
    clear()


if __name__ == "__main__":

    clear_con()
    menu = Menu()
    players = []
    
    while True:

        board = Board()

        print(menu)

        #Unless a game is chosen to play, stay on the menu
        while menu.choice not in ("1", "2"):
            match menu.choice:
                case "Q":
                    break
                case "3":
                    menu.show_score(players)
                    print(menu)


        #Game Start
        players = menu.get_players()
        
        winner = False
        while not winner:
        
            for p in players:
                p.get_choice(board)
                
                winner = board.winner(players)
                
                if winner:
                    print(board)
                    if winner == "DRAW":
                        title_display("\t\tDRAW!", False)
                    else:
                        title_display("\t\tWINNER!", False)
                    break

        time.sleep(2)
 
