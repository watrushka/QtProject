import sqlite3


class EmployeesDBService:

    def __init__(self):
        self.connection = sqlite3.connect("personnel_management_system.db")

    def add_employee(self, name, dob, groupid, positionid, picture):
        cur = self.connection.cursor()
        cur.execute(f"""INSERT INTO employees(Fullname, DOB, GroupId, PositionId, Picture)
                            VALUES('{name}', '{dob}', {groupid}, {positionid}, '{picture}')""")
        self.connection.commit()

    def update_employee(self, fullname, DOB, group, position, picture, ID):
        self.connection.cursor().execute(f"""UPDATE employees
                        SET Fullname = '{fullname}', DOB = '{DOB}', GroupId = {group}, PositionId = {position}, 
Picture = '{picture}' WHERE id = {ID}""")
        self.connection.commit()

    def get_employees(self):
        query = """SELECT employees.id, employees.Fullname, employees.DOB, groups.Title, positions.Title 
        FROM employees LEFT JOIN groups ON employees.GroupId = groups.id 
        LEFT JOIN positions ON employees.PositionId = positions.id;"""
        return self.execute_query(query)

    def get_groups(self):
        query = """SELECT groups.id, groups.Title, departments.Title 
        FROM groups LEFT JOIN departments ON groups.DepartmentId = departments.id;"""
        return self.execute_query(query)

    def get_departments(self):
        query = """SELECT id, Title FROM departments"""
        return self.execute_query(query)

    def get_positions(self):
        query = """SELECT id, Title FROM positions"""
        return self.execute_query(query)

    def execute_query(self, query):
        return self.connection.cursor().execute(query).fetchall()

    def get_photo(self, id):
        cur = self.connection.cursor()
        return [i[5] for i in cur.execute(f"""SELECT * FROM employees WHERE id = {id}""")][0]

    def get_employee(self, ID):
        cur = self.connection.cursor()
        return cur.execute(f"""SELECT * FROM employees WHERE id = {ID}""").fetchall()[0]

    def get_group_title(self, ID):
        cur = self.connection.cursor()
        return cur.execute(f"""SELECT Title FROM groups WHERE id = {ID}""").fetchall()[0][0]

    def get_position_title(self, ID):
        cur = self.connection.cursor()
        return cur.execute(f"""SELECT Title FROM positions WHERE id = {ID}""").fetchall()[0][0]

    def get_group(self, ID):
        cur = self.connection.cursor()
        return cur.execute(f"""SELECT * FROM groups WHERE id = {ID}""").fetchall()[0]

    def get_department(self, ID):
        cur = self.connection.cursor()
        return cur.execute(f"""SELECT * FROM departments WHERE id = {ID}""").fetchall()[0]

    def get_position(self, ID):
        cur = self.connection.cursor()
        return cur.execute(f"""SELECT * FROM positions WHERE id = {ID}""").fetchall()[0]

    def delete_employee(self, ID):
        cur = self.connection.cursor()
        cur.execute(f"DELETE FROM employees WHERE id = {ID}")
        self.connection.commit()

    def delete_group(self, ID):
        cur = self.connection.cursor()
        cur.execute(f"DELETE FROM groups WHERE id = {ID}")
        self.connection.commit()

    def delete_department(self, ID):
        cur = self.connection.cursor()
        cur.execute(f"DELETE FROM departments WHERE id = {ID}")
        self.connection.commit()

    def delete_position(self, ID):
        cur = self.connection.cursor()
        cur.execute(f"DELETE FROM positions WHERE id = {ID}")
        self.connection.commit()

    def get_group_titles(self):
        return self.connection.cursor().execute(f"""SELECT Title FROM groups""").fetchall()

    def get_position_titles(self):
        return self.connection.cursor().execute(f"""SELECT Title FROM positions""").fetchall()

    def get_group_id(self, title):
        return self.connection.cursor().execute(f"""SELECT id FROM groups
            WHERE Title = '{title}'""").fetchall()[0][0]

    def get_position_id(self, title):
        return self.connection.cursor().execute(f"""SELECT id FROM positions
            WHERE Title = '{title}'""").fetchall()[0][0]

    def get_department_titles(self):
        return self.connection.cursor().execute("""SELECT Title from departments""").fetchall()

    def get_departments_id(self, title):
        return self.connection.cursor().execute(f"""SELECT id FROM departments
            WHERE Title = '{title}'""").fetchall()[0][0]

    def add_groups(self, title, department):
        self.connection.cursor().execute(f"""INSERT INTO groups(Title, DepartmentId)
                                    VALUES('{title}', '{department}')""")
        self.connection.commit()

    def update_groups(self, title, department, ID):
        self.connection.cursor().execute(f"""UPDATE groups
                                SET Title = '{title}', DepartmentId = {department} WHERE id = {ID}""")
        self.connection.commit()

    def add_departments(self, title):
        self.connection.cursor().execute(f"""INSERT INTO departments(Title)
                                        VALUES('{title}')""")
        self.connection.commit()

    def update_departments(self, title, ID):
        self.connection.cursor().execute(f"""UPDATE departments
                                    SET Title = '{title}' WHERE id = {ID}""")
        self.connection.commit()

    def add_positions(self, title):
        self.connection.cursor().execute(f"""INSERT INTO positions(Title)
                                        VALUES('{title}')""")
        self.connection.commit()

    def update_positions(self, title, ID):
        self.connection.cursor().execute(f"""UPDATE positions
                                    SET Title = '{title}' WHERE id = {ID}""")
        self.connection.commit()
