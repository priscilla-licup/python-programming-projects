from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from datetime import date
import os
import csv
from reportlab.pdfgen import canvas


at=False
dotcom=False
bemail=False
bbday=False
inc=False
minor=False

infos = [['ID', 'Name','Address', 'Contact', 'Email', 'Bday', 'Gender']]
ID = []
r=0

z=0
table1 = [['ID', 'PType','PDesc', 'Supplier', 'Total Quantity', 'Orders']]
table2 = [[['ID','PType', 'PDesc','Supplier' ,'Quantity', 'Cost', 'Date Rec', 'Orders']]]

order = [[['Invoice No.','PID','PType','PDesc','Quantity','Unit Price','Date Rec',0]]]
for a in range(10):
    order.append([])
aid = 0
arow = 0
up = 0

def save():
    global inc
    global minor
    
    if len(custname.get())==0 or len(custemail.get())==0 or len(custcon.get())==0 or len(custad.get())==0 or len(custbday.get())==0:
       msgbox("Incomplete", "Record")
       inc=True
    if bemail==True:
        msgbox("Bad Email Format", "Record")

    if bbday==True:
        msgbox("Wrong Birthday Format", "Record")
        print("bra")

    mon = custbday.get() [0:2]
    day = custbday.get() [3:5]
    year = custbday.get() [6:10]
    length=len(custbday.get())

    m = int(mon)
    d = int(day)
    y = int(year)

    birth = date(y, m, d)

    age = count (birth)
    a = int(age)

    if a<18:
        msgbox("Minors are not allowed.", "Record")
        minor=True
    
    if inc==False and bemail==False and minor==False and bbday==False:
        msgbox("Save Record!!", "Record")

        ID.sort()

        if custid.get() in ID:
            mID()
        
        ID.append(custid.get())
            
        infos.append([custid.get(),cname.get(),cad.get(),ccon.get(),cemail.get(),cbday.get(),custgen.get()])
        createtable()
        mID()

        writecsvC()
       
def mID():
    a = 1
    for b in ID:
        if int(b) != a:
            cid.set(a)
            break
        elif a  == len(ID):
            cid.set(a+1)
        a += 1
    
        

def keyup (e):
    global at
    global dotcom
    global bemail
    for x in range(len(custemail.get())):
        if custemail.get() [-1] == "@" and x>1:
            at=True
        else:
            labelemail.config (text="Bad Email")
            bemail=True
        if x>4 and custemail.get() [-4:] == ".com" and at==True:
            dotcom=True
        else:
            labelemail.config (text="Bad Email")
            bemail=True
        if at==True and dotcom==True:
            labelemail.config (text="Good Email")
            bemail=False
        else:
            labelemail.config (text="Bad Email")
            bemail=True

def count (bday):
    today = date.today() 
    age = today.year - bday.year - ((today.month, today.day) < (bday.month, bday.day))
    return age


def keyday (e):
    global bbday
    try:
        mon = custbday.get() [0:2]
        day = custbday.get() [3:5]
        year = custbday.get() [6:10]
        length=len(custbday.get())

        m = int(mon)
        d = int(day)
        y = int(year)
        print (y,m,d)
        
        birth = date(y, m, d)
        print (birth)

        age = count (birth)
        print (age)
        a = int(age)
        print (length)

        if a<18:
            labelbday.config (text="Minor")
            
            print("age")
        else:
            labelbday.config (text="Good Format")
            bbday=False
            print("all good")

    except:
        labelbday.config (text="Wrong Format")
        bbday=True
        print("ex")


def delete():
    ID.remove(custid.get())
    #del(ID[int(custid.get())])
    del(infos[r])
    createtable()
    a = tbl.grid_slaves(row=len(infos))
    for z in a:
        z.destroy()
    mID()

def update():
    infos[r]=[custid.get(),custname.get(),custad.get(),custcon.get(),custemail.get(),custbday.get(),custgen.get()]
    createtable()

def callback (event):
    global r
    r=event.widget._values
    for x in ntbl.grid_slaves():
        x.destroy()
    createtable0()
    shord()

    cid.set(infos[event.widget._values][0])
    cname.set(infos[event.widget._values][1])
    cad.set(infos[event.widget._values][2])
    ccon.set(infos[event.widget._values][3])
    cemail.set(infos[event.widget._values][4])
    cbday.set(infos[event.widget._values][5])
    if (infos[event.widget._values][6]=="Male"):
        custgen.current(0)
    elif (infos[event.widget._values][6]=="Female"):
        custgen.current(1)
    else:
        custgen.set(' ')

