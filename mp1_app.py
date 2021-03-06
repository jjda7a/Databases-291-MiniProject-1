#CMPUT 291 Mini Project 1
#Group Members: Justin Daza. Klark Bliss, Siddhart Khanna
#Project GUI main code to run our application. Module contains front-end functionality dealing with how the data is displayed to the user.
#

import tkinter as tk
from tkinter import ttk
from tkinter import *
from mp1 import *
from mp1_models import *
from mp1_search import *
import mp1_globals

LARGE_FONT = ("Veranda", 18)
SMALL_FONT = ("Veranda", 9)



n = 0
__USERBASKET__ = None

class MiniProjectapp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        tk.Tk.wm_title(self, "291_MiniProject1")

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        # List of all pages 
        frame_list = [StartPage, UserDashBoard, Register, AgentLogin, AgentDashBoard, Stock, placeOrder,
                      searchProducts]
        for F in frame_list:
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):  # function to move desired frame to the front
        frame = self.frames[cont]
        frame.tkraise()


# Initial Login Page
class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        userLabel= ttk.Label(self, text="UserID",font=SMALL_FONT)
        userLabel.pack()
        userInfo = Entry(self)
        userInfo.pack()
        
        passLabel = ttk.Label(self, text="Password",font=SMALL_FONT)
        passLabel.pack()
        passInfo = Entry(self, show="*")
        passInfo.pack()

        loginButton = ttk.Button(self, text="Login",
                             command=lambda: self.LoginCheck(controller,userInfo.get(),passInfo.get()))
        loginButton.pack()

        registerButton = ttk.Button(self, text="Register",
                             command=lambda: controller.show_frame(Register))
        registerButton.pack()

        agentButton = ttk.Button(self, text="Agent?",
                             command=lambda: controller.show_frame(AgentLogin))
        agentButton.pack()

        quitButton = ttk.Button(self, text="Quit",
                             command= quit)
        quitButton.pack()

    def LoginCheck(self, controller,username, password):
        if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
            if(log_in(username, password) == True):
                controller.show_frame(UserDashBoard)
                mp1_globals.initUSER(username)
                print(mp1_globals.__USERID__)
                global __USERBASKET__
                __USERBASKET__ = Basket()
        else:
            messagebox.showerror("Problem", "Invalid characters")



# User Dashboard after successful login
class UserDashBoard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Welcome", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        Button1 = ttk.Button(self, text="Search Products",
                             command=lambda: controller.show_frame(searchProducts))
        Button1.pack()

        Button2 = ttk.Button(self, text="Place an order",
                             command=lambda: controller.show_frame(placeOrder))
        Button2.pack()
        Button3 = ttk.Button(self, text="List Orders",
                             command=lambda: self.ListOrders())
        Button3.pack()

        logoutButton = ttk.Button(self, text="Logout",
                             command=lambda: self.logout(controller))
        logoutButton.pack()

    def ListOrders(self):
        list_order_window = ListOrderPage()
        list_order_window.geometry("270x320")
        list_order_window.mainloop()

    def logout(self,controller):
        global __USERBASKET__
        __USERBASKET__.clearBasket()

        mp1_globals.__USERID__ = None

        controller.show_frame(StartPage)

class searchProducts(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Search Products", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        searchEntry = ttk.Entry(self, width=20)
        searchEntry.pack()
        searchButton = ttk.Button(self, text = "Find",
                                  command=lambda: self.openSearch(searchEntry.get()))
        searchButton.pack()
        returnButton = ttk.Button(self, text="Return",
                                      command=lambda: controller.show_frame(UserDashBoard))
        returnButton.pack()

    def openSearch(self,termString):
        # print(termString)
        if(termString!= ''):
            searchResult = Search_products(termString)
            result_window = SearchResultWindow(termString, searchResult.getFormattedResultList())
            result_window.geometry("800x270")
            result_window.mainloop()
        else:
            messagebox.showinfo("No results", "Please enter key words")

class SearchResultWindow(tk.Tk):
    start_index = 0  # tracker for result list
    def __init__(self,termString,result_list, *args, **kwargs):
        self.result_list =result_list
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Search Results")
        label = ttk.Label(self, text="Search Results", font=LARGE_FONT)
        label.pack(side="top")
        label2 = ttk.Label(self, text="Searched: '"+termString+"'", font=SMALL_FONT)
        label2.pack(side="top")
        self.resListBox = Listbox(self, width=120,height=5, selectmode=EXTENDED)
        self.resListBox.pack()
        self.resListBox.bind('<<ListboxSelect>>',self.onSelect)
        for i in range(self.start_index,self.start_index+5):
            try:
                item = result_list[i]
                self.resListBox.insert(END, item)
            except:
                pass
        if (len(result_list) > 5):
            nextButton = ttk.Button(self, text="Next", command=lambda:self.updateIndecies(5))
            nextButton.pack()
            prevButton = ttk.Button(self, text="Prev", command=lambda: self.updateIndecies(-5))
            prevButton.pack()

        ReturnButton = ttk.Button(self, text="Close",
                                  command=lambda: self.destroy())
        ReturnButton.pack()

    def updateIndecies(self, d_i):
        cur_index = self.start_index
        self.start_index += d_i
        if(self.start_index > len(self.result_list) or self.start_index < 0):
            self.start_index = cur_index
        self.resListBox.delete(0,END)
        for i in range(self.start_index, self.start_index + 5):
            try:
                item = [self.result_list[i][0], self.result_list[i][1]]
                self.resListBox.insert(END, item)
            except:
                pass

    def onSelect(self,evt):
        try:
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            detail_window = DetailWindow(value[0])
            detail_window.geometry("320x480")
            detail_window.mainloop()
        except:
            pass

class DetailWindow(tk.Tk):
    def __init__(self, pid, *args, **kwargs):
        self.pid = pid
        self.details = list_product_details(pid)
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Product ID: "+pid+" Details")
        titlelabel = ttk.Label(self, text="Product ID: "+pid+" Details", font=LARGE_FONT)
        titlelabel.pack()
        namelabel = ttk.Label(self, text="Product Name: " + self.details[1], font=SMALL_FONT)
        namelabel.pack()
        unitlabel = ttk.Label(self, text="Unit: " + self.details[2], font=SMALL_FONT)
        unitlabel.pack()
        catlabel = ttk.Label(self, text="Category: " + self.details[3], font=SMALL_FONT)
        catlabel.pack()
        storeListLabel = ttk.Label(self, text="\nList of Stores:(Name/id/Price/Qty/# of Orders) ", font=SMALL_FONT)
        storeListLabel.pack()
        storeListBox = Listbox(self, width=30)
        storeListBox.pack()
        storeListBox.bind('<<ListboxSelect>>', self.onSelect)
        for store in self.details[4]:
            storeListBox.insert(END, store)
        ReturnButton = ttk.Button(self, text="Close",
                                  command=lambda: self.destroy())
        ReturnButton.pack()

    def onSelect(self,evt):
        try:
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            addwindow = addBasketItemView(self.pid, value[1])
            addwindow.geometry("120x160")
            addwindow.mainloop()
        except:
            pass

class addBasketItemView(tk.Tk):
    def __init__(self, pid, sid, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Add to Basket")
        self.sid = sid
        self.pid = pid
        qtyLabel = ttk.Label(self, text="Set Qty:", font=SMALL_FONT)
        qtyLabel.pack()
        qtyEntry = ttk.Entry(self, width=10)
        qtyEntry.delete(0, END)
        qtyEntry.insert(0, "1")
        qtyEntry.pack()
        addButton = ttk.Button(self, text="Add",
                                  command=lambda: self.addItem(qtyEntry.get()))
        addButton.pack()
        cancelButton = ttk.Button(self, text="Cancel",
                                  command=lambda: self.destroy())
        cancelButton.pack()

    def addItem(self,qty): #item:[sid, pid, qty]
        try:
            global __USERBASKET__
            item = [int(self.sid),self.pid,int(qty)]
            __USERBASKET__.additem(item)
            print(item)
            messagebox.showinfo("Item Added", self.pid+ " has been added to you basket.\n Qty: "+ str(qty))
            for i in __USERBASKET__.getitems():
                print(i)
            self.destroy()
        except:
            messagebox.showerror("Problem", "Value is invalid")


# Registration Page for Regular Users
class Register(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Register", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        uIDLabel = ttk.Label(self, text="Enter ID",font=SMALL_FONT)
        uIDLabel.pack()
        uIDInfo = Entry(self)
        uIDInfo.pack()
        nameLabel = ttk.Label(self, text="Enter name",font=SMALL_FONT)
        nameLabel.pack()
        nameInfo = Entry(self)
        nameInfo.pack()
        addressLabel = ttk.Label(self, text="Enter address",font=SMALL_FONT)
        addressLabel.pack()
        addressInfo = Entry(self)
        addressInfo.pack()
        passwordLabel = ttk.Label(self, text="Enter password",font=SMALL_FONT)
        passwordLabel.pack()
        passwordInfo = Entry(self, show='*')
        passwordInfo.pack()
        conpasswordLabel = ttk.Label(self, text="Confirm Password",font=SMALL_FONT)
        conpasswordLabel.pack()
        conpasswordInfo = Entry(self, show='*')
        conpasswordInfo.pack()

        registerButton =  ttk.Button(self, text="Register",
                             command=lambda: self.registerUser(controller,uIDInfo.get(),nameInfo.get(),addressInfo.get(),passwordInfo.get(),conpasswordInfo.get()))
        registerButton.pack()
        cancelButton = ttk.Button(self, text="Cancel",
                             command=lambda: controller.show_frame(StartPage))
        cancelButton.pack()

    def registerUser(self,controller, uID, name, address, password,conpass):
        if re.match("^[A-Za-z0-9_]*$", uID) and re.match("^[A-Za-z0-9_]*$", password):
            if(conpass == password):
                if (sign_up(uID, name, address, password) == True):
                    messagebox._show("Success","You have successfully registered your account!")
                    controller.show_frame(StartPage)
            else:
                messagebox.showerror("Different passwords","The passwords you entered must match.")
        else:
            messagebox.showerror("Invalid ID", "Username or Password contains invalid characters")


# Login page for agents
class AgentLogin(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="Login", font=LARGE_FONT)
        label.pack(pady=10, padx=10)
        userLabel = ttk.Label(self, text="AgentID",font=SMALL_FONT)
        userLabel.pack()
        userInfo = Entry(self)
        userInfo.pack()
        passLabel = ttk.Label(self, text="Password",font=SMALL_FONT)
        passLabel.pack()
        passInfo = Entry(self, show="*")
        passInfo.pack()

        loginButton = ttk.Button(self, text="Login",
                                 command=lambda: self.AgentLoginCheck(controller, userInfo.get(), passInfo.get()))
        loginButton.pack()


        button1 = ttk.Button(self, text="Return",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

    def AgentLoginCheck(self, controller,username, password):
        if re.match("^[A-Za-z0-9_]*$", username) and re.match("^[A-Za-z0-9_]*$", password):
            if(agent_log_in(username, password) == True):
                controller.show_frame(AgentDashBoard)
        else:
            messagebox.showerror("Invalid ID", "Username or Password contains invalid characters")

#Dashboard for agents, containing all the actions that agents can perform
class AgentDashBoard(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = tk.Label(self, text="AgentDashboard", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        Button1 = ttk.Button(self, text="Setup Delivery",
                                 command=lambda: self.SetUpDelivery())
        Button1.pack()
        Button2 = ttk.Button(self, text="Update Delivery",
                             command=lambda: self.UpdateDelivery())
        Button2.pack()
        Button3 = ttk.Button(self, text="Add to Stocks",
                             command=lambda: controller.show_frame(Stock))
        Button3.pack()
        logoutButton = ttk.Button(self, text="Logout",
                             command=lambda: controller.show_frame(StartPage))
        logoutButton.pack()

    def SetUpDelivery(self):
        set_up_window = SetUpDeliveryWindow()
        set_up_window.geometry("270x480")
        set_up_window.mainloop()

    def UpdateDelivery(self):
        update_window = UpdateDeliveryWIndow()
        update_window.geometry("270x480")
        update_window.mainloop()


class UpdateDeliveryWIndow(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.curDelivery = Delivery()
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Update Delivery")
        label = ttk.Label(self, text="Update Delivery", font=LARGE_FONT)
        label.pack(side="top")
        selDelLabel = ttk.Label(self, text="Select Delivery No.: ", font=SMALL_FONT)
        selDelLabel.pack()
        selDelEntry = ttk.Entry(self, width = 8)
        selDelEntry.pack()
        selDelButton = ttk.Button(self, text="Get Delivery",
                                          command=lambda: self.GetDelivery(selDelEntry.get()))
        selDelButton.pack()


        ReturnButton = ttk.Button(self, text="Close",
                                  command=lambda: self.destroy())
        ReturnButton.pack()

    def GetDelivery(self, ID):
        if(self.curDelivery.getDelivery(ID)):
            delnumlabel = ttk.Label(self, text="Delivery No. " + str(self.curDelivery.getTrackingNum()), font=SMALL_FONT)
            delnumlabel.pack()
            ol = StringVar(self, value=','.join(map(str, self.curDelivery.orders)))
            orderLabel = ttk.Label(self, text="Change Orders:", font=SMALL_FONT)
            orderLabel.pack()
            orderList = Entry(self, textvariable=ol)
            orderList.pack()
            pdl = StringVar(self, value=self.curDelivery.pickUpTime)
            pickupDateLabel = ttk.Label(self, text="Change Date[YYYY-MM-DD hh:mm]:", font=SMALL_FONT)
            pickupDateLabel.pack()
            pickDateInp = Entry(self, width=20, textvariable=pdl)
            pickDateInp.pack()
            ddl = StringVar(self, value=self.curDelivery.dropOffTime)
            dropupDateLabel = ttk.Label(self, text="Add Drop-Off Date[YYYY-MM-DD hh:mm]:", font=SMALL_FONT)
            dropupDateLabel.pack()
            dropDateInp = Entry(self, width=20, textvariable=ddl)
            dropDateInp.pack()

            UpdateDeliveryButton = ttk.Button(self, text="Update",
                                              command=lambda: self.updateDelivery(orderList.get(),pickDateInp.get(),dropDateInp.get()))
            UpdateDeliveryButton.pack()


    def updateDelivery(self,nOrders, npDate, ndDate):
        self.curDelivery.removeDelivery(self.curDelivery.trackingNum)   # remove any rows with the delivery tracking num
        if npDate != '':
            npDate = datetime.datetime.strptime(npDate, '%Y-%m-%d %H:%M')
        if ndDate != '':
            ndDate = datetime.datetime.strptime(ndDate, '%Y-%m-%d %H:%M')
        orderlist = map(int, nOrders.split(','))
        try:
            self.curDelivery.pickUpTime = npDate
            self.curDelivery.dropOffTime = ndDate
            self.curDelivery.orders = orderlist
            self.curDelivery.saveDelivery()
            messagebox.showinfo("Delivery Updated", "Delivery No."+str(self.curDelivery.trackingNum)+" has been updated!")

        except Exception as ex:
            messagebox.showerror("Error", "Something went wrong when updating")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        self.destroy()


class SetUpDeliveryWindow(tk.Tk):
    def __init__(self, *args, **kwargs):
        self.newDelivery = Delivery()
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Setup Delivery")
        label = ttk.Label(self, text="Setup New Delivery", font=LARGE_FONT)
        label.pack(side="top")
        delnumlabel = ttk.Label(self, text="Delivery No. "+str(self.newDelivery.getTrackingNum()), font=SMALL_FONT)
        delnumlabel.pack()
        orderLabel = ttk.Label(self, text="Enter Orders (1,3,12,etc..):", font=SMALL_FONT)
        orderLabel.pack()
        orderList = Entry(self)
        orderList.pack()
        dateLabel =  ttk.Label(self, text="Pick up Date[YYYY-MM-DD hh:mm] (optional):", font=SMALL_FONT)
        dateLabel.pack()
        dateInp = Entry(self, width=20)
        dateInp.pack()

        CreateDeliveryButton =ttk.Button(self, text="Create Delivery",command = lambda: self.CreateNewDelivery( orderList.get(),str(dateInp.get())))
        CreateDeliveryButton.pack()

        ReturnButton = ttk.Button(self, text="Return",
                                  command=lambda: self.destroy())
        ReturnButton.pack()

    def CreateNewDelivery(self,orders, datestring=None ):
        if datestring != '':
            datestring = datetime.datetime.strptime(datestring, '%Y-%m-%d %H:%M')
        orderlist = map(int, orders.split(','))
        try:
            self.newDelivery.pickUpTime = datestring
            self.newDelivery.orders = orderlist
            self.newDelivery.saveDelivery()
            messagebox.showinfo("Delivery Created", "Delivery No."+str(self.newDelivery.trackingNum)+" has been added to the database!")

        except Exception as ex:
            messagebox.showerror("Error", "Something went wrong")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)
        self.destroy()


class Stock(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)        
        userLabel4= ttk.Label(self, text="Enter Store ID(sid)",font=SMALL_FONT)
        userLabel4.pack()
        sidInfo = Entry(self)
        sidInfo.pack()    
        
        userLabel3= ttk.Label(self, text="Enter Product ID(pid)",font=SMALL_FONT)
        userLabel3.pack()
        pidInfo = Entry(self)
        pidInfo.pack()        
        
        CheckButton = ttk.Button(self, text="Check",
                             command=lambda: self.StockImplement(sidInfo.get(), pidInfo.get()))
        CheckButton.pack()
        
        buttonReturn = ttk.Button(self, text="Return",
                             command=lambda: controller.show_frame(AgentDashBoard))
        buttonReturn.pack()            
    
    def StockImplement(self, sid, pid):
        #display quantity button
        if(StockCheck(self, sid, pid)==True):
            userLabel= ttk.Label(self, text="Enter Qty",font=SMALL_FONT)
            userLabel.pack()
            qtyInfo = Entry(self)
            qtyInfo.pack()                
            qtyButton = ttk.Button(self, text="Add Quantity", command=lambda: StockQTY(sid,pid, qtyInfo.get()))
            qtyButton.pack()
        
            userLabel2= ttk.Label(self, text="Enter Price",font=SMALL_FONT)
            userLabel2.pack()
            priceInfo = Entry(self)
            priceInfo.pack()                
            priceButton = ttk.Button(self, text="Change Price", command=lambda: StockPrice(sid,pid, priceInfo.get()))
            priceButton.pack()         
            
        else:
            mylabel = Label(self, text = "Store Not Present", font = ("Verdana", 12))
            mylabel.pack()


class placeOrder(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)   
        basketItem = Label(self, text = "Items in Basket", font = ("Verdana", 12))
        basketItem.pack()
        # listBasket = [[1, 'p1', 4],[2, 'p4', 4],[1, 'p1', 5], [1, 'p2', 9]] #sid, pid, qty

        checkQuantity = ttk.Button(self, text="Check Order", command=lambda: self.setOrder())
        checkQuantity.pack()

        buttonReturn = ttk.Button(self, text="Return",
                                  command=lambda: controller.show_frame(UserDashBoard))
        buttonReturn.pack()

    def setOrder(self):
        setorderwindow = orderSetUp()
        setorderwindow.geometry("240x480")
        setorderwindow.mainloop()

class orderSetUp(tk.Tk): #New Window to set up order
    def __init__(self, *args, **kwargs):
        self.basket = __USERBASKET__
        self.uid = mp1_globals.__USERID__
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Setup Order")
        label = ttk.Label(self, text="Order Items", font=LARGE_FONT)
        label.pack()
        itemListBox = Listbox(self)
        itemListBox.pack()
        itemListBox.bind('<<ListboxSelect>>', self.onSelect)
        for item in self.basket.getitems():
            itemListBox.insert(END, item)
        invalterms = self.basket.checkInvalidTerms()
        #print(invalterms)
        if self.basket.getitems(): #Check if items are in basket
            if not invalterms: # If there are no invalid items
                conf_label = ttk.Label(self, text= "No problems detected.\n Proceed with placing order.", font=SMALL_FONT)
                conf_label.pack()
                conf_button = ttk.Button(self, text="Confirm", command=lambda:self.confirmOrder())
                conf_button.pack()
            else:
                for i in invalterms:
                    self.displayWarning(i)
        else:
            label = ttk.Label(self, text="No items in basket.", font=SMALL_FONT)
            label.pack()
        ReturnButton = ttk.Button(self, text="Close",
                                  command=lambda: self.destroy())
        ReturnButton.pack()

    def onSelect(self,evt):
        try:
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            print(value, index)
            update_window = UpdateBasketItemWIndow(index, value[2])
            update_window.geometry("270x480")
            update_window.mainloop()
        except:
            pass

    def displayWarning(self, input): # input:[pid, max_qty]
        warningLabel = ttk.Label(self,text="WARNING:\n Qty for product, ["+str(input[0])+", "+str(input[1])+"] is too high!\n   Max qty: "+str(input[2])+"\n   Order cannot be processed.")
        warningLabel.pack()

    def confirmOrder(self): # Function is called whenever the items in the user basket are all okay
        global __USERBASKET__
        process_basket = __USERBASKET__
        processOrder(process_basket.getitems(), mp1_globals.__USERID__)
        __USERBASKET__.clearBasket()


class UpdateBasketItemWIndow(tk.Tk):
    def __init__(self, index,curqty, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        self.index = index
        tk.Tk.wm_title(self, "Update Item")
        label = ttk.Label(self, text="Update Item", font=LARGE_FONT)
        label.pack(side="top")
        newQtyLabel = ttk.Label(self, text="Change qty: ", font=SMALL_FONT)
        newQtyLabel.pack()
        v = StringVar(self, str(curqty))
        qtyEntry = ttk.Entry(self, width=8,textvariable = v)
        qtyEntry.pack()
        UpdateButton = ttk.Button(self, text="Update",
                                  command=lambda: self.updateBasketItem(self.index,qtyEntry.get()))
        UpdateButton.pack()
        DeleteButton = ttk.Button(self, text="Delete Item",
                                  command=lambda: self.deleteBasketItem(self.index))
        DeleteButton.pack()
        ReturnButton = ttk.Button(self, text="Close",
                                  command=lambda: self.destroy())
        ReturnButton.pack()

    def updateBasketItem(self, index, newqty):
        global __USERBASKET__
        newitem = __USERBASKET__.getitems()[index]
        try:
            newitem[2] = int(newqty)
            __USERBASKET__.removeItem(index)
            __USERBASKET__.getitems().insert(index,newitem)
            messagebox.showinfo("Item Updated",
                                "Item has been updated! Restart order.")
        except Exception as ex:
            messagebox.showerror("Error", "Something went wrong when updating")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

        self.destroy()

    def deleteBasketItem(self, index):
        try:
            global __USERBASKET__
            __USERBASKET__.removeItem(index)
            messagebox.showinfo("Item Removed",
                                "Item has been removed! Restart order.")
        except Exception as ex:
            messagebox.showerror("Error", "Something went wrong when updating")
            template = "An exception of type {0} occurred. Arguments:\n{1!r}"
            message = template.format(type(ex).__name__, ex.args)
            print(message)

        self.destroy()


class ListOrderPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        label = ttk.Label(self, text="Your Orders", font=LARGE_FONT)
        label.pack(side="top")
        self.result_list = list_orders(mp1_globals.__USERID__)
        self.start_index = 0
        self.resListBox = Listbox(self, width=120, height=5, selectmode=EXTENDED)
        self.resListBox.pack()
        self.resListBox.bind('<<ListboxSelect>>', self.onSelect)
        for i in range(self.start_index, self.start_index + 5):
            try:
                item = self.result_list[i]
                self.resListBox.insert(END, item)
            except:
                pass
        if (len(self.result_list) > 5):
            nextButton = ttk.Button(self, text="Next", command=lambda: self.updateIndecies(5))
            nextButton.pack()
            prevButton = ttk.Button(self, text="Prev", command=lambda: self.updateIndecies(-5))
            prevButton.pack()

        ReturnButton = ttk.Button(self, text="Close",
                                  command=lambda: self.destroy())
        ReturnButton.pack()

    def updateIndecies(self, d_i):
        cur_index = self.start_index
        self.start_index += d_i
        if (self.start_index > len(self.result_list) or self.start_index < 0):
            self.start_index = cur_index
        self.resListBox.delete(0, END)
        for i in range(self.start_index, self.start_index + 5):
            try:
                item = [self.result_list[i][0], self.result_list[i][1]]
                self.resListBox.insert(END, item)
            except:
                pass

    def onSelect(self, evt):
        try:
            w = evt.widget
            index = int(w.curselection()[0])
            value = w.get(index)
            detail_window = OrderDetailWindow(value)
            detail_window.geometry("320x720")
            detail_window.mainloop()
        except:
            pass

class OrderDetailWindow(tk.Tk):
    def __init__(self, input, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Order details")
        self.input = input
        #print(self.input[0])
        self.userID = mp1_globals.__USERID__
        self.details = show_details(self.userID, self.input[0])
        olines = self.details[4]
        titlelabel = ttk.Label(self, text="Order #"+str(input[0])+" Details", font=LARGE_FONT)
        titlelabel.pack()
        delLabel = ttk.Label(self, text="Deliver Info:", font=LARGE_FONT)       #[Tracking no., pickuptime, drop off, address,[list of olines in order]]
        delLabel.pack()
        tno = ttk.Label(self, text="Tracking #: "+str(self.details[0]), font=SMALL_FONT)  # Tracking no. pickuptime, drop off, address
        tno.pack()
        pt = ttk.Label(self, text="Pick up time: " + str(self.details[1]),
                        font=SMALL_FONT)
        pt.pack()
        dt = ttk.Label(self, text="Drop offtime: " + str(self.details[2]),
                       font=SMALL_FONT)
        dt.pack()
        ad = ttk.Label(self, text="Address: " + str(self.details[3]),
                       font=SMALL_FONT)
        ad.pack()
        ol = ttk.Label(self, text="Olines: " + str(self.details[3]),
                       font=SMALL_FONT)
        ol.pack()
        resListBox = Listbox(self, width=100, height=5)
        resListBox.pack()
        #print("2",olines)
        for i in olines:
            print(i)
            resListBox.insert(0,i)

        ReturnButton = ttk.Button(self, text="Close",
                                  command=lambda: self.destroy())
        ReturnButton.pack()


