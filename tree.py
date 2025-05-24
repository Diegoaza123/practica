class MoveNode:
    def __init__(self, move: str, player: str, turn: int):
        self.move = move
        self.player = player  # 'white' o 'black'
        self.turn = turn
        self.left = None  # Movimiento blanco siguiente
        self.right = None  # Movimiento negro siguiente


class ChessGameTree:
    def __init__(self):
        self.root = MoveNode("Game Start", None, 0)

    def add_move(self, turn: int, white_move: str, black_move: str = None):
        current = self.root
        # Navegar hasta el último turno completo
        while current.right and turn > current.turn:
            current = current.right

        # Añadir movimientos del turno actual
        if white_move:
            current.left = MoveNode(white_move, 'white', turn)
        if black_move:
            current.right = MoveNode(black_move, 'black', turn)