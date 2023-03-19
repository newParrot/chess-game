import copy

class ChessGame:

    def __init__(self):
        self.board = [
            ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R'],
            ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
            ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
            ['r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        ]
        self.current_player = 'white'
        self.white_pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
        self.black_pieces = ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p', 'r', 'n', 'b', 'q', 'k', 'b', 'n', 'r']
        self.white_king = "e1" #white is bottom
        self.black_king = "e8" #black is top
        self.moves_played = []

    def move_piece(self, from_square, to_square):
        # Get the row and column indices of the squares
        from_row, from_col = self.square_to_index(from_square)
        to_row, to_col = self.square_to_index(to_square)

        # Keeping current space of king updated
        if (from_square == self.white_king):
            self.white_king = to_square
        if (from_square == self.black_king):
            self.black_king = to_square

        # Move the piece from the from_square to the to_square
        self.board[to_row][to_col] = self.board[from_row][from_col]
        self.board[from_row][from_col] = ' '

    def square_to_index(self, square):
        # Convert a square string (e.g. 'a1') to a row and column index
        col_index = ord(square[0]) - ord('a')
        row_index = int(square[1]) - 1
        return row_index, col_index

    def index_to_square(self, row, col):
        # Convert a row and column index to a square string (e.g. 'a1')
        col_letter = chr(col + ord('a'))
        row_number = str(row + 1)
        return col_letter + row_number

    def is_valid_move(self, from_square, to_square):
        # Convert the start and end positions to coordinates
        start_pos = self.square_to_index(from_square)
        end_pos = self.square_to_index(to_square)

        # Check if the start position contains a piece and if it belongs to the current player
        if not self.board[start_pos[0]][start_pos[1]]:
            return False

        # Check if the piece being moved is owned by the current player
        if self.current_player == "black" and self.board[start_pos[0]][start_pos[1]].islower():
            return False
        if self.current_player == "white" and self.board[start_pos[0]][start_pos[1]].isupper():
            return False

        # Check if the end position is within the bounds of the board
        if not self.is_on_board(*end_pos):
            return False

        # Check if the piece can move to the end position
        if not self.board[start_pos[0]][start_pos[1]].can_move(end_pos[0], end_pos[1], self.board):
            return False

        # Check if the move puts the current player in check
        test_board = copy.deepcopy(self)
        test_board.move_piece(start_pos, end_pos)
        if test_board.is_check(self.current_player):
            return False

        # All checks passed, the move is valid
        return True

    def is_checkmate(self):
        # Check if the current player is in checkmate
        if self.current_player == "white":

            attacking_pieces = self.find_attacking_pieces(self.white_king)
            if not attacking_pieces:
                # The king is not in check, so not checkmate
                return False
            # Check if the king can move out of check
            for move in self.generate_moves(self.white_king):
                if self.is_valid_move(self.white_king, move):
                    return False
            # Check if any other piece can block the check
            for piece_square in self.get_player_pieces(self.current_player):
                for move in self.generate_moves(piece_square):
                    if self.is_valid_move(piece_square, move):
                        return False
            # The player is in checkmate
            print("White is in checkmate")

        else:

            attacking_pieces = self.find_attacking_pieces(self.black_king)
            if not attacking_pieces:
                # The king is not in check, so not checkmate
                return False
            # Check if the king can move out of check
            for move in self.generate_moves(self.black_king):
                if self.is_valid_move(self.black_king, move):
                    return False
            # Check if any other piece can block the check
            for piece_square in self.get_player_pieces(self.current_player):
                for move in self.generate_moves(piece_square):
                    if self.is_valid_move(piece_square, move):
                        return False
            # The player is in checkmate
            print("Black is in checkmate")
        return True

    def is_stalemate(self):
        # Check if the game is in stalemate
        # Check if the current player is in check
        if self.is_check(self.board, self.current_player):
            return False
        if self.current_player == "white":
            piece_list = self.white_pieces
        else:
            piece_list = self.black_pieces
        # Check if any pieces of the current player can move
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece in piece_list:
                    for move in self.generate_moves(piece):
                        # If the piece has a valid move, the game is not in stalemate
                        if self.is_valid_move(move[0], move[1]):
                            return False

        # If no pieces of the current player can move, the game is in stalemate
        return True

    def switch_player(self):
        # Switch the current player to the other player
        if self.current_player == 'white':
            self.current_player = 'black'
        else:
            self.current_player = 'white'

    # Loops over the self.board 2D list and prints each row, with the pieces
    # separated by vertical bars. The horizontal lines are made using dashes.
    def print_board(self):
        # Print the current state of the board to the console
        for row in self.board:
            row_string = '| '
            for piece in row:
                row_string += piece + ' | '
            print(row_string)
            print('-' * 33)

    def play_game(self):
        # Main game loop, alternate turns until checkmate or stalemate
        while True:
            self.print_board()
            print(f"{self.current_player}'s turn")
            move = input("Enter a move (e.g. 'e2 e4'): ")
            from_square, to_square = move.split()
            if self.is_valid_move(from_square, to_square):
                self.move_piece(from_square, to_square)
                self.moves_played.append(move)
                if self.is_checkmate():
                    self.print_board()
                    print(f"{self.current_player} is in checkmate!")
                    break
                elif self.is_stalemate():
                    self.print_board()
                    print("The game is in stalemate!")
                    break
                self.switch_player()
            else:
                print("Invalid move, try again")

    def get_player_pieces(self, current_player):
        if current_player == "white":
            return self.white_pieces
        return self.black_pieces


    def find_attacking_pieces(self, white_king):
        pass

    def generate_moves(self, piece_square): #use can_move to find immediate moves and generate a list of the moves
        pass

    def is_on_board(self, end_index):
        # endIndex is a tuple right now
        row = end_index[0]
        col = end_index[1]
        return 0 <= row < 8 and 0 <= col < 8

    def is_check(self, current_player):
        # identify correct king location
        if current_player == "white":
            current_king = self.white_king
        else:
            current_king = self.black_king

        # Check if any of the opposing player's pieces can attack the king
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece and piece not in self.get_player_pieces(current_player):
                    if self.is_valid_move(piece, current_king):
                        return True

        # If none of the opposing player's pieces can attack the king, the game is not in check
        return False


