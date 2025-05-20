from tree import ChessTree
from parser import ChessParser
from display import TreeVisualizer

def main():
    # Partida de ejemplo (puedes reemplazarla con tu entrada)
    game_san = """
    1. e4 e5
    2. Nf3 Nc6
    3. Bb5 a6
    4. Ba4 Nf6
    5. O-O Be7
    """
    
    # Procesamiento
    parser = ChessParser()
    game_tree = ChessTree()
    
    # Construcción del árbol con estructura θ exacta
    for white, black in parser.parse_game(game_san):
        game_tree.add_turn(white, black)
    
    # Visualización
    print("Árbol de Movimientos (Estructura θ Exacta):")
    TreeVisualizer.display(game_tree.root)

if _name_ == "_main_":
    main()