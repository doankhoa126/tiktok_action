from PyQt6 import QtCore, QtGui, QtWidgets
from functools import partial
import utils
class ui_InputProxy(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1050, 692)
        Dialog.setStyleSheet("background-color: #121212")
        self.addProxyGroupBox = QtWidgets.QGroupBox(parent=Dialog)
        self.addProxyGroupBox.setGeometry(QtCore.QRect(10, 20, 1021, 651))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.addProxyGroupBox.setFont(font)
        self.addProxyGroupBox.setStyleSheet("color:#E0E0E0")
        self.addProxyGroupBox.setObjectName("addProxyGroupBox")
        self.horizontalLayoutWidget = QtWidgets.QWidget(parent=self.addProxyGroupBox)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(30, 20, 681, 80))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        # Initialize ComboBoxes
        self.comboBoxes = []
        for i in range(4):
            comboBox = QtWidgets.QComboBox(parent=self.horizontalLayoutWidget)
            font = QtGui.QFont()
            font.setPointSize(12)
            comboBox.setFont(font)
            comboBox.setStyleSheet("background-color: #272727;color:#E0E0E0")
            comboBox.setObjectName(f"comboBox{i+1}")
            comboBox.addItem("")
            comboBox.addItem("")
            comboBox.addItem("")
            comboBox.addItem("")
            self.horizontalLayout.addWidget(comboBox)
            self.comboBoxes.append(comboBox)
        
        self.saveProxy = QtWidgets.QPushButton(parent=self.addProxyGroupBox)
        self.saveProxy.setGeometry(QtCore.QRect(940, 30, 61, 51))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.saveProxy.setFont(font)
        self.saveProxy.setStyleSheet("background-color: #272727;color:#E0E0E0")
        self.saveProxy.setObjectName("saveProxy")
        
        self.inputTextProxy = QtWidgets.QPlainTextEdit(parent=self.addProxyGroupBox)
        self.inputTextProxy.setGeometry(QtCore.QRect(20, 120, 981, 171))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.inputTextProxy.setFont(font)
        self.inputTextProxy.setStyleSheet("background-color:#999999;border-radius:10px;color:#E0E0E0")
        self.inputTextProxy.setObjectName("inputTextProxy")
       
        self.proxyTextTable = QtWidgets.QTableWidget(parent=self.addProxyGroupBox)
        self.proxyTextTable.setGeometry(QtCore.QRect(20, 300, 981, 331))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.proxyTextTable.setFont(font)
        self.proxyTextTable.setStyleSheet("background-color:#999999; border-radius:10px; color:#E0E0E0")
        self.proxyTextTable.setObjectName("proxyTextTable")
        self.proxyTextTable.setColumnCount(4)
        self.proxyTextTable.setHorizontalHeaderLabels(['', '', '', '']) # Initialize with empty headers
        for i in range(4):
            self.proxyTextTable.setColumnWidth(i, 200)
        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        
        for i, comboBox in enumerate(self.comboBoxes):
            comboBox.currentIndexChanged.connect(partial(self.updateHeader, i, comboBox))
        self.inputTextProxy.textChanged.connect(self.processInput)
        self.saveProxy.clicked.connect(self.saveData)

    
    def saveData(self):
    # Mở hộp thoại để lưu tệp tin
        # file_name, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "", "Text Files (*.txt)")
        file_name = utils.PROXY_TXT
        if file_name:
            with open(file_name, 'w') as file:
                # Danh sách các tên cột theo thứ tự mong muốn
                default_column_names = ["proxyID", "port", "username", "pass"]
                # Danh sách cột hiện tại trong bảng
                current_column_names = [self.proxyTextTable.horizontalHeaderItem(i).text() for i in range(self.proxyTextTable.columnCount())]

                rows = self.proxyTextTable.rowCount()

                for row in range(rows):
                    row_data = []
                    # Xác định số lượng cột cần lưu dựa trên dữ liệu có 2 hoặc 4 thành phần
                    data_length = 2 if len(self.inputTextProxy.toPlainText().split(":")) == 2 else 4
                    column_names = default_column_names[:data_length]
                    for col_name in column_names:
                        # Tìm chỉ mục của cột có tên col_name trong danh sách cột hiện tại
                        col_index = current_column_names.index(col_name) if col_name in current_column_names else None
                        if col_index is not None:
                            item = self.proxyTextTable.item(row, col_index)
                            if item is not None:
                                data = item.text()
                                row_data.append(data)
                            else:
                                row_data.append("")  
                        else:
                            row_data.append("")  
                    file.write(":".join(row_data) + "\n")

            QtWidgets.QMessageBox.information(None, "Saved", "Data saved successfully!")





    def getColumnIndexByName(self, column_name):
        # Lấy số cột trong bảng
        columns = self.proxyTextTable.columnCount()
        # Duyệt qua từng cột để tìm chỉ mục của cột có tên column_name
        for col in range(columns):
            header = self.proxyTextTable.horizontalHeaderItem(col)
            if header.text() == column_name:
                return col
        return None
    def processInput(self):
    # Xóa nội dung cũ của bảng
        self.proxyTextTable.clearContents()
        
        # Lấy nội dung mới từ inputTextProxy
        proxy_data = self.inputTextProxy.toPlainText()
        
        # Tách chuỗi thành danh sách các dòng
        lines = proxy_data.split('\n')
        
        # Thiết lập số hàng mới cho bảng
        self.proxyTextTable.setRowCount(len(lines))
        
        # Duyệt qua từng dòng và cập nhật bảng
        for row, line in enumerate(lines):
            # Tách chuỗi dựa trên dấu ":" hoặc " "
            items = line.split(':')  # hoặc items = line.split(' ')
            for column, item in enumerate(items):
                # Kiểm tra giới hạn số cột
                if column < self.proxyTextTable.columnCount():
                    # Thêm dữ liệu vào ô tương ứng
                    self.proxyTextTable.setItem(row, column, QtWidgets.QTableWidgetItem(item))

    def updateHeader(self, column, comboBox):
        # Get the selected item text
        selected_text = comboBox.currentText()
        # Update the column header in the table
        item = QtWidgets.QTableWidgetItem(selected_text)
        font = QtGui.QFont()
        font.setPointSize(12)
        item.setFont(font)
        self.proxyTextTable.setHorizontalHeaderItem(column, item)

            

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.addProxyGroupBox.setTitle(_translate("Dialog", "Thêm proxy"))
        
        comboBoxItems = ["proxyID", "port", "username", "pass"]
        for comboBox in self.comboBoxes:
            for index, item in enumerate(comboBoxItems):
                comboBox.setItemText(index, _translate("Dialog", item))
        
        self.saveProxy.setText(_translate("Dialog", "Lưu"))

    

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = ui_InputProxy()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
