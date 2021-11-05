import sqlite3
import sys
import datetime as dt

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QFileDialog, QMessageBox


class Main_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pr.ui', self)
        self.connection = sqlite3.connect("personnel_management_system.db")
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit)
        self.pushButton_3.clicked.connect(self.delete)
        self.addgroup.clicked.connect(self.add)
        self.editgroup.clicked.connect(self.edit)
        self.deletegroup.clicked.connect(self.delete)
        self.adddep.clicked.connect(self.add)
        self.editdep.clicked.connect(self.edit)
        self.deletedep.clicked.connect(self.delete)
        self.addpos.clicked.connect(self.add)
        self.editpos.clicked.connect(self.edit)
        self.deletepos.clicked.connect(self.delete)
        self.select_data()
        self.tableWidget.itemClicked.connect(self.photo)

    def get_id_by_row(self, table):
        ID = False
        row = table.currentRow()
        if row >= 0:
            fl = table.item(row, 0).text()
            ID = int(fl)
        return ID

    def photo(self):
        cur = self.connection.cursor()
        result = [i[5] for i in cur.execute(f"""SELECT * FROM employees WHERE id = {self.get_id_by_row(self.tableWidget)}""")][0]
        pixmap = QPixmap(f'{result}')
        pixmap = pixmap.scaled(350, 450)
        self.picture.setPixmap(pixmap)

    def select_data(self):
        self.output_data("""SELECT employees.id, employees.Fullname, employees.DOB, groups.Title, positions.Title 
        FROM employees LEFT JOIN groups ON employees.GroupId = groups.id 
        LEFT JOIN positions ON employees.PositionId = positions.id;""", self.tableWidget, 5,
                         ["ИД", "ФИО", "Дата рождения", "Группа", "Должность"])
        self.output_data("""SELECT groups.id, groups.Title, departments.Title 
        FROM groups LEFT JOIN departments ON groups.DepartmentId = departments.id;""", self.tablegroup, 3,
                         ["ИД", "Группа", "Отдел"])
        self.output_data("""SELECT id, Title FROM departments""", self.tabledep, 2, ["ИД", "Отдел"])
        self.output_data("""SELECT id, Title FROM positions""", self.tablepos, 2, ["ИД", "Должность"])

    def output_data(self, value, table, num, values):
        res = self.connection.cursor().execute(value).fetchall()
        table.setColumnCount(num)
        table.setRowCount(0)
        table.setHorizontalHeaderLabels(values)
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
            self.child = Dialog_window(self)
            self.child.update_combo()
            self.child.func = "INSERT"
            self.child.show()
        elif source == self.addgroup:
            self.child1 = Dialog_window1(self)
            self.child1.update_combo()
            self.child1.func = "INSERT"
            self.child1.show()
        elif source == self.adddep:
            self.child2 = Dialog_window2(self)
            self.child2.func = "INSERT"
            self.child2.place = 'Departments'
            self.child2.show()
        elif source == self.addpos:
            self.child3 = Dialog_window2(self)
            self.child3.func = "INSERT"
            self.child3.place = 'Positions'
            self.child3.show()

    def edit(self):
        source = self.sender()
        if source == self.pushButton_2:
            ID = self.get_id_by_row(self.tableWidget)
            self.child = Dialog_window(self)
            if ID:
                cur = self.connection.cursor()
                result = cur.execute(f"""SELECT * FROM employees WHERE id = {ID}""").fetchall()[0]
                data = [int(i) for i in result[2].split(".")]
                data = dt.date(data[2], data[1], data[0])
                try:
                    res1 = cur.execute(f"""SELECT Title FROM groups WHERE id = {result[3]}""").fetchall()[0][0]
                except:
                    res1 = None
                try:
                    res2 = cur.execute(f"""SELECT Title FROM positions WHERE id = {result[4]}""").fetchall()[0][0]
                except:
                    res2 = None
                self.child.update_combo()
                self.child.lineEdit.setText(result[1])
                self.child.dateEdit.setDate(data)
                self.child.comboBox.setCurrentText(res1)
                self.child.comboBox.setCurrentText(res2)
                self.child.fileName = result[5]
                self.child.ID = ID
                self.child.func = "UPDATE"
                self.child.show()
        elif source == self.editgroup:
            ID = self.get_id_by_row(self.tablegroup)
            self.child1 = Dialog_window1(self)
            if ID:
                cur = self.connection.cursor()
                result = cur.execute(f"""SELECT * FROM groups WHERE id = {ID}""").fetchall()[0]
                try:
                    res = cur.execute(f"""SELECT Title FROM groups WHERE id = {result[2]}""").fetchall()[0][0]
                except:
                    res = "Не назначено"
                self.child1.update_combo()
                self.child1.lineEdit.setText(result[1])
                self.child1.comboBox.setCurrentText(res)
                self.child1.ID = ID
                self.child1.func = "UPDATE"
                self.child1.show()
        elif source == self.editdep:
            ID = self.get_id_by_row(self.tabledep)
            self.child2 = Dialog_window2(self)
            if ID:
                cur = self.connection.cursor()
                result = cur.execute(f"""SELECT * FROM departments WHERE id = {ID}""").fetchall()[0]
                self.child2.lineEdit.setText(result[1])
                self.child2.ID = ID
                self.child2.func = "UPDATE"
                self.child2.place = 'Departments'
                self.child2.show()
        elif source == self.editpos:
            ID = self.get_id_by_row(self.tablepos)
            self.child3 = Dialog_window2(self)
            if ID:
                cur = self.connection.cursor()
                result = cur.execute(f"""SELECT * FROM positions WHERE id = {ID}""").fetchall()[0]
                self.child3.lineEdit.setText(result[1])
                self.child3.ID = ID
                self.child3.func = "UPDATE"
                self.child3.place = 'Positions'
                self.child3.show()

    def delete(self):
        source = self.sender()
        if source == self.pushButton_3:
            ID = self.get_id_by_row(self.tableWidget)
            if ID:
                valid = QMessageBox.question(
                    self, '', f"Действительно удалить элементы с id {ID}",
                    QMessageBox.Yes, QMessageBox.No)
                if valid == QMessageBox.Yes:
                    cur = self.connection.cursor()
                    cur.execute(f"DELETE FROM employees WHERE id = {ID}")
                    self.connection.commit()
                    self.select_data()
        elif source == self.deletegroup:
            ID = self.get_id_by_row(self.tablegroup)
            if ID:
                valid = QMessageBox.question(
                    self, '', f"Действительно удалить элементы с id {ID}",
                    QMessageBox.Yes, QMessageBox.No)
                if valid == QMessageBox.Yes:
                    cur = self.connection.cursor()
                    cur.execute(f"DELETE FROM groups WHERE id = {ID}")
                    self.connection.commit()
                    self.select_data()
        elif source == self.deletedep:
            ID = self.get_id_by_row(self.tabledep)
            if ID:
                valid = QMessageBox.question(
                    self, '', f"Действительно удалить элементы с id {ID}",
                    QMessageBox.Yes, QMessageBox.No)
                if valid == QMessageBox.Yes:
                    cur = self.connection.cursor()
                    cur.execute(f"DELETE FROM departments WHERE id = {ID}")
                    self.connection.commit()
                    self.select_data()
        elif source == self.deletepos:
            ID = self.get_id_by_row(self.tablepos)
            if ID:
                valid = QMessageBox.question(
                    self, '', f"Действительно удалить элементы с id {ID}",
                    QMessageBox.Yes, QMessageBox.No)
                if valid == QMessageBox.Yes:
                    cur = self.connection.cursor()
                    cur.execute(f"DELETE FROM positions WHERE id = {ID}")
                    self.connection.commit()
                    self.select_data()

    def sorting(self):
        pass

    def find(self):
        pass


