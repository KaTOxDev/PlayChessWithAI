import pygame
import chess
import chess.engine
import os
import threading

class ChessGame:
    def __init__(self):
        pygame.init()
        self.SQUARE_SIZE = 80
        self.BOARD_SIZE = self.SQUARE_SIZE * 8
        self.screen = pygame.display.set_mode((self.BOARD_SIZE, self.BOARD_SIZE))
        pygame.display.set_caption("Chess vs Stockfish AI")

        self.clock = pygame.time.Clock()
        self.board = chess.Board()
        self.selected_square = None
        self.pieces = {}
        self.running = True
        self.player_turn = True
        self.game_over = False
        self.last_move = None

        self.load_pieces()
        self.engine = chess.engine.SimpleEngine.popen_uci("stockfish-windows-x86-64-avx2")

    def load_pieces(self):
        piece_mapping = {
            'p': 'pawn', 'n': 'knight', 'b': 'bishop',
            'r': 'rook', 'q': 'queen', 'k': 'king'
        }
        color_mapping = {'w': 'white', 'b': 'black'}

        for piece_short, piece_name in piece_mapping.items():
            for color_short, color_name in color_mapping.items():
                filename = f"{color_name}_{piece_name}.png"
                image = pygame.image.load(os.path.join("chess", filename))
                self.pieces[f"{color_short}{piece_short}"] = pygame.transform.scale(image, (self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_board(self):
        colors = [(235, 235, 208), (119, 148, 85)]
        for row in range(8):
            for col in range(8):
                color = colors[(row + col) % 2]
                rect = pygame.Rect(col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

        # Highlight last move
        if self.last_move:
            for square in [self.last_move.from_square, self.last_move.to_square]:
                x = chess.square_file(square) * self.SQUARE_SIZE
                y = (7 - chess.square_rank(square)) * self.SQUARE_SIZE
                pygame.draw.rect(self.screen, (246, 246, 105), (x, y, self.SQUARE_SIZE, self.SQUARE_SIZE))

    def draw_pieces(self):
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                color = 'w' if piece.color else 'b'
                name = f"{color}{piece.symbol().lower()}"
                x = chess.square_file(square) * self.SQUARE_SIZE
                y = (7 - chess.square_rank(square)) * self.SQUARE_SIZE
                self.screen.blit(self.pieces[name], (x, y))

    def get_ai_move(self):
        try:
            result = self.engine.play(self.board, chess.engine.Limit(time=0.5))
            self.board.push(result.move)
            self.last_move = result.move
            self.player_turn = True
        except Exception as e:
            print("Stockfish had a meltdown:", e)
            self.running = False

    def handle_click(self, pos):
        x, y = pos
        file = x // self.SQUARE_SIZE
        rank = 7 - (y // self.SQUARE_SIZE)
        square = chess.square(file, rank)

        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                self.selected_square = square
        else:
            move = chess.Move(self.selected_square, square)
            if move in self.board.legal_moves:
                self.board.push(move)
                self.last_move = move
                self.player_turn = False
                threading.Thread(target=self.get_ai_move).start()
            self.selected_square = None

    def display_game_over(self):
        font = pygame.font.SysFont("Arial", 36)
        text = font.render(f"Game Over: {self.board.result()}", True, (255, 0, 0))
        rect = text.get_rect(center=(self.BOARD_SIZE//2, self.BOARD_SIZE//2))
        self.screen.blit(text, rect)

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN and self.player_turn and not self.game_over:
                    self.handle_click(pygame.mouse.get_pos())

            self.draw_board()
            self.draw_pieces()

            if self.board.is_game_over() and not self.game_over:
                self.game_over = True
                print("Game Over!", self.board.result())

            if self.game_over:
                self.display_game_over()

            pygame.display.flip()
            self.clock.tick(60)

        self.engine.quit()
        pygame.quit()

if __name__ == "__main__":
    game = ChessGame()
    game.run()
