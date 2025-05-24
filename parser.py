import re


class ChessParser:
    def __init__(self):
        self.move_pattern = re.compile(r'(\d+)\.\s+(\S+)\s+(\S+)')
        self.single_move_pattern = re.compile(r'^([KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#]?|O-O(?:-O)?)$')

    def parse_game(self, game_str: str):
        turns = []
        for line in game_str.split('\n'):
            line = line.strip()
            if not line:
                continue

            matches = self.move_pattern.findall(line)
            for match in matches:
                turn_num = int(match[0])
                white = match[1]
                black = match[2] if len(match) > 2 else None

                if not self._validate_move(white) or (black and not self._validate_move(black)):
                    raise ValueError(f"Invalid move in turn {turn_num}")

                turns.append((turn_num, white, black))
        return turns

    def _validate_move(self, move: str) -> bool:
        return bool(self.single_move_pattern.match(move))