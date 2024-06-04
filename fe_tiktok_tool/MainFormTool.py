# Form implementation generated from reading ui file 'formUI.ui'
#
# Created by: PyQt6 UI code generator 6.7.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic6 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QTableWidgetItem

from fe_tiktok_tool.formUI2 import Ui_MainWindow
import json 
import os 
import utils
from fe_tiktok_tool.InputHotmail import ui_InputHotmail
from fe_tiktok_tool.InputProxyForm import ui_InputProxy
from fe_tiktok_tool.InputUserAgent import ui_InputUserAgent
from be_tiktok_tool.regAcc import TikTokWorker
from fe_tiktok_tool.InputAccTiktok import ui_InputAccTiktok
from fe_tiktok_tool.UpdateXpathRegAcc import ui_UpdateXpathRegAcc
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QDateTimeEdit
import sys
from PyQt6.QtCore import QThread
from fe_tiktok_tool.ConfigAcctionTiktok import ui_ConfigAcctionTiktok 
from be_tiktok_tool.router_acction import TikTokActionWorker

class MainForm(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainForm, self).__init__()
        self.setupUi(self)
        self.thread = None
        self.worker = None

    def open_config_acc_tiktok_form(self):
        self.config_dialog = QtWidgets.QDialog()
        self.update_config_acc_tiktok = ui_ConfigAcctionTiktok()
        self.update_config_acc_tiktok.setupUi(self.config_dialog)
        self.config_dialog.exec()

    def open_update_xpath_regacc_form(self):
        self.update_xpath_regacc_dialog = QtWidgets.QDialog()
        self.ui_update_xpath_regacc = ui_UpdateXpathRegAcc()
        self.ui_update_xpath_regacc.setupUi(self.update_xpath_regacc_dialog)
        self.update_xpath_regacc_dialog.exec()

    def open_input_acc_tiktok_form(self):
        self.input_acc_tiktok_dialog = QtWidgets.QDialog()
        self.ui_input_acc_tiktok = ui_InputAccTiktok()
        self.ui_input_acc_tiktok.setupUi(self.input_acc_tiktok_dialog)
        self.input_acc_tiktok_dialog.exec()

    def open_input_user_agent_form(self):
        self.input_user_agent_dialog = QtWidgets.QDialog()
        self.ui_input_user_agent = ui_InputUserAgent()
        self.ui_input_user_agent.setupUi(self.input_user_agent_dialog)
        self.input_user_agent_dialog.exec()

    def open_input_hotmail_form(self):
        self.input_hotmail_dialog = QtWidgets.QDialog()
        self.ui_input_hotmail = ui_InputHotmail()
        self.ui_input_hotmail.setupUi(self.input_hotmail_dialog)
        self.input_hotmail_dialog.exec()

    def open_input_proxy_form(self):
        self.input_proxy_dialog = QtWidgets.QDialog()
        self.ui_input_proxy = ui_InputProxy()
        self.ui_input_proxy.setupUi(self.input_proxy_dialog)
        self.input_proxy_dialog.exec()

    def display_hotmail_data(self, index):
        selected_group = self.regAccCombobox.itemText(index)
        path_file = utils.HOTMAIL_JSON
        with open(path_file, 'r') as file:
            data = json.load(file)

        for item in data:
            if item['groupHotmail'] == selected_group:
                hotmail_list = item['listHotmail']
                self.regAccTable.setRowCount(0)
                for i, hotmail_item in enumerate(hotmail_list):
                    hotmail, password = hotmail_item['hotmail'].split('|')
                    self.regAccTable.insertRow(i)
                    self.regAccTable.setItem(i, 0, QtWidgets.QTableWidgetItem(hotmail))
                    self.regAccTable.setItem(i, 1, QtWidgets.QTableWidgetItem(password))
    
    def display_acc_tiktok_data(self, index):
        selected_group = self.tiktokCombobox.itemText(index)
        path_file = utils.ACC_TIKTOK_JSON
        with open(path_file, 'r') as file:
            data = json.load(file)

        for item in data:
            if item['groupAcc'] == selected_group:
                acc_list = item['listAcc']
                self.tiktokTable.setRowCount(0)
                for i, acc_item in enumerate(acc_list):
                    username, password = acc_item['acc'].split('|')
                    self.tiktokTable.insertRow(i)
                    self.tiktokTable.setItem(i, 1, QtWidgets.QTableWidgetItem(username))
                    self.tiktokTable.setItem(i, 2, QtWidgets.QTableWidgetItem(password))

    def load_group_hotmail(self):
        path_file = utils.HOTMAIL_JSON
        current_index = self.regAccCombobox.currentIndex()
        try:
            with open(path_file, 'r') as file:
                data = json.load(file)
            self.regAccCombobox.clear()
            for item in data:
                group_Hotmail = item.get('groupHotmail', '')  # Use .get to handle missing keys
                self.regAccCombobox.addItem(group_Hotmail)
            
            # Restore previous selection if possible
            if current_index >= 0 and current_index < self.regAccCombobox.count():
                self.regAccCombobox.setCurrentIndex(current_index)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def load_group_acc(self):
        path_file = utils.ACC_TIKTOK_JSON
        current_index = self.tiktokCombobox.currentIndex()
        try:
            with open(path_file, 'r') as file:
                data = json.load(file)
            self.tiktokCombobox.clear()
            for item in data:
                group_acc = item.get('groupAcc', '')  # Use .get to handle missing keys
                self.tiktokCombobox.addItem(group_acc)
            
            # Restore previous selection if possible
            if current_index >= 0 and current_index < self.tiktokCombobox.count():
                self.tiktokCombobox.setCurrentIndex(current_index)
        except json.JSONDecodeError as e:
            print(f"Error decoding JSON from file: {e}")
        except Exception as e:
            print(f"An error occurred: {e}")

    def updateDateTime(self):
        currentDateTime = QtCore.QDateTime.currentDateTime()
        currentDateTimeString = currentDateTime.toString("  dd/MM/yyyy  hh:mm:ss")
        self.dateTimeLable.setText(currentDateTimeString)

    def outputAcctiktok(self):
        selected_ranges = self.regAccTable.selectedRanges()
        if not selected_ranges:
            self.showMessageBox("No selection", "Chưa chọn dữ liệu")
            return

        selected_data = []
        for selection_range in selected_ranges:
            for row in range(selection_range.topRow(), selection_range.bottomRow() + 1):
                item_col_0 = self.regAccTable.item(row, 0)
                item_col_1 = self.regAccTable.item(row, 1)
                if item_col_0 and item_col_1:
                    data_col_0 = item_col_0.text()
                    data_col_1 = item_col_1.text()
                    selected_data.append(f"{data_col_0}|{data_col_1}")

        if not selected_data:
            self.showMessageBox("No valid data", "Chưa chọn dữ liệu")
            return

        current_group = self.regAccCombobox.currentText()

        current_date_time = QtCore.QDateTime.currentDateTime().toString("yyyyMMdd_hhmmss")
        file_name, _ = QtWidgets.QFileDialog.getSaveFileName(None, "Save File", "", "TXT Files (*.txt)")
        with open(file_name, 'w') as file:
            file.write("\n".join(selected_data))

        self.showMessageBox("Success", f"Xuất dữ liệu thành công tại: {file_name}")

    def showMessageBox(self, title, message):
        msg_box = QtWidgets.QMessageBox()
        msg_box.setStyleSheet("color: white; background-color: #272727")
        msg_box.setText(title)
        msg_box.setInformativeText(message)
        msg_box.setWindowTitle(title)
        msg_box.exec()
    def get_selected_reg_acc_data(self):
        data = []
        selected_rows = set()
        for item in self.regAccTable.selectedItems():
            selected_rows.add(item.row())

        for row in selected_rows:
            row_data = []
            for column in range(2):  # Assuming the first two columns contain necessary data
                item = self.regAccTable.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")
            data.append(row_data)
        return data

    def get_thread_value(self):
        return self.threadValue.text()

    def runRegAcc(self):
        reg_acc_data = self.get_selected_reg_acc_data()
        thread_value = self.get_thread_value()

        self.thread = QThread()
        self.worker = TikTokWorker(reg_acc_data, thread_value)  # Pass data to worker

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        # self.worker.finished.connect(self.worker.deleteLater)
        # self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()
        self.startBtn_RegAcc.setEnabled(False)
        self.thread.finished.connect(lambda: self.startBtn_RegAcc.setEnabled(True))

    def update_table_status_tiktokTable(self, account, status):
        # Update table with account ID and status
        for row in range(self.tiktokTable.rowCount()):
            if self.tiktokTable.item(row, 1).text() == account:  # Check if username matches
                status_item = QTableWidgetItem(status)
                self.tiktokTable.setItem(row, 3, status_item)  # Update column 3 (index 2)
                break
    
    def get_selected_acc_tiktok_data(self):
        data = []
        selected_rows = set()
        
        # Collect all selected rows
        for item in self.tiktokTable.selectedItems():
            selected_rows.add(item.row())

        # Iterate over each selected row
        for row in selected_rows:
            row_data = []
            
            columns = [1,2]
            for column in columns:  # Columns 0 and 1 (first and second columns)
                item = self.tiktokTable.item(row, column)
                if item is not None:
                    row_data.append(item.text())
                else:
                    row_data.append("")  # Add an empty string if the cell is empty

            data.append(row_data)

        return data


    def runActionTikok(self):
        acc_tiktok_data = self.get_selected_acc_tiktok_data()
        thread_value = self.threadValue.text()

        if thread_value == '' or not acc_tiktok_data:
            # Show warning message box
            msg = QMessageBox()
            msg.setText("Please select the number of threads and accounts")
            msg.setWindowTitle("Warning")
            msg.exec()
            return

        self.thread = QtCore.QThread()
        self.worker = TikTokActionWorker(acc_tiktok_data, thread_value)

        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)

        self.thread.start()
        self.startBtn_tiktok.setEnabled(False)
        self.thread.finished.connect(lambda: self.startBtn_tiktok.setEnabled(True))
        self.worker.update_table_signal.connect(self.update_table_status_tiktokTable)



    def on_regAccCombobox_changed(self, index):
        # Get the currently selected item text
        selected_text = self.regAccCombobox.currentText()
    def on_tiktokCombobox_changed(self, index):
        # Get the currently selected item text
        selected_text = self.tiktokCombobox.currentText()

    
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateDateTime)
        self.timer.start(1000)
        self.load_group_hotmail()
        self.load_group_acc()
        self.regAccCombobox.activated.connect(self.load_group_hotmail)
        self.tiktokCombobox.activated.connect(self.load_group_acc)
        self.regAccCombobox.activated.connect(self.display_hotmail_data)
        self.tiktokCombobox.activated.connect(self.display_acc_tiktok_data)
        self.addHotmailBtn.clicked.connect(self.open_input_hotmail_form)
        self.addProxyBtn.clicked.connect(self.open_input_proxy_form)
        self.addUserAgentBtn.clicked.connect(self.open_input_user_agent_form)
        self.startBtn_RegAcc.clicked.connect(self.runRegAcc)
        self.addAccBtn.clicked.connect(self.open_input_acc_tiktok_form)
        self.toolSettingRegBtn.clicked.connect(self.open_update_xpath_regacc_form)
        self.outputAccTiktok.clicked.connect(self.outputAcctiktok)
        self.regAccCombobox.currentIndexChanged.connect(self.on_regAccCombobox_changed)
        self.tiktokCombobox.currentIndexChanged.connect(self.on_tiktokCombobox_changed)
        self.growAccBtn.clicked.connect(self.open_config_acc_tiktok_form)
        self.newfeedBtn.clicked.connect(self.open_config_acc_tiktok_form)
        self.userBtn.clicked.connect(self.open_config_acc_tiktok_form)
        self.topicBtn.clicked.connect(self.open_config_acc_tiktok_form)
        self.liveBtn.clicked.connect(self.open_config_acc_tiktok_form)
        self.startBtn_tiktok.clicked.connect(self.runActionTikok)


   
    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        item = self.regAccTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "Hotmail"))
        item = self.regAccTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Pass hotmail"))
        item = self.regAccTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Pass tiktok"))
        item = self.regAccTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Trạng thái"))
        item = self.regAccTable.horizontalHeaderItem(4)
        item.setText(_translate("MainWindow", "Thời gian tạo"))
        self.addHotmailBtn.setText(_translate("MainWindow", "Thêm Hotmail"))
        self.startBtn_RegAcc.setText(_translate("MainWindow", "Start"))
        self.endBtn_RegAcc.setText(_translate("MainWindow", "End"))
        self.tiktokTab.setTabText(self.tiktokTab.indexOf(self.tab), _translate("MainWindow", "RegAcc"))
        self.growAccBtn.setText(_translate("MainWindow", "Nuôi acc"))
        self.newfeedBtn.setText(_translate("MainWindow", "Tương tác newfeed"))
        self.userBtn.setText(_translate("MainWindow", "Tương tác user"))
        self.topicBtn.setText(_translate("MainWindow", "Tương tác theo chủ đề"))
        self.liveBtn.setText(_translate("MainWindow", "Tương tác live"))
        self.tiktokCombobox.setItemText(0, _translate("MainWindow", "Nhom acc 1"))
       
        item = self.tiktokTable.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "ID Profile"))
        item = self.tiktokTable.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "Username"))
        item = self.tiktokTable.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "Password"))
        item = self.tiktokTable.horizontalHeaderItem(3)
        item.setText(_translate("MainWindow", "Trạng thái"))
        self.startBtn_tiktok.setText(_translate("MainWindow", "Start"))
        self.endBtn_tiktok.setText(_translate("MainWindow", "End"))
        self.tiktokTab.setTabText(self.tiktokTab.indexOf(self.tab_2), _translate("MainWindow", "Tương tác Tikotk"))
        self.addUserAgentBtn.setText(_translate("MainWindow", "Thêm UserAgents"))
        self.addProxyBtn.setText(_translate("MainWindow", "Thêm Proxy"))
        self.addAccBtn.setText(_translate("MainWindow", "Thêm Accounts"))
        self.checkProfileBtn.setText(_translate("MainWindow", "Check Live Profile"))
        self.checkProxyBtn.setText(_translate("MainWindow", "Check Live Proxy "))
        self.threadLable.setText(_translate("MainWindow", "Số luồng"))
        self.outputAccTiktok.setText(_translate("MainWindow", "Xuất file txt"))
        self.toolSettingRegBtn.setText(_translate("MainWindow", "Cấu hình xpath"))

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = MainForm()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())