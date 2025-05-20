class TreeVisualizer:
    @staticmethod
    def display(node, prefix="", is_last=True):
        if node is None:
            return
        
        # Configuración de colores
        color_code = ""
        reset_code = "\033[0m"
        if not node.is_root():
            color_code = "\033[34m" if int(node.theta_id.split('_')[1]) % 2 == 1 else "\033[31m"
        
        # Línea de conexión especial
        connector = "└─ " if is_last else "├─ "
        
        # Formato θ con movimiento
        display_text = f"{node.theta_id}"
        if node.move and not node.is_root():
            display_text += f" ({node.move})"
        
        print(f"{prefix}{connector}{color_code}{display_text}{reset_code}")
        
        # Prefijo para niveles inferiores
        new_prefix = prefix + ("   " if is_last else "│  ")
        
        # Solo mostrar conexiones derechas como en la imagen
        if node.right:
            TreeVisualizer.display(node.right, new_prefix, True)