from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction, QApplication, QHBoxLayout, QLineEdit, QMainWindow, QMenu, QPlainTextEdit, QScrollArea, QTabWidget, QVBoxLayout, QWidget

import sys
import json
import qt_material
from pathlib import Path

from source.kernel import KernelGame
from source.mine import Mine
from source.web_viewer import WebViewer


class Win(QMainWindow):
    def __init__(self) -> None:
        self.kernel = KernelGame()

        super().__init__()
        qt_material.apply_stylesheet(self, theme=self.kernel.currentTheme)
        
        self.mine_list_all = list()
        self.mine_list = list()

        self.mine_json = None
        with open(Path('source', 'data', 'mine'), 'r') as f:
            self.mine_json = json.loads(f.read())

        if not self.initSocket():
            pass

        self.initUI()

    def initSocket(self) -> bool:
        pass

    def initUI(self) -> None:
        self.setWindowTitle('HackerGame')
        self.setGeometry(100, 50, 650, 450)


        historyMenu = QAction(QIcon(), 'History', self)
        #historyMenu.triggered.connect()

        themesMenu = QMenu('Theme', self)
        for theme in qt_material.list_themes():
            action = QAction(QIcon(), theme, self)
            action.triggered.connect(lambda _, theme=theme:self.changeTheme(theme))
            themesMenu.addAction(action)

        menuBar = self.menuBar()
        infoMenu = menuBar.addMenu('Info')
        infoMenu.addAction(historyMenu)
        infoMenu.addMenu(themesMenu)


        body = QWidget()
        self.setCentralWidget(body)
        self.hbox = QHBoxLayout()
        body.setLayout(self.hbox)
        
        self.tabs = QTabWidget()
        self.hbox.addWidget(self.tabs)

        self.tab_shell = QWidget()
        self.tab_room = QWidget()
        self.tab_server = QWidget()
        self.tab_team = QWidget()
        self.tab_options = QWidget()

        self.tabs.addTab(self.tab_shell, 'Shell')
        self.initTagShell()
        self.tabs.addTab(self.tab_room, 'Room')
        self.initTabRoom()
        self.tabs.addTab(self.tab_server, 'Server')
        self.initTabServer()
        self.tabs.addTab(self.tab_team, 'Team')
        self.initTabTeam()
        self.tabs.addTab(self.tab_options, 'Options')
        self.initTabOptions()


    def initTagShell(self) -> None:
        def callback(*_) -> None:
            cmd = self.entry_shell.text()
            self.shell.appendPlainText(f'>>> {cmd}')
            self.entry_shell.setText('')

        vbox = QVBoxLayout()
        self.tab_shell.setLayout(vbox)

        self.shell = QPlainTextEdit()
        self.shell.setStyleSheet('background-color: #000000;')
        self.shell.setReadOnly(True)
        vbox.addWidget(self.shell)

        self.entry_shell = QLineEdit()
        self.entry_shell.setStyleSheet('background-color: #000000;')
        self.entry_shell.returnPressed.connect(callback)
        vbox.addWidget(self.entry_shell)
    
    def initTabRoom(self) -> None:
        vbox = QVBoxLayout()
        self.tab_room.setLayout(vbox)

        scroll = QScrollArea(self.tab_room)
        vbox.addWidget(scroll)
        scroll.setWidgetResizable(True)
        scrollContent = QWidget(scroll)
        hbox = QHBoxLayout(scrollContent)
        scrollContent.setLayout(hbox)

        for mine in self.mine_json:
            if mine.get('name')!=None:
                mine = Mine(kernel=self.kernel, name=mine['name'], pc_name=mine['pc'], power=mine['power'])
                hbox.addWidget(mine)
                self.mine_list.append(mine)
                self.mine_list_all.append(mine)
            else:
                mine = Mine(kernel=self.kernel)
                hbox.addWidget(mine)
                self.mine_list_all.append(mine)

        scroll.setWidget(scrollContent)
    
    def initTabServer(self) -> None:
        vbox = QVBoxLayout()
        self.tab_server.setLayout(vbox)
        self.web_viewer = WebViewer(self.kernel)
        vbox.addWidget(self.web_viewer)

    def initTabTeam(self) -> None:
        pass

    def initTabOptions(self) -> None:
        pass


    def stopMining(self) -> None:
        for mine in self.mine_list:
            mine.stop()
    
    def changeTheme(self, theme:str) -> None:
        self.kernel.setCurrentTheme(theme)
        qt_material.apply_stylesheet(self, theme=theme)
        if theme.startswith('dark'):
            self.shell.setStyleSheet('background-color: #000000;')
            self.entry_shell.setStyleSheet('background-color: #000000;')
        else:
            self.shell.setStyleSheet('background-color: #ffffff;')
            self.entry_shell.setStyleSheet('background-color: #ffffff;')
        for mine in self.mine_list_all:
            mine.changeTheme()





if __name__=='__main__':
    app = QApplication(sys.argv)
    win = Win()
    win.show()
    app.exec_()
    win.stopMining()