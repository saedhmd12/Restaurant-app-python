import mysql.connector
from tkinter import *
from datetime import *
from tkinter.messagebox import *

class DBase(object):
    cn = ''
    cr = ''

    def __init__(self):
        self.cn = mysql.connector.connect(host='localhost',
                                          database='RestFarid',
                                          user='phpmyadmin',
                                          password='Root1234!@#$')
        self.cr = self.cn.cursor()
        self.cr.execute('''create table IF NOT EXISTS drinks(
        id int AUTO_INCREMENT PRIMARY KEY,
        description varchar(100) UNIQUE,
        price int)''')
        
        self.cr.execute('''create table IF NOT EXISTS OrderF (
                        Id_Inc int auto_increment,
                        C_Num int,
                        R_Date date,
                        Descrip varchar(25),
                        Price int,
                        Qtty int,
                        primary key (Id_Inc)) ''')
        print("created")
        self.cn.commit()
        
        self.cr.execute('''create table IF NOT EXISTS admin(
            admin_id int AUTO_INCREMENT PRIMARY KEY,
            admin_name varchar(20),
            password varchar(50))''')
        
        self.stable_data = [
            ["Pepsi",5],
            ["Water",3],
            ["Juices",4],
            ["Boom Boom", 4],
            ["frappuccino",15],
            ["Americano", 12],
            ["Latte", 10],
            ["Mocha", 7],
            ["Irish", 14],
            ["Glace", 10],
            ["Amaretto", 8],
        ]
        try:
            for i in self.stable_data:
                sql = "INSERT INTO drinks (description, price) VALUES (%s, %s)"
                self.cr.execute(sql, i)
                print("inserted")
                self.cn.commit()
                print(i)
        except mysql.connector.errors.IntegrityError:
            pass

        self.cr.execute('''create table IF NOT EXISTS sandwiches(
                id int AUTO_INCREMENT PRIMARY KEY,
                description varchar(100) UNIQUE,
                price int)''')
        self.cn.commit()
        self.sandwiches = [['Kafta', 30],  # data inserted in the table
        ['Shawarma', 35,],
        ['Tabouleh', 15,],
        ['Steak', 50, ],
        ['Shrimp', 40,],
        ['Burger', 30,],
        ['Grilled Cheese', 25,],
        ['Turkey', 60, ],
        ['Roast Beef', 55, ],
        ['Tuna', 20, ],
        ['Bacon', 30,],
        ['Meatball', 23,],
        ['Club', 21,],
        ['Egg Salad', 18,],
        ['BLT', 60, ],
        ['Backed Bean', 10,],
        ['Beef on weck', 35,],
        ['Bratwurst', 30],
        ['Breakfast roll', 15],
        ['Dagwood', 120],
        ['Dynamite', 30],
        ]
        try:
            for i in self.sandwiches:
                sql = "INSERT INTO sandwiches (description, price) VALUES (%s, %s)"
                self.cr.execute(sql, i)
                self.cn.commit()
                print("inserted")
                print(i)
        except mysql.connector.errors.IntegrityError:
            return

    def Save_Data(self,x):
        sq = """insert into OrderF (C_Num, R_Date, Descrip, Price, Qtty) 
               values(%s, %s, %s, %s, %s) """
        self.cr.execute(sq, x)
        self.cn.commit()
        print("inserted")
        return "b"

    def select_me(self, num):
        vd = date.today()
        date1 = vd.strftime("%Y-%m-%d")
        sql1 = "Select * FROM OrderF Where (R_date=%s and C_Num=%s);"
        self.cr.execute(sql1, (str(date1), int(num)))
        result = self.cr.fetchall()
        print(result)
        return result

    def save_drinks(self, des, price):
        sql = """INSERT INTO drinks(description,price) values ('%s', %d)"""
        test = des
        test1 = price
        self.cr.execute(sql % (test, test1))
        self.cn.commit()

    def save_sandwiches(self, desc, price):
            sql = "INSERT INTO sandwiches(description,price) values ('%s', %d)"
            test = desc
            test1 = price
            self.cr.execute(sql % (test, test1))
            self.cn.commit()

    def get_drinks(self):
        self.cr.execute("SELECT description, price FROM drinks")
        test = self.cr.fetchall()
        data = []
        for self.i in test:
            data.append((*self.i, 0, 0))
        return data

    def get_sandwiches(self):
        self.cr.execute("SELECT description, price FROM sandwiches")
        test = self.cr.fetchall()
        data = []
        for i in test:
            data.append((*i, 0, 0))
        return data

    def select_admin(self):
        sql1 = "Select * FROM sandwiches UNION Select * from drinks;"
        self.cr.execute(sql1)
        result = self.cr.fetchall()
        return result

    def search_item_admin(self,name):
        sql1 = "Select description from sandwiches where (description = '%s');"
        self.cr.execute(sql1, (name,))
        result = self.cr.fetchall()
        print(result)
        return result
    
    def delete_item(self,item):
        sql = "select * from sandwiches"
        self.cr.execute(sql)
        result = self.cr.fetchall()
        for i in result[1]:
            if item:
                rest= askyesno("Sure??","Are you sure you want to delete?")
                if rest:
                    sql1 = "DELETE FROM sandwiches where description = %s"
                    self.cr.execute(sql1, [item])
                    self.cn.commit()
                    print("Sandwich deleted")
                    return
        else:
            sql = "select * from drinks"
            self.cr.execute(sql)
            result = self.cr.fetchall()
            for i in result[1]:
                if item:
                    rest= askyesno("Sure??","Are you sure you want to delete?")
                    if rest:
                        sql1 = "DELETE FROM drinks where description = %s"
                        self.cr.execute(sql1, [item])
                        self.cn.commit()
                        print("Drink deleted")
                        return

    def Exit_Data(self):
        self.cr.close()
        self.cn.close()


