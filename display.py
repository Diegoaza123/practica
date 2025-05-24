class TreeDisplay:
    @staticmethod
    def print_tree(node, prefix="", is_last=True):
        if node is None:
            return

        # Configuración de colores
        colors = {
            'white': '\033[34m',  # Azul
            'black': '\033[31m',  # Rojo
            'reset': '\033[0m'
        }

        # Determinar el color según el jugador
        color = colors.get(node.player, '')
        reset = colors['reset']

        # Construir el prefijo visual
        branch = "└── " if is_last else "├── "
        print(f"{prefix}{branch}{color}{node.move}{reset}")

        # Nuevo prefijo para los siguientes niveles
        new_prefix = prefix + ("    " if is_last else "│   ")

        # Mostrar hijos (primero izquierdo, luego derecho)
        children = []
        if node.left:
            children.append(node.left)
        if node.right:
            children.append(node.right)

        for i, child in enumerate(children):
            is_last_child = i == len(children) - 1
            TreeDisplay.print_tree(child, new_prefix, is_last_child)