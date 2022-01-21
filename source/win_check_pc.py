import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QDialog, QGridLayout, QHBoxLayout, QLabel, QProgressBar, QPushButton, QScrollArea, QVBoxLayout, QWidget
import qt_material
from source.kernel import KernelGame

from source.pc import Pc


class WinCheckPc(QDialog):
    def __init__(self, kernel:KernelGame, pc:Pc, power:int, parent:QWidget=None) -> None:
        super().__init__(parent=parent)
        self.setWindowTitle(pc.name)
        self.kernel = kernel
        self.pc = pc
        self.power = power
        self.initUI()

    def initUI(self) -> None:
        self.setGeometry(250, 100, 450, 250)
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        bars_widget = QWidget()
        bars_layout = QGridLayout()
        bars_widget.setLayout(bars_layout)

        label_life = QLabel('Life')
        bars_layout.addWidget(label_life, 0, 0)
        bar_life = QProgressBar()
        bar_life.setRange(0, 100)
        bar_life.setValue(self.pc.get_life())
        bars_layout.addWidget(bar_life, 0, 1)

        label_power = QLabel('Power')
        bars_layout.addWidget(label_power, 1, 0)
        bar_power = QProgressBar()
        bar_power.setRange(0, 100)
        bar_power.setValue(self.power)
        bars_layout.addWidget(bar_power, 1, 1)

        vbox.addWidget(bars_widget)


        scroll = QScrollArea(self)
        vbox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        scollbox = QVBoxLayout(scrollContent)
        scrollContent.setLayout(scollbox)

        for component in self.pc.get_component():
            wid = QWidget()
            wid.setAttribute(QtCore.Qt.WA_StyledBackground, True)
            color = qt_material.get_theme(self.kernel.getCurrentTheme())['secondaryDarkColor']
            wid.setStyleSheet(f'background-color: {color}; border-radius: 5px; margin-left: 5px; margin-right: 5px;')
            wid_layout = QVBoxLayout()
            wid.setLayout(wid_layout)

            top_wid = QWidget()
            top_layout = QHBoxLayout()
            top_wid.setLayout(top_layout)
            name_label = QLabel(component.name)
            top_layout.addWidget(name_label)
            power_label = QLabel(str(component.power))
            top_layout.addWidget(power_label)
            wid_layout.addWidget(top_wid)

            middle_wid = QWidget()
            middle_layout = QHBoxLayout()
            middle_wid.setLayout(middle_layout)
            life_label = QLabel('Life')
            middle_layout.addWidget(life_label)
            life_bar = QProgressBar()
            life_bar.setValue(component.life)
            middle_layout.addWidget(life_bar)
            wid_layout.addWidget(middle_wid)

            remove_btn = QPushButton('-')
            wid_layout.addWidget(remove_btn)

            scollbox.addWidget(wid)

        scroll.setWidget(scrollContent)


if __name__=='__main__':
    app = QApplication(sys.argv)
    widget = WinCheckPc()
    widget.show()
    app.exec_()