class new_item(Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.geometry("350x250")
        self.title("Add Item")

        des = Label(self, text="Description")
        des.place(x=10, y=50)

        price = Label(self, text="Price")
        price.place(x=10, y=90)

        category = Label(self, text="Category")
        category.place(x=10, y=130)

        menu_item_validator = self.register(self.validate_item)
        price_validator = self.register(self.validate_price)
        self.entry1_var = StringVar()
        self.entry1 = Entry(
            self,
            bd=3,
            textvariable=self.entry1_var,
            validatecommand=(menu_item_validator, "%P"),
            validate="key",
        )
        self.entry1.place(x=100, y=50)
        self.entry2_var = StringVar()
        self.entry2 = Entry(
            self,
            bd=3,
            textvariable=self.entry2_var,
            validate="key",
            validatecommand=(price_validator, "%P"),
        )
        self.entry2.place(x=100, y=90)

        choices = ("Sandwich", "Drinks")
        self.choice = StringVar(self)
        self.choice.set(choices[0])
        self.popupMenu = OptionMenu(self, self.choice, *choices)
        self.popupMenu.place(x=100, y=130)
        button = Button(self, text="Add", width=10,bg="#6689EA", command=self.on_btn)
        button.place(x=130, y=200)

    def on_btn(self):
        desc = self.entry1.get()
        price = int(self.entry2.get())
        cat = self.choice.get()
        print(f"Description: {desc}, Price: {price}, Category: {cat}")
        db = DBase()
        if cat == "Drinks":
            print(price)
            db.save_drinks(desc, price)
        else:
           db.save_sandwiches(desc, price)
        self.destroy()

    def validate_item(self, x: str) -> bool:
        print(x)
        return x.replace(" ", "").isalpha() or x == ""

    def validate_price(self, x: str) -> bool:
        print(x)
        return x.isdigit() or x == ""
print("Hello")


