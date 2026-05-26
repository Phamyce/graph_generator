import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QSpinBox, QDoubleSpinBox,
    QPushButton, QFormLayout, QMessageBox, QAbstractSpinBox,
    QGridLayout, QTabWidget, QFileDialog, QLineEdit
)
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import Qt

import write_graph.writeGraph as writer
import visualization.visualizeGraph as viz
import generation.generateGraph as gen

from pathlib import Path
import shutil

class GraphGeneratorUI(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.setWindowTitle('Graph Generator')
        self.resize(900, 700)

        main_layout = QGridLayout(self)
        self.setLayout(main_layout)

        # Метка для отображения графа
        self.image_label = QLabel("Здесь будет изображение графа")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(450)
        self.image_label.setStyleSheet("""
            QLabel {
                border: 2px solid gray;
                color: gray;
                background-color: white;
                font-size: 16px;
                font-weight: 600;
            }
        """)

        # Вкладки
        self.tab_widget = QTabWidget(self)

        # ----- Вкладка 1: Барабаши-Альберт -----
        ba_tab = QWidget()
        ba_layout = QFormLayout(ba_tab)
        self.ba_n = QSpinBox()
        self.ba_n.setRange(0, 100000)
        self.ba_n.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.ba_m = QSpinBox()
        self.ba_m.setRange(0, 100000)
        self.ba_m.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        ba_layout.addRow('Количество вершин (n):', self.ba_n)
        ba_layout.addRow('Количество рёбер на шаг (m):', self.ba_m)
        self.tab_widget.addTab(ba_tab, 'Барабаши-Альберт')

        # ----- Вкладка 2: Эрдёш-Реньи -----
        er_tab = QWidget()
        er_layout = QFormLayout(er_tab)
        self.er_n = QSpinBox()
        self.er_n.setRange(0, 100000)
        self.er_n.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.er_p = QDoubleSpinBox()
        self.er_p.setRange(0.0, 1.0)
        self.er_p.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.er_p.setSingleStep(0.01)
        er_layout.addRow('Количество вершин (n):', self.er_n)
        er_layout.addRow('Вероятность появления ребра (p):', self.er_p)
        self.tab_widget.addTab(er_tab, 'Эрдёш-Реньи')

        # ----- Вкладка 3: Уоттс-Строгац -----
        ws_tab = QWidget()
        ws_layout = QFormLayout(ws_tab)
        self.ws_n = QSpinBox()
        self.ws_n.setRange(0, 100000)
        self.ws_n.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.ws_k = QSpinBox()
        self.ws_k.setRange(0, 100000)
        self.ws_k.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.ws_beta = QDoubleSpinBox()
        self.ws_beta.setRange(0.0, 1.0)
        self.ws_beta.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.ws_beta.setSingleStep(0.01)
        ws_layout.addRow('Количество вершин (n):', self.ws_n)
        ws_layout.addRow('Средняя степень (k):', self.ws_k)
        ws_layout.addRow('Вероятность переподключения (β):', self.ws_beta)
        self.tab_widget.addTab(ws_tab, 'Уоттс-Строгац')

        # ----- Вкладка 4: Forest Fire -----
        ff_tab = QWidget()
        ff_layout = QFormLayout(ff_tab)
        self.ff_n = QSpinBox()
        self.ff_n.setRange(0, 100000)
        self.ff_n.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.ff_p = QDoubleSpinBox()
        self.ff_p.setRange(0.0, 1.0)
        self.ff_p.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.ff_p.setSingleStep(0.01)
        self.ff_r = QDoubleSpinBox()
        self.ff_r.setRange(0.0, 1.0)
        self.ff_r.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.ff_r.setSingleStep(0.01)
        ff_layout.addRow('Количество вершин (n):', self.ff_n)
        ff_layout.addRow('Вероятность "прямого" горения (p):', self.ff_p)
        ff_layout.addRow('Вероятность "обратного" горения (r):', self.ff_r)
        self.tab_widget.addTab(ff_tab, 'Forest Fire')

        # ----- Вкладка 5: Модель копирования -----
        cp_tab = QWidget()
        cp_layout = QFormLayout(cp_tab)
        self.cp_n = QSpinBox()
        self.cp_n.setRange(0, 100000)
        self.cp_n.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.cp_beta = QDoubleSpinBox()
        self.cp_beta.setRange(0.0, 1.0)
        self.cp_beta.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.cp_beta.setSingleStep(0.01)
        self.cp_d = QSpinBox()
        self.cp_d.setRange(0, 100000)
        self.cp_d.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        cp_layout.addRow('Количество вершин (n):', self.cp_n)
        cp_layout.addRow('Вероятность копирования (β):', self.cp_beta)
        cp_layout.addRow('Регулярный граф числа (d):', self.cp_d)
        self.tab_widget.addTab(cp_tab, 'Модель копирования')

        # ----- Вкладка 6: Граф Лейтона -----
        lg_tab = QWidget()
        lg_layout = QFormLayout(lg_tab)
        self.lg_n = QSpinBox()
        self.lg_n.setRange(0, 100000)
        self.lg_n.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.lg_chi = QSpinBox()
        self.lg_chi.setRange(0, 100000)
        self.lg_chi.setButtonSymbols(QAbstractSpinBox.ButtonSymbols.NoButtons)
        lg_layout.addRow('Количество вершин (n):', self.lg_n)
        lg_layout.addRow('Хроматическое число (χ):', self.lg_chi)

        self.lg_b_vector = QLineEdit()
        self.lg_b_vector.setPlaceholderText('Пример: 1,0,2,3  (b2,b3,...,bk)')
        lg_layout.addRow('Вектор b (b₂,b₃,…,bₖ):', self.lg_b_vector)

        self.tab_widget.addTab(lg_tab, 'Граф Лейтона')

        # Кнопка генерации
        self.generate_button = QPushButton("Сгенерировать граф")
        self.generate_button.clicked.connect(self.generate_graph)

        # Кнопка экспорта в dot
        self.exp_dot_button = QPushButton("Экспортировать граф в .dot")
        self.exp_dot_button.clicked.connect(self.export_dot)

        # Кнопка экспорта в png
        self.exp_png_button = QPushButton("Экспортировать граф в .png")
        self.exp_png_button.clicked.connect(self.export_png)

        # Кнопка запуска тестовых примеров
        #self.test_run_button = QPushButton("Запустить пример")
        #self.test_run_button.clicked.connect(self.test_run)

        # Размещение
        main_layout.addWidget(self.image_label, 0, 0, 1, 3)
        main_layout.addWidget(self.tab_widget, 1, 0, 1, 3)
        main_layout.addWidget(self.generate_button, 2, 0, 1, 1)
        main_layout.addWidget(self.exp_dot_button, 2, 1, 1, 1)
        main_layout.addWidget(self.exp_png_button, 2, 2, 1, 1)
        #main_layout.addWidget(self.test_run_button, 2, 3, 1, 1)

        self.original_pixmap = None
        self.current_image_path = None

    def generate_graph(self):
        current_index = self.tab_widget.currentIndex()
        graph_title = None
        G = None

        try:
            if current_index == 0:  # Барабаши-Альберт
                n = self.ba_n.value()
                m = self.ba_m.value()
                if n == 0 or m == 0:
                    QMessageBox.warning(self, "Ошибка", "Количество вершин и рёбер должно быть > 0")
                    return
                G, graph_title = gen.barabasi_albert(n, m)

            elif current_index == 1:  # Эрдёш-Реньи
                n = self.er_n.value()
                p = self.er_p.value()
                if n == 0:
                    QMessageBox.warning(self, "Ошибка", "Количество вершин должно быть > 0")
                    return
                G, graph_title = gen.erdos_renyi(n, p)

            elif current_index == 2:  # Уоттс-Строгац
                n = self.ws_n.value()
                k = self.ws_k.value()
                beta = self.ws_beta.value()
                if n == 0 or k == 0:
                    QMessageBox.warning(self, "Ошибка", "Количество вершин и степень должны быть > 0")
                    return
                G, graph_title = gen.watts_strogatz(n, k, beta)

            elif current_index == 3:  # Forest Fire
                n = self.ff_n.value()
                p = self.ff_p.value()
                r = self.ff_r.value()
                if n == 0:
                    QMessageBox.warning(self, "Ошибка", "Количество вершин должно быть > 0")
                    return
                G, graph_title = gen.forest_fire(n, p, r)

            elif current_index == 4:  # Модель копирования
                n = self.cp_n.value()
                beta = self.cp_beta.value()
                cp_d_val = self.cp_d.value()
                if n == 0 or cp_d_val == 0:
                    QMessageBox.warning(self, "Ошибка", "Количество вершин и d должны быть > 0")
                    return
                G, graph_title = gen.copying_model(n, beta, cp_d_val)
            
            elif current_index == 5:  # Граф Лейтона

                def parse_b_vector(text, k):
                    """Преобразует строку 'b2,b3,...,bk' в словарь {размер: количество}."""
                    if not text.strip():
                        return {}
                    parts = text.strip().split(',')
                    if len(parts) != k - 1:  # от 2 до k включительно -> k-1 элементов
                        raise ValueError(f'Ожидается {k-1} чисел, получено {len(parts)}')
                    b_dict = {}
                    for i, val in enumerate(parts, start=2):
                        cnt = int(val.strip())
                        if cnt < 0:
                            raise ValueError(f'b{i} не может быть отрицательным')
                        b_dict[i] = cnt
                    return b_dict
                
                n = self.lg_n.value()
                chi_val = self.lg_chi.value()
                b_text = self.lg_b_vector.text()
                try:
                    b = parse_b_vector(b_text, chi_val)
                except ValueError as e:
                    QMessageBox.warning(self, 'Ошибка', str(e))
                    return
                if n == 0 or chi_val == 0:
                    QMessageBox.warning(self, "Ошибка", "Все параметры должны быть > 0")
                    return
                #G, graph_title = gen.leighton_graph(n, m, chi_val, b)
                G, graph_title = gen.leighton_graph(n, chi_val, b)

            if G is not None and graph_title:
                writer.G_write_dot(G, graph_title)
                viz.G_viz(graph_title)
                self.load_image(f"default_png/{graph_title}")
            else:
                QMessageBox.warning(self, "Ошибка", "Не удалось сгенерировать граф")

        except Exception as e:
            QMessageBox.critical(self, "Ошибка генерации", str(e))

    def export_dot(self):
        destination_file, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            f"{self.current_image_path}",
            "Dot Files (*.dot)"
        )
        if destination_file:
            shutil.copy("default_dot/" + self.current_image_path + ".dot", destination_file)
    
    def export_png(self):
        destination_file, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            f"{self.current_image_path}",
            "Png Files (*.png)"
        )
        if destination_file:
            shutil.copy("default_png/" + self.current_image_path + ".png", destination_file)

    def load_image(self, image_path):
        pixmap = QPixmap(image_path)
        if pixmap.isNull():
            self.image_label.setText("Ошибка загрузки изображения")
            self.original_pixmap = None
        else:
            self.original_pixmap = pixmap
            self.current_image_path = Path(image_path).stem
            self.update_image()

    def update_image(self):
        if self.original_pixmap:
            screen = self.screen()
            dpi_ratio = screen.devicePixelRatio() if screen else 1.0
            target_size = self.image_label.size() * dpi_ratio
            
            scaled = self.original_pixmap.scaled(
                target_size,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )
            
            scaled.setDevicePixelRatio(dpi_ratio)
            
            self.image_label.setPixmap(scaled)

    def resizeEvent(self, event):
        self.update_image()
        super().resizeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = GraphGeneratorUI()
    window.show()
    exit_code = app.exec()

    # Очистка папок default_dot и default_png
    for dir_path in (Path('default_dot'), Path('default_png')):
        if dir_path.exists():
            for item in dir_path.iterdir():
                if item.is_dir():
                    shutil.rmtree(item)
                else:
                    item.unlink()
    sys.exit(exit_code)