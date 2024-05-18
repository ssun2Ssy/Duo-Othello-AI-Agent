import copy

BOARD_SIZE = 12
PLAYER, OPPONENT = 'X', 'O'
DIRECTIONS = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

def read_input(filename="input.txt"):
    with open(filename, 'r') as file:
        lines = file.readlines()
        player = lines[0].strip()
        remaining_time, _ = map(float, lines[1].strip().split())
        board = [list(line.strip()) for line in lines[2:2 + BOARD_SIZE]]
    return player, remaining_time, board

def determine_depth(remaining_time):
    if remaining_time > 50:
        return 4
    elif remaining_time < 15:
        return 1
    else:
        return 3

def game_phase(board):
    empty_spaces = sum(row.count('.') for row in board)
    if empty_spaces > (BOARD_SIZE ** 2) * 0.75:
        return 'early'
    elif empty_spaces > (BOARD_SIZE ** 2) * 0.25:
        return 'mid'
    else:
        return 'late'

def evaluate_board(board, player):
    opponent = 'O' if player == 'X' else 'X'
    board_control_score = 0
    corner_control_score = 0
    edge_control_score = 0
    stability_score = 0
    mobility_score = 0
    potential_mobility_score = 0

    # Define weights for different aspects of the evaluation
    weight_board_control = 1.0
    weight_corner_control = 40.0
    weight_edge_control = 10.0
    weight_stability = 5.0
    weight_mobility = 2.0
    weight_potential_mobility = 2.0

    # Board Control: indicates who controls more pieces on the board
    board_control_score = sum(row.count(player) for row in board) - sum(row.count(opponent) for row in board)

    # Corner Control: if the player has a piece in a corner, the score is incremented, and if the opponent has a piece in a corner, the score is decremented.
    corners = [(0, 0), (0, 11), (11, 0), (11, 11)]
    for x, y in corners:
        if board[x][y] == player:
            corner_control_score += 1
        elif board[x][y] == opponent:
            corner_control_score -= 1

    # Edge Control: it increments the score if the player has a piece on an edge and decrements if the opponent has a piece on an edge.
    edge_positions = get_edge_positions()
    for x, y in edge_positions:
        if board[x][y] == player:
            edge_control_score += 1
        elif board[x][y] == opponent:
            edge_control_score -= 1

    # Mobility: the mobility advantage of the player over the opponent (the difference of legal moves available counts between the player and the opponent)
    player_legal_moves = len(find_legal_moves(board, player))
    opponent_legal_moves = len(find_legal_moves(board, opponent))
    mobility_score = player_legal_moves - opponent_legal_moves

    # Potential Mobility: compare the number of empty squares adjacent to opponent's pieces and player's pieces.
    potential_mobility_score = calculate_potential_mobility(board, player) - calculate_potential_mobility(board, opponent)

    # Combine scores
    total_score = (weight_board_control * board_control_score +
                   weight_corner_control * corner_control_score +
                   weight_edge_control * edge_control_score +
                   weight_stability * stability_score +
                   weight_mobility * mobility_score +
                   weight_potential_mobility * potential_mobility_score)
    return total_score


def get_edge_positions():
    """
    Returns a list of positions located on the edges of the board
    excluding the corners to avoid double counting them in corner control.
    """
    edge_positions = []
    for i in range(12):
        if i not in [0, 11]:  # Exclude corners
            edge_positions.extend([(i, 0), (i, 11), (0, i), (11, i)])
    return edge_positions


def calculate_potential_mobility(board, player):
    opponent = 'O' if player == 'X' else 'X'
    potential_mobility = 0
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]

    for x in range(12):
        for y in range(12):
            if board[x][y] == '.':
                for dx, dy in directions:
                    nx, ny = x + dx, y + dy
                    if (0 <= nx < 12 and 0 <= ny < 12) and board[nx][ny] == opponent:
                        # Check if the empty space is adjacent to an opponent's piece
                        # Then, check if it can potentially become a legal move
                        potential_mobility += 1
                        break  # Move to the next empty square after finding at least one adjacent opponent piece
    return potential_mobility


def find_legal_moves(board, current_player):
    legal_moves = {}
    opponent = 'O' if current_player == 'X' else 'X'

    # Identify cells adjacent to the opponent's pieces.
    adjacent_to_opponent = set()
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == opponent:
                for dx, dy in DIRECTIONS:
                    nx, ny = x + dx, y + dy
                    if 0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE and board[nx][ny] == '.':
                        adjacent_to_opponent.add((nx, ny))

    # For each cell adjacent to an opponent's piece, check if it's a legal move.
    for x, y in adjacent_to_opponent:
        for dx, dy in DIRECTIONS:
                nx, ny = x + dx, y + dy
                flips = []
                while True:
                    if not (0 <= nx < BOARD_SIZE and 0 <= ny < BOARD_SIZE):
                        break  # Out of bounds
                    if board[nx][ny] == '.':
                        break  # Empty space encountered, not a valid flip
                    if board[nx][ny] == current_player:
                        if flips:  # Check if flips list is not empty
                            if (x, y) not in legal_moves:
                                legal_moves[(x, y)] = []
                            legal_moves[(x, y)].extend(flips)  # Add valid flips to legal moves
                        break  # End of a valid bracket
                    flips.append((nx, ny))  # Add opponent's piece to potential flips
                    nx += dx
                    ny += dy
    return legal_moves


def apply_move(board, move, player):
    flips = find_legal_moves(board, player).get(move, [])
    new_board = copy.deepcopy(board)
    new_board[move[0]][move[1]] = player
    for flip in flips:
        new_board[flip[0]][flip[1]] = player
    return new_board


def minimax(board, depth, alpha, beta, maximizingPlayer, player):
    opponent = 'O' if player == 'X' else 'X'
    legal_moves = find_legal_moves(board, player)

    if depth == 0 or not legal_moves:
        return evaluate_board(board, player), None

    if maximizingPlayer:
        maxEval = float('-inf')
        best_move = None
        for move, _ in legal_moves.items():
            new_board = apply_move(copy.deepcopy(board), move, player)
            evaluation, _ = minimax(new_board, depth-1, alpha, beta, False, opponent)
            if evaluation > maxEval:
                maxEval, best_move = evaluation, move
            alpha = max(alpha, evaluation)
            if beta <= alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move, _ in legal_moves.items():
            new_board = apply_move(copy.deepcopy(board), move, player)
            evaluation, _ = minimax(new_board, depth-1, alpha, beta, True, opponent)
            if evaluation < minEval:
                minEval, best_move = evaluation, move
            beta = min(beta, evaluation)
            if beta <= alpha:
                break
        return minEval, best_move


def write_output(move, filename="output.txt"):
    col = chr(move[1] + ord('a'))
    row = str(move[0] + 1)
    with open(filename, 'w') as file:
        file.write(f"{col}{row}\n")

def main():
    player, remaining_time, board = read_input()
    depth = determine_depth(remaining_time)
    _, move = minimax(board, depth, float('-inf'), float('inf'), True, player)
    if move:
        write_output(move)
    else:
        print("No legal move found.")

if __name__ == "__main__":
    main()