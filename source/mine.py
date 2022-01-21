import time
import json
from pathlib import Path
import qt_material
import requests
from threading import Thread
from PyQt5 import QtCore
from PyQt5.QtWidgets import QHBoxLayout, QLabel, QProgressBar, QPushButton, QVBoxLayout, QWidget
from source.component import Component

from source.win_check_pc import WinCheckPc
from source.component import Component
from source.kernel import KernelGame
from source.pc import Pc



class Mine(QWidget):
    def __init__(self, kernel:KernelGame, name:str=None, pc_name:str=None, power:int=None, parent:QWidget=None) -> None:
        super().__init__(parent=parent)
        self.kernel = kernel
        self.name = name
        self.pc = None
        self.pc_name = pc_name
        self.power = power
        self.wasInit = False

        if name!=None:
            self.init()
        else:
            self.notInit()
        
        self.setFixedSize(120, 300)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        color = qt_material.get_theme('dark_teal.xml')['secondaryColor']
        self.setStyleSheet(f'background-color: {color}; border-radius: 5px; margin-left: 5px; margin-right: 5px;')

    def notInit(self) -> None:
        label = QLabel('+')
        label.setStyleSheet('font-size: 40px;')
        label.setAlignment(QtCore.Qt.AlignCenter)
        vbox = QVBoxLayout()
        vbox.addWidget(label)
        self.setLayout(vbox)
        self.wasInit = False

    def init(self) -> None:
        pc_data = None
        with open(Path('source', 'data', 'pc'), 'r') as f:
            pc_data = json.loads(f.read())

        if pc_data.get(self.pc_name)!=None:
            pc_components = pc_data[self.pc_name]
            components = list()

            components_data = None
            with open(Path('source', 'data', 'magazine'), 'r') as f:
                components_data = json.loads(f.read())

            for comp in pc_components:
                if components_data.get(comp)!=None:
                    components.append(Component(
                        components_data[comp]['name'],
                        components_data[comp]['type'],
                        components_data[comp]['power'],
                        components_data[comp]['life']
                    ))
            self.pc = Pc(self.pc, *[(i, c)for (i, c) in zip(range(len(components)), components)])
        else:
            self.notInit()
            return

        self._run = True
        self._bitcoins_rate = requests.get('https://api.coindesk.com/v1/bpi/currentprice.json').json()['bpi']['EUR']['rate_float']

        vbox = QVBoxLayout()
        self.setLayout(vbox)

        label_name = QLabel(self.name)
        label_name.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(label_name)

        bars = QWidget()
        hbox = QHBoxLayout()
        bars.setLayout(hbox)

        self.life_bar = QProgressBar()
        self.life_bar.setOrientation(QtCore.Qt.Vertical)
        self.life_bar.setFixedSize(7, 150)
        self.life_bar.setRange(0, 100)
        self.life_bar.setValue(self.pc.get_life())
        hbox.addWidget(self.life_bar)

        self.power_bar = QProgressBar()
        self.power_bar.setOrientation(QtCore.Qt.Vertical)
        self.power_bar.setFixedSize(7, 150)
        self.power_bar.setRange(0, 100)
        self.power_bar.setValue(self.power)
        hbox.addWidget(self.power_bar)

        vbox.addWidget(bars)

        self.label_mining_per_day = QLabel('')
        self.label_mining_per_day.setAlignment(QtCore.Qt.AlignCenter)
        vbox.addWidget(self.label_mining_per_day)

        self.initThread()
        self.wasInit = True
    
    def initThread(self) -> None:
        self._thread = Thread(target=self.run)
        self._thread.start()

    def run(self) -> None:
        power = self.pc.get_mining_power()
        power = power*self.power/100
        power /= 100000000 #(GPU 2080 procude 0.0000208 al giorno)
        self.label_mining_per_day.setText(f'{power:.6f} Bit/g')
        power /= 24 #giorno -> ore
        power /= 60 #ore -> minuti
        self.production = power

        while self._run:
            for _ in range(60):
                time.sleep(1)
                if not self._run:
                    break
            self.kernel.add_bitcoins(self.production)
    
    def stop(self):
        self._run = False
    
    def mousePressEvent(self, _) -> None:
        color = qt_material.get_theme(self.kernel.getCurrentTheme())['secondaryLightColor']
        self.setStyleSheet(f'background-color: {color}; border-radius: 5px; margin-left: 5px; margin-right: 5px;')
    
    def mouseReleaseEvent(self, _) -> None:
        color = qt_material.get_theme(self.kernel.getCurrentTheme())['secondaryColor']
        self.setStyleSheet(f'background-color: {color}; border-radius: 5px; margin-left: 5px; margin-right: 5px;')

        if self.wasInit:
            win = WinCheckPc(self.kernel, self.pc, self.power,  self)
            win.show()
        else:
            win = QPushButton()
            win.show()

    def changeTheme(self) -> None:
        color = qt_material.get_theme(self.kernel.getCurrentTheme())['secondaryColor']
        self.setStyleSheet(f'background-color: {color}; border-radius: 5px; margin-left: 5px; margin-right: 5px;')