def createtable ():
    ID.sort()
    for i in range(len(infos)):
        for j in range (len(infos[0])):
            mgrid = Entry(tbl, width=10,bg='yellow')
            mgrid.insert (END,infos[i][j])
            mgrid._values=i
            mgrid.grid (row=i, column=j)
            mgrid.bind("<Button-1>",callback)

def createtable0 ():
    for j in range(7):
            mgrid = Entry(ntbl, width=11, bg = '#66CCCC')  
            mgrid.insert(END,order[0][0][j])
            mgrid.grid(row=0,column=j)

def shord():
    for i in range(len(order[int(custid.get())])):
        for j in range(7):               
            mgrid = Entry(ntbl, width=11, bg = '#66CCCC')
            mgrid.insert(END,order[int(custid.get())][i][j])
            mgrid.grid(row=i+1,column=j)

def addord():
    global aid
    global arow
    global up
    a = int(custid.get())

    b = []
    b.append(100 + a) # invoice 0
    b.append(table2[aid][arow][0]) # pid    1
    b.append(table2[aid][arow][1]) # ptype  2
    b.append(table2[aid][arow][2]) # pdes   3
    b.append(1)                     # q      4
    b.append(up)                    # up     5
    b.append(date.today())          # date   6 
    b.append((a*100)+(aid*10)+arow)       # identity 7
    
    if len(order[a]) == 0:
        order[a].append(b)
        qna()
        print('initial')
    else:
        for x in range(len(order[a])): #x represents index
            if b[7] == order[a][x][7]:
                order[a][x][4]= order[a][x][4]+1
                qna()
                print('add q!!!!!')
                break
            elif x == len(order[a])-1:
                order[a].append(b)
                qna()
                print('new!!!!!')
                break
    shord()
    writecsvO()

def qna():
    table2[aid][arow][4] = int(table2[aid][arow][4])-1 #minus qqt in stock
    table2[aid][arow][7] = int(table2[aid][arow][7])+1  #add orders in stock
    table1[int(table2[aid][arow][0])][5] = int(table1[int(table2[aid][arow][0])][5])+1   #add orders in products
        
def msgbox(msg,titlebar):
    messagebox.showinfo (title=titlebar, message=msg)

def writecsvC():
    with open ('customerspy.csv','w', newline='') as file:
        write = csv.writer(file)
        write.writerows(infos)

def readcsvC():
    try:
        with open ('customerspy.csv','r') as file:
            reader = csv.reader(file)
            mylist = list(reader)
        return mylist
    except:
        print ("no file to read csv cust")
        return False

def writecsvO():
    yes = []
    for i in order:
        for j in i:
            yes.append(j)

    with open ('orderspy.csv','w',newline='') as file:
        write = csv.writer(file)
        write.writerows(yes)

def readcsvO():
    try:
        with open ('orderspy.csv','r') as file:
            reader = csv.reader(file)
            mylist = list(reader)
        return mylist
    except:
        print ("no file to read csv orders")
        return False

def invoice():
    c = canvas.Canvas("invoice.pdf")
    id = int(custid.get())

    c.setFont('Helvetica-Bold',20)
    c.drawString(150,800,"Computer Programming Store")
    c.line(70,770,530,770)
    
    c.setFont('Helvetica-Bold',14)
    c.drawString(70,750, "Bill To:")
    c.setFont('Helvetica',13)
    c.drawString(70,730, infos[id][1])
    c.drawString(70,710, infos[id][2])
    c.drawString(70,690, infos[id][3])
    
    c.setFont('Helvetica-Bold',14)
    c.drawString(420,750, "Invoice")
    c.setFont('Helvetica',13)
    c.drawString(420,730, "Date: " + str(date.today()))
    c.drawString(420,710, "Invoice: " + str(id+100))
    c.drawString(420,690, "Customer ID: " + custid.get()) 
    
    c.line(70,670,530,670)

    c.setFont('Helvetica-Bold',14)
    c.drawString(100,650, "Product/Description")
    c.drawString(300,650, "Quantity")
    c.drawString(420,650, "Unit Price")
    c.line(70,630,530,630)
    
    st = 0
    y = 610
    c.setFont('Helvetica',13)
    for x in range(len(order[id])):
        c.drawString(70,y,order[id][x][2] + "   " + order[id][x][3])
        c.drawString(320,y,str(order[id][x][4]))
        c.drawString(425,y,str(order[id][x][5]))
        st += float(order[id][x][4])*float(order[id][x][5])
        y -= 20
    c.line(70,y,530,y)

    c.setFont('Helvetica-Bold',13)
    c.drawString(300,y-20, "Sub Total: P" + str(st))
    c.drawString(300,y-40, "Tax 12%: P" + str(round(st*0.12,2))) #round(n,2)
    c.drawString(300,y-60, "Total: P" + str(round(st*1.12,2)))

    c.save()
    os.startfile("invoice.pdf")


