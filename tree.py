class ChessNode:
    def __init__(self, name: str, turn: int = None, player: str = None):
        """
        Nodo del árbol de ajedrez
        :param name: Nombre del nodo (ej: "e4", "Turno 1")
        :param turn: Número de turno
        :param player: 'white' o 'black'
        """
        self.name = name
        self.turn = turn
        self.player = player
        self.children = []
        self.parent = None

    def add_child(self, child_node):
        """Añade un nodo hijo y establece la relación padre-hijo"""
        child_node.parent = self
        self.children.append(child_node)
        return child_node


class ChessGameTree:
    def __init__(self):
        """Inicializa el árbol con un nodo raíz 'Partida'"""
        self.root = ChessNode("Partida")
        self.current_white = None  # Último nodo de movimiento blanco añadido
        self.current_black = None  # Último nodo de movimiento negro añadido

    def add_turn(self, turn_num: int, white_move: str, black_move: str):
        """
        Añade un turno completo al árbol
        :param turn_num: Número de turno (1, 2, 3...)
        :param white_move: Movimiento blanco en notación algebraica
        :param black_move: Movimiento negro en notación algebraica
        """
        # Crear nodo de turno
        turn_node = ChessNode(f"Turno {turn_num}", turn_num)

        # Añadir movimiento blanco
        white_node = ChessNode(f"Blanco: {white_move}", turn_num, 'white')
        turn_node.add_child(white_node)

        # Añadir movimiento negro
        black_node = ChessNode(f"Negro: {black_move}", turn_num, 'black')
        turn_node.add_child(black_node)

        # Enlazar el turno al árbol
        if not self.root.children:
            # Primer turno
            self.root.add_child(turn_node)
        else:
            # Enlazar con el último movimiento negro
            self.current_black.add_child(turn_node)

        # Actualizar referencias
        self.current_white = white_node
        self.current_black = black_node