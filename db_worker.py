import psycopg2


class db_worker:
    def __init__(self):
        self.conn = psycopg2.connect(database='pbz_lr2', user='dante', password='zqxwceasd')
        self.cursor = self.conn.cursor()

    def get_tables(self):
        self.cursor.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_schema NOT IN ('information_schema','pg_catalog');")
        return self.cursor.fetchall()

    def get_params_colums(self, name):
        text = "SELECT * FROM " + name + ';'
        self.cursor.execute(text)
        colnames = [desc[0] for desc in self.cursor.description]
        return [colnames, self.cursor.fetchall()]

    def change_data(self, const, changed, name):
        text = 'UPDATE ' + name + " SET " + changed[0] + "=" + '\'' + changed[1] + '\'' + " WHERE "
        for i in const:
            text += i[0] + '=' + '\'' + i[1] + '\'' + ' AND '
        text = text[:-4] + ';'
        self.cursor.execute(text)
        # self.conn.commit()
        print(text)

    def delete_data(self, data, name):
        text = 'DELETE FROM ' + name + " WHERE "
        for i in data:
            text += i[0] + '=' + '\'' + i[1] + '\'' + ' AND '
        text = text[:-4] + ';'
        self.cursor.execute(text)
        # self.conn.commit()

    def add_data(self, name, data):
        text = 'INSERT INTO ' + name + " VALUES ("
        for line in data:
            text += '\'' + line + '\', '
        text = text[:-2] + ');'
        self.cursor.execute(text)
        # self.conn.commit()

    def first_request(self):
        self.cursor.execute(
            'SELECT i.date,i.equipment_id,e.name,a.name FROM inspection i '
            'JOIN equipment e ON(e.ID=i.equipment_id) JOIN area a ON(a.ID = e.area_id) WHERE i.result = \'broken\';')
        return self.cursor.fetchall()

    def second_requset(self, string):
        req = 'SELECT i.date,i.equipment_id,e.name,i.result FROM inspection i JOIN equipment e ON(e.ID=i.equipment_id) WHERE i.equipment_id=\'' + str(
            string) + '\';'
        self.cursor.execute(req)
        return self.cursor.fetchall()

    def third_request(self, string):
        req = 'SELECT i.date,e.fio,i.result FROM inspection i JOIN employee e ON(e.ID=i.employee_id) WHERE i.date=\'' + str(
            string) + '\';'
        self.cursor.execute(req)
        return self.cursor.fetchall()
        pass

# cursor.execute('SELECT * FROM teacher;')
# for a in cursor:
#    print(a)
# colnames = [desc[0] for desc in cursor.description]
# print(colnames)
# информация о всех таблицах
# SELECT table_name FROM information_schema.tables
# WHERE table_schema NOT IN ('information_schema','pg_catalog');
# информация о полях одной таблицы
# select "column_name" from information_schema.columns
# where table_catalog = 'pbz_lr1' and
# table_schema = 'public' and
# table_name = 'teacher';
#
#
