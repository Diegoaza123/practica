class ChessTreeVisualizer:
    def __init__(self):
        """Inicializa los códigos de color para la visualización"""
        self.colors = {
            'white': '\033[34m',  # Azul para blancas
            'black': '\033[31m',  # Rojo para negras
            'turn': '\033[1m',    # Negrita para turnos
            'reset': '\033[0m'    # Resetear color
        }

    def display(self, node, prefix="", is_last=True):
        """
        Muestra el árbol de forma recursiva con formato jerárquico
        :param node: Nodo actual
        :param prefix: Prefijo para indentación
        :param is_last: Si es el último hijo de su padre
        """
        if not node:
            return

        # Configurar conexión y color
        connector = "└── " if is_last else "├── "
        color = self.colors.get(node.player, self.colors['turn'])
        reset = self.colors['reset']

        # Imprimir nodo actual
        print(f"{prefix}{connector}{color}{node.name}{reset}")

        # Nuevo prefijo para hijos
        new_prefix = prefix + ("    " if is_last else "│   ")

        # Imprimir hijos recursivamente
        for i, child in enumerate(node.children):
            self.display(child, new_prefix, i == len(node.children) - 1)