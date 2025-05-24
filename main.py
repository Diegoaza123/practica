from tree import ChessGameTree
from parser import ChessParser
from display import TreeDisplay


def main():
    # Ejemplo de partida de ajedrez
    game_san = """
    1. e4 e5
    2. Nf3 Nc6
    3. Bb5 a6
    4. Ba4 Nf6
    5. O-O Be7
    6. Re1 b5
    7. Bb3 d6
    8. c3 O-O
    """

    # Procesar la partida
    parser = ChessParser()
    game_tree = ChessGameTree()

    try:
        moves = parser.parse_game(game_san)
        for turn, white, black in moves:
            game_tree.add_move(turn, white, black)

        # Mostrar el árbol
        print("Árbol de Movimientos de Ajedrez:")
        TreeDisplay.print_tree(game_tree.root)

    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()