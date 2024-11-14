from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTextEdit, QDockWidget
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QWindow
from PySide6.QtWidgets import QWidget
from .objects_bar import ObjectsBar
from .state_bar import StateWidget
from .code_preview_window import CodePreviewWindow
from .preview_window import PreviewWindow

class MainWindow(QMainWindow):
    def __init__(self, scene_controller, scene_state_controller, close_handler, pyqt5_app, renderer):
        super().__init__()
        self.setWindowTitle("Manimate")
        self.setGeometry(100, 100, 1600, 900)
        self.close_handler = close_handler
        
        self.widgets = []
        
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        splitter = QSplitter(Qt.Horizontal)
        
        self.objects_panel = ObjectsBar(scene_state_controller, self.handle_child_close)
        self.objects_panel.setMaximumWidth(300)
        splitter.addWidget(self.objects_panel)
        self.widgets.append(self.objects_panel)
        
        self.preview_window = PreviewWindow(pyqt5_app, renderer, self.handle_child_close)
        
        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        
        window = QWindow.fromWinId(self.preview_window._widget.winId())
        widget_container = QWidget.createWindowContainer(window)
        preview_layout.addWidget(widget_container)
        preview_layout.setContentsMargins(0, 0, 0, 0)
        
        splitter.addWidget(preview_container)
        self.widgets.append(self.preview_window._widget)
        
        self.code_preview = CodePreviewWindow(scene_state_controller, self.handle_child_close)
        self.code_preview.setMaximumWidth(400)
        splitter.addWidget(self.code_preview)
        self.widgets.append(self.code_preview)
        
        main_layout.addWidget(splitter)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        state_dock = QDockWidget("Timeline", self)
        state_dock.setFeatures(QDockWidget.DockWidgetFloatable | QDockWidget.DockWidgetMovable)
        self.state_widget = StateWidget(scene_controller, scene_state_controller, self.handle_child_close)
        state_dock.setWidget(self.state_widget)
        self.addDockWidget(Qt.BottomDockWidgetArea, state_dock)
        self.widgets.append(self.state_widget)
        
        splitter.setSizes([300, 1000, 300])
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e1e;
            }
            QDockWidget {
                color: #f0f0f0;
                titlebar-close-icon: url(close.png);
                titlebar-normal-icon: url(float.png);
            }
            QDockWidget::title {
                background-color: #2a2a2a;
                padding-left: 5px;
                padding-top: 2px;
            }
            QSplitter::handle {
                background-color: #2a2a2a;
            }
            QSplitter::handle:horizontal {
                width: 2px;
            }
        """)

    def handle_child_close(self):
        sender = self.sender()
        if sender in self.widgets:
            sender.hide()

    def closeEvent(self, event):
        for widget in self.widgets:
            widget.close()
        
        self.close_handler()
        event.accept()

