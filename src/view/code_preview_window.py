from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from PySide6.QtGui import QFont

class CodePreviewWindow(QWidget):
    def __init__(self, scene_state_controller, close_handler):
        super().__init__()

        self.scene_state_controller = scene_state_controller
        self.close_handler = close_handler

        self.setWindowTitle("Generated Code Preview")
        self.setGeometry(1450, 850, 450, 300)

        layout = QVBoxLayout()
        self.code_text = QTextEdit()
        self.code_text.setReadOnly(True)
        font = QFont("Courier", 10)
        self.code_text.setFont(font)

        layout.addWidget(self.code_text)
        self.setLayout(layout)

        # Connect to scene state controller's signal for code updates
        self.scene_state_controller.codeUpdated.connect(self.update_code)

    def update_code(self, code):
        self.code_text.setText(code)

    def closeEvent(self, event):
        self.close_handler()
        event.accept()
