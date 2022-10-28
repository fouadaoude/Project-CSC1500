import sqlite3

class Database:
    DB_LOCATION = "database/database.db"

    def __init__(self):
        self.connection = self.connect()
        self.cursor = self.get_cursor()

        self.user_info = {}

    def log_out(self):        
        self.user_info = {}
        self.close()

    def validate_login(self, **kwargs):
        """attempt to select all user information based on user input"""        
        
        try:
            employee_name = kwargs['employee_name']
            password = kwargs['password']
            sql = '''SELECT * FROM employees WHERE [employee_name]=? AND [password]=?;'''
            values = (employee_name, password)
            self.execute(sql, values)
            result = self.cursor.fetchall()
            result = [list(i) for i in result]
            self.commit()   

            columns = []            
            for col in self.cursor.description:
                columns.append(col[0])

            for x in range(len(columns)):
                self.user_info[columns[x]] = result[0][x]                    
            
            return self.user_info
        except sqlite3.Error as e:
            print("Something went wrong, either username or password is incorrect",e)
        finally:
            if self.connection:
                self.close()                

    def create(self):
        """create employees database if does not exist"""
        try:
            sql = '''CREATE TABLE IF NOT EXISTS employees
                        ([employee_id] INTEGER PRIMARY KEY AUTOINCREMENT,
                        [employee_name] TEXT,
                        [password] TEXT,
                        [position] TEXT,
                        [ssn] text,
                        [home_address] TEXT,
                        [email] TEXT,
                        [phone_number] TEXT,
                        [skills] TEXT)'''
            self.execute(sql)
            self.create_admin() # creates admin account
            print("Database created successfully")
        except sqlite3.Error as e:
            print("Database already exists", e)
        finally:
            if self.connection:
                self.close()
                print("Database closed successfully.")

    def delete_entry(self, **kwargs):
        """delete row(s) based on parameters"""
        try:
            sql = '''DELETE FROM employees WHERE employee_id = {};'''.format(kwargs['employee_id'])
            self.execute(sql)
            self.commit()
            print("Successfully removed entry")
        except sqlite3.Error as e:
            print("Database error deleting data", e)
        finally:
            if self.connection:
                self.close()

    def select(self, **kwargs):
        """select one row based on parameters/id"""
        try:
            sql = '''SELECT * FROM employees WHERE employee_id={};'''.format(kwargs['employee_id'])
            self.execute(sql)
            result = self.cursor.fetchall()
            self.commit()
            result = [list(i) for i in result]

            columns = []
            info = {}

            for col in self.cursor.description:
                columns.append(col[0])

            for x in range(len(columns)):
                info[columns[x]] = result[0][x]

            return info            
        except sqlite3.Error as e:
            print("Something went wrong retrieving employee data", e)

    def select_all(self, reverse=False):
        """select all columns and rows, return result"""
        
        if reverse:
            sql = '''SELECT * FROM employees ORDER BY employee_id DESC;'''
        else:
            sql = '''SELECT * FROM employees;'''
        try:            
            self.execute(sql)
            result = self.cursor.fetchall()            
            result = [list(i) for i in result]
            self.commit()   

            columns = []            
            employees = {}
            info = {}

            for col in self.cursor.description:
                columns.append(col[0])

            for x in range(len(columns)):
                for i in range(len(result)):
                    # make info dict multi-dimensional with setdefault
                    info.setdefault(result[i][0], {})[columns[x]] = result[i][x]
                    
            for i in range(len(result)):                
                employees[result[i][0]] = result[i]

            return info
        except sqlite3.Error as e:
            print("Something went wrong getting all employees from database", e)

    def create_admin(self):
        """creates admin account"""
        try:
            sql = '''INSERT OR IGNORE INTO employees 
                        ([employee_id], [employee_name],
                        [password],
                        [position], [ssn],
                        [home_address], [email],
                        [phone_number], [skills]) 
                    VALUES
                        (1, "admin", "123", "admin", "00-000-0000", "123 Forest View", "admin@forestview.com",
                        "(123)-456-7891", "admin\n")'''
            self.execute(sql)
            print("Created admin successfully")
            self.commit()
        except sqlite3.Error as e:
            print("Something went wrong creating admin",e)
        finally:
            if self.connection:
                self.close()
                print("Database closed successfully.")

    def update(self, data=None):        
        if data:
            print("DATRA", data)
            f = ['employee_id', 'employee_name', 'password', 
                  'position', 'ssn', 'home_address', 'email',
                  'phone_number', 'skills']
            try:
                sql ='''UPDATE 
                            employees 
                        SET 
                            "employee_name"='{}', "password"='{}',"position"='{}',
                            "ssn"='{}',"home_address"='{}',"email"='{}',
                            "phone_number"='{}',"skills"='{}'
                        WHERE "employee_id"='{}';'''.format(data[f[1]], data[f[2]], data[f[3]],
                                                       data[f[4]], data[f[5]], data[f[6]],
                                                       data[f[7]], data[f[8]], data[f[0]])
                self.execute(sql)
                self.commit()
                print("Updated rows successfully.")
            except sqlite3.Error as e:
                print("Something went wrong updating employees in database",e)
            finally:
                if self.connection:
                    self.close()
                    print("Database closed successfully")

    def insert(self, dict=None, **kwargs):
        if dict:
            try:
                sql = '''INSERT OR IGNORE INTO employees 
                            ([employee_id], [employee_name], [password],
                            [position], [ssn],
                            [home_address], [email],
                            [phone_number], [skills])
                        VALUES
                            (?, ?, ?, ?, ?, ?, ?, ?, ?)'''
                values = (dict['employee_id'],dict['employee_name'], dict['password'], 
                            dict['position'], dict['ssn'], dict['home_address'], 
                            dict['email'], dict['phone_number'], 
                            dict['skills'])
                self.execute(sql, values)
                print("Inserted into employee database successfully")
                self.commit()
            except sqlite3.Error as e:
                print("Something went wrong inserting into employee database",e)
            finally:
                if self.connection:
                    self.close()
                    print("Database closed successfully.")
        else:
            try:
                sql = '''INSERT OR IGNORE INTO employees 
                            ([employee_name], [password],
                            [position], [ssn],
                            [home_address], [email],
                            [phone_number], [skills])
                        VALUES
                            (?, ?, ?, ?, ?, ?, ?, ?)'''
                values = (kwargs['employee_name'], kwargs['password'], kwargs['position'],
                            kwargs['ssn'], kwargs['home_address'], kwargs['email'], 
                            kwargs['phone_number'], kwargs['skills'])
                self.execute(sql, values)
                print("Inserted into employee database successfully")
                self.commit()
            except sqlite3.Error as e:
                print("Something went wrong inserting into employee database",e)
            finally:
                if self.connection:
                    self.close()
                    print("Database closed successfully.")

    def get_table_names(self):
        """get all tables in the database"""
        try:
            sql = '''SELECT name FROM sqlite_master WHERE type='table';'''
            self.execute(sql)
            result = self.cursor.fetchall()
            print("DATABASE:",result)
        except sqlite3.Error as e:
            print("Something went wrong getting table names from database", e)
        finally:
            if self.connection:
                self.close()
                print("Database closed successfully")

    def execute(self, sql, values=None):
        """execute one row of data to current cursor"""
        if values:
            self.cursor.execute(sql, values) 
        else:
            self.cursor.execute(sql)

    def commit(self):
        """commit changes to database"""
        self.connection.commit()
        
    def close(self):
        """close database connection"""
        self.connection.close()

    def connect(self):
        try:
            connection = sqlite3.connect(Database.DB_LOCATION)
            return connection
        except sqlite3.Error as e:
            print("Something went wrong connecting to database.",e)
    
    def get_cursor(self):
        try:
            cursor = self.connection.cursor()
            return cursor
        except sqlite3.Error as e:
            print("Something went wrong getting cursor", e)
