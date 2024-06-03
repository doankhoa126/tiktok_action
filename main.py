from fe_tiktok_tool.MainFormTool import MainForm
from PyQt6 import QtWidgets
import warnings

warnings.filterwarnings('ignore')

warnings.filterwarnings('ignore', category=UserWarning)

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainForm()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())