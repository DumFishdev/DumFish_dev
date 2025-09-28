#!/usr/bin/env python3
import sys
import chess
import chess.engine
from engine import Engine
from search import Search
from evaluation import Evaluate
from transposition import TranspositionTable

class UCI:
    def __init__(self):
        self.board = chess.Board()
        self.tt = TranspositionTable()
        self.search = Search(tt=self.tt)  # Pass TT to Search

    def run(self):
        while True:
            line = sys.stdin.readline()
            if not line:
                break
            line = line.strip()
            if line == "uci":
                print("id name Dedicated DumFish")
                print("id author pg")
                print("uciok")
            elif line == "isready":
                print("readyok")
            elif line.startswith("setoption"):
                pass
            elif line.startswith("ucinewgame"):
                self.board.reset()
                self.tt.clear()
            elif line.startswith("position"):
                self._set_position(line)
            elif line.startswith("go"):
                self._go(line)
            elif line == "quit":
                break

    def _set_position(self, line):
        if "startpos" in line:
            self.board.reset()
            moves = line.split("moves")
            if len(moves) > 1:
                for move in moves[1].strip().split():
                    self.board.push_uci(move)
        elif "fen" in line:
            fen = line.split("fen")[1].split("moves")[0].strip()
            self.board.set_fen(fen)
            if "moves" in line:
                moves = line.split("moves")[1].strip().split()
                for move in moves:
                    self.board.push_uci(move)

    def _go(self, line):
        # Default depth
        depth = self.search.depth
        if "depth" in line:
            try:
                depth = int(line.split("depth")[1].strip().split()[0])
                self.search.set_depth(depth)
            except Exception:
                pass
        # Search one ply deeper
        search_depth = depth + 1

        best_move = None
        best_score = float('-inf') if self.board.turn == chess.WHITE else float('inf')
        for move in self.board.legal_moves:
            self.board.push(move)
            score = self.search.alpha_beta(self.board, depth=search_depth, maximizing_player=not self.board.turn)
            self.board.pop()
            if self.board.turn == chess.WHITE:
                if score > best_score:
                    best_score = score
                    best_move = move
            else:
                if score < best_score:
                    best_score = score
                    best_move = move
        if best_move:
            print(f"bestmove {best_move.uci()}")

if __name__ == "__main__":
    UCI().run()
