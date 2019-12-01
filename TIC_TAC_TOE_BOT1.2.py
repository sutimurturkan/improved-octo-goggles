import random
import copy
import sys


class Game:

    def __init__(self):
        self.board = [' '] * 25
        self.player_name = ''
        self.player_marker = ''
        self.bot_name = 'Tic-Tac-Toe-Bot'
        self.bot_marker = ''
        self.winning_combos = (
            [0, 1, 2, 3], [1, 2, 3, 4], [5, 6, 7, 8], [6, 7, 8, 9], [10, 11, 12, 13], [11, 12, 13, 14],
            [15, 16, 17, 18],
            [16, 17, 18, 19], [20, 21, 22, 23], [21, 22, 23, 24], [0, 5, 10, 15], [5, 10, 15, 20], [1, 6, 11, 16],
            [6, 11, 16, 21],
            [2, 7, 12, 17], [7, 12, 17, 22], [3, 8, 13, 18], [8, 13, 18, 23], [4, 9, 14, 19], [9, 14, 19, 24],
            [5, 11, 17, 23], [0, 6, 12, 18],
            [6, 12, 18, 24], [1, 7, 13, 19], [3, 7, 11, 15], [4, 8, 12, 16], [8, 12, 16, 20], [9, 13, 17, 21],
        )
        self.corners = [0,4,20,24]
        self.sides = [1,2,3,5,6,7,8,9,10,11,13,14,15,16,17,18,19,21,22,23]
        self.middle = 12


    def print_board(self, board=None):
        print (" %s | %s | %s | %s | %s " % (self.board[0], self.board[1], self.board[2], self.board[3], self.board[4],))
        print ("-------------------")
        print (" %s | %s | %s | %s | %s " % (self.board[5], self.board[6], self.board[7], self.board[8], self.board[9],))
        print ("-------------------")
        print (" %s | %s | %s | %s | %s " % (self.board[10], self.board[11], self.board[12], self.board[13], self.board[14],))
        print ("-------------------")
        print (" %s | %s | %s | %s | %s " % (self.board[15], self.board[16], self.board[17], self.board[18], self.board[19],))
        print ("-------------------")
        print (" %s | %s | %s | %s | %s " % (self.board[20], self.board[21], self.board[22], self.board[23], self.board[24],))
        print ("                   ")
        print ("                   ")
        print ("                   ")

    def get_marker(self):
        marker = raw_input("Would you like your marker to be X or O?\n").upper()
        while marker not in ["X", "O"]:
            marker = raw_input("Would you like your marker to be X  or O?\n").upper()
        if marker == "X":
            return ('X', 'O')
        else:
            return ('O', 'X')


    def is_winner(self, board, marker):
        for combo in self.winning_combos:
            if (board[combo[0]] == board[combo[1]] == board[combo[2]] == board[combo[3]] == marker):
                return True
        return False

    def get_bot_move(self):

        for i in range(0, len(self.board)):
            board_copy = copy.deepcopy(self.board)
            if self.is_space_free(board_copy, i):
                self.make_move(board_copy, i, self.bot_marker)
                if self.is_winner(board_copy, self.bot_marker):
                    return i


        for i in range(0, len(self.board)):
            board_copy = copy.deepcopy(self.board)
            if self.is_space_free(board_copy, i):
                self.make_move(board_copy, i, self.player_marker)
                if self.is_winner(board_copy, self.player_marker):
                    return i


        move = self.choose_random_move(self.corners)
        if move != None:
            return move


        if self.is_space_free(self.board, self.middle):
            return self.middle


        return self.choose_random_move(self.sides)

    def is_space_free(self, board, index):

        return board[index] == ' '

    def is_board_full(self):
        for i in range(1, 25):
            if self.is_space_free(self.board, i):
                return False
        return True

    def make_move(self, board, index, move):
        board[index] = move

    def choose_random_move(self, move_list):
        possible_winning_moves = []
        for index in move_list:
            if self.is_space_free(self.board, index):
                possible_winning_moves.append(index)
                if len(possible_winning_moves) != 0:
                    return random.choice(possible_winning_moves)
                else:
                    return None

    def start_game(self):
        v = random.randint(0, 25)

        self.board[v] = "U"
        self.print_board(range(1, 26))
        self.player_name = self.get_player_name()

        self.player_marker, self.bot_marker = self.get_marker()
        print "Your marker is " + self.player_marker

        if random.randint(0, 1) == 0:
            print "I will go first"
            self.enter_game_loop('a')
        else:
            print "You will go first"
            self.enter_game_loop('z')

    def get_player_move(self):
        move = int(input("Pick a spot to move: (1-25)\n"))
        while move not in [1, 2, 3, 4, 5, 6, 7, 8, 9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25] or not self.is_space_free(self.board, move - 1):
            move = int(input("Invalid move. Please try again: (1-25)\n"))
        return move - 1

    def get_player_name(self):
        return raw_input("Hi, i am %s" % self.bot_name + ". What is your name?\n")

    def enter_game_loop(self, turn):
        is_running = True
        player = turn
        while is_running:
            if player == 'z':
                user_input = self.get_player_move()
                self.make_move(self.board, user_input, self.player_marker)
                if (self.is_winner(self.board, self.player_marker)):
                    self.print_board()
                    print "\n\tCONGRATULATIONS %s, YOU HAVE WON THE GAME!!! \\tn" % self.player_name
                    is_running = False
                else:
                    if self.is_board_full():
                        self.print_board()
                        print "\n\t-- Match Draw --\t\n"
                        is_running = False
                    else:
                        self.print_board()
                        player = 'a'
            else:
                bot_move = self.get_bot_move()
                self.make_move(self.board, bot_move, self.bot_marker)
                if (self.is_winner(self.board, self.bot_marker)):
                    self.print_board()
                    print "\n\t%s HAS WON!!!!\t\n" % self.bot_name
                    is_running = False
                    break
                else:
                    if self.is_board_full():
                        self.print_board()
                        print "\n\t -- Match Draw -- \n\t"
                        is_running = False
                    else:
                        self.print_board()
                        player = 'z'

        self.end_game()

    def end_game(self):
        play_again = raw_input("Would you like to play again? (y/n): ").lower()
        if play_again == 'y':
            self.__init__()
            self.start_game()
        else:
            print "\n\t-- GAME OVER!!!--\n\t"
            sys.exit()


if __name__ == "__main__":
    TicTacToe = Game()
    TicTacToe.start_game()
