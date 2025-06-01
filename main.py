import pygame
import chess
import chess.engine
import os
import threading
import sys
from typing import Optional, Tuple, List, Dict
from enum import Enum
import time

class MoveRating(Enum):
    BRILLIANT = "***"
    GREAT = "**"
    GOOD = "*"
    INACCURACY = "?!"
    MISTAKE = "?"
    BLUNDER = "??"

class ChessGame:
    def __init__(self):
        pygame.init()
        
        # Board configuration
        self.SQUARE_SIZE = 60
        self.BOARD_SIZE = self.SQUARE_SIZE * 8
        self.HISTORY_WIDTH = 300
        self.CONTROL_HEIGHT = 100
        self.screen = pygame.display.set_mode((
            self.HISTORY_WIDTH + self.BOARD_SIZE, 
            self.BOARD_SIZE + self.CONTROL_HEIGHT
        ))
        pygame.display.set_caption("Chess vs Stockfish AI")
        
        # Colors
        self.LIGHT_SQUARE = (240, 217, 181)
        self.DARK_SQUARE = (181, 136, 99)
        self.HIGHLIGHT_COLOR = (255, 255, 0, 128)
        self.SELECTED_COLOR = (0, 255, 0, 128)
        self.LAST_MOVE_COLOR = (255, 165, 0, 128)
        self.PANEL_COLOR = (250, 250, 250)
        self.BORDER_COLOR = (200, 200, 200)
        
        # Game state
        self.clock = pygame.time.Clock()
        self.board = chess.Board()
        self.selected_square: Optional[int] = None
        self.pieces = {}
        self.running = True
        self.player_turn = True
        self.game_over = False
        self.last_move: Optional[chess.Move] = None
        self.ai_thinking = False
        
        # Move history and evaluation
        self.move_history: List[Dict] = []
        self.evaluating_move = False
        
        # AI difficulty settings
        self.ai_levels = {
            1: {"time": 0.1, "depth": 5, "name": "Beginner"},
            2: {"time": 0.2, "depth": 8, "name": "Easy"},
            3: {"time": 0.5, "depth": 10, "name": "Medium"},
            4: {"time": 1.0, "depth": 12, "name": "Hard"},
            5: {"time": 2.0, "depth": 15, "name": "Expert"},
            6: {"time": 3.0, "depth": 18, "name": "Master"},
            7: {"time": 5.0, "depth": 20, "name": "Grandmaster"}
        }
        self.current_ai_level = 3
        self.show_level_selector = True
        
        # Fonts
        self.small_font = pygame.font.SysFont("Arial", 16)
        self.font = pygame.font.SysFont("Arial", 20)
        self.big_font = pygame.font.SysFont("Arial", 28)
        self.title_font = pygame.font.SysFont("Arial", 24, bold=True)
        
        # UI elements
        self.scroll_offset = 0
        self.max_visible_moves = 20
        
        # Initialize components
        self.load_pieces()
        self.initialize_engine()
    
    def initialize_engine(self):
        """Initialize the Stockfish engine with error handling."""
        try:
            stockfish_names = [
                "stockfish",
                "stockfish.exe", 
                "stockfish-windows-x86-64-avx2.exe",
                "stockfish-windows-x86-64-avx2",
                "/usr/bin/stockfish",
                "/usr/local/bin/stockfish"
            ]
            
            self.engine = None
            for name in stockfish_names:
                try:
                    self.engine = chess.engine.SimpleEngine.popen_uci(name)
                    print(f"Successfully loaded Stockfish: {name}")
                    break
                except (FileNotFoundError, chess.engine.EngineError):
                    continue
            
            if not self.engine:
                raise FileNotFoundError("Stockfish engine not found")
                
        except Exception as e:
            print(f"Error initializing Stockfish: {e}")
            print("Please install Stockfish and ensure it's in your PATH")
            self.engine = None
    
    def load_pieces(self):
        """Load piece images with error handling."""
        piece_mapping = {
            'p': 'pawn', 'n': 'knight', 'b': 'bishop',
            'r': 'rook', 'q': 'queen', 'k': 'king'
        }
        color_mapping = {'w': 'white', 'b': 'black'}
        
        pieces_loaded = True
        
        for piece_short, piece_name in piece_mapping.items():
            for color_short, color_name in color_mapping.items():
                filename = f"{color_name}_{piece_name}.png"
                filepath = os.path.join("chess", filename)
                
                try:
                    if os.path.exists(filepath):
                        image = pygame.image.load(filepath)
                        self.pieces[f"{color_short}{piece_short}"] = pygame.transform.scale(
                            image, (self.SQUARE_SIZE, self.SQUARE_SIZE)
                        )
                    else:
                        surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
                        color = (255, 255, 255) if color_short == 'w' else (0, 0, 0)
                        pygame.draw.rect(surface, color, (8, 8, self.SQUARE_SIZE-16, self.SQUARE_SIZE-16))
                        
                        text = self.font.render(piece_short.upper(), True, 
                                              (0, 0, 0) if color_short == 'w' else (255, 255, 255))
                        text_rect = text.get_rect(center=(self.SQUARE_SIZE//2, self.SQUARE_SIZE//2))
                        surface.blit(text, text_rect)
                        
                        self.pieces[f"{color_short}{piece_short}"] = surface
                        pieces_loaded = False
                        
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
                    pieces_loaded = False
        
        if not pieces_loaded:
            print("Warning: Using fallback piece graphics.")
    
    def draw_level_selector(self):
        """Draw the AI difficulty level selector."""
        if not self.show_level_selector:
            return
            
        # Semi-transparent overlay
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Selector panel
        panel_width = 400
        panel_height = 350
        panel_x = (self.screen.get_width() - panel_width) // 2
        panel_y = (self.screen.get_height() - panel_height) // 2
        
        panel_rect = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        pygame.draw.rect(self.screen, (255, 255, 255), panel_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), panel_rect, 2)
        
        # Title
        title_text = self.title_font.render("Select AI Difficulty", True, (50, 50, 50))
        title_rect = title_text.get_rect(center=(panel_x + panel_width//2, panel_y + 30))
        self.screen.blit(title_text, title_rect)
        
        # Level buttons
        button_height = 35
        button_spacing = 5
        start_y = panel_y + 70
        
        for level, config in self.ai_levels.items():
            button_y = start_y + (level - 1) * (button_height + button_spacing)
            button_rect = pygame.Rect(panel_x + 20, button_y, panel_width - 40, button_height)
            
            # Button color
            if level == self.current_ai_level:
                button_color = (100, 200, 100)
                text_color = (255, 255, 255)
            else:
                button_color = (220, 220, 220)
                text_color = (50, 50, 50)
            
            pygame.draw.rect(self.screen, button_color, button_rect)
            pygame.draw.rect(self.screen, (100, 100, 100), button_rect, 1)
            
            # Button text
            level_text = f"Level {level}: {config['name']} ({config['time']}s)"
            text_surface = self.font.render(level_text, True, text_color)
            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)
        
        # Start button
        start_button_rect = pygame.Rect(panel_x + 150, panel_y + panel_height , 100, 30)
        pygame.draw.rect(self.screen, (50, 150, 50), start_button_rect)
        pygame.draw.rect(self.screen, (100, 100, 100), start_button_rect, 1)
        
        start_text = self.font.render("Start Game", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=start_button_rect.center)
        self.screen.blit(start_text, start_text_rect)
        
        return panel_rect, start_button_rect
    
    def draw_board(self):
        """Draw the chess board with coordinates."""
        board_x = self.HISTORY_WIDTH
        
        for row in range(8):
            for col in range(8):
                color = self.LIGHT_SQUARE if (row + col) % 2 == 0 else self.DARK_SQUARE
                rect = pygame.Rect(board_x + col * self.SQUARE_SIZE, row * self.SQUARE_SIZE, 
                                 self.SQUARE_SIZE, self.SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
        
        # Draw coordinate labels
        for i in range(8):
            file_label = chr(ord('a') + i)
            text = self.small_font.render(file_label, True, (100, 100, 100))
            self.screen.blit(text, (board_x + i * self.SQUARE_SIZE + 3, self.BOARD_SIZE - 15))
            
            rank_label = str(8 - i)
            text = self.small_font.render(rank_label, True, (100, 100, 100))
            self.screen.blit(text, (board_x + 3, i * self.SQUARE_SIZE + 3))
    
    def draw_highlights(self):
        """Draw square highlights for selected piece and last move."""
        board_x = self.HISTORY_WIDTH
        highlight_surface = pygame.Surface((self.SQUARE_SIZE, self.SQUARE_SIZE), pygame.SRCALPHA)
        
        if self.last_move:
            for square in [self.last_move.from_square, self.last_move.to_square]:
                x = board_x + chess.square_file(square) * self.SQUARE_SIZE
                y = (7 - chess.square_rank(square)) * self.SQUARE_SIZE
                highlight_surface.fill(self.LAST_MOVE_COLOR)
                self.screen.blit(highlight_surface, (x, y))
        
        if self.selected_square is not None:
            x = board_x + chess.square_file(self.selected_square) * self.SQUARE_SIZE
            y = (7 - chess.square_rank(self.selected_square)) * self.SQUARE_SIZE
            highlight_surface.fill(self.SELECTED_COLOR)
            self.screen.blit(highlight_surface, (x, y))
            
            piece = self.board.piece_at(self.selected_square)
            if piece and piece.color == chess.WHITE:
                legal_moves = [move for move in self.board.legal_moves 
                             if move.from_square == self.selected_square]
                
                for move in legal_moves:
                    x = board_x + chess.square_file(move.to_square) * self.SQUARE_SIZE
                    y = (7 - chess.square_rank(move.to_square)) * self.SQUARE_SIZE
                    highlight_surface.fill(self.HIGHLIGHT_COLOR)
                    self.screen.blit(highlight_surface, (x, y))
    
    def draw_pieces(self):
        """Draw all pieces on the board."""
        board_x = self.HISTORY_WIDTH
        
        for square in chess.SQUARES:
            piece = self.board.piece_at(square)
            if piece:
                color = 'w' if piece.color else 'b'
                piece_key = f"{color}{piece.symbol().lower()}"
                
                if piece_key in self.pieces:
                    x = board_x + chess.square_file(square) * self.SQUARE_SIZE
                    y = (7 - chess.square_rank(square)) * self.SQUARE_SIZE
                    self.screen.blit(self.pieces[piece_key], (x, y))
    
    def evaluate_move(self, move: chess.Move, position_before: chess.Board) -> Tuple[MoveRating, float]:
        """Evaluate a move and return rating and score difference."""
        if not self.engine:
            return MoveRating.GOOD, 0.0
        
        try:
            # Get evaluation before the move
            eval_before = self.engine.analyse(position_before, chess.engine.Limit(depth=12))
            score_before = eval_before["score"].relative.score(mate_score=10000) or 0
            
            # Make the move and evaluate
            temp_board = position_before.copy()
            temp_board.push(move)
            eval_after = self.engine.analyse(temp_board, chess.engine.Limit(depth=12))
            score_after = eval_after["score"].relative.score(mate_score=10000) or 0
            
            # Calculate score difference (from the player's perspective)
            if position_before.turn == chess.WHITE:
                score_diff = score_after - score_before
            else:
                score_diff = score_before - score_after
            
            # Rate the move based on score difference
            if score_diff >= 300:
                return MoveRating.BRILLIANT, score_diff / 100
            elif score_diff >= 100:
                return MoveRating.GREAT, score_diff / 100
            elif score_diff >= 0:
                return MoveRating.GOOD, score_diff / 100
            elif score_diff >= -50:
                return MoveRating.INACCURACY, score_diff / 100
            elif score_diff >= -150:
                return MoveRating.MISTAKE, score_diff / 100
            else:
                return MoveRating.BLUNDER, score_diff / 100
                
        except Exception as e:
            print(f"Evaluation error: {e}")
            return MoveRating.GOOD, 0.0
    
    def draw_move_history(self):
        """Draw the move history panel with ratings."""
        # History panel background
        history_rect = pygame.Rect(0, 0, self.HISTORY_WIDTH, self.BOARD_SIZE)
        pygame.draw.rect(self.screen, self.PANEL_COLOR, history_rect)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, history_rect, 1)
        
        # Title
        title_text = self.title_font.render("Move History", True, (50, 50, 50))
        self.screen.blit(title_text, (10, 10))
        
        # AI level display
        level_info = f"AI Level: {self.ai_levels[self.current_ai_level]['name']}"
        level_text = self.small_font.render(level_info, True, (100, 100, 100))
        self.screen.blit(level_text, (10, 35))
        
        # Move list
        start_y = 60
        line_height = 25
        
        visible_moves = self.move_history[-self.max_visible_moves:]
        
        for i, move_data in enumerate(visible_moves):
            y_pos = start_y + i * line_height
            
            if y_pos > self.BOARD_SIZE - 30:
                break
            
            # Move number (for white moves)
            if move_data['color'] == 'white':
                move_num_text = f"{move_data['move_number']}."
                num_surface = self.small_font.render(move_num_text, True, (100, 100, 100))
                self.screen.blit(num_surface, (10, y_pos))
                x_offset = 35
            else:
                x_offset = 45
            
            # Move notation
            move_text = move_data['san']
            color = (50, 50, 50) if move_data['color'] == 'white' else (100, 50, 50)
            move_surface = self.font.render(move_text, True, color)
            self.screen.blit(move_surface, (x_offset, y_pos))
            
            # Move rating
            if 'rating' in move_data:
                rating_color = self.get_rating_color(move_data['rating'])
                rating_surface = self.small_font.render(move_data['rating'].value, True, rating_color)
                self.screen.blit(rating_surface, (x_offset + 80, y_pos + 2))
            
            # Evaluation score
            if 'eval_score' in move_data and abs(move_data['eval_score']) > 0.1:
                score_text = f"{move_data['eval_score']:+.1f}"
                score_color = (0, 150, 0) if move_data['eval_score'] > 0 else (150, 0, 0)
                score_surface = self.small_font.render(score_text, True, score_color)
                self.screen.blit(score_surface, (x_offset + 120, y_pos + 2))
        
        # Evaluation status
        if self.evaluating_move:
            eval_text = self.small_font.render("Evaluating move...", True, (0, 0, 200))
            self.screen.blit(eval_text, (10, self.BOARD_SIZE - 25))
    
    def get_rating_color(self, rating: MoveRating) -> Tuple[int, int, int]:
        """Get color for move rating."""
        colors = {
            MoveRating.BRILLIANT: (255, 215, 0),  # Gold
            MoveRating.GREAT: (0, 200, 0),        # Green
            MoveRating.GOOD: (100, 150, 100),     # Light green
            MoveRating.INACCURACY: (255, 165, 0), # Orange
            MoveRating.MISTAKE: (255, 100, 0),    # Red-orange
            MoveRating.BLUNDER: (200, 0, 0)       # Red
        }
        return colors.get(rating, (100, 100, 100))
    
    def draw_controls(self):
        """Draw the control panel at the bottom."""
        control_rect = pygame.Rect(0, self.BOARD_SIZE, 
                                 self.screen.get_width(), self.CONTROL_HEIGHT)
        pygame.draw.rect(self.screen, self.PANEL_COLOR, control_rect)
        pygame.draw.rect(self.screen, self.BORDER_COLOR, control_rect, 1)
        
        # Game status
        if self.game_over:
            result = self.board.result()
            if result == "1-0":
                status = "White Wins!"
                color = (0, 150, 0)
            elif result == "0-1":
                status = "Black Wins!"
                color = (150, 0, 0)
            else:
                status = "Draw!"
                color = (100, 100, 100)
        elif self.ai_thinking:
            status = "AI is thinking..."
            color = (0, 0, 200)
        elif self.player_turn:
            status = "Your turn (White)"
            color = (0, 150, 0)
        else:
            status = "AI's turn (Black)"
            color = (150, 0, 0)
        
        status_text = self.big_font.render(status, True, color)
        self.screen.blit(status_text, (10, self.BOARD_SIZE + 20))
        
        # Game controls
        controls_text = "R: Restart | L: Change Level | ESC: Quit"
        if self.game_over:
            controls_text += " | Press R to restart"
        
        controls_surface = self.small_font.render(controls_text, True, (100, 100, 100))
        self.screen.blit(controls_surface, (10, self.BOARD_SIZE + 60))
        
        # Move count and check status
        move_info = f"Move: {self.board.fullmove_number}"
        if self.board.is_check():
            move_info += " | CHECK!"
        
        info_surface = self.font.render(move_info, True, (50, 50, 50))
        info_rect = info_surface.get_rect()
        info_rect.topright = (self.screen.get_width() - 10, self.BOARD_SIZE + 20)
        self.screen.blit(info_surface, info_rect)
    
    def get_ai_move(self):
        """Get AI move with selected difficulty level."""
        if not self.engine:
            print("No engine available")
            self.running = False
            return
            
        self.ai_thinking = True
        
        try:
            ai_config = self.ai_levels[self.current_ai_level]
            
            # Store position before AI move for evaluation
            position_before = self.board.copy()
            
            result = self.engine.play(
                self.board, 
                chess.engine.Limit(time=ai_config["time"], depth=ai_config["depth"])
            )
            
            # Evaluate AI move
            self.evaluating_move = True
            rating, eval_score = self.evaluate_move(result.move, position_before)
            self.evaluating_move = False
            
            self.board.push(result.move)
            self.last_move = result.move
            
            # Add move to history
            self.move_history.append({
                'move_number': self.board.fullmove_number - (1 if self.board.turn == chess.WHITE else 0),
                'san': position_before.san(result.move),
                'uci': result.move.uci(),
                'color': 'black',
                'rating': rating,
                'eval_score': eval_score
            })
            
            self.player_turn = True
            print(f"AI played: {result.move} ({rating.value})")
            
        except Exception as e:
            print(f"AI error: {e}")
            self.running = False
        finally:
            self.ai_thinking = False
            self.evaluating_move = False
    
    def handle_promotion(self, move: chess.Move) -> chess.Move:
        """Handle pawn promotion."""
        if move.promotion is None and self.board.piece_at(move.from_square).piece_type == chess.PAWN:
            if (chess.square_rank(move.to_square) == 7 and self.board.turn == chess.WHITE) or \
               (chess.square_rank(move.to_square) == 0 and self.board.turn == chess.BLACK):
                return chess.Move(move.from_square, move.to_square, promotion=chess.QUEEN)
        return move
    
    def handle_click(self, pos: Tuple[int, int]):
        """Handle mouse clicks."""
        x, y = pos
        
        # Handle level selector clicks
        if self.show_level_selector:
            panel_rect, start_button_rect = self.draw_level_selector()
            
            if start_button_rect.collidepoint(pos):
                self.show_level_selector = False
                return
            
            # Check level button clicks
            panel_width = 400
            panel_height = 350
            panel_x = (self.screen.get_width() - panel_width) // 2
            panel_y = (self.screen.get_height() - panel_height) // 2
            
            button_height = 35
            button_spacing = 5
            start_y = panel_y + 70
            
            for level in self.ai_levels.keys():
                button_y = start_y + (level - 1) * (button_height + button_spacing)
                button_rect = pygame.Rect(panel_x + 20, button_y, panel_width - 40, button_height)
                if button_rect.collidepoint(pos):
                    self.current_ai_level = level
                    return
            return
        
        # Handle board clicks
        if not self.player_turn or self.game_over or self.ai_thinking:
            return
            
        if x < self.HISTORY_WIDTH or y >= self.BOARD_SIZE:
            return
            
        board_x = x - self.HISTORY_WIDTH
        file = board_x // self.SQUARE_SIZE
        rank = 7 - (y // self.SQUARE_SIZE)
        
        if file < 0 or file > 7 or rank < 0 or rank > 7:
            return
            
        square = chess.square(file, rank)
        
        if self.selected_square is None:
            piece = self.board.piece_at(square)
            if piece and piece.color == chess.WHITE:
                self.selected_square = square
        else:
            if square == self.selected_square:
                self.selected_square = None
                return
                
            move = chess.Move(self.selected_square, square)
            move = self.handle_promotion(move)
            
            if move in self.board.legal_moves:
                # Store position before move for evaluation
                position_before = self.board.copy()
                
                # Evaluate player move
                self.evaluating_move = True
                rating, eval_score = self.evaluate_move(move, position_before)
                self.evaluating_move = False
                
                self.board.push(move)
                self.last_move = move
                self.player_turn = False
                self.selected_square = None
                
                # Add move to history
                self.move_history.append({
                    'move_number': self.board.fullmove_number - (0 if self.board.turn == chess.WHITE else 1),
                    'san': position_before.san(move),
                    'uci': move.uci(),
                    'color': 'white',
                    'rating': rating,
                    'eval_score': eval_score
                })
                
                print(f"You played: {move} ({rating.value})")
                
                if not self.board.is_game_over():
                    threading.Thread(target=self.get_ai_move, daemon=True).start()
            else:
                piece = self.board.piece_at(square)
                if piece and piece.color == chess.WHITE:
                    self.selected_square = square
                else:
                    self.selected_square = None
    
    def restart_game(self):
        """Restart the game."""
        self.board = chess.Board()
        self.selected_square = None
        self.player_turn = True
        self.game_over = False
        self.last_move = None
        self.ai_thinking = False
        self.move_history = []
        self.evaluating_move = False
        print("Game restarted!")
    
    def run(self):
        """Main game loop."""
        print("Chess Game Started!")
        print("You are playing as White")
        if not self.engine:
            print("Warning: No AI opponent available")
        
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self.handle_click(pygame.mouse.get_pos())
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.restart_game()
                    elif event.key == pygame.K_l:
                        self.show_level_selector = True
                    elif event.key == pygame.K_ESCAPE:
                        self.running = False
            
            # Check for game over
            if self.board.is_game_over() and not self.game_over:
                self.game_over = True
                result = self.board.result()
                print(f"Game Over! Result: {result}")
                if result == "1-0":
                    print("You won!")
                elif result == "0-1":
                    print("AI won!")
                else:
                    print("It's a draw!")
            
            # Draw everything
            self.screen.fill(self.PANEL_COLOR)
            
            if not self.show_level_selector:
                self.draw_move_history()
                self.draw_board()
                self.draw_highlights()
                self.draw_pieces()
                self.draw_controls()
            else:
                self.draw_level_selector()
            
            pygame.display.flip()
            self.clock.tick(60)
        
        # Cleanup
        if self.engine:
            self.engine.quit()
        pygame.quit()
        print("Thanks for playing!")

def main():
    """Entry point of the application."""
    try:
        game = ChessGame()
        game.run()
    except KeyboardInterrupt:
        print("\nGame interrupted by user")
    except Exception as e:
        print(f"An error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()