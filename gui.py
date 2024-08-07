########################################################################################################################
###################################WELCOME TO FARIDO'S RESTAURANT#######################################################
###################################MADE BY SAED HAMAD###################################################################


from tkinter import *
from tkinter.ttk import *
from datetime import *
from tkinter.messagebox import *
from db import *
from scroll import Scroll
from itertools import chain
import random
from reportlab.pdfgen import canvas 
from datetime import *


# =======================================================================================================================
# =====================================================Functions=========================================================
# =======================================================================================================================

db = DBase()


def is_num(x):
    try:
        float(x)
    except:
        return False
    else:
        return True


def validate_cash(cash):
    if cash.isdigit():
        return int(cash) >= 0
    return not cash


def Exit(test=""):
    db.Exit_Data()
    win.destroy()


def Clear():
    print("clearing")
    #lb5.config(text="0")
    global rows, drink_rows, DATA, DRINKS
    del rows, drink_rows, DATA, DRINKS
    DATA = db.get_sandwiches()
    rows = order_tables(swin, DATA, 0.25, 0.2, 0.5, rel_h(DATA))
    DRINKS = db.get_drinks()
    drink_rows = order_tables(swin, DRINKS, 0.25, 0.55, 0.5, rel_h(DRINKS))
    if e1.get() == "":
        pass
    else:
        e1.delete(0, END)


def Calc(test=""):
    s = 0
    items = tuple(chain(rows, drink_rows))
    for i, rd in enumerate(items):
        # print(*(j.get() for j in rd))
        if not is_num(rd[1].get()) or not is_num(rd[2].get()):
            showerror("W a r n i n g", "Values must be Numeric")
            return
        c = int(rd[1].get()) * int(rd[2].get())
        s = s + c
        items[i][3].delete("0", END)
        items[i][3].insert(END, c)
    lb5.config(text=(str(s) + "$"))


def Save(test=""):
    items = tuple(chain(rows, drink_rows))
    for rd in items:
        if not is_num(rd[1].get()):
            showerror("W a r n i n g", "Price Must Be a Number")
            return "a"
        if not is_num(rd[2].get()):
            showerror("W a r n i n g", "Qtty Must Be a Number")
            return "a"
        if not int(rd[2].get()) == 0:
            x = (e1.get(), vd, rd[0].get(), rd[1].get(), rd[2].get())
            if e1.get() == "":
                showerror("W a r n i n g", "You Must fill a Number in Client Number")
                e1.focus()
                return
            rt = db.Save_Data(x)
    if rt == "b":
        Clear()


def Payment():
    def calcul(event):
        if int(entry_enter_cash_var.get()) < int(entry_total_amount_var.get()):
            showerror(
                "Hmm...!",
                "Please check if the entered cash = or > than the total amount",
            )
        elif int(entry_enter_cash_var.get()) >= int(entry_total_amount_var.get()):
            test = int(entry_enter_cash_var.get()) - int(entry_total_amount_var.get())
            ret_entry_var.set(test)
    global client_id
    client_id = e1.get()
    if client_id == "":
        return showwarning("Hmm...!", "Please enter a client number")
    else:
        win = Toplevel()
        win.geometry("750x550")
        win.title("Pay Cash")
        a = Label(win, text="Total Amount")
        a.place(x=450, y=380)
        b = Label(win, text="Enter Cash")
        b.place(x=450, y=420)
        c = Label(win, text="Return")
        c.place(x=450, y=460)

        fr1 = Frame(win)
        sb1 = Scrollbar(fr1)
        ls1 = Listbox(
            fr1, yscrollcommand=sb1.set, font=("courier", 10), width=80, height=15
        )

        sb1.config(command=ls1.yview)

        entry_total_amount_var = StringVar()

        DATA = db.select_me(client_id)

        try:
            assert DATA, "No Order placed"
        except AssertionError as e:
            win.destroy()
            return showwarning("Error", e)

        total = 0

        for row in DATA:
            test = row[4] * row[5]
            # print(test)
            s2 = "{:^9}{:^29}{:^15}{:^10}{:^10}".format(
                int(row[1]), row[3], row[4], row[5], test
            )
            ls1.insert(END, s2)
            total += test
            testt = test + 0
            # print(testt, total)
        entry_total_amount_var.set(str(total))
        # print(entry_total_amount_var.get())

        entry_total_amount = Entry(
            win,
            bd=2,
            textvariable=entry_total_amount_var,
            justify="center",
            state="readonly",
        )
        entry_total_amount.place(x=550, y=380)

        entry_enter_cash_var = StringVar()
        entry_enter_cash = Entry(
            win, bd=2, textvariable=entry_enter_cash_var, justify="center"
        )
        entry_enter_cash.place(x=550, y=420)
        entry_enter_cash.bind("<Return>", calcul)

        ret_entry_var = StringVar()
        ret_entry = Entry(
            win, bd=2, textvariable=ret_entry_var, justify="center", state="readonly"
        )
        ret_entry.place(x=550, y=460)

        y = ["ID", "Client_num", "Date", "Description", "Price", "Qtty", "Amount"]
        s1 = "{:^9}{:^30}{:^12}{:^12}{:^12}".format(y[1], y[3], y[4], y[5], y[6])
        text = Label(win, text=s1, bg="lightblue", font=("courier", 10))

        text.place(x=30, y=30)
        fr1.place(x=30, y=60)
        ls1.pack(side=LEFT)
        sb1.pack(side=LEFT, fill=Y)
        prnt = print_receipt(e1.get())
        btn = Button(win, text="Print Receipt", width=15, command=prnt)
        btn.place(x=520, y=500)
        win.mainloop()


