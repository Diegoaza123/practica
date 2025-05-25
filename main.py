import sys
import re
from PyQt5.QtWidgets import (QApplication, QMainWindow, QTextEdit, QPushButton,
                             QVBoxLayout, QWidget, QLabel, QHBoxLayout, QTreeView,
                             QMessageBox)
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt


class ChessParser:
    def __init__(self):
        """Inicializa con patrones regex para validar movimientos"""
        self.turn_pattern = re.compile(r'^\s*(\d+)\.\s+(\S+)\s+(\S+)\s*$')
        self.move_pattern = re.compile(
            r'^([KQRBN]?[a-h]?[1-8]?x?[a-h][1-8](?:=[QRBN])?[+#]?|O-O(?:-O)?|0-0(?:-0)?)$'
        )

    def parse_game(self, game_str):
        """Analiza la partida y devuelve los movimientos o errores"""
        turns = []
        errors = []
        for line_num, line in enumerate(game_str.split('\n'), 1):
            line = line.strip()
            if not line:
                continue

            match = self.turn_pattern.match(line)
            if match:
                turn_num = match.group(1)
                white = match.group(2)
                black = match.group(3)

                if not self.is_valid_move(white):
                    errors.append(f"Turno {turn_num}: Movimiento blanco inválido '{white}'")
                if not self.is_valid_move(black):
                    errors.append(f"Turno {turn_num}: Movimiento negro inválido '{black}'")

                turns.append((turn_num, white, black))
            elif line:  # Si hay contenido pero no coincide con el patrón
                errors.append(f"Línea {line_num}: Formato inválido '{line}'")

        return turns, errors

    def is_valid_move(self, move):
        """Valida si un movimiento sigue la notación algebraica estándar"""
        return bool(self.move_pattern.match(move))


class ChessTreeBuilder:
    def __init__(self):
        """Inicializa el modelo para el árbol visual"""
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(['Árbol de Partida de Ajedrez'])

    def build_tree(self, turns):
        """Construye la estructura jerárquica del árbol"""
        self.model.clear()
        self.model.setHorizontalHeaderLabels(['Árbol de Partida de Ajedrez'])
        root = self.model.invisibleRootItem()

        # Nodo raíz
        partida_item = QStandardItem("Partida")
        root.appendRow(partida_item)

        last_black_item = partida_item

        for turn_num, white, black in turns:
            # Crear items para el turno
            turn_item = QStandardItem(f"Turno {turn_num}")
            white_item = QStandardItem(f"Blanco: {white}")
            black_item = QStandardItem(f"Negro: {black}")

            # Establecer colores y formato
            white_item.setForeground(Qt.blue)
            black_item.setForeground(Qt.red)
            turn_item.setForeground(Qt.darkMagenta)
            turn_item.setFont(self.bold_font())

            # Añadir movimientos al turno
            turn_item.appendRow(white_item)
            turn_item.appendRow(black_item)

            # Conectar con el último movimiento negro
            last_black_item.appendRow(turn_item)
            last_black_item = black_item

        return self.model

    def bold_font(self):
        """Devuelve una fuente en negrita"""
        font = QStandardItem().font()
        font.setBold(True)
        return font


class ChessApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Analizador de Ajedrez - Visualizador de Árbol")
        self.setGeometry(100, 100, 900, 700)
        self.setup_ui()

        # Componentes principales
        self.parser = ChessParser()
        self.tree_builder = ChessTreeBuilder()

    def setup_ui(self):
        """Configura la interfaz de usuario"""
        # Widgets principales
        self.input_text = QTextEdit()
        self.input_text.setPlaceholderText(
            "Ingresa la partida en notación algebraica (ej: 1. e4 e5)\n"
            "Cada turno en una línea separada"
        )
        self.input_text.setStyleSheet("font-family: Consolas; font-size: 12px;")

        self.tree_view = QTreeView()
        self.tree_view.setHeaderHidden(False)
        self.tree_view.setStyleSheet("""
            QTreeView {
                font-family: Consolas;
                font-size: 12px;
                show-decoration-selected: 1;
            }
            QTreeView::item {
                height: 22px;
                padding: 2px;
            }
        """)

        self.status_label = QLabel("Estado: Esperando entrada de partida...")
        self.status_label.setStyleSheet("""
            font-weight: bold;
            font-size: 12px;
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 3px;
        """)

        # Botones
        self.analyze_btn = QPushButton("Analizar Movimientos")
        self.analyze_btn.setStyleSheet("padding: 5px;")
        self.analyze_btn.clicked.connect(self.analyze_game)

        self.example_btn = QPushButton("Cargar Ejemplo")
        self.example_btn.setStyleSheet("padding: 5px;")
        self.example_btn.clicked.connect(self.load_example)

        self.clear_btn = QPushButton("Limpiar Todo")
        self.clear_btn.setStyleSheet("padding: 5px;")
        self.clear_btn.clicked.connect(self.clear_all)

        # Diseño de los botones
        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.analyze_btn)
        btn_layout.addWidget(self.example_btn)
        btn_layout.addWidget(self.clear_btn)
        btn_layout.setSpacing(10)

        # Diseño principal
        main_layout = QVBoxLayout()
        main_layout.addWidget(QLabel("Ingresa la partida de ajedrez:"))
        main_layout.addWidget(self.input_text)
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(QLabel("Árbol de Movimientos:"))
        main_layout.addWidget(self.tree_view)
        main_layout.addWidget(self.status_label)
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(10, 10, 10, 10)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def analyze_game(self):
        """Analiza la partida y muestra el árbol"""
        game_text = self.input_text.toPlainText().strip()
        if not game_text:
            self.show_warning("Por favor ingresa una partida para analizar")
            return

        turns, errors = self.parser.parse_game(game_text)

        if errors:
            error_msg = "\n".join(errors)
            self.show_errors(error_msg)
            self.status_label.setText("Estado: Partida con errores - Ver detalles")
            self.status_label.setStyleSheet("""
                color: #d32f2f;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
                border: 1px solid #d32f2f;
                border-radius: 3px;
                background-color: #ffebee;
            """)
        else:
            model = self.tree_builder.build_tree(turns)
            self.tree_view.setModel(model)
            self.expand_all_nodes()
            self.status_label.setText("Estado: Partida válida - Árbol generado")
            self.status_label.setStyleSheet("""
                color: #388e3c;
                font-weight: bold;
                font-size: 12px;
                padding: 5px;
                border: 1px solid #388e3c;
                border-radius: 3px;
                background-color: #e8f5e9;
            """)

    def expand_all_nodes(self):
        """Expande todos los nodos del árbol automáticamente"""

        def recursive_expand(index):
            self.tree_view.expand(index)
            for i in range(self.tree_view.model().rowCount(index)):
                recursive_expand(self.tree_view.model().index(i, 0, index))

        root_index = self.tree_view.model().index(0, 0)
        recursive_expand(root_index)

    def load_example(self):
        """Carga una partida de ejemplo"""
        example = """1. e4 e5
2. Nf3 Nc6
3. Bb5 a6
4. Ba4 Nf6
5. O-O Be7
6. Re1 b5
7. Bb3 d6
8. c3 O-O
9. h3 Bb7
10. d4 Re8"""
        self.input_text.setPlainText(example)
        self.status_label.setText("Estado: Ejemplo cargado - Listo para analizar")
        self.status_label.setStyleSheet("""
            color: #1976d2;
            font-weight: bold;
            font-size: 12px;
            padding: 5px;
            border: 1px solid #1976d2;
            border-radius: 3px;
            background-color: #e3f2fd;
        """)

    def clear_all(self):
        """Limpia toda la entrada y resultados"""
        self.input_text.clear()
        self.tree_view.setModel(QStandardItemModel())
        self.status_label.setText("Estado: Esperando entrada de partida...")
        self.status_label.setStyleSheet("""
            font-weight: bold;
            font-size: 12px;
            padding: 5px;
            border: 1px solid #ccc;
            border-radius: 3px;
        """)

    def show_errors(self, error_msg):
        """Muestra un diálogo con los errores encontrados"""
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowTitle("Errores en la partida")
        msg.setText("Se encontraron los siguientes errores:")
        msg.setDetailedText(error_msg)
        msg.setStandardButtons(QMessageBox.Ok)
        msg.exec_()

    def show_warning(self, message):
        """Muestra un mensaje de advertencia simple"""
        QMessageBox.warning(self, "Advertencia", message)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle('Fusion')  # Mejor aspecto visual

    # Establecer paleta de colores consistente
    palette = app.palette()
    palette.setColor(palette.Window, Qt.white)
    palette.setColor(palette.WindowText, Qt.black)
    app.setPalette(palette)

    window = ChessApp()
    window.show()
    sys.exit(app.exec_())