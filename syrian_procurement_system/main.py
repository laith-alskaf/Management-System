import sys
from PyQt6.QtWidgets import QApplication, QMainWindow

def main():
    """
    The main entry point for the Syrian National Procurement Management System.
    """
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("نظام إدارة المشتريات الوطني السوري")
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