def test() -> None:
    app = new_item()
    app.mainloop()
    win.quit()
    Clear()


def print_receipt(entry):
    # Creating Canvas
    c = canvas.Canvas("invoice.pdf", pagesize=(200, 250), bottomup=0)
    # Logo Section
    # Setting th origin to (10,40)
    c.translate(10, 40)
    # Inverting the scale for getting mirror Image of logo
    c.scale(1, -1)
    # Inserting Logo into the Canvas at required position
    c.drawImage("logo.png", 0, 0, width=50, height=30)
    # Title Section
    # Again Inverting Scale For strings insertion
    c.scale(1, -1)
    # Again Setting the origin back to (0,0) of top-left
    c.translate(-10, -40)
    # Setting the font for Name title of company
    c.setFont("Helvetica-Bold", 7)
    # Inserting the name of the company
    c.drawCentredString(125, 20, "Welcome To Farido's Restaurant")
    # For under lining the title
    c.line(70, 22, 180, 22)
    # Changing the font size for Specifying Address
    c.setFont("Helvetica-Bold", 5)
    c.drawCentredString(125, 30, "Beirut , Madine ryadiye")
    c.drawCentredString(125, 35, "Bir Hasan institute")
    # Changing the font size for Specifying GST Number of firm
    c.setFont("Helvetica-Bold", 4)
    ran = random.randint(111111111111111, 999999999999999)
    c.drawCentredString(125, 42, f"GSTIN : {ran}")
    # Line Seprating the page header from the body
    c.line(5, 45, 195, 45)
    # This Block Consist of Costumer Details
    c.roundRect(15, 50, 170, 40, 10, stroke=1, fill=0)
    c.setFont("Times-Bold", 5)
    test = random.randint(0, 99999)
    c.drawRightString(60, 58, "INVOICE No.  :")
    c.drawString(65, 58, f"{test}")
    c.drawRightString(60, 68, "DATE SUB.      :")
    dat = date.today()
    dat1 = dat.strftime("%Y-%m-%d")
    c.drawString(65, 68, f"{str(dat1)}")
    c.drawRightString(60, 78, "Cashier Name  :")
    c.drawString(65, 78, "Elie Hakim")
    c.drawRightString(60, 88, "PHONE No.     :")
    c.drawString(65, 88, "XXXXXXXXXXXX")
    # This Block Consist of Item Description
    c.roundRect(15, 108, 170, 130, 10, stroke=1, fill=0)
    c.line(15, 120, 185, 120)
    c.drawCentredString(25, 118, "Client")
    c.drawCentredString(75, 118, "Description")
    c.drawCentredString(125, 118, "Price")
    c.drawCentredString(148, 118, "Quantity")
    c.drawCentredString(173, 118, "TOTAL")
    DATA = db.select_me(entry)
    y = 129
    total = 0
    for row in DATA:
        entry = row[1]
        des = row[3]
        price = row[4]
        qtty = row[5]
        amount = row[4] * row[5]
        total += amount
        c.drawString(25, y, str(entry))  # client
        c.drawString(65, y, des)  # des
        c.drawString(120, y, str(price))  # price
        c.drawString(144, y, str(qtty))  # qtty
        c.drawString(168, y, str(amount))  # total
        y += 7
    c.drawString(168, 217, str(total))
    c.setFont("Times-Bold", 8)
    c.drawString(46, 232, "Welcome To Farido's Restaurant")
    # Drawing table for Item8 Description
    c.line(15, 210, 185, 210)
    c.line(35, 108, 35, 210)
    c.line(115, 108, 115, 210)
    c.line(135, 108, 135, 210)
    c.line(160, 108, 160, 220)
    # Declaration and Signature
    c.line(15, 220, 185, 220)
    c.setFont("Helvetica-Bold", 5)
    c.drawString(25, 217, "THANKS FOR COMING TO FARIDO'S RESTAURANT")
    # End the Page and Start with new
    c.showPage()
    # Saving the PDF
    c.save()


