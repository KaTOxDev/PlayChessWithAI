import pygame
import chess
import requests
import os

class ChessGame:
    def __init__(self):
        pygame.init()
        self.SQUARE_SIZE = 80
        self.BOARD_SIZE = self.SQUARE_SIZE * 8
        self.screen = pygame.display.set_mode((self.BOARD_SIZE, self.BOARD_SIZE))
        pygame.display.set_caption("Chess vs AI")
        
        # Load piece images
        self.pieces = {}
        self.load_pieces()
        
        # Initialize chess board
        self.board = chess.Board()
        self.selected_square = None
        
    def load_pieces(self):
        piece_mapping = {
            'p': 'pawn',
            'n': 'knight',
            'b': 'bishop',
            'r': 'rook',
            'q': 'queen',
            'k': 'king'
        }
        color_mapping = {
            'w': 'white',
            'b': 'black'
        }
        
        for piece_short, piece_name in piece_mapping.items():
            for color_short, color_name in color_mapping.items():
                filename = f"{color_name}_{piece_name}.png"
                # Load using the original filename
                piece_image = pygame.image.load(filename)
                # Store using the short name format (e.g., 'wp' for white pawn)
                self.pieces[f"{color_short}{piece_short}"] = pygame.transform.scale(
                    piece_image,
                    (self.SQUARE_SIZE, self.SQUARE_SIZE)
                )

    def draw_board(self):
        for row in range(8):
            for col in range(8):
                color = (235, 235, 208) if (row + col) % 2 == 0 else (119, 148, 85)
                pygame.draw.rect(
                    self.screen, 
                    color, 
                    pygame.Rect(
                        col * self.SQUARE_SIZE, 
                        row * self.SQUARE_SIZE, 
                        self.SQUARE_SIZE, 
                        self.SQUARE_SIZE
                    )
                )

    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                color = 'w' if piece.color else 'b'
                piece_name = f"{color}{piece.symbol().lower()}"
                x = (chess.square_file(square) * self.SQUARE_SIZE)
                y = ((7 - chess.square_rank(square)) * self.SQUARE_SIZE)
                self.screen.blit(self.pieces[piece_name], (x, y))

    def get_ai_move(self):
        fen = self.board.fen()
        url = f"https://lichess.org/api/cloud-eval"
        headers = {"Accept": "application/json"}
        params = {"fen": fen}
        
        try:
            response = requests.get(url, headers=headers, params=params)
            data = response.json()
            move = data['pvs'][0]['moves'].split()[0]
            return chess.Move.from_uci(move)
        except:
            # Fallback to random legal move if API fails
            legal_moves = list(self.board.legal_moves)
            return legal_moves[0] if legal_moves else None

    def run(self):
        running = True
        player_turn = True

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN and player_turn:
                    x, y = pygame.mouse.get_pos()
                    file = x // self.SQUARE_SIZE
                    rank = 7 - (y // self.SQUARE_SIZE)
                    square = chess.square(file, rank)

                    if self.selected_square is None:
                        self.selected_square = square
                    else:
                        move = chess.Move(self.selected_square, square)
                        if move in self.board.legal_moves:
                            self.board.push(move)
                            player_turn = False
                        self.selected_square = None

            if not player_turn and not self.board.is_game_over():
                ai_move = self.get_ai_move()
                if ai_move:
                    self.board.push(ai_move)
                player_turn = True

            # Draw the game state
            self.draw_board()
            self.draw_pieces()
            pygame.display.flip()

            if self.board.is_game_over():
                print("Game Over")
                print(f"Result: {self.board.result()}")
                running = False

        pygame.quit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()