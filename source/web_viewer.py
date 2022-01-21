from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QAction, QDialog, QLayout, QMenu, QPlainTextEdit, QTextEdit, QVBoxLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView, QWebEnginePage

from source.kernel import KernelGame


class WebViewer(QWebEngineView):
    def __init__(self, kernel:KernelGame) -> None:
        super().__init__()
        self.kernel = kernel
        if self.kernel.localServerIsOnline:
            self.html = """<html>
    <head></head>
    <body>
        <h1>Hello World!</h1>
    </body>
</html>"""
        else:
            self.html = """<html>
    <head></head>
    <body>
        <h1>Error 404! Not found</h1>
    </body>
</html>"""
        self.setHtml(self.html)
        self.setFixedSize(625, 350)
    
    def contextMenuEvent(self, a0: QtGui.QContextMenuEvent) -> None:
        menu = QMenu(self)
        reload_action = menu.addAction('Reload')
        reload_action.triggered.connect(self.reload)
        view_action = menu.addAction('View Source Code')
        view_action.triggered.connect(self.viewSourceCode)
        menu.popup(a0.globalPos())
        #return super().contextMenuEvent(a0)
    
    def viewSourceCode(self, *_) -> None:
        dialog = QDialog(self)
        dialog.setWindowTitle('Source Code')
        dialog.setGeometry(250, 100, 400, 350)
        vbox = QVBoxLayout()
        text_area = QPlainTextEdit(self.html)
        text_area.setReadOnly(True)
        vbox.addWidget(text_area)
        dialog.setLayout(vbox)
        dialog.show()

    def loadUrl(self, url:str) -> None:
        pass