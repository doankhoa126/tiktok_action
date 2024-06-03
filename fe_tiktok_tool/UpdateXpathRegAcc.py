from PyQt6 import QtCore, QtGui, QtWidgets
import json
import utils
class ui_UpdateXpathRegAcc(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(791, 360)
        Dialog.setStyleSheet("background-color: #121212    ")
        self.updateXpathRegAccGroupBox = QtWidgets.QGroupBox(parent=Dialog)
        self.updateXpathRegAccGroupBox.setGeometry(QtCore.QRect(20, 10, 751, 331))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateXpathRegAccGroupBox.setFont(font)
        self.updateXpathRegAccGroupBox.setStyleSheet("color:#E0E0E0")
        self.updateXpathRegAccGroupBox.setObjectName("updateXpathRegAccGroupBox")
        self.nameXpathLabel = QtWidgets.QLabel(parent=self.updateXpathRegAccGroupBox)
        self.nameXpathLabel.setGeometry(QtCore.QRect(30, 30, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameXpathLabel.setFont(font)
        self.nameXpathLabel.setStyleSheet("background-color: #272727;color:#E0E0E0")
        self.nameXpathLabel.setObjectName("nameXpathLabel")
        self.xpathComboBox = QtWidgets.QComboBox(parent=self.updateXpathRegAccGroupBox)
        self.xpathComboBox.setGeometry(QtCore.QRect(128, 21, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.xpathComboBox.setFont(font)
        self.xpathComboBox.setStyleSheet("background-color: #272727;color:#E0E0E0")
        self.xpathComboBox.setObjectName("xpathComboBox")
        self.currentXpathText = QtWidgets.QTextEdit(parent=self.updateXpathRegAccGroupBox)
        self.currentXpathText.setGeometry(QtCore.QRect(160, 90, 581, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.currentXpathText.setFont(font)
        self.currentXpathText.setStyleSheet("background-color:#999999;border-radius:10px;color:#E0E0E0")
        self.currentXpathText.setObjectName("currentXpathText")
        self.curentXpathLabel = QtWidgets.QLabel(parent=self.updateXpathRegAccGroupBox)
        self.curentXpathLabel.setGeometry(QtCore.QRect(20, 110, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.curentXpathLabel.setFont(font)
        self.curentXpathLabel.setStyleSheet("background-color: #272727;color:#E0E0E0")
        self.curentXpathLabel.setObjectName("curentXpathLabel")
        self.updateXpathLabel_3 = QtWidgets.QLabel(parent=self.updateXpathRegAccGroupBox)
        self.updateXpathLabel_3.setGeometry(QtCore.QRect(20, 230, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateXpathLabel_3.setFont(font)
        self.updateXpathLabel_3.setStyleSheet("background-color: #272727;color:#E0E0E0")
        self.updateXpathLabel_3.setObjectName("updateXpathLabel_3")
        self.updateXpathText = QtWidgets.QTextEdit(parent=self.updateXpathRegAccGroupBox)
        self.updateXpathText.setGeometry(QtCore.QRect(160, 210, 581, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateXpathText.setFont(font)
        self.updateXpathText.setStyleSheet("background-color:#999999;border-radius:10px;color:#E0E0E0")
        self.updateXpathText.setObjectName("updateXpathText")
        self.updateXpathBtn = QtWidgets.QPushButton(parent=self.updateXpathRegAccGroupBox)
        self.updateXpathBtn.setGeometry(QtCore.QRect(650, 20, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.updateXpathBtn.setFont(font)
        self.updateXpathBtn.setStyleSheet("background-color: #272727;color:#E0E0E0; border-radius:20px\n"
"")
        self.updateXpathBtn.setObjectName("updateXpathBtn")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Custom method calls
        self.loadXpathData()
        self.xpathComboBox.currentIndexChanged.connect(self.loadCurrentXpath)
        self.updateXpathBtn.clicked.connect(self.updateXpath)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.updateXpathRegAccGroupBox.setTitle(_translate("Dialog", "Cập nhật xpath"))
        self.nameXpathLabel.setText(_translate("Dialog", "Tên xpath:"))
        self.curentXpathLabel.setText(_translate("Dialog", "Xpath hiện tại:"))
        self.updateXpathLabel_3.setText(_translate("Dialog", "Xpath cập nhật:"))
        self.updateXpathBtn.setText(_translate("Dialog", "Lưu"))

    def loadXpathData(self):
        self.json_file_path = utils.XPATH_REGACC_JSON
        self.xpath_dict = self.readJsonFile(self.json_file_path)
        self.xpathComboBox.addItems(self.xpath_dict.keys())

    def loadCurrentXpath(self):
        xpath_name = self.xpathComboBox.currentText()
        self.currentXpathText.setText(self.xpath_dict.get(xpath_name, ""))

    def updateXpath(self):
        xpath_name = self.xpathComboBox.currentText()
        new_xpath = self.updateXpathText.toPlainText()
        if xpath_name and new_xpath:
            self.xpath_dict[xpath_name] = new_xpath
            self.currentXpathText.setText(new_xpath)
            self.writeJsonFile(self.json_file_path, self.xpath_dict)
            QtWidgets.QMessageBox.information(None, "Success", "XPath updated successfully!")

    def readJsonFile(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
                # Assuming the JSON structure is {"xpath_list": [{key: value}, ...]}
                xpath_dict = {k: v for d in data["xpath_list"] for k, v in d.items()}
                return xpath_dict
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return {}

    def writeJsonFile(self, file_path, xpath_dict):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
            for xpath in data["xpath_list"]:
                for key in xpath:
                    if key in xpath_dict:
                        xpath[key] = xpath_dict[key]
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error writing JSON file: {e}")

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = ui_UpdateXpathRegAcc()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
