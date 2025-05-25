import re
from typing import List, Tuple


class ChessParser:
    def __init__(self):
        """Inicializa con los patrones regex para análisis de movimientos"""
        self.turn_pattern = re.compile(r'^\s*(\d+)\.\s+(\S+)\s+(\S+)\s*$')
        self.move_pattern = re.compile(
            r'^([KQRBNP]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#]?|O-O(?:-O)?|0-0(?:-0)?)$'
        )

    def parse_game(self, game_str: str) -> List[Tuple[int, str, str]]:
        """
        Analiza una partida en notación algebraica
        :param game_str: Cadena con la partida en SAN
        :return: Lista de tuplas (turno, movimiento_blanco, movimiento_negro)
        """
        turns = []
        for line in game_str.split('\n'):
            line = line.strip()
            if not line:
                continue

            match = self.turn_pattern.match(line)
            if match:
                turn_num = int(match.group(1))
                white_move = match.group(2)
                black_move = match.group(3)

                if not self.is_valid_move(white_move) or not self.is_valid_move(black_move):
                    raise ValueError(f"Movimiento inválido en turno {turn_num}")

                turns.append((turn_num, white_move, black_move))

        return turns

    def is_valid_move(self, move: str) -> bool:
        """Valida si un movimiento sigue la notación algebraica estándar"""
        return bool(self.move_pattern.match(move))