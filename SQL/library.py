import pymysql

# TODO err: pymysql.err.OperationalError: (1142, "ALTER command denied to user 'pi'@'192.168.100.6' for table `exampledb`.`test`")


class _5G_SQL:

    def __debugPrint(self, txt):
        if self.isdebug:
            print(txt)

    def __init__(self, host, user, passwd, databaseName="", port=3306, debug=False):
        self.isdebug = debug
        self.__debugPrint("Debug Mods have been turned on!")
        try:
            self.__debugPrint("Connecting to Server...")
            self.conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db=databaseName)
            self.cursor = self.conn.cursor()
            self.__debugPrint("Server Connected, auth successful")
        except Exception as e:
            if "Connection refused" in str(e):
                raise ConnectionError("Connection refused")

    def close(self):
        self.conn.close()

    def getALL(self, tableName: str, orderBy: str = ""):
        # Check tableName class
        if tableName.__class__ is not str:
            raise TypeError("tableName must be a string")

        # Check orderBy class
        if orderBy.__class__ is not str:
            raise TypeError("order must be a string")
        elif orderBy == "":
            orderQuery = ""
        else:
            orderQuery = " ORDER BY " + orderBy

        # Execute SQL
        try:
            self.cursor.execute("SELECT * FROM " + tableName + orderQuery + ";")
            data = self.cursor.fetchall()
            self.__debugPrint(data)
            return data
        except pymysql.err.ProgrammingError as e:
            if "doesn't exist" in str(e):
                err = str(e)
                raise FileExistsError(err[err.rindex(",") + 3:-2])

    def getColumns(self, tableName: str, columnNames: list or str, orderBy: str = ""):
        # Check tableName class
        if tableName.__class__ is not str:
            raise TypeError("tableName must be a string")

        # Check columnNames class
        if columnNames.__class__ is list:
            for i in columnNames:
                if i.__class__ is not str:
                    raise TypeError("columnNames must be a list of string or string")
        elif columnNames.__class__ is not str:
            raise TypeError("columnNames must be a list of string or string, you have : " + str(columnNames.__class__))

        # Collect columnNames
        names = ""
        if columnNames.__class__ is list:
            for i in columnNames:
                names += i + ", "
            names = names[:-2]
        else:
            names = str(columnNames)

        # Check orderBy class
        if orderBy.__class__ is not str:
            raise TypeError("order must be a string")
        elif orderBy == "":
            orderQuery = ""
        else:
            orderQuery = " ORDER BY " + orderBy

        # Execute SQL
        self.cursor.execute("SELECT " + names + " FROM " + tableName + orderQuery + ";")
        data = self.cursor.fetchall()
        self.__debugPrint(data)
        return data

    def insert(self, tableName: str, columnNames: list, values: list):
        # Check tableName class
        if tableName.__class__ is not str:
            raise TypeError("tableName must be a string")

        # Check no of columnNames and values
        if len(columnNames) != len(values):
            raise ValueError("columnNames and values must have the same length")

        # Check columnNames class
        if columnNames.__class__ is not list:
            raise TypeError("columnNames must be a list of string")
        else:
            for i in columnNames:
                if i.__class__ is not str:
                    raise TypeError("columnNames must be a list of string")

        # Check values class
        if values.__class__ is not list:
            raise TypeError("values must be a list")

        # Collect columnNames
        names = ""
        for i in columnNames:
            names += i + ", "
        names = names[:-2]

        # Collect values
        vals = ""
        for i in values:
            if i.__class__ is str:
                vals = vals + "'" + i + "', "
            else:
                vals = vals + str(i) + ", "
        vals = vals[:-2]

        # Execute SQL
        self.cursor.execute("INSERT INTO " + tableName + " (" + names + ") VALUES (" + vals + ");")
        data = self.cursor.fetchall()
        self.__debugPrint(data)
        return data

    def addColumn(self, tableName: str, columnName: str, dataType: str):
        # Check tableName class
        if tableName.__class__ is not str:
            raise TypeError("tableName must be a string")

        # Check columnName class
        if columnName.__class__ is not str:
            raise TypeError("columnName must be a string")

        # Check dataType class
        if dataType.__class__ is not str:
            raise TypeError("dataType must be a string")

        # Execute SQL

        self.cursor.execute("ALTER TABLE " + tableName + " ADD COLUMN " + columnName + " " + dataType + " NOT NULL;")
        data = self.cursor.fetchall()
        self.__debugPrint(data)
        return data

    def updateData(self, tableName: str, setColumnNames: list, setValues: list,
                   whereColumnNames: list = None, whereData: list = None):
        # Check tableName class
        if tableName.__class__ is not str:
            raise TypeError("tableName must be a string")

        # Check no of columnNames and values
        if len(setColumnNames) != len(setValues):
            raise ValueError("columnNames and values must have the same length")

        if not((whereColumnNames is None) or (whereData is None)):
            if len(whereColumnNames) != len(whereData):
                raise ValueError("whereColumnNames and whereData must have the same length")

        # Check columnNames class
        if setColumnNames.__class__ is not list:
            raise TypeError("columnNames must be a list of string")
        else:
            for i in setColumnNames:
                if i.__class__ is not str:
                    raise TypeError("columnNames must be a list of string")

        # Check values class
        if setValues.__class__ is not list:
            raise TypeError("values must be a list")

        if not ((whereColumnNames is None) or (whereData is None)):
            # Check whereColumnNames class
            if whereColumnNames.__class__ is not list:
                raise TypeError("values must be a list of string")
            else:
                for i in whereColumnNames:
                    if i.__class__ is not str:
                        raise TypeError("columnNames must be a list of string")

            # Check data class
            if whereData.__class__ is not list:
                raise TypeError("values must be a list")

        # Collect columnNames and values
        setNames = ""
        for i in range(len(setColumnNames)):
            if setValues[i].__class__ is str:
                setNames = setNames + setColumnNames[i] + " = '" + setValues[i] + "', "
            else:
                setNames = setNames + setColumnNames[i] + " = " + str(setValues[i]) + ", "
        setNames = setNames[:-2]

        # Check where class
        if not ((whereColumnNames is None) or (whereData is None)):
            whereQuery = " WHERE "
            for i in range(len(whereColumnNames)):
                if whereData[i].__class__ is str:
                    whereQuery = whereQuery + whereColumnNames[i] + " = '" + whereData[i] + "' AND "
                else:
                    whereQuery = whereQuery + whereColumnNames[i] + " = " + str(whereData[i]) + " AND "
            whereQuery = whereQuery[:-5]
        else:
            whereQuery = ""

        # Execute SQL
        self.cursor.execute("UPDATE " + tableName + " SET " + setNames + whereQuery + ";")
        data = self.cursor.fetchall()
        self.__debugPrint(data)
        return data

    def deleteColumn(self, tableName: str, columnName: str):
        # Check tableName class
        if tableName.__class__ is not str:
            raise TypeError("tableName must be a string")

        # Check columnName class
        if columnName.__class__ is not str:
            raise TypeError("columnName must be a string")

        # Execute SQL
        self.cursor.execute("ALTER TABLE " + tableName + " DROP COLUMN " + columnName + ";")
        data = self.cursor.fetchall()
        self.__debugPrint(data)
        return data

    def clearTable(self, tableName: str):
        # Check tableName class
        if tableName.__class__ is not str:
            raise TypeError("tableName must be a string")

        # Execute SQL
        self.cursor.execute("DELETE FROM " + tableName + ";")
        data = self.cursor.fetchall()
        self.__debugPrint(data)
        return data

    def SQL_query(self, query: str):
        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            self.__debugPrint(result)
            return result
        except Exception as e:
            raise e