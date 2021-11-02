import sqlite3
import sys
import datetime as dt

from PyQt5 import uic
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem, QDialog, QFileDialog, QMessageBox


class Parent_window(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pr.ui', self)
        self.connection = sqlite3.connect("personnel_management_system.db")
        self.pushButton.clicked.connect(self.add)
        self.pushButton_2.clicked.connect(self.edit)
        self.pushButton_3.clicked.connect(self.delete)
        self.select_data()
        self.tableWidget.itemClicked.connect(self.choice)

    def get_id_by_row(self):
        ID = False
        row = self.tableWidget.currentRow()
        if row >= 0:
            fl = self.tableWidget.item(row, 0).text()
            ID = int(fl)
        return ID

    def choice(self):
        cur = self.connection.cursor()
        result = [i[5] for i in cur.execute(f"""SELECT * FROM employees WHERE id = {self.get_id_by_row()}""")][0]
        pixmap = QPixmap(f'{result}')
        pixmap = pixmap.scaled(350, 450)
        self.picture.setPixmap(pixmap)

    def select_data(self):
        res = self.connection.cursor().execute("""SELECT
    employees.id,
    employees.Fullname,
    employees.DOB,
    groups.Title,
    positions.Title
FROM
    employees
LEFT JOIN groups ON employees.GroupId = groups.id
LEFT JOIN positions ON employees.PositionId = positions.id;""").fetchall()
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setRowCount(0)
        self.tableWidget.setHorizontalHeaderLabels(["ИД", "ФИО", "Дата рождения", "Группа", "Должность"])
        for i, row in enumerate(res):
            self.tableWidget.setRowCount(
                self.tableWidget.rowCount() + 1)
            for j, elem in enumerate(row):
                self.tableWidget.setItem(
                    i, j, QTableWidgetItem(str(elem)))

    def closeEvent(self, event):
        self.connection.close()

    def add(self):
        self.child = Child_window(self)
        self.child.func = "INSERT"
        self.child.show()

    def edit(self):
        self.child = Child_window(self)
        ID = self.get_id_by_row()
        if ID:
            cur = self.connection.cursor()
            result = cur.execute(f"""SELECT * FROM employees WHERE id = {ID}""").fetchall()[0]
            data = [int(i) for i in result[2].split(".")]
            data = dt.date(data[2], data[1], data[0])
            res1 = cur.execute(f"""SELECT Title FROM groups WHERE id = {result[3]}""").fetchall()[0][0]
            res2 = cur.execute(f"""SELECT Title FROM positions WHERE id = {result[4]}""").fetchall()[0][0]
            self.child.lineEdit.setText(result[1])
            self.child.dateEdit.setDate(data)
            self.child.comboBox.setCurrentText(res1)
            self.child.comboBox.setCurrentText(res2)
            self.child.fileName = result[5]
            self.child.ID = ID
            self.child.func = "UPDATE"
            self.child.show()

    def delete(self):
        ID = self.get_id_by_row()
        if ID:
            valid = QMessageBox.question(
                self, '', f"Действительно удалить элементы с id {ID}",
                QMessageBox.Yes, QMessageBox.No)
            if valid == QMessageBox.Yes:
                cur = self.connection.cursor()
                cur.execute(f"DELETE FROM employees WHERE id = {ID}")
                self.connection.commit()
                self.select_data()


class Child_window(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        uic.loadUi('dialog.ui', self)
        self.ID = None
        self.fileName = None
        self.func = None
        self.connection = sqlite3.connect("personnel_management_system.db")
        cur = self.connection.cursor()
        result = [i[0] for i in cur.execute("""SELECT Title from groups""").fetchall()]
        for i in result:
            self.comboBox.addItem(i)
        result = [i[0] for i in cur.execute("""SELECT Title from positions""").fetchall()]
        for i in result:
            self.comboBox_2.addItem(i)
        self.buttonBox.accepted.connect(self.dialog)

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
        self.fileName, _ = QFileDialog.getOpenFileName(self,"QFileDialog.getOpenFileName()", "","All Files (*)", options=options)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Parent_window()
    window.show()
    sys.exit(app.exec())
