import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QSpinBox, QDoubleSpinBox,
    QRadioButton, QPushButton, QVBoxLayout, QFormLayout,
    QMessageBox, QGroupBox, QAbstractSpinBox, QCheckBox
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

import export.writeGraph as w
import visualization.drawGraph as d
import generation.generateGraph as gen

from pathlib import Path
import shutil

class GraphGeneratorUI(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Генератор графов")
        self.resize(900, 700)

        # Главный layout
        main_layout = QVBoxLayout()

        # -------------------------
        # Верхняя часть — изображение
        # -------------------------
        self.image_label = QLabel("Здесь будет изображение графа")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(450)

        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px solid gray;
                background-color: black;
                font-size: 16px;
            }
        """)

        main_layout.addWidget(self.image_label)

        # -------------------------
        # Нижняя часть — панель параметров
        # -------------------------
        controls_group = QGroupBox("Параметры генерации")
        controls_layout = QFormLayout()

        # n — количество вершин
        self.n_input = QSpinBox()
        self.n_input.setRange(0, 100000)
        self.n_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        controls_layout.addRow("n (вершины):", self.n_input)

        # m - количество рёбер
        self.m_radio = QCheckBox("m (рёбра)")
        self.m_input = QSpinBox()
        self.m_input.setRange(0, 100000)
        self.m_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        # k - количество соседей
        self.k_radio = QCheckBox("k (количество соседей)")
        self.k_input = QSpinBox()
        self.k_input.setRange(0, 100000)
        self.k_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        # p - вероятность создания ребра 
        self.p_radio = QCheckBox("p (вероятность создания ребра)")
        self.p_input = QDoubleSpinBox()
        self.p_input.setRange(0.0, 1.0)
        self.p_input.setSingleStep(0.01)
        self.p_input.setDecimals(3)
        self.p_input.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)

        controls_layout.addRow(self.m_radio, self.m_input)
        controls_layout.addRow(self.k_radio, self.k_input)
        controls_layout.addRow(self.p_radio, self.p_input)

        # -------------------------
        # Кнопка генерации
        # -------------------------
        self.generate_button = QPushButton("Сгенерировать граф")
        self.generate_button.clicked.connect(self.generate_graph)

        controls_layout.addRow(self.generate_button)

        controls_group.setLayout(controls_layout)

        main_layout.addWidget(controls_group)

        self.setLayout(main_layout)

        # Хранение исходного изображения
        self.original_pixmap = None

    def generate_graph(self):
        _n = self.n_input.value()
        _m = self.m_input.value()
        _k = self.k_input.value()
        _p = self.p_input.value()

        G, graph_title = gen.gen(n = _n, m = _m, k = _k, p = _p)
        w.G_write_dot(G, graph_title)
        d.G_draw(graph_title)

        self.load_image(f"default_viz\\{graph_title}")

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)

        if pixmap.isNull():
            self.image_label.setText("Ошибка загрузки изображения")
            self.original_pixmap = None
            return

        self.original_pixmap = pixmap
        self.update_image()

    def update_image(self):
        """Масштабирование изображения под размер QLabel"""
        if self.original_pixmap:
            scaled_pixmap = self.original_pixmap.scaled(
                self.image_label.size(),
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            self.image_label.setPixmap(scaled_pixmap)

    def resizeEvent(self, event):
        """Обновление картинки при изменении размера окна"""
        self.update_image()
        super().resizeEvent(event)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    window = GraphGeneratorUI()
    window.show()

    exit_code = app.exec()
    
    # удаление сгенерированных графов
    dir_paths = [Path('default_exp'), Path('default_viz')]
    for dir_path in dir_paths:
        for item in dir_path.iterdir():
            if item.is_dir():
                shutil.rmtree(item)
            else:
                item.unlink()
    
    sys.exit(exit_code)