def on_select(tree):
    values = tree.item(tree.focus())["values"]
    print(values[1])


def search(entry):
    if entry == "":
            for row_name in DATA:
                name = row_name[1]
                print("HELLOOOOO", name)    
            else:
                db.search_item_admin(entry)

    

def admin():
        global tester
        win = Toplevel()
        win.geometry("750x450")
        win.title("Admin")
        a = Label(win, text="Item Name")
        a.place(x=50, y=350)

        fr1 = Frame(win)
        style = Style()
        style.theme_use("clam")
        
        columns = ["id", "item_name", "item_price"]

        tree = Treeview(win, columns=columns, show="headings")

        tree.heading("id", text="ID")
        tree.heading("item_name", text="Item Name")
        tree.heading("item_price", text="Item Price")

        tree.column("id", anchor="center",width=120)
        tree.column("item_name", anchor="center",width=300)
        tree.column("item_price", anchor="center",width=300)

        style.configure("Treeview.Heading", background="#6689EA", foreground="black")
        style.configure('Treeview', rowheight=30)

        tree.grid(row=0, column=2, sticky=NSEW)

        scrollbar = Scrollbar(win, orient=VERTICAL, command=tree.yview)
        tree.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=0, column=3, sticky=NS)


        DATA = db.select_admin()
        
        try:
            assert DATA, "No Data"
        except AssertionError as e:
            win.destroy()
            return showwarning("Error", e)

        for dt in DATA:
            tree.insert("", END, values=(dt[0], dt[1], dt[2]))
        
        total = 0
        
        search_entry_var = StringVar()
        search_entry = Entry(
            win,
            bd=2,
            justify="center",
            textvariable=search_entry_var
        )
        
        tree.bind('<<TreeviewSelect>>', lambda *e: on_select(tree))
        
        search_entry.place(x=150, y=350)
        
        x = lambda: search(search_entry_var.get())
        search_entry.bind("<Return>", lambda event: db.search_item_admin(x()))
       
        search_button = Button(win,text = 'Search', width=8, bd = 2, bg="#6689EA",command=x)
        search_button.place(x = 350, y = 350)
        
        add_button = Button(win,text="Add Item", width=8, bg="#6689EA",command=test)
        add_button.place(x = 450, y = 350)
        
        update_button = Button(win , text = "Edit",bg="#6689EA", width=8)
        update_button.place(x = 550, y = 350)
        
        delete_button = Button(win , text = "Delete",bg="red", width=8, command=lambda:db.delete_item(dt[1]))
        delete_button.place(x = 650,y = 350)
        
        fr1.place(x=30, y=60)
        
        win.mainloop()

def validate_login(username_entry, password_entry,form):
    userid = username_entry
    password = password_entry
    if userid == "admin" and password == "password":
        form.destroy()
        admin()
    else:
        showerror("Login Failed", "Invalid username or password")


def admin_register_form():
    parent = Tk()
    parent.eval('tk::PlaceWindow . center')
    parent.title("Login Form")
    parent.geometry("350x350")

        # Create and place the username label and entry
    username_label = Label(parent, text="Name :")
    username_label.place(relx=.5, rely=.2,anchor=CENTER)

    username_entry = Entry(parent)
    username_entry.place(relx=.5, rely=.3,anchor=CENTER)

            # Create and place the password label and entry
    password_label = Label(parent, text="Password:")
    password_label.place(relx=.5, rely=.4,anchor=CENTER)

    password_entry = Entry(parent, show="*")  # Show asterisks for password
    password_entry.place(relx=.5, rely=.5,anchor=CENTER)
    s = lambda:validate_login(username_entry.get(),password_entry.get(),parent)

    login_button = Button(parent, text="Login", command=s)
    login_button.place(relx=.5, rely=.6,anchor=CENTER)
    parent.mainloop()


def order_tables(
    root: Tk, data: list, rel_x: float, rel_y: float, rel_w: float, rel_h: float
) -> list:
    TableContainerFrame = Frame(win)
    TableContainerFrame.config(bg="white")
    TableContainerFrame.place(relx=rel_x, rely=rel_y, relwidth=rel_w, relheight=rel_h)
    tableTitle = Label(
        TableContainerFrame, text=s2, bg="#6689EA", font=("courier", 10)
    )
    tableTitle.place(x=0, y=0)
    scrollframe = Frame(TableContainerFrame)
    scrollframe.config(bg="white")
    scrollframe.place(x=0, y=20, relwidth=1, relheight=0.9)
    scrollReg = Scroll(scrollframe, "white", RIGHT)
    mainFrame = scrollReg.returnFrame()
    scrollReg.bindScrollAction()

    rows = []
    for i in range(len(data)):
        rd = data[i]
        cols = []
        for j in range(4):
            if j != 1 :
                e2 = Entry(mainFrame, relief=RIDGE)
                e2.grid(row=i, column=j)
                e2.insert(END, rd[j])
                cols.append(e2)
            else:
                e2 = Entry(mainFrame, relief=RIDGE) ## Hayda l Code Hooon
                e2.grid(row=i, column=j)
                e2.insert(END, rd[j])
                e2["state"]="readonly"
                cols.append(e2)
        rows.append(cols)

    return rows