class Dialog_window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('dialog.ui', self)
        self.ID = None
        self.fileName = None
        self.func = None
        self.connection = sqlite3.connect("personnel_management_system.db")
        self.update_combo()
        self.lineEdit.textChanged.connect(self.on_text_changed)
        self.buttonBox.accepted.connect(self.dialog)

    def on_text_changed(self):
        self.buttonBox.setEnabled(bool(self.lineEdit.text()))

    def update_combo(self):
        self.comboBox.clear()
        self.comboBox_2.clear()
        cur = self.connection.cursor()
        result = [i[0] for i in cur.execute("""SELECT Title from groups""").fetchall()]
        for i in result:
            self.comboBox.addItem(i)
        result = [i[0] for i in cur.execute("""SELECT Title from positions""").fetchall()]
        for i in result:
            self.comboBox_2.addItem(i)

    def dialog(self):
        cur = self.connection.cursor()
        self.fullname = self.lineEdit.text()
        if self.fullname != "":
            DOB = self.dateEdit.text()
            group = cur.execute(f"""SELECT id FROM groups
    WHERE Title = '{self.comboBox.currentText()}'""").fetchall()[0][0]
            position = cur.execute(f"""SELECT id FROM positions
    WHERE Title = '{self.comboBox_2.currentText()}'""").fetchall()[0][0]
            if self.func == "INSERT":
                cur.execute(f"""INSERT INTO employees(Fullname, DOB, GroupId, PositionId, Picture)
                    VALUES('{self.fullname}', '{DOB}', {group}, {position}, '{self.fileName}')""")
            else:
                cur.execute(f"""UPDATE employees
                SET Fullname = '{self.fullname}', DOB = '{DOB}', GroupId = {group}, PositionId = {position},
Picture = '{self.fileName}'
                WHERE id = {self.ID}""")
            self.connection.commit()
            window.select_data()

    def mybutton_clicked(self):
        options = QFileDialog.Options()
        self.fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "All Files (*)",
                                                       options=options)