def products():
    def addprod():
        global z
        pid.set(len(table1))
        z = int(prodid.get())
        table1.append([prodid.get(),prodty.get(),proddes.get(), supp.get(),quan.get(),"0"])
        createtable1()
        table2.append([])
        table2[z].append([prodid.get(),prodty.get(),proddes.get(),supp.get(),quan.get(),totcos.get(),daterec.get(),0])

        writecsvprod()
        writecsvsto()
        
    def stockin():
        global z
        z = int(prodid.get())
        table2.append([])
        table2[z].append([prodid.get(),prodty.get(),proddes.get(),supp.get(),addquan.get(),totcos.get(),daterec.get(),0])
        table1[z][4]= str(int(table1[z][4])+int(addquan.get()))
        createtable1()
        showlist()

        writecsvsto()

    def callback(event):
        global z
        z=event.widget._values
        for x in tbl2.grid_slaves():
            x.destroy()
        createtable2()
        showlist()

        writecsvprod()
        writecsvsto()

        w = tbl1.grid_slaves(column=5) #update orders in prod table
        z = len(table1)-1
        for y in range(len(table1)):
            w[z].delete(0,END)
            w[z].insert(0,table1[y][5])
            z -= 1
        
        pid.set(table1[event.widget._values][0])
        ptype.set(table1[event.widget._values][1])
        pdesc.set(table1[event.widget._values][2])
        sp.set(table1[event.widget._values][3])
        qn.set(table1[event.widget._values][4])
        aq.set("")
        tc.set("")

    def tableclick(event):
        global aid
        global arow
        global up
        aid = event.widget.why
        arow = event.widget.bee
        up = (int(table2[aid][arow][5])/(int(table2[aid][arow][4])+int(table2[aid][arow][7])))+int(labcos.get())+int(ovcos.get())+int(desprof.get())

    def createtable1 ():
        for i in range(len(table1)):
            for j in range (len(table1[0])):
                mgrid = Entry(tbl1, width=10,bg='yellow')
                mgrid.insert (END,table1[i][j])
                mgrid._values=i
                mgrid.grid (row=i, column=j)
                mgrid.bind("<Button-1>",callback)

    def createtable2 ():
        for j in range(len(table2[0][0])):
                mgrid = Entry(tbl2, width=11, bg = 'yellow')
                mgrid.insert(END,table2[0][0][j])
                mgrid.grid(row=0,column=j)

    def showlist():
        global z
        for i in range(len(table2[z])):
            for j in range(8):
                mgrid = Entry(tbl2, width=11, bg = 'yellow')
                mgrid.insert(END,table2[z][i][j])
                mgrid.why=z
                mgrid.bee=i
                mgrid.grid(row=i+1,column=j)
                mgrid.bind("<Button-1>",tableclick)

    def writecsvprod():
        with open ('productspy.csv','w',newline='') as file:
            write = csv.writer(file)
            write.writerows(table1)

    def readcsvprod():
        try:
            with open ('productspy.csv','r') as file:
                reader = csv.reader(file)
                mylist = list(reader)
            return mylist
        except:
            print("no file to read csv prod")
            return False

    def writecsvsto():
        yes = []
        for i in table2:
            for j in i:
                yes.append(j)
        with open ('stockspy.csv','w',newline='') as file:
            write = csv.writer(file)
            write.writerows(yes)

    def readcsvsto():
        try:
            with open('stockspy.csv','r') as file:
                reader = csv.reader(file)
                mylist = list(reader)
            yes = [[]]
            x = mylist[0][0]
            y = 0
            for i in mylist:
                if (x == i[0]):
                    yes[y].append(i)
                else:
                    x = i[0]
                    y += 1
                    yes.append([])
                    yes[y].append(i)
            return yes
        except:
            print ("no file to read csv stock")
            return False

    def writecsvcost(x,y,z):
        yes = [[x],[y],[z]]
        with open ('costspy.csv','w',newline='') as file:
            write = csv.writer(file)
            write.writerows(yes)

    def readcsvcost():
        yes = ["0","0","0"]
        try:
            with open('costspy.csv','r') as file:
                reader = csv.reader(file)
                mylist = list(reader)
            return mylist
        except:
            print("no file to read csv LOD")
            return yes


    window2 = Tk()
    window2.title ("Products Form")
    window2.geometry ("550x400")
    window2.configure (bg="orange")

    label = Label(window2, text="New Products Stock-In", width=25, height=1, bg="yellow")
    label.grid (column=2, row=1)

    tbl1 = Frame(window2)
    tbl1.grid(row=2, rowspan=8, column=5, sticky=N)

    tbl2 = Frame(window2)
    tbl2.grid(row=10, rowspan=5, column=5, sticky=N)

    
    label = Label(window2, text="Product ID", width=12, height=1, bg="yellow")
    label.grid (column=1, row=2)
    pid = StringVar(window2)
    prodid = Entry(window2, textvariable=pid)
    prodid.config(state='readonly')
    prodid.grid (column=2, row=2)
    pid.set("1")
    
    label = Label(window2, text="Product Type", width=14, height=1, bg="yellow")
    label.grid (column=1, row=3)
    prodty = Entry(window2)
    ptype = StringVar(window2)
    prodty.grid (column=2, row=3)

    label = Label(window2, text="Product Description", width=21, height=1, bg="yellow")
    label.grid (column=1, row=4)
    proddes = Entry(window2)
    pdesc = StringVar(window2)
    proddes.grid (column=2, row=4)

    label = Label(window2, text="Supplier", width=10, height=1, bg="yellow")
    label.grid (column=1, row=5)
    supp = Entry(window2)
    sp = StringVar(window2)
    supp.grid (column=2, row=5)

    label = Label(window2, text="Quantity", width=5, height=1, bg="yellow")
    label.grid (column=1, row=7)
    quan = Entry(window2)
    qn = StringVar(window2)
    quan.grid (column=2, row=7)
    label = Label(window2, text="+", width=2, height="1", bg="white")
    label.grid(column=3,row=7)
    aq = StringVar(window2)
    addquan = Entry(window2,width=5, textvariable=aq)
    addquan.grid(column=4, row=7)

    label = Label(window2, text="Total Cost", width=12, height=1, bg="yellow")
    label.grid (column=1, row=8)
    totcos = Entry(window2)
    tc = StringVar(window2)
    totcos.grid (column=2, row=8)

    label = Label(window2, text="Date Received", width=15, height=1, bg="yellow")
    label.grid (column=1, row=9)
    dr = StringVar(window2)
    daterec = Entry(window2, textvariable=dr)
    daterec.config(state='readonly')
    daterec.grid (column=2, row=9)
    dr.set(str(date.today()))

    label =  Label(window2, text="Labor Cost:", width=15, height="1", bg="white")
    label.grid(column=2,row=11)
    lc = StringVar(window2)
    labcos = Entry(window2,width=10, textvariable=lc)
    labcos.grid(column=3, row=11, sticky=W)
    lc.set(readcsvcost()[0])

    label =  Label(window2, text="Overhead Cost:", width=15, height="1", bg="white")
    label.grid(column=2,row=12,)
    oc = StringVar(window2)
    ovcos = Entry(window2, width=10, textvariable=oc)
    ovcos.grid(column=3, row=12, sticky=W)
    oc.set(readcsvcost()[1])

    label =  Label(window2, text="Desired Profit:", width=15, height="1", bg="white")
    label.grid(column=2,row=13)
    dp = StringVar(window2)
    desprof = Entry(window2, width=10, textvariable=dp)
    desprof.grid(column=3, row=13, sticky=W)
    dp.set(readcsvcost()[2])

    cb = Button(window2, text = "Save", command= lambda: writecsvcost(labcos.get(),ovcos.get(),desprof.get()))
    cb.grid(column=4,row=13, sticky=W)

    sb = Button (window2,text="New Product", command = addprod)
    sb.grid (column=1, row=10)
    eb = Button (window2,text="Stock In", command=stockin)
    eb.grid (column=2, row=10)

    if(readcsvprod()):
        for i in range(1, len(readcsvprod())):
            table1.append(readcsvprod()[i])
    if(readcsvsto()):
        for i in range(1, len(readcsvsto())):
            table2.append(readcsvsto()[i])

    createtable1()
    createtable2()
        
