import tkinter
import sqlite3
from userAction import *
from productAction import *
#=======================login========================

def login():
    global session
    global cnt
    user=txt_user.get()
    pas=txt_pass.get()
    
    result=user_login(user,pas)   
    if result:
         lbl_msg.configure(text="welcome to your account",fg="green")
         txt_user.delete(0,"end")
         txt_pass.delete(0,"end")
         btn_login.configure(state="disabled")
         btn_submit.configure(state="disabled")
         btn_logout.configure(state="active")
         btn_shop.configure(state="active")
         session=result
         if user=="admin":        
               btn_admin_panel.configure(state="active")
         else:
             btn_admin_panel.configure(state="disabled")
         
         score=get_score(user)
         if score:
              btn_shop.configure(state="active")
         else:
              btn_shop.configure(state="disabled")
              lbl_msg.configure(text="you dont have access to the shop panel!",fg="red")
                       
    else:
         lbl_msg.configure(text="wrong username or password!",fg="red")
         cnt+=1 
         if cnt==3:
             btn_login.configure(state="disabled")
             lbl_msg.configure(text="3 times error occurred! the login button is disabled!",fg="red")     
#=========================submit======================================       
def submit(): 
    user=txt_user.get()
    pas=txt_pass.get()
    result,errormsg=user_submit(user,pas)
    if result:
       lbl_msg.configure(text="submit done!",fg="green")  
    else:
       lbl_msg.configure(text=errormsg ,fg="red")
#=====================logout=============================
def logout():
    btn_login.configure(state="active")
    btn_logout.configure(state="disabled")
    lbl_msg.configure(text="you are logged out now!",fg="pink")
    btn_shop.configure(state="disabled")
#======================shop===============================
def shop():
    def buy():
        pid=pidtxt.get()
        qnt=pqnttxt.get()
        if pid=="" or qnt=="" :
            lbl_msg2.configure(text="fill the inputs!",fg="red")
            return
        
        if not pid.isdigit() or not qnt.isdigit():
            lbl_msg2.configure(text="enter a number in input!",fg="red")
            return
        
        result=get_single_product(pid)
        
        if not result:
            lbl_msg2.configure(text="wrong product id!",fg="red")
            return
        
        if int(qnt)>result[3]:
            lbl_msg2.configure(text="not enough products!",fg="red")
            return
        
        if int(qnt)<1:
            lbl_msg2.configure(text="quantity should be at least 1!",fg="red")
            return
        
        save_to_cart(pid,session,qnt)
        lbl_msg2.configure(text="add to cart successfully",fg="green")
        pidtxt.delete(0,"end")
        pqnttxt.delete(0,"end")

        update_qnt(qnt,pid)
        lst.delete(0,"end")
        products=get_product()
        for product in products:
            text=f"ID={product[0]} , NAME={product[1]} , PRICE={product[2]} , QUANTITY={product[3]}"
            lst.insert("end",text)

    win_shop=tkinter.Toplevel(win)
    win_shop.geometry("400x400")
    win_shop.title("shopping panel")

    lst=tkinter.Listbox(win_shop,width=50)
    lst.pack()

    products=get_product()
    for product in products:
        
        text=f"ID={product[0]} , NAME={product[1]} , PRICE={product[2]} , QUANTITY={product[3]}"
        lst.insert("end",text)

    pidlbl=tkinter.Label(win_shop,text="id: ")
    pidlbl.pack()
    pidtxt=tkinter.Entry(win_shop)
    pidtxt.pack()
    
    pqntlbl=tkinter.Label(win_shop,text="qnt: ")
    pqntlbl.pack()
    pqnttxt=tkinter.Entry(win_shop)
    pqnttxt.pack()
    
    lbl_msg2=tkinter.Label(win_shop,text="")
    lbl_msg2.pack()

    btn_buy=tkinter.Button(win_shop,text="buy",command=buy)
    btn_buy.pack()

    win_shop.mainloop()
#==================admin panel=======================
def admin_panel():
   def product_panel():
    def add_product_panel():
        pname=pnametxt.get()
        pprice=ppricetxt.get()
        qnt=pqnttxt.get()
        if(pprice=="" or qnt=="" or pname==""):
            lbl_msg2.configure(text="fill the inputs!",fg="red")
            return
        
        add_new_product(pname,pprice,qnt)
        print("the new product added")
        
    win_new=tkinter.Toplevel(win)
    win_new.geometry("300x300")
    win_new.title("new products panel")

    
    pnamelbl=tkinter.Label(win_new,text="name: ")
    pnamelbl.pack()
    
    pnametxt=tkinter.Entry(win_new)
    pnametxt.pack()
    
    ppricelbl=tkinter.Label(win_new,text="price: ")
    ppricelbl.pack()
    
    ppricetxt=tkinter.Entry(win_new)
    ppricetxt.pack()
    
    pqntlbl=tkinter.Label(win_new,text="qnt: ")
    pqntlbl.pack()
    
    pqnttxt=tkinter.Entry(win_new)
    pqnttxt.pack()    
    
    btn_add=tkinter.Button(win_new,text="add",command=add_product_panel)
    btn_add.pack()
    
    lbl_msg2=tkinter.Label(win_new,text="")
    lbl_msg2.pack()
    
    win_new.mainloop()
      
  
   win_admin=tkinter.Toplevel(win)
   win_admin.geometry("250x250")
   win_admin.title("admin panel")
  
   btn_new=tkinter.Button(win_admin,text="add a new product",command=product_panel)
   btn_new.pack()
  
  
   win_admin.mainloop()
#------------------------------------------------------------------------------
session=""
cnt=0

win=tkinter.Tk()
win.geometry("300x300")

lbl_user=tkinter.Label(win,text="username :")
lbl_user.pack()
txt_user=tkinter.Entry(win)
txt_user.pack()

lbl_pass=tkinter.Label(win,text="password :")
lbl_pass.pack()
txt_pass=tkinter.Entry(win)
txt_pass.pack()

lbl_msg=tkinter.Label(win,text="")
lbl_msg.pack()

lbl_msg2=tkinter.Label(win,text="")
lbl_msg2.pack()

btn_login=tkinter.Button(win,text="login",command=login)
btn_login.pack()

btn_submit=tkinter.Button(win,text="submit",command=submit)
btn_submit.pack()

btn_logout=tkinter.Button(win,text="logout",state="disabled",command=logout)
btn_logout.pack()

btn_shop=tkinter.Button(win,text="shop",state="disabled",command=shop)
btn_shop.pack()

btn_admin_panel=tkinter.Button(win,text="admin panel",state="disabled",command=admin_panel)
btn_admin_panel.pack()

win.mainloop()