class Dialog_window1(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('dialog1.ui', self)
        self.ID = None
        self.title = None
        self.func = None
        self.connection = sqlite3.connect("personnel_management_system.db")
        self.update_combo()
        self.lineEdit.textChanged.connect(self.on_text_changed)
        self.buttonBox.accepted.connect(self.dialog)

    def on_text_changed(self):
        self.buttonBox.setEnabled(bool(self.lineEdit.text()))

    def update_combo(self):
        self.comboBox.clear()
        cur = self.connection.cursor()
        result = [i[0] for i in cur.execute("""SELECT Title from departments""").fetchall()]
        for i in result:
            self.comboBox.addItem(i)

    def dialog(self):
        cur = self.connection.cursor()
        self.title = self.lineEdit.text()
        if self.title != "":
            department = cur.execute(f"""SELECT id FROM departments
            WHERE Title = '{self.comboBox.currentText()}'""").fetchall()[0][0]
            if self.func == "INSERT":
                cur.execute(f"""INSERT INTO groups(Title, DepartmentId)
                            VALUES('{self.title}', '{department}')""")
            else:
                cur.execute(f"""UPDATE groups
                        SET Title = '{self.title}', DepartmentId = {department} WHERE id = {self.ID}""")
            self.connection.commit()
            window.select_data()


class Dialog_window2(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('dialog2.ui', self)
        self.ID = None
        self.title = None
        self.func = None
        self.place = None
        self.connection = sqlite3.connect("personnel_management_system.db")
        self.lineEdit.textChanged.connect(self.on_text_changed)
        self.buttonBox.accepted.connect(self.dialog)

    def on_text_changed(self):
        self.buttonBox.setEnabled(bool(self.lineEdit.text()))

    def dialog(self):
        cur = self.connection.cursor()
        self.title = self.lineEdit.text()
        if self.title != "":
            if self.place == 'Departments':
                if self.func == "INSERT":
                    cur.execute(f"""INSERT INTO departments(Title)
                                VALUES('{self.title}')""")
                else:
                    cur.execute(f"""UPDATE departments
                            SET Title = '{self.title}' WHERE id = {self.ID}""")
            elif self.place == "Positions":
                if self.func == "INSERT":
                    cur.execute(f"""INSERT INTO positions(Title)
                                VALUES('{self.title}')""")
                else:
                    cur.execute(f"""UPDATE positions
                            SET Title = '{self.title}' WHERE id = {self.ID}""")
            self.connection.commit()
            window.select_data()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Main_window()
    window.show()
    sys.exit(app.exec())