window = Tk()
window.title ("Customer Recording System")
window.geometry ("550x400")
window.configure (bg="orange")

menubar = Menu(window)
filemenu = Menu(menubar, tearoff=0)
editmenu = Menu(menubar, tearoff=0)
menubar.add_cascade (label="File", menu=filemenu)
menubar.add_cascade (label="Edit", menu=editmenu)
filemenu.add_command (label="Products", command=products)
filemenu.add_command (label="Orders", command=products)
filemenu.add_separator()
filemenu.add_command (label="Close", command=window.quit)
window.config(menu=menubar)

label = Label(window, text="Customer Registration System", width=30, height=1, bg="yellow")
label.grid (column=2, row=1)

tbl = Frame(window)
tbl.grid (row=2, rowspan=7, column=4, sticky=N)

ntbl = Frame(window) 
ntbl.grid(row=9, rowspan=6, column=4,sticky=N)

label = Label(window, text="Customer ID:", width=10, height=1, bg="yellow")
label.grid (column=1, row=2)
cid = StringVar() 
custid = Entry(window, textvariable=cid)
custid.config (state='readonly')
custid.grid (column=2, row=2)
cid.set("1")

label = Label(window, text="Customer Name:", width=15, height=1, bg="yellow")
label.grid (column=1, row=3)
cname = StringVar()
custname = Entry(window, textvariable=cname)
custname.grid (column=2, row=3)
label = Label(window, text="Lastname, Firstname", width=21, height=1, bg="yellow")
label.grid (column=3, row=3)

