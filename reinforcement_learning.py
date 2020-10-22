import numpy as np
import pandas as pd

class Game(object):
    def __init__(self, n=3, player_sym='x'):
        self.board = None
        self.reset_board(n)
        self.stale = False
        self.sym_o = {'mark': 'O','value': 1 }
        self.sym_x = {'mark': 'X','value': 2}
        self.sym_empty = {'mark': ' ','value': 0}
        self.player_sym, self.bot_sym = (self.sym_x, self.sym_o) \
            if player_sym.lower() == 'x' \
            else (self.sym_o, self.sym_x)
        self.winner = None

    def reset_board(self, n=3):
        self.board = np.zeros((n, n)).astype(int)
        self.winner = None

    def draw_char_for_item(self, item):
        if item == self.sym_x.get('value'):
            return self.sym_x.get('mark')
        elif item == self.sym_o.get('value'):
            return self.sym_o.get('mark')
        else:
            return self.sym_empty.get('mark')

    def draw_board(self):
        elements_in_board = self.board.size
        items = [
            self.draw_char_for_item(self.board.item(item_idx))
            for item_idx in range(elements_in_board)
        ]
        board = """
             {} | {} | {}
            -----------
             {} | {} | {}
            -----------
             {} | {} | {}
        """.format(*items)
        print(board)

    def have_same_val(self, axis, item, item_x, item_y):
        max_limit, _ = self.board.shape
        result = True
        row_idx = col_idx = 0
        main_idx, fixed_idx, ignore_idx = (col_idx, item_x, item_y) \
            if axis == 0 \
            else (row_idx, item_y, item_x)
        while main_idx < max_limit:
            if main_idx != ignore_idx:
                board_item = self.board[fixed_idx][main_idx] \
                    if axis == 0 \
                    else self.board[main_idx][fixed_idx]
                if board_item != item or board_item == 0:
                    result = False
                    break
            main_idx += 1
        return result

    def left_diagonal_has_same_values(self, item, item_x, item_y):
        i = j = 0
        result = True
        max_limit, _ = self.board.shape
        while i < max_limit:
            if i != item_x:
                if self.board[i][j] != item or self.board[i][j] == 0:
                    result = False
                    break
            i += 1
            j += 1
        return result

    def right_diagonal_has_same_values(self, item, item_x, item_y):
        result = True
        max_limit, _ = self.board.shape
        i = 0
        j = max_limit - 1
        while i < max_limit:
            if i != item_x:
                if self.board[i][j] != item or self.board[i][j] == 0:
                    result = False
                    break
            i += 1
            j -= 1
        return result

    def cols_have_same_values(self, item, item_x, item_y):
        axis = 1
        return self.have_same_val(axis, item, item_x, item_y)

    def rows_have_same_values(self, item, item_x, item_y):
        axis = 0
        return self.have_same_val(axis, item, item_x, item_y)

    def element_diagonal_has_same_value(self, item, item_x, item_y):
        max_limit, _ = self.board.shape
        if item_x == item_y and item_x + item_y == max_limit - 1:
            return self.left_diagonal_has_same_values(item, item_x, item_y) or \
                   self.right_diagonal_has_same_values(item, item_x, item_y)

        if item_x == item_y:
            return self.left_diagonal_has_same_values(item, item_x, item_y)

        if item_x + item_y == max_limit - 1:
            return self.right_diagonal_has_same_values(item, item_x, item_y)
        return False

    def is_game_over(self, player, item, item_x, item_y):
        return self.cols_have_same_values(item, item_x, item_y) or \
               self.rows_have_same_values(item, item_x, item_y) or \
               self.element_diagonal_has_same_value(item, item_x, item_y)

    def is_winning_move(self, player, item, item_x, item_y):
        if self.is_game_over(player, item, item_x, item_y):
            self.winner = player
            return True
        return False

    def is_stale(self):
        x, y = np.where(self.board == 0)
        if len(x) == 0 and len(y) == 0:
            self.stale = True
        log('is game stale? ', self.stale)
        return self.stale

    def player_move(self, input_symbol, item_x, item_y):
        symbol = None
        if input_symbol == self.sym_o.get('mark'):
            symbol = self.sym_o

        elif input_symbol == self.sym_x.get('mark'):
            symbol = self.sym_x

        else:
            return
        if self.board[item_x][item_y] == 0:
            self.board[item_x][item_y] = symbol.get('value')
            self.draw_board()

            if self.is_winning_move(symbol.get('mark'), symbol.get('value'), item_x, item_y):
                print('Winner is: {}'.format(self.winner))
                return self.winner
            elif self.is_stale():
                print('Draw')
                return 'draw'

    def play(self, item_x, item_y):

        max_limit, _ = self.board.shape
        if item_x > max_limit - 1 or item_y > max_limit:
            return
        self.player_move(self.player_sym.get('mark'), item_x, item_y)

    def bot_play(self, item_x, item_y):

        max_limit, _ = self.board.shape
        if item_x > max_limit - 1 or item_y > max_limit:
            return
        self.player_move(self.bot_sym.get('mark'), item_x, item_y)

