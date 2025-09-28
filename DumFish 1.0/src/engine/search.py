from evaluation import Evaluate
import chess

class Search:
    MAX_DEPTH = 30

    def __init__(self, depth=28, tt=None):
        self.depth = min(depth + 1, self.MAX_DEPTH)  # Always search one deeper
        self.tt = tt

    def alpha_beta(self, board, depth=None, alpha=float('-inf'), beta=float('inf'), maximizing_player=True, ply=1):
        if depth is None:
            depth = self.depth
        if depth == 0 or board.is_game_over():
            print(f"Reached ply {ply}: {board.fen()} | Eval: {Evaluate.evaluation_from_board(board)}")
            return Evaluate.evaluation_from_board(board)

        # Transposition table lookup
        if self.tt:
            entry = self.tt.lookup(board, depth)
            if entry:
                print(f"TT hit at ply {ply}: {board.fen()} | Score: {entry['score']}")
                return entry["score"]

        if maximizing_player:
            max_eval = float('-inf')
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, False, ply + 1)
                board.pop()
                if eval > max_eval:
                    max_eval = eval
                    best_move = move
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break
            if self.tt:
                self.tt.store(board, depth, max_eval, best_move)
            if ply == 1:
                print(f"Best move at root: {best_move} | Score: {max_eval}")
            return max_eval
        else:
            min_eval = float('inf')
            best_move = None
            for move in board.legal_moves:
                board.push(move)
                eval = self.alpha_beta(board, depth - 1, alpha, beta, True, ply + 1)
                board.pop()
                if eval < min_eval:
                    min_eval = eval
                    best_move = move
                beta = min(beta, eval)
                if beta <= alpha:
                    break
            if self.tt:
                self.tt.store(board, depth, min_eval, best_move)
            if ply == 1:
                print(f"Best move at root: {best_move} | Score: {min_eval}")
            return min_eval

    def iterative_deepening(self, board, max_depth=None, maximizing_player=True):
        if max_depth is None:
            max_depth = self.depth
        best_score = None
        # Go one depth higher than requested
        for current_depth in range(1, max_depth + 2):
            print(f"\nAnalyzing position up to ply {current_depth}: {board.fen()}")
            best_score = self.alpha_beta(board, depth=current_depth, maximizing_player=maximizing_player, ply=1)
            print(f"Depth {current_depth}: Best score {best_score}")
        return best_score

    def set_depth(self, ply):
        self.depth = min(ply + 1, self.MAX_DEPTH)  # Always search one deeper

    def analyze_positions(self, positions_with_plys):
        for board, ply in positions_with_plys:
            print(f"\n--- Iterative Deepening up to ply {ply} ---")
            self.iterative_deepening(board, max_depth=ply, maximizing_player=board.turn)
