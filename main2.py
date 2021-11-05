import sqlite3
import sys
import datetime as dt

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QFileDialog, QMessageBox

from employeedbservice import EmployeesDBService


class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.dbservice = EmployeesDBService()

        uic.loadUi('pr.ui', self)
        self.buttons_connections()
        self.select_data()

    def buttons_connections(self):
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit_employees)
        self.pushButton_3.clicked.connect(self.delete_employee)
        self.addgroup.clicked.connect(self.add)
        self.editgroup.clicked.connect(self.edit_groups)
        self.deletegroup.clicked.connect(self.delete_group)
        self.adddep.clicked.connect(self.add)
        self.editdep.clicked.connect(self.edit_departments)
        self.deletedep.clicked.connect(self.delete_department)
        self.addpos.clicked.connect(self.add)
        self.editpos.clicked.connect(self.edit_positions)
        self.deletepos.clicked.connect(self.delete_position)
        self.tableWidget.itemClicked.connect(self.set_photo)

    def get_id_by_row(self, table):
        ID = False
        row = table.currentRow()
        if row >= 0:
            fl = table.item(row, 0).text()
            ID = int(fl)
        return ID

    def set_photo(self):
        result = self.dbservice.get_photo(window.get_id_by_row(window.tableWidget))
        pixmap = QPixmap(f'{result}')
        pixmap = pixmap.scaled(350, 450)
        self.picture.setPixmap(pixmap)

    def select_data(self):
        self.insert_data_in_table(self.dbservice.get_employees(), self.tableWidget, 5,
                                  ["ИД", "ФИО", "Дата рождения", "Группа", "Должность"])
        self.insert_data_in_table(self.dbservice.get_groups(), self.tablegroup, 3, ["ИД", "Группа", "Отдел"])
        self.insert_data_in_table(self.dbservice.get_departments(), self.tabledep, 2, ["ИД", "Отдел"])
        self.insert_data_in_table(self.dbservice.get_positions(), self.tablepos, 2, ["ИД", "Должность"])

    def insert_data_in_table(self, res, table, number_of_columns, columns_names):
        table.setColumnCount(number_of_columns)
        table.setRowCount(0)
        table.setHorizontalHeaderLabels(columns_names)
        for i, row in enumerate(res):
            table.setRowCount(
                table.rowCount() + 1)
            for j, elem in enumerate(row):
                if elem is None:
                    elem = "Не назначено"
                table.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()

    def add(self):
        source = self.sender()
        if source == self.pushButton:
            self.child = EmployeeWindow(self.dbservice, self)
            self.child.update_combo()
            self.child.func = "INSERT"
            self.child.show()
        elif source == self.addgroup:
            self.child1 = Dialog_window1(self.dbservice, self)
            self.child1.update_combo()
            self.child1.func = "INSERT"
            self.child1.show()
        elif source == self.adddep:
            self.child2 = Dialog_window2(self.dbservice, self)
            self.child2.func = "INSERT"
            self.child2.place = 'Departments'
            self.child2.show()
        elif source == self.addpos:
            self.child3 = Dialog_window2(self.dbservice, self)
            self.child3.func = "INSERT"
            self.child3.place = 'Positions'
            self.child3.show()

    def edit_employees(self):
        ID = self.get_id_by_row(self.tableWidget)
        self.child = EmployeeWindow(self.dbservice, self)
        if ID:
            employee = self.dbservice.get_employee(ID)
            dob = [int(i) for i in employee[2].split(".")]
            dob = dt.date(dob[2], dob[1], dob[0])
            try:
                res1 = self.dbservice.get_group_title(employee[3])
            except:
                res1 = None
            try:
                res2 = self.dbservice.get_position_title(employee[4])
            except:
                res2 = None
            self.child.update_combo()
            self.child.lineEdit.setText(employee[1])
            self.child.dateEdit.setDate(dob)
            self.child.comboBox.setCurrentText(res1)
            self.child.comboBox_2.setCurrentText(res2)
            self.child.fileName = employee[5]
            self.child.ID = ID
            self.child.func = "UPDATE"
            self.child.show()

    def edit_groups(self):
        ID = self.get_id_by_row(self.tablegroup)
        self.child1 = Dialog_window1(self.dbservice, self)
        if ID:
            result = self.dbservice.get_group(ID)
            try:
                res = self.dbservice.get_group_title(result[2])
            except:
                res = "Не назначено"
            self.child1.update_combo()
            self.child1.lineEdit.setText(result[1])
            self.child1.comboBox.setCurrentText(res)
            self.child1.ID = ID
            self.child1.func = "UPDATE"
            self.child1.show()

    def edit_departments(self):
        ID = self.get_id_by_row(self.tabledep)
        self.child2 = Dialog_window2(self.dbservice, self)
        if ID:
            result = self.dbservice.get_department(ID)
            self.child2.lineEdit.setText(result[1])
            self.child2.ID = ID
            self.child2.func = "UPDATE"
            self.child2.place = 'Departments'
            self.child2.show()

    def edit_positions(self):
        ID = self.get_id_by_row(self.tablepos)
        self.child3 = Dialog_window2(self.dbservice, self)
        if ID:
            result = self.dbservice.get_position(ID)
            self.child3.lineEdit.setText(result[1])
            self.child3.ID = ID
            self.child3.func = "UPDATE"
            self.child3.place = 'Positions'
            self.child3.show()

    def delete_employee(self):
        source = self.sender()
        if source == self.pushButton_3:
            ID = self.get_id_by_row(self.tableWidget)
            if ID:
                valid = QMessageBox.question(
                    self, '', f"Действительно удалить элементы с id {ID}",
                    QMessageBox.Yes, QMessageBox.No)
                if valid == QMessageBox.Yes:
                    self.dbservice.delete_employee(ID)
                    self.select_data()

    def delete_group(self):
        ID = self.get_id_by_row(self.tablegroup)
        if ID:
            valid = QMessageBox.question(
                self, '', f"Действительно удалить элемент с id {ID}",
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.dbservice.delete_group(ID)
                self.select_data()

    def delete_department(self):
        ID = self.get_id_by_row(self.tabledep)
        if ID:
            valid = QMessageBox.question(
                self, '', f"Действительно удалить элемент с id {ID}",
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.dbservice.delete_department(ID)
                self.select_data()

    def delete_position(self):
        ID = self.get_id_by_row(self.tablepos)
        if ID:
            valid = QMessageBox.question(
                self, '', f"Действительно удалить элемент с id {ID}",
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                self.dbservice.delete_position(ID)
                self.select_data()

    def sorting(self):
        pass

    def find(self):
        pass


class EmployeeWindow(QDialog):

    def __init__(self, dbservice, parent=None):
        super().__init__(parent)
        uic.loadUi('dialog.ui', self)
        self.ID = None
        self.fileName = None
        self.func = None
        self.dbservice = dbservice
        self.update_combo()
        self.lineEdit.textChanged.connect(self.on_text_changed)
        self.buttonBox.accepted.connect(self.dialog)

    def on_text_changed(self):
        self.buttonBox.setEnabled(bool(self.lineEdit.text()))

    def update_combo(self):
        self.comboBox.clear()
        self.comboBox_2.clear()
        result = [i[0] for i in self.dbservice.get_group_titles()]
        for i in result:
            self.comboBox.addItem(i)
        result = [i[0] for i in self.dbservice.get_position_titles()]
        for i in result:
            self.comboBox_2.addItem(i)

    def dialog(self):
        fullname = self.lineEdit.text()
        if fullname != "":
            DOB = self.dateEdit.text()
            group = self.dbservice.get_group_id(self.comboBox.currentText())
            position = self.dbservice.get_position_id(self.comboBox_2.currentText())
            if self.func == "INSERT":
                self.dbservice.add_employee(fullname, DOB, group, position, self.fileName)
            else:
                self.dbservice.update_employee(fullname, DOB, group, position, self.fileName, self.ID)
            window.select_data()

    def mybutton_clicked(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)",
                                                       options=options)


class Dialog_window1(QDialog):
    def __init__(self, dbservice, parent=None):
        super().__init__(parent)
        uic.loadUi('dialog1.ui', self)
        self.ID = None
        self.title = None
        self.func = None
        self.dbservice = dbservice
        self.connection = sqlite3.connect("personnel_management_system.db")
        self.update_combo()
        self.lineEdit.textChanged.connect(self.on_text_changed)
        self.buttonBox.accepted.connect(self.dialog)

    def on_text_changed(self):
        self.buttonBox.setEnabled(bool(self.lineEdit.text()))

    def update_combo(self):
        self.comboBox.clear()
        result = [i[0] for i in self.dbservice.get_department_titles()]
        for i in result:
            self.comboBox.addItem(i)

    def dialog(self):
        self.title = self.lineEdit.text()
        if self.title != "":
            department = self.dbservice.get_departments_id(self.comboBox.currentText())
            if self.func == "INSERT":
                self.dbservice.add_groups(self.title, department)
            else:
                self.dbservice.update_groups(self.title, department, self.ID)
            window.select_data()


class Dialog_window2(QDialog):
    def __init__(self, dbservice, parent=None):
        super().__init__(parent)
        uic.loadUi('dialog2.ui', self)
        self.ID = None
        self.title = None
        self.func = None
        self.place = None
        self.dbservice = dbservice
        self.connection = sqlite3.connect("personnel_management_system.db")
        self.lineEdit.textChanged.connect(self.on_text_changed)
        self.buttonBox.accepted.connect(self.dialog)

    def on_text_changed(self):
        self.buttonBox.setEnabled(bool(self.lineEdit.text()))

    def dialog(self):
        self.title = self.lineEdit.text()
        if self.title != "":
            if self.place == 'Departments':
                if self.func == "INSERT":
                    self.dbservice.add_departments(self.title)
                else:
                    self.dbservice.update_departments(self.title, self.ID)
            elif self.place == "Positions":
                if self.func == "INSERT":
                    self.dbservice.add_positions(self.title)
                else:
                    self.dbservice.update_positions(self.title, self.ID)
            window.select_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_window()
    window.show()
    sys.exit(app.exec())
