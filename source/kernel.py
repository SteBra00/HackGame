from pathlib import Path
import logging

class KernelGame:
    def __init__(self) -> None:
        self.bitcoins = 0.0
        self.currentTheme = 'dark_teal.xml'
        logging.basicConfig(filename=str(Path('source', 'data', 'logFile.log').absolute()),
                            filemode='a',
                            format='[%(asctime)s] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            level=logging.NOTSET)
        self.logger = logging.getLogger('HackerGame')
        self.localServerIsOnline = True

    def add_bitcoins(self, coins) -> None:
        self.bitcoins += coins
        self.logger.info(f'add_bitcoins {coins:.10f} -> {self.bitcoins:.10f}')
    
    def del_bitcoins(self, coins) -> bool:
        if self.bitcoins>coins:
            self.bitcoins -= coins
            self.logger.info(f'del_bitcoins {coins:.10f} -> {self.bitcoins:.10f}')
            return True
        else:
            return False
    
    def setCurrentTheme(self, theme) -> None:
        self.currentTheme = theme
    
    def getCurrentTheme(self) -> str:
        return self.currentTheme