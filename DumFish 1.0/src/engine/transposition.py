import chess
from typing import Optional, Dict, Tuple, Any

class TranspositionTable:
    """
    Stores evaluated positions to avoid redundant calculations during search.
    Key: (hash(board.fen()), ply)
    Value: dict with score, depth, seen count, move (as UCI string)
    """
    def __init__(self):
        self.table: Dict[Tuple[int, int], Dict[str, Any]] = {}

    def store(self, board: chess.Board, ply: int, score: float, move: Optional[chess.Move] = None) -> None:
        key = (hash(board.fen()), ply)
        move_uci = move.uci() if move is not None else None
        entry = self.table.get(key)
        if entry is None or ply > entry["depth"]:
            self.table[key] = {
                "score": score,
                "depth": ply,
                "seen": 1,
                "move": move_uci
            }
        else:
            self.table[key]["seen"] += 1
            if move_uci is not None:
                self.table[key]["move"] = move_uci

    def lookup(self, board: chess.Board, ply: int) -> Optional[Dict[str, Any]]:
        key = (hash(board.fen()), ply)
        return self.table.get(key, None)

    def update_after_game(self, board_list) -> None:
        for board, ply in board_list:
            key = (hash(board.fen()), ply)
            if key in self.table:
                self.table[key]["seen"] += 1

    def clear(self) -> None:
        self.table.clear()
