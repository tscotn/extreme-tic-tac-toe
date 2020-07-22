from board import Board, ExtremeBoard, Player

#TODO: flip numbers to look like number pad and still be accessible correctly
# 7-8-9
# 4-5-6
# 1-2-3
#TODO: get the game to record elsewhere, maybe make one of the players controlled by a bot?? use ML on the bot to get it to improve...idk

def main():
    
    board = ExtremeBoard() #set up boards, players
    players = [Player(1), Player(2)]
    
    while board.extreme_board_playable: #play until someone has won
        print('building board...')
        board.RenderExtremeBoard()
        print('player 1 turn...')
        board.ChooseBoard(players[0])
        print('checking for winner...')
        if board.CheckIfXBWon():
            break
        board.RenderExtremeBoard()
        board.ChooseBoard(players[1])
        if board.CheckIfXBWon():
            break
        
    #TODO: just make this a little more spiffy, maybe an if statement for alt. message if there's no winner...and set up the asterisks to adjust??? idk
    if board.extreme_board_won_by == '[X]':
        winner = '1'
    else:
        winner = '2'
    print('*******************************')
    print('\tPlayer ' + winner + ' won!')
    print('*******************************')


#player 1 chooses a board and then a square. This square is saved as a new board location and used to determine the board that player 2 must play in, etc. If the square leads to an unplayable board, the player has the choice of a new board

main()


#What might a dataset look like for this? maybe read a bit about how chess moves are analyzed...


#[\] [ ] [/] : [/] [-] [\] : [X] [ ] [ ]
#
#[ ] [X] [ ] : [|] [O] [|]
#
#[/] [ ] [\] : [\] [-] [/]