label = Label(window, text="Customer Address:", width=18, height=1, bg="yellow")
label.grid (column=1, row=4)
cad = StringVar()
custad = Entry(window, textvariable=cad)
custad.grid (column=2, row=4)

label = Label(window, text="Customer Contact #:", width=20, height=1, bg="yellow")
label.grid (column=1, row=5)
ccon = StringVar()
custcon = Entry(window, textvariable=ccon)
custcon.grid (column=2, row=5)

label = Label(window, text="Customer Email:", width=15, height=1, bg="yellow")
label.grid (column=1, row=6)
cemail = StringVar()
custemail = Entry(window, textvariable=cemail)
custemail.grid (column=2, row=6)
custemail.bind ("<KeyRelease>", keyup)
labelemail = Label(window, text="[a-z]@[a-z].com", width=15, height=1, bg="yellow")
labelemail.grid (column=3, row=6)

label = Label(window, text="Customer Bday:", width=15, height=1, bg="yellow")
label.grid (column=1, row=7)
cbday = StringVar()
custbday = Entry(window, textvariable=cbday)
custbday.grid (column=2, row=7)
custbday.bind ("<KeyRelease>", keyday)
labelbday = Label(window, text="mm/dd/yyyy", width=12, height=1, bg="yellow")
labelbday.grid (column=3, row=7)

label = Label(window, text="Customer Gender:", width=17, height=1, bg="yellow")
label.grid (column=1, row=8)
custgen = ttk.Combobox(window, width = 8)
custgen['values'] = ('Male','Female')
custgen.grid(column = 2, row = 8)
custgen.current()

savebtn = Button (text="Save", command=save)
savebtn.grid (column=1, row=9)
savebtn2 = Button (text="Delete", command=delete)
savebtn2.grid (column=1, row=10)
savebtn3 = Button (text="Update", command=update)
savebtn3.grid (column=1, row=11)

aord = Button(window, text = "Add Order", width=15, command=addord)
aord.grid(column=3,row=9)
inv = Button(window, text = "Invoice", width=15, command=invoice)
inv.grid(column=2,row=10)

if(readcsvC()):
    for i in range(1, len(readcsvC())):
        infos.append(readcsvC()[i])
        ID.append(readcsvC()[i][0])
ids = 0
if(readcsvO()):
    for i in readcsvO():
        if(int(int(i[7])/100) == 0):
            continue
        elif(ids == int(int(i[7])/100)):
            order[ids].append(i) 
        else:
            ids = int(int(i[7])/100)
            order[ids].append(i)


createtable()
createtable0()
window.mainloop()