# =======================================================================================================================
# =====================================================Variables=========================================================
# =======================================================================================================================


win = Tk()
win.title("M e n u")
width= win.winfo_screenwidth()               
height= win.winfo_screenheight()               
win.geometry("%dx%d" % (width, height))
win.overrideredirect(0)
p_scrollReg = Scroll(win)
p_scrollReg.bindScrollAction()

swin = p_scrollReg.returnFrame()







# buttona = Button(text="View all", command = viewall)
# buttona.place(x=150, y=620)

vd = date.today()
date1 = vd.strftime("%Y-%m-%d")
s1 = " FARIDO'S Restaurant Menu "
s2 = "{:^21}{:^22}{:^21}{:^21}".format("Description", "Price", "Qtty", "Amount")

lb1 = Label(win, text=s1, bg = "#D1D1D1",font=("courier", 18, "bold"))
lb2 = Label(win, text="Client No", bg = "#D1D1D1")
lb3 = Label(swin, text=s2, font=('courier', 10), bg = "#D1D1D1")
lb4 = Label(win, text="Total Amount", font=("Arial", 12, "bold"), bg = "#D1D1D1")
lb5 = Label(win, text="0$", width=14, relief=SUNKEN, font=("Arial", 10), bg = "#D1D1D1")
lb6 = Label(win, text="Date", bg = "#D1D1D1")
lb7 = Label(win, text=vd, relief=SUNKEN, bg = "#D1D1D1")
lb8 = Label(win, text="Sandwiches : ", fg="red", bg = "#D1D1D1")
l9 = Label(win, text="Drinks : ", fg="red", bg = "#D1D1D1")


b1 = Button(text="Clear", width=8,  bg="#6689EA",command=Clear)
b2 = Button(text="Claculate", width=8,  bg="#6689EA",command=Calc)
b3 = Button(text="Save", width=8, bg="#6689EA", command=Save)
b4 = Button(text="Pay cash", width=8, bg="#6689EA", command=Payment)
b5 = Button(text="Admin",width=8, bg="green", command=admin_register_form)


rel_h = lambda x: 0.038 * len(x) if len(x) < 8 else 0.3

DATA = db.get_sandwiches()
rows = order_tables(swin, DATA, 0.25, 0.2, 0.5, rel_h(DATA))
DRINKS = db.get_drinks()
drink_rows = order_tables(swin, DRINKS, 0.25, 0.55, 0.5, rel_h(DRINKS))
# disc_rows = order_tables(swin, DRINKS, 0.1, 0.8, 0.8, rel_h(DRINKS))

e1 = Entry()

menubar = Menu(win)

file = Menu(menubar, tearoff=False)
menubar.add_cascade(label="File", menu=file)
file.add_command(label="Clear", accelerator="Ctrl+R", command=Clear)
file.add_command(label="Calculate", accelerator="Shift+Ctrl+C", command=Calc)
file.add_command(label="Save", accelerator="Ctrl + S", command=Save)
file.add_separator()
file.add_command(label="Exit", accelerator="Alt + F4", command=Exit)
Restart = Clear
file.add_command(label="Restart App", accelerator="F5", command=Restart)
win.bind("<F5>", Restart)
win.config(menu=menubar)
win.bind("<Control-s>", Save)
win.bind("<Control-r>", Clear)
win.bind("<Control-C>", Calc)

copyright_symbol = "Reserved By Saed Hamad" 

lab = Label(text = copyright_symbol, fg = 'purple')

lb1.place(x=700, y=30,anchor="center")
lb2.place(x=50, y=80)
e1.place(x=120, y=78)
lb6.place(x=1060, y=80)
lb7.place(x=1100, y=80)
lb3.place(x=30, y=130)
lb4.place(x=1050, y=580)
lb5.place(x=1180, y=580)
lb8.place(x=650, y=109)
l9.place(x=650, y=345)
lab.place(x = 1100, y = 630)

# fr1.place(x=30, y=150)
b1.place(x=580, y=610)
b2.place(x=680, y=610)
b3.place(x=780, y=610)
b4.place(x=290, y=75)
b5.place(x=480, y=610)

win.protocol("WM_DELETE_WINDOW", Exit)

win.mainloop()

#==============================================NEW UPDATES SOON========================================================#
#==============================================Copyright Reserved======================================================#
#==============================================Saed Hamad==============================================================#
#Thanks#