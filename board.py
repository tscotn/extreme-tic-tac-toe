#TODO: figure out how to stop player from accessing boards that have been won...if they get sent there, make them choose a board from valid boards
#TODO: Get the renderboard function to highlight whichever board the player is to  play in
import itertools

class Board:
    def __init__(self):
        self.board_won = False
        self.board_playable = True
        self.board_won_by = None
        self.square_loc = ['top_left', 'top_center', 'top_right', 'middle_left', 'middle_center', 'middle_right', 'bottom_left', 'bottom_center', 'bottom_right'] #relative location of each square to number pad
        self.board = {self.square_loc[i]: '[ ]' for i in range(len(self.square_loc))} #dict containing character associated with square_loc
    
    def RenderBoard(self): #print out one board
        for loc in self.square_loc:
            if self.square_loc.index(loc) in [2, 5, 8]:
                print(self.board[loc])
            else:
                print(self.board[loc]  + '', end='')
    
    def ChooseSquare(self, player): #ask the player for a square to play in, if square is open, change value to player token
        self.RenderBoard()
        square = input('Choose a square (1-9) to play in: ')
        while (not square.isdigit()) or (int(square)-1 not in range(9)) or (self.board[self.square_loc[int(square)-1]] != '[ ]'):
            square = input('Choose a valid square to play in: ')
        self.board[self.square_loc[int(square)-1]] = player.token
        return int(square)
        
    def CheckIfWon(self): #check if the board has been won by either player, if a player has won, assign board_won_by to that player id? If board is unwinnable (no open spaces could lead to a row of three by any player), do nothing?
        won = [(0, 1, 2),(3, 4, 5),(6, 7, 8),(0, 3, 6),(1, 4, 7),(2, 5, 8),(0, 4, 8),(2, 4, 6)]
        if len([self.square_loc.index(loc) for loc, square in self.board.items() if square=='[ ]']) == 0: #checks if board has any open spaces, if not, board is not playable
            self.board_playable = False;
        for token in ['[X]', '[O]']: #check if either player won by getting the location of their squares, and seeing if combinations of the squares exist in a list of combinations needed to win
            if any(x in won for x in itertools.combinations([self.square_loc.index(loc) for loc, square in self.board.items() if square==token], 3)): #if a player has won, set board_won_by to that player's token, and change board to unplayable, exit loop
                self.board_won_by = token
                self.board_playable = False
                if token == '[X]':
                    self.board = {self.square_loc[0]: '[\]', self.square_loc[1]: '[ ]', self.square_loc[2]: '[/]', self.square_loc[3]: '[ ]', self.square_loc[4]: '[X]', self.square_loc[5]: '[ ]', self.square_loc[6]: '[/]', self.square_loc[7]: '[ ]', self.square_loc[8]: '[\]'}
                elif token == '[O]':
                    self.board = {self.square_loc[0]: '[/]', self.square_loc[1]: '[-]', self.square_loc[2]: '[\]', self.square_loc[3]: '[|]', self.square_loc[4]: '[O]', self.square_loc[5]: '[|]', self.square_loc[6]: '[\]', self.square_loc[7]: '[-]', self.square_loc[8]: '[/]'}
                break


class ExtremeBoard:
    def __init__(self):
        self.extreme_board_playable = True
        self.extreme_board_won_by = None
        self.board_loc = ['top_left', 'top_center', 'top_right', 'middle_left', 'middle_center', 'middle_right', 'bottom_left', 'bottom_center', 'bottom_right'] #relative location of each board
        self.boards = [Board() for loc in range(len(self.board_loc))]
        self.extreme_board = {self.board_loc[i]: self.boards[i] for i in range(len(self.board_loc))} #dict containing Board associated with each board_loc
        self.playable_boards = self.board_loc.copy() #list of locations of each board yet to be won or complete, remove as playable boards are completed
        self.board_to_play = None

    def RenderExtremeBoard(self): #print all boards (see printing logic, it gets a bit complicated) #TODO: make the boards render as either a big X or O if they've been won by either...do this in the Board class?
        for x in range(3):
            if x is not 0:
                print('\n. . . . . . . . . . . . . . . . . . . .', end='')
            for k in range(3):
                print('\n')
                for j in range(3):
                    if j == 0:
                        print('', end='')
                    else:
                        print(' : ', end='')
                    for i in range(0+k*3,3+k*3):
                        square = self.extreme_board[self.board_loc[(x*3)+j]].board[self.board_loc[i]]
                        if i == (3+k*3)-1:
                            print(square, end='')
                        else:
                            print(square, end=' ')

    def ChooseBoard(self, player): #if player has been sent to a complete board, or is starting out, give them the choice of unwon boards to go to, show squared that haven't been won
        next_board = self.board_to_play
        if next_board == None or (self.board_loc[int(next_board)-1] not in self.playable_boards):
            next_board = input('\n Player ' + str(player.id) + ', please choose a board (1-9) to play in: ')
            while (not next_board.isdigit()) or (int(next_board)-1 not in range(9)) or (self.board_loc[int(next_board)-1] not in self.playable_boards):
                print('Valid boards are: ' + str(self.playable_boards))
                next_board = input('\n Please choose a valid board to play in: ')
        print('\n Player ' + str(player.id) + ', you\'re playing in the ' + self.board_loc[int(next_board)-1] + ' board')
        self.board_to_play =  self.extreme_board[self.board_loc[int(next_board)-1]].ChooseSquare(player)
        self.RefreshPlayability()

    def RefreshPlayability(self):
        for loc, board in self.extreme_board.items():
            board.CheckIfWon()
        for loc in self.playable_boards: #check to remove unplayable boards
            if not self.extreme_board[loc].board_playable:
                self.playable_boards.remove(loc)

    def CheckIfXBWon(self): #check if the extreme board has been won by either player and if any moves still exist, if a player has won, assign extreme_board_won_by to that player token or id, change extreme_board_playable to False...add
    #       TODO: This can be streamlined--loop through playable boards rather than all boards each time...
        won = [(0, 1, 2),(3, 4, 5),(6, 7, 8),(0, 3, 6),(1, 4, 7),(2, 5, 8),(0, 4, 8),(2, 4, 6)]
        if [loc for loc, board in self.extreme_board.items() if board.board_playable] == []:
            self.board_playable = False;
            print('if len crap returned True') #DELETEME
            return True #this checks if there's even anywhere left to play...but i need to figure out a way for it to exit if the players are stuck? hm
        for token in ['[X]', '[O]']:
            if any(x in won for x in itertools.combinations([self.board_loc.index(loc) for loc, board in self.extreme_board.items() if board.board_won_by==token], 3)):
                self.extreme_board_won_by = token
                self.extreme_board_playable = False
                print('if any crap returned true...') #DELETEME
                return True #im not sure this is doing what I want it to
        return False


class Player:
    def __init__(self, id):
        while id not in [1,2]: #require id to be 1 or 2
            id = int(input("invalid player id, choose 1 or 2: "))
        self.id = id
        if id == 1: #assign X to player 1, O to player 2
            self.token = '[X]'
        elif id == 2:
            self.token = '[O]'
