import re

class ChessParser:
    def _init_(self):
        self.move_pattern = re.compile(r'(\d+)\.\s+(\S+)\s+(\S+)')

    def parse_game(self, game_str: str):
        moves = []
        for line in game_str.split('\n'):
            line = line.strip()
            if not line:
                continue
            matches = self.move_pattern.findall(line)
            for match in matches:
                white = match[1]
                black = match[2] if len(match) > 2 else None
                moves.append((white, black))
        return moves