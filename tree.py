class ThetaNode:
    def _init_(self, theta_id: str, move: str = None):
        self.theta_id = theta_id  # Identificador como "θ_1", "θ_2", etc.
        self.move = move          # Movimiento en notación algebraica
        self.left = None          # Rama izquierda (siempre None en nodos θ)
        self.right = None         # Rama derecha (siguiente θ en secuencia)
    
    def is_root(self) -> bool:
        return self.theta_id == "θ_0"

class ChessTree:
    def _init_(self):
        self.root = ThetaNode("θ_0", "Partida")
        self.current_theta = 1
    
    def add_turn(self, white_move: str, black_move: str = None):
        """Añade un turno completo con la estructura exacta de la imagen"""
        new_white = ThetaNode(f"θ_{self.current_theta}", white_move)
        self.current_theta += 1
        
        # Conexión especial como muestra la imagen
        if not self.root.right:
            self.root.right = new_white
        else:
            last = self.root.right
            while last.right:
                last = last.right
            last.right = new_white
        
        if black_move:
            new_black = ThetaNode(f"θ_{self.current_theta}", black_move)
            self.current_theta += 1
            new_white.right = new_black