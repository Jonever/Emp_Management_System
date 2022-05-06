from tkinter import *
from tkinter import ttk
import pymysql
import tkinter.messagebox
import time
from datetime import datetime
import random
from string import digits


class DataEntryForm:
    def __init__(self, root):
        self.root = root
        self.root.geometry("1350x800+0+0")
        self.root.configure(bg="#34568B")

        Firstname = StringVar()
        Surname = StringVar()
        Address = StringVar()
        Telephone = StringVar()
        RegDate = StringVar()
        WorkType = StringVar()
        WorkStatus = StringVar()
        Salary = StringVar()
        Search = StringVar()
        DateToDay = StringVar()

        UpperFrame = Frame(self.root, width=1350, height=70, bg="#34568B", relief=RIDGE)
        UpperFrame.grid()
        Label(UpperFrame, text="JONSOFT EMPLOYEE MANAGEMENT", fg="white", font=('font', 30, 'bold'),
              bg="#34568B").place(x=290, y=5)

        MainFrame = Frame(self.root, width=1350, height=700, relief=RIDGE)
        MainFrame.grid()

        TopFrame1 = Frame(MainFrame, bd=1, width=1370, height=200, relief=RIDGE)
        TopFrame1.grid(row=0, column=0)

        TopFrame2 = Frame(MainFrame, bg="#bf96fa", bd=1, width=1370, height=50, relief=RIDGE)
        TopFrame2.grid(row=1, column=0)

        TopFrame3 = Frame(MainFrame, bg="#cbadf7", bd=1, width=1370, height=300, relief=RIDGE)
        TopFrame3.grid(row=2, column=0)

        InnerTopFrame1 = Frame(TopFrame1, bd=1, width=1370, height=190, relief=RIDGE)
        InnerTopFrame1.grid()

        InnerTopFrame2 = Frame(TopFrame2, bd=1, width=1370, height=480, relief=RIDGE)
        InnerTopFrame2.grid()

        InnerTopFrame3 = Frame(TopFrame3, bg="#cbadf7", bd=1, width=1370, height=280, relief=RIDGE)
        InnerTopFrame3.grid()

        UpperFrame = Frame(self.root, width=1350, height=70, bg="#34568B", relief=RIDGE)
        UpperFrame.grid()
        Label(UpperFrame, text="DEVELOPER: JON BRAYDEN CODES-v1.1", fg="white", font=('font', 6, 'bold'),
              bg="#34568B").place(x=1100, y=2)

        RegDate.set(time.strftime("%d/%m/%y"))
        DateToDay.set(time.strftime("%d/%m/%y"))

        def Reset():
            txtReference.delete(0, END)
            txtFirstname.delete(0, END)
            txtLastName.delete(0, END)
            txtAddress.delete(0, END)
            txtTelephone.delete(0, END)
            # RegDate.set("")
            WorkType.set("")
            WorkStatus.set("")
            Salary.set("")

            RegDate.set(time.strftime("%m/%d/%y"))
            DateToDay.set(time.strftime("%m/%d/%y"))

        def iExit():
            iExit = tkinter.messagebox.askyesno("Employee Data Management", "You really want to exit?")
            if iExit > 0:
                root.destroy()
                return

        def addData():
            Generated_RefNo = get_refID()
            if Surname.get() == "" or Address.get() == "" or Telephone.get() == "":
                tkinter.messagebox.showerror("Employee Data Management", "Fill all fields.")

            else:
                sqlCon = pymysql.connect(host="localhost", user="root", password="qwert", database="employee_data")
                cur = sqlCon.cursor()
                cur.execute("INSERT INTO record_management values (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (
                    Generated_RefNo,
                    Firstname.get(),
                    Surname.get(),
                    Address.get(),
                    Telephone.get(),
                    RegDate.get(),
                    WorkType.get(),
                    WorkStatus.get(),
                    Salary.get()
                ))

                sqlCon.commit()
                DisplayData()
                sqlCon.close()
                tkinter.messagebox.showinfo("Employee Data Management", "Data Saved Successfully")
                txtReference.insert(0, Generated_RefNo)

        def get_refID():
            symbol = digits
            secure_random = random.SystemRandom()
            return datetime.now().strftime('%d%m%y').join(secure_random.choice(symbol) for i in range(2))

        RefNo = get_refID()

        def DisplayData():
            sqlCon = pymysql.connect(host="localhost", user="root", password="qwert", database="employee_data")
            cur = sqlCon.cursor()
            cur.execute("SELECT * FROM record_management")
            result = cur.fetchall()
            if len(result) != 0:
                tree_records.delete(*tree_records.get_children())
                for row in result:
                    tree_records.insert('', END, values=row)
                    sqlCon.commit()
                sqlCon.close()
            else:
                tkinter.messagebox.showwarning("Employee Data Management", "No records yet.")

        def update():
            if txtReference.get() == "" or txtFirstname.get() == "" or txtLastName.get() == "" \
                    or txtAddress.get() == "" or txtTelephone.get() == "":
                tkinter.messagebox.showerror("Employee Data Management", "Unknown Records.")

            else:
                sqlCon = pymysql.connect(host="localhost", user="root", password="qwert", database="employee_data")
                cur = sqlCon.cursor()
                cur.execute("update record_management set Firstname = %s, Surname = %s, Address=%s, Telephone = %s,"
                            "RegDate = %s, WorkType = %s, WorkStatus = %s, Salary = %s where RefNo = %s",
                            (
                                Firstname.get(),
                                Surname.get(),
                                Address.get(),
                                Telephone.get(),
                                RegDate.get(),
                                WorkType.get(),
                                WorkStatus.get(),
                                Salary.get(),
                                txtReference.get()
                            ))

                sqlCon.commit()
                DisplayData()
                sqlCon.close()
                tkinter.messagebox.showinfo("Employee Data Management", "Data Successfully Updated")

        def delete():
            if txtReference.get() == "":
                tkinter.messagebox.showerror("Employee Data Management", "Reference Number Required.")

            else:
                sqlCon = pymysql.connect(host="localhost", user="root", password="qwert", database="employee_data")
                cur = sqlCon.cursor()
                cur.execute("delete from record_management where RefNo = %s", txtReference.get())

                sqlCon.commit()
                DisplayData()
                sqlCon.close()
                tkinter.messagebox.showinfo("Employee Data Management", "Data Successfully Deleted")

            txtReference.delete(0, END)
            txtFirstname.delete(0, END)
            txtLastName.delete(0, END)
            txtAddress.delete(0, END)
            txtTelephone.delete(0, END)
            RegDate.set("")
            WorkType.set("")
            WorkStatus.set("")
            Salary.set("")

        def search():
            try:
                sqlCon = pymysql.connect(host="localhost", user="root", password="qwert", database="employee_data")
                cur = sqlCon.cursor()
                cur.execute("SELECT * FROM record_management WHERE RefNo='%s'" % Search.get())

                row = cur.fetchone()

                txtReference.insert(0, row[0])
                txtFirstname.insert(0, row[1])
                txtLastName.insert(0, row[2])
                txtAddress.insert(0, row[3])
                txtTelephone.insert(0, row[4])
                RegDate.set(row[5])
                WorkType.set(row[6])
                WorkStatus.set(row[7])
                Salary.set(row[8])

                sqlCon.commit()

            except:
                tkinter.messagebox.showinfo("Employee Data Management", "No records found.")
                Reset()
            sqlCon.close()
            Search.set("")

        # WIDGET
        lblReference = Label(InnerTopFrame1, font=('font', 12, 'bold'), text="Reference No.", bg="red", bd=1)
        lblReference.grid(row=0, column=0, sticky='w')
        txtReference = Entry(InnerTopFrame1, font=('font', 12, 'bold'), bd=1, width=32, justify='left',
                             textvariable=RefNo)
        # txtReference.configure(state='normal')
        txtReference.grid(row=0, column=1)

        lblFirstname = Label(InnerTopFrame1, font=('font', 12, 'bold'), text="Firstname", bd=1)
        lblFirstname.grid(row=1, column=0, sticky='w')
        txtFirstname = Entry(InnerTopFrame1, font=('font', 12,), bd=1, width=32, justify='left',
                             textvariable=Firstname)
        txtFirstname.grid(row=1, column=1)

        lblLastName = Label(InnerTopFrame1, font=('font', 12, 'bold'), text="Lastname", bd=1)
        lblLastName.grid(row=2, column=0, sticky='w')
        txtLastName = Entry(InnerTopFrame1, font=('arial', 12,), bd=1, width=32, justify='left',
                            textvariable=Surname)
        txtLastName.grid(row=2, column=1)

        self.lblTelephone = Label(InnerTopFrame1, font=('font', 12, 'bold'), text="Telephone", bd=1)
        self.lblTelephone.grid(row=0, column=2, sticky='w')
        txtTelephone = Entry(InnerTopFrame1, font=('font', 12,), bd=1, width=32, justify='left',
                             textvariable=Telephone)
        txtTelephone.grid(row=0, column=3)

        self.lblRegistrationDate = Label(InnerTopFrame1, font=('font', 12, 'bold'), text="Registration Date", bd=1)
        self.lblRegistrationDate.grid(row=1, column=2, sticky='w')
        txtRegistrationDate = Entry(InnerTopFrame1, font=('font', 12), bd=1, width=32, justify='left',
                                    textvariable=RegDate)
        txtRegistrationDate.grid(row=1, column=3)

        lblWorkType = Label(InnerTopFrame1, font=('font', 12, 'bold'), text="Work Type")
        lblWorkType.grid(row=2, column=2, sticky='w')
        lblWorkType = ttk.Combobox(InnerTopFrame1, font=('font', 12,), width=30, textvariable=WorkType)
        lblWorkType['value'] = ('Support Specialist', 'IT Security Specialist', 'Computer Programmer', 'QA Tester',
                                'UI Designer', 'UX Designer', 'System Analyst', 'Web Developer',
                                'Database Administrator', 'Software Engineer', 'Network Engineer',
                                'IT Director', 'IT Technician', 'Data Scientist', 'Computer Scientist',)
        lblWorkType.set('Support Specialist')
        lblWorkType.grid(row=2, column=3)

        self.lblSearch = Label(InnerTopFrame1, font=('font', 12, 'bold'), text="Search           ", bg="#43B8FF", bd=1)
        self.lblSearch.grid(row=0, column=4, sticky='w')
        self.txtSearch = Entry(InnerTopFrame1, font=('font', 12), bd=1, width=33, justify='left', textvariable=Search)
        self.txtSearch.grid(row=0, column=5)

        self.lblDate = Label(InnerTopFrame1, font=('font', 12, 'bold'), text="Date", bd=1)
        self.lblDate.grid(row=1, column=4, sticky='w')
        self.txtDate = Entry(InnerTopFrame1, font=('font', 12,), bd=1, width=33, justify='left',
                             textvariable=DateToDay)
        self.txtDate.grid(row=1, column=5)

        self.cboWorkStatus = Label(InnerTopFrame1, font=('font', 12, 'bold'), text="Work Status", bd=1)
        self.cboWorkStatus.grid(row=2, column=4, sticky='w')

        self.cboWorkStatus = ttk.Combobox(InnerTopFrame1, font=('font', 12,), width=31, textvariable=WorkStatus)
        self.cboWorkStatus['value'] = ('Probationary', 'Regular', 'Fixed Term', 'Casual', 'Project Base', 'Seasonal')
        self.cboWorkStatus.set('Probationary')
        self.cboWorkStatus.grid(row=2, column=5)

        self.lblMemberSalary = Label(InnerTopFrame1, font=('font', 12, 'bold'), text="Salary", bd=1)
        self.lblMemberSalary.grid(row=3, column=4, sticky='w')

        self.lblMemberSalary = ttk.Combobox(InnerTopFrame1, font=('font', 12), width=31, textvariable=Salary)
        self.lblMemberSalary['value'] = ('PHP 21,000.00', 'PHP 30, 000.00', 'PHP 45, 000.00', 'PHP 55, 000.00',
                                         'PHP 68, 000.00', 'PHP 80, 000.00', 'PHP 100, 000.00', 'PHP 120, 000.00')
        self.lblMemberSalary.set('PHP 21,000.00')
        self.lblMemberSalary.grid(row=3, column=5)

        self.lblAddress = Label(InnerTopFrame1, font=('font', 12, 'bold'), text="Address", bd=1)
        self.lblAddress.grid(row=3, column=0, sticky='w')
        txtAddress = Entry(InnerTopFrame1, font=('font', 12), bd=1, width=80, justify='left', textvariable=Address)
        txtAddress.grid(row=3, column=1, columnspan=3)

        # Data Table
        scroll_x = Scrollbar(InnerTopFrame3, orient=HORIZONTAL)
        scroll_y = Scrollbar(InnerTopFrame3, orient=VERTICAL)
        tree_records = ttk.Treeview(InnerTopFrame3, height=21, columns=("RefNo", "Firstname", "Surname", "Address",
                                                                        "Telephone", "RegDate", "WorkType",
                                                                        "WorkStatus", "Salary"),
                                    xscrollcommand=scroll_x.set, yscrollcommand=scroll_y.set)
        scroll_x.pack(side=BOTTOM, fill=X)
        scroll_y.pack(side=RIGHT, fill=Y)

        tree_records.heading("RefNo", text="Reference No")
        tree_records.heading("Firstname", text="Firstname")
        tree_records.heading("Surname", text="Surname")
        tree_records.heading("Address", text="Address")
        tree_records.heading("Telephone", text="Telephone")
        tree_records.heading("RegDate", text="Register Date")
        tree_records.heading("WorkType", text="Work Type")
        tree_records.heading("WorkStatus", text="Work Status")
        tree_records.heading("Salary", text="Salary")

        tree_records['show'] = 'headings'

        tree_records.column("RefNo", width=100)
        tree_records.column("Firstname", width=150)
        tree_records.column("Surname", width=150)
        tree_records.column("Address", width=252)
        tree_records.column("Telephone", width=100)
        tree_records.column("RegDate", width=100)
        tree_records.column("WorkType", width=150)
        tree_records.column("WorkStatus", width=100)
        tree_records.column("Salary", width=100)

        tree_records.pack(fill=BOTH, expand=1)

        # OPTION BUTTON
        self.btn_AddNew = Button(InnerTopFrame2, bd=1, font=('font', 13, 'bold'), bg="#A46AF7", width=13,
                                 text="Add New", command=addData)
        self.btn_AddNew.grid(row=0, column=0, padx=0)

        self.btn_Display = Button(InnerTopFrame2, font=('font', 13, 'bold'), bg="#A46AF7", width=13,
                                  text="Display", command=DisplayData)
        self.btn_Display.grid(row=0, column=1, padx=10)

        self.btn_Update = Button(InnerTopFrame2, bd=1, font=('font', 13, 'bold'), bg="#A46AF7", width=13,
                                 text="Update", command=update)
        self.btn_Update.grid(row=0, column=2, padx=10)

        self.btn_Delete = Button(InnerTopFrame2, bd=1, font=('font', 13, 'bold'), bg="#A46AF7", width=13,
                                 text="Delete", command=delete)
        self.btn_Delete.grid(row=0, column=3, padx=10)

        self.btn_Reset = Button(InnerTopFrame2, bd=1, font=('font', 13, 'bold'), bg="#A46AF7", width=13,
                                text="Reset", command=Reset)
        self.btn_Reset.grid(row=0, column=4, padx=10)

        self.btn_Search = Button(InnerTopFrame2, bd=1, font=('font', 13, 'bold'), bg="#A46AF7", width=13,
                                 text="Search", command=search)
        self.btn_Search.grid(row=0, column=5, padx=10)

        self.btn_Exit = Button(InnerTopFrame2, bd=1, font=('font', 13, 'bold'), bg="#A46AF7", width=13,
                               text="Exit", command=iExit)
        self.btn_Exit.grid(row=0, column=6, padx=0)
