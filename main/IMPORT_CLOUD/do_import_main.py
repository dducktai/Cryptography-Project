import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QFileDialog, QVBoxLayout, QTableWidgetItem
from PyQt6.QtGui import QIcon
from do_import_gui import Ui_MainWindow
from cloud import ProcessCloud

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowTitle("My App")
        self.setWindowIcon(QIcon('/Users/wanthinnn/Downloads/nekocoffee.icns'))
        self.db_handler = ProcessCloud()

        self.ui.comboBox_table.addItems(self.db_handler.get_tables())
        self.ui.comboBox_table.currentTextChanged.connect(self.populate_table_view)

        self.ui.pushButton_import.clicked.connect(self.import_data)
        self.ui.pushButton_plaintextfile.clicked.connect(lambda: self.db_handler.select_plaintextfile(self))
        self.ui.pushButton_Refresh.clicked.connect(self.refresh_tables)

    def import_data(self):
        self.db_handler.import_data(self.ui)

    def refresh_tables(self):
        self.ui.comboBox_table.clear()
        self.ui.comboBox_table.addItems(self.db_handler.get_tables())

    def populate_table_view(self):
        table_name = self.ui.comboBox_table.currentText()
        data, columns = self.db_handler.get_table_data(table_name)

        # Clear old data
        self.ui.tableWidget.setRowCount(0)
        self.ui.tableWidget.setColumnCount(0)

        if data:
            self.ui.tableWidget.setColumnCount(len(columns))
            self.ui.tableWidget.setHorizontalHeaderLabels(columns)
            
            for row_number, row_data in enumerate(data):
                self.ui.tableWidget.insertRow(row_number)
                for column_number, data in enumerate(row_data):
                    self.ui.tableWidget.setItem(row_number, column_number, QTableWidgetItem(str(data)))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())