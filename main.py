import Entry_Form
from tkinter import *


if __name__ == '__main__':
    root = Tk()
    root.title("Jonsoft Management System")
    root.iconbitmap(r'C:\Users\JONEVER-PC\Desktop\JONSOFT\img\js.ico')
    application = Entry_Form.DataEntryForm(root)
    root.mainloop()
