from PyQt6 import QtCore, QtGui, QtWidgets
import json
import utils

class ui_UpdateXpathTikok(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(790, 415)
        Dialog.setStyleSheet("background-color: #121212")
        self.updateXpathRegAccGroupBox = QtWidgets.QGroupBox(parent=Dialog)
        self.updateXpathRegAccGroupBox.setGeometry(QtCore.QRect(20, 10, 751, 391))
        font = QtGui.QFont()
        font.setFamily("MS Shell Dlg 2")
        font.setPointSize(12)
        self.updateXpathRegAccGroupBox.setFont(font)
        self.updateXpathRegAccGroupBox.setContextMenuPolicy(QtCore.Qt.ContextMenuPolicy.NoContextMenu)
        self.updateXpathRegAccGroupBox.setStyleSheet("color:#E0E0E0")
        self.updateXpathRegAccGroupBox.setObjectName("updateXpathRegAccGroupBox")
        self.nameXpathLabel = QtWidgets.QLabel(parent=self.updateXpathRegAccGroupBox)
        self.nameXpathLabel.setGeometry(QtCore.QRect(32, 109, 81, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.nameXpathLabel.setFont(font)
        self.nameXpathLabel.setStyleSheet("background-color: #272727;color:#E0E0E0")
        self.nameXpathLabel.setObjectName("nameXpathLabel")
        self.xpathComboBox = QtWidgets.QComboBox(parent=self.updateXpathRegAccGroupBox)
        self.xpathComboBox.setGeometry(QtCore.QRect(180, 100, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.xpathComboBox.setFont(font)
        self.xpathComboBox.setStyleSheet("background-color: #272727;color:#E0E0E0")
        self.xpathComboBox.setObjectName("xpathComboBox")
        self.currentXpathText = QtWidgets.QTextEdit(parent=self.updateXpathRegAccGroupBox)
        self.currentXpathText.setGeometry(QtCore.QRect(162, 169, 581, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.currentXpathText.setFont(font)
        self.currentXpathText.setStyleSheet("background-color:#999999;border-radius:10px;color:#E0E0E0")
        self.currentXpathText.setObjectName("currentXpathText")
        self.curentXpathLabel = QtWidgets.QLabel(parent=self.updateXpathRegAccGroupBox)
        self.curentXpathLabel.setGeometry(QtCore.QRect(22, 189, 111, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.curentXpathLabel.setFont(font)
        self.curentXpathLabel.setStyleSheet("background-color: #272727;color:#E0E0E0")
        self.curentXpathLabel.setObjectName("curentXpathLabel")
        self.updateXpathLabel_3 = QtWidgets.QLabel(parent=self.updateXpathRegAccGroupBox)
        self.updateXpathLabel_3.setGeometry(QtCore.QRect(22, 309, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateXpathLabel_3.setFont(font)
        self.updateXpathLabel_3.setStyleSheet("background-color: #272727;color:#E0E0E0")
        self.updateXpathLabel_3.setObjectName("updateXpathLabel_3")
        self.updateXpathText = QtWidgets.QTextEdit(parent=self.updateXpathRegAccGroupBox)
        self.updateXpathText.setGeometry(QtCore.QRect(162, 289, 581, 81))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.updateXpathText.setFont(font)
        self.updateXpathText.setStyleSheet("background-color:#999999;border-radius:10px;color:#E0E0E0")
        self.updateXpathText.setObjectName("updateXpathText")
        self.updateXpathBtn = QtWidgets.QPushButton(parent=self.updateXpathRegAccGroupBox)
        self.updateXpathBtn.setGeometry(QtCore.QRect(650, 30, 91, 41))
        font = QtGui.QFont()
        font.setPointSize(14)
        self.updateXpathBtn.setFont(font)
        self.updateXpathBtn.setStyleSheet("background-color: #272727;color:#E0E0E0; border-radius:20px")
        self.updateXpathBtn.setObjectName("updateXpathBtn")
        self.InteractionLabel = QtWidgets.QLabel(parent=self.updateXpathRegAccGroupBox)
        self.InteractionLabel.setGeometry(QtCore.QRect(30, 50, 121, 31))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.InteractionLabel.setFont(font)
        self.InteractionLabel.setStyleSheet("background-color: #272727;color:#E0E0E0")
        self.InteractionLabel.setObjectName("InteractionLabel")
        self.interactionComboBox = QtWidgets.QComboBox(parent=self.updateXpathRegAccGroupBox)
        self.interactionComboBox.setGeometry(QtCore.QRect(180, 40, 221, 41))
        font = QtGui.QFont()
        font.setPointSize(12)
        self.interactionComboBox.setFont(font)
        self.interactionComboBox.setStyleSheet("background-color: #272727;color:#E0E0E0")
        self.interactionComboBox.setObjectName("interactionComboBox")
        self.interactionComboBox.addItem("")
        self.interactionComboBox.addItem("")
        self.interactionComboBox.addItem("")
        self.interactionComboBox.addItem("")
        self.interactionComboBox.addItem("")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

        # Custom code
        self.interactionComboBox.currentTextChanged.connect(self.on_interaction_changed)
        self.xpathComboBox.currentTextChanged.connect(self.on_xpath_changed)
        self.updateXpathBtn.clicked.connect(self.save_xpath)

        self.load_data()

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.updateXpathRegAccGroupBox.setTitle(_translate("Dialog", "Cập nhật xpath"))
        self.nameXpathLabel.setText(_translate("Dialog", "Tên xpath:"))
        self.curentXpathLabel.setText(_translate("Dialog", "Xpath hiện tại:"))
        self.updateXpathLabel_3.setText(_translate("Dialog", "Xpath cập nhật:"))
        self.updateXpathBtn.setText(_translate("Dialog", "Lưu"))
        self.InteractionLabel.setText(_translate("Dialog", "Tên tương tác:"))
        self.interactionComboBox.setItemText(0, _translate("Dialog", "Nuôi acc"))
        self.interactionComboBox.setItemText(1, _translate("Dialog", "Tương tác newfeed"))
        self.interactionComboBox.setItemText(2, _translate("Dialog", "Tương tác user"))
        self.interactionComboBox.setItemText(3, _translate("Dialog", "Tương tác theo chủ đề"))
        self.interactionComboBox.setItemText(4, _translate("Dialog", "Tương tác live"))

    def load_data(self):
        self.interaction_map = {
            "Nuôi acc": "growAcc",
            "Tương tác newfeed": "newfeed",
            "Tương tác user": "interactUser",
            "Tương tác theo chủ đề": "interactTopic",
            "Tương tác live": "interactLive"
        }
        file_path = utils.XPATH_CONFIG_INTERACTION_JSON
        self.json_data = self.load_json(file_path)  # replace with your JSON file path

    def load_json(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except Exception as e:
            print(f"Error reading JSON file: {e}")
            return []

    def save_json(self, file_path, data):
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error writing JSON file: {e}")

    def on_interaction_changed(self):
        selected_interaction = self.interactionComboBox.currentText()
        interaction_key = self.interaction_map.get(selected_interaction)

        self.xpathComboBox.clear()
        for interaction in self.json_data:
            if interaction["name_interaction"] == interaction_key:
                self.current_xpaths = interaction["xpath_list"]
                for xpath_dict in self.current_xpaths:
                    for xpath_name in xpath_dict.keys():
                        self.xpathComboBox.addItem(xpath_name)
                break

    def on_xpath_changed(self):
        selected_xpath_name = self.xpathComboBox.currentText()
        for xpath_dict in self.current_xpaths:
            if selected_xpath_name in xpath_dict:
                self.currentXpathText.setPlainText(xpath_dict[selected_xpath_name])
                break

    def save_xpath(self):
        selected_interaction = self.interactionComboBox.currentText()
        interaction_key = self.interaction_map.get(selected_interaction)
        selected_xpath_name = self.xpathComboBox.currentText()
        new_xpath_value = self.updateXpathText.toPlainText()

        for interaction in self.json_data:
            if interaction["name_interaction"] == interaction_key:
                for xpath_dict in interaction["xpath_list"]:
                    if selected_xpath_name in xpath_dict:
                        xpath_dict[selected_xpath_name] = new_xpath_value
                        self.currentXpathText.setPlainText(new_xpath_value)
                        break
        self.updateXpathText.clear()
        # Save the updated JSON data back to the file
        self.save_json(utils.XPATH_CONFIG_INTERACTION_JSON, self.json_data)
        msg = QtWidgets.QMessageBox()
        msg.setIcon(QtWidgets.QMessageBox.Icon.Information)
        msg.setText("Update dữ liệu thành công")
        msg.setWindowTitle("Success")
        msg.exec()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = ui_UpdateXpathTikok()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec())