class Agent():
    def __init__(self, exploration_rate=0.33, learning_rate=0.5, discount_factor=0.01):
        self.states = {}
        self.state_order = []
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate

    def serialize_board(board):
        serialized_board = board.flatten()
        return ''.join([str(i) for i in serialized_board.flatten().tolist()])

    def get_serious(self):
        self.exploration_rate = 0

    def learn_by_temporal_difference(self, reward, new_state_key, state_key):
        old_state = self.states.get(state_key, np.zeros((3, 3)))
        return self.learning_rate * ((reward * self.states[new_state_key]) - old_state)

    def set_state(self, old_board, action):
        state_key = Agent.serialize_board(old_board)
        self.state_order.append((state_key, action))

    def on_reward(self, reward):
        if len(self.state_order) == 0:
            return None
        new_state_key, new_action = self.state_order.pop()
        self.states[new_state_key] = np.zeros((3, 3))
        self.states[new_state_key].itemset(new_action, reward)
        while self.state_order:
            state_key, action = self.state_order.pop()
            reward *= self.discount_factor
            if state_key in self.states:
                reward += self.learn_by_temporal_difference(reward, new_state_key, state_key).item(new_action)
                self.states[state_key].itemset(action, reward)
            else:
                self.states[state_key] = np.zeros((3, 3))
                reward = self.learn_by_temporal_difference(reward, new_state_key, state_key).item(new_action)
                self.states[state_key].itemset(action, reward)
            new_state_key = state_key
            new_action = action
    def exploit_board(self, state_key):
        state_values = self.states[state_key]
        print('State rewards')
        print(state_values)
        best_actions_x, best_actions_y = np.where(state_values == state_values.max())
        best_value_indices = [(x, y) for x, y in zip(best_actions_x, best_actions_y)]
        select_index = np.random.choice(len(best_value_indices))
        return best_value_indices[select_index]

    def select_move(self, board):
        explore_message = 'No experience for this state: explore'
        state_key = Agent.serialize_board(board)
        exploration = np.random.random() < self.exploration_rate
        log(explore_message if exploration or state_key not in self.states else 'exploit')
        action = self.explore_board(board) \
            if exploration or state_key not in self.states \
            else self.exploit_board(state_key)
        log('Choose cell', action)
        self.set_state(board, action)
        return action

    def explore_board(self, board):

        zero_x, zero_y = np.where(board == 0)
        vacant_cells = [(x, y) for x, y in zip(zero_x, zero_y)]
        randomly_selected_vacant_cell = np.random.choice(len(vacant_cells))
        return vacant_cells[randomly_selected_vacant_cell]


def optimize_bot(game, bot1, bot2):
    
    if game.winner == 'O':
        bot1.on_reward(1)
        # reward
        bot2.on_reward(-1)
        # punishment
    elif game.winner == 'X':
        bot1.on_reward(-1)
        bot2.on_reward(1)

def train(epochs, bot1, bot2):
    bots = [{'mdl': bot1,'name': 'bot1','sym': 'O','wins': 0}, {'mdl': bot2, 'name': 'bot2', 'sym': 'X',  'wins': 0 }]

    win_trace = pd.DataFrame(data=np.zeros((epochs, 2)), columns=['bot1', 'bot2'])
    for i in range(epochs):
        print('-' * 100)
        print('epoch: {}'.format(i + 1))
        game = Game()
        while not game.stale and not game.winner:
            for bot in bots:
                winner = game.player_move(bot['sym'], *bot['mdl'].select_move(game.board))
                log('winner found:', winner)
                if winner:
                    optimize_bot(game, bot1, bot2)
                    bot['wins'] += 1
                    win_trace.set_value(i, bot['name'], 1)
                    break
                    win_trace[i] = 2
                elif winner == 'draw':
                    break
    return win_trace, bots[0]['wins'], bots[1]['wins']

def log(*args):
    if True:
        print(*args)

bot1 = Agent()
bot2 = Agent()
epochs = 10000
win_trace, bot1_wins, bot2_wins = train(epochs, bot1, bot2)