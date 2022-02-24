########## PORT SCANNER - Developed by Parth Dhungana ##############

#importing modules

import csv
import socket
import time
import datetime
import threading
from queue import Queue
from tkinter import *
from tkinter import ttk
from tkinter.font import Font
from tkinter import messagebox

#from logdisplayer import logdisplayer_fun

#logo path

logo_path="det2.ico"

#file path

file_path="logs.csv"


#main windown (root) properties:

main_window=Tk()
main_window.geometry("600x600")
main_window.resizable(False,False)
main_window.title("Port Scanner")
main_window.iconbitmap(logo_path)
main_window.configure(bg="black")          

#name var for text entry:

namebox = StringVar()
ipbox = StringVar() 
spbox = IntVar()
epbox = IntVar()

#fonts:

header_font= Font(family="Papyrus", size=30, weight="bold")
sub_font=Font(family="Papyrus", size=20, weight="bold",underline=1)
normal_font=Font(family="Papyrus", size=16, weight="bold")
input_font=Font(family="Papyrus", size=16, weight="bold")
footer_font=Font(family="Papyrus", size=11,weight="bold")

results = StringVar()
#functions for buttons:

#for scan button:

def scan_res():
    
    if namebox.get()=="" or ipbox.get()=="" or spbox.get()=="" or epbox.get()=="":
        msg=messagebox.showerror("ERROR", "Empty feild(s)!\n\nPlease fill out all the feilds with the correct details!!")
        
    elif spbox.get()>epbox.get():
        msg=messagebox.showerror("ERROR", "ERROR!!\n\nValue of start port cannot be greater than that of end port!!")
        
    elif epbox.get()>65535 or epbox.get()<=0:
        msg=messagebox.showerror("ERROR", "ERROR!!\n\nValue of end port must be greater than 1 and less than or equal to 65,535!!")
    
    elif spbox.get()<0 or epbox.get()<0:
        msg=messagebox.showerror("ERROR", "ERROR!!\n\nValue of start port and end port must be a positive integer between 0 and 65,535!!")
        
    
###########################################################################################################################################################################################################################################################################################################################################

    else:

                                                                                                    #PORT SCANNER (MAIN)

        target = ipbox.get()
        queue = Queue()
        open_ports=[]
        
        display_dt=datetime.datetime.now()
        c_dt=display_dt.strftime("%c")
        
        start_time = time.time()

        def scanner(port):
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((target, port))
                return True
            
            except:
                return False
        
        def queue_range(port_lst):
            for port in port_lst:
                queue.put(port)
                
        def thread_func():
            while not queue.empty():
                port = queue.get()
                if scanner(port):
                    open_scanned=print("Port #{} is open!".format(port))
                    open_ports.append(port)
                    

        port_lst = range(spbox.get(),epbox.get()+1)
        queue_range(port_lst)

        thread_lst = []

        for t in range(1000):
            thread=threading.Thread(target = thread_func)
            thread_lst.append(thread)
            
        for thread in thread_lst:
            thread.start()
            
        for thread in thread_lst:
            thread.join()

        end_time = time.time()
        
        elapsed_time = end_time-start_time
        
        op_results=("{} \n\nTarget Name: {} \n\n{} OPEN PORTS FOUND!!!\n\nPorts open on: {} \n\nTime elapsed: {} seconds.\n").format(c_dt,namebox.get(),len(open_ports),open_ports,elapsed_time)

        #Writing output to csv file
        
        with open(file_path, "a", newline="") as file_op:
            
            writer= csv.writer(file_op)
           
            a=c_dt
            b=namebox.get()
            c=ipbox.get()
            d=spbox.get()
            e=epbox.get()
            f=open_ports
            g=elapsed_time
            data=[a,b,c,d,e,f,g]
            writer.writerow(data)
        file_op.close()
              
###########################################################################################################################################################################################################################################################################################################################################
        
        res_window=Tk()
        res_window.geometry("1200x720")
        res_window.resizable(False,False)

        res_window.title("Port Scanner (Scan Results)")
        res_window.iconbitmap(logo_path)
        res_window.configure(bg="black")
        
        lbl_header1=Label(res_window, text = "Scan results 🔎",bg="black", fg="Green", font=("Papyrus", 30,"bold"))
        lbl_header1.place(relx=0.5,rely=0.110,anchor=CENTER)
       
        #output display
        
        lbl_op=Label(res_window, text=op_results, fg="Black", bg="Green",font=("Papyrus", 16,"bold"))
        lbl_op.place(relx=0.5,rely=0.505, anchor=CENTER)
        
        bt_exit_res=ttk.Button(res_window, text="Exit", command= res_window.destroy)
        bt_exit_res.place(relx=0.695,rely=0.810)
        
        #op_text.place(relx=0.5,rely=0.5,anchor=CENTER)
        lbl_CR=Label(res_window, text="Copyright © 2022   Parth Dhungana, All Rights Reserved.", bg="Green", fg="black", padx=400, font=("Papyrus", 11,"bold"))
        lbl_CR.place(relx=0.5,rely=0.980,anchor=CENTER)

        res_window.mainloop()
        
        
#for view logs button:
def prev_logs():
    msg_vlogs=messagebox.askyesno("View Logs", "Do you wish to view previous logs??")
    
    if msg_vlogs==True:
        
        log_window=Tk()
        log_window.geometry("1555x900")
        log_window.resizable(False,False)

        log_window.title("Port Scanner (View Logs)")
        log_window.iconbitmap(logo_path)
        log_window.configure(bg="white")

        #Scrollable page:

        #Frame 1:
        frame1 = Frame(log_window)
        frame1.pack(fill=BOTH, expand=1)

        #Canvas1:
        canvas1 = Canvas(frame1)
        canvas1.pack(side=LEFT, fill=BOTH, expand=1)

        #Scrollbar:
        scroll_bar = ttk.Scrollbar(frame1, orient = VERTICAL, command = canvas1.yview)
        scroll_bar.pack(side=RIGHT, fill=Y)

        #Canvas2:
        canvas1.configure(yscrollcommand=scroll_bar.set)
        
        #binding configure to event e which is the action of scrolling in lambda function
        canvas1.bind("<Configure>", lambda e: canvas1.configure(scrollregion=canvas1.bbox("all")))

        #Frame 2:
        frame2 = Frame(canvas1)

        #Add frame 2 inside canvas:
        canvas1.create_window((0,0), window= frame2, anchor="nw")
        
        #Output CSV file
        
        with open(file_path, newline="") as logged_file:
            reader= csv.reader(logged_file)
            i=0
            for row in reader:
                
                j=0
                for col in row:
                    
                    label_op = Label(frame2, width = 200, height=2, text=row, relief= RIDGE, bg="Black", fg="White", font=("Helvetica", 10,"bold"))
                    label_op.grid(row=i, column =0)
                    j=j+1
                i=i+1
        
        logged_file.close()
        label_details = Label(log_window, text = "Log Details 🔎:", fg="White", bg="Black", font=("Papyrus", 30, "bold")).place(relx=0.001, rely = 0.00175)
        lbl_CR.place(relx=0.5,rely=0.980,anchor=CENTER)
        log_window.mainloop()
    else:
        pass

#for reset button:

def re_set():
    if ipbox.get()=="" and spbox.get()=="" and epbox.get()=="" and namebox.get()=="":
        pass
    
    elif ipbox.get()!="" or spbox.get()!="" or epbox.get()!="" or namebox.get():
        msg_re=messagebox.askyesno("RESET", "Are you sure you want to reset all the feilds??")
        
        if msg_re==True:
            ipbox.set("")
            spbox.set("")
            epbox.set("")
            namebox.set("")
            msg_done=messagebox.showinfo("RESET","Reset successful!!")
        else:
            pass
    
#for exit button:

def exit_prog():
    msg_ex=messagebox.askyesno("EXIT", "Are you sure you want to exit 🔎ort Scanner??")
    if msg_ex==True:
        exit()
    else:
        pass
  

#widgets:

lbl_header=Label(main_window, text = "🔎ort Scanner",bg="black", fg="Green", font=header_font)
lbl_header.place(relx=0.5,rely=0.110,anchor=CENTER)

lbl_text1=Label(main_window, text = "Enter the required details below:", bg="black", fg ="white", font=sub_font)
lbl_text1.place(relx=0.5,rely=0.250, anchor=CENTER)

#Target name:

lbl_name=Label(main_window, text="👉 Target Name:", bg="black", fg="Green", font=normal_font)
lbl_name.place(relx=0.075,rely=0.370)

#target name input box:

text_name=Entry(main_window, font=input_font, textvariable=namebox)
text_name.place(relx=0.480,rely=0.370)
text_name.focus()

#Target IP:

lbl_ip=Label(main_window, text="👉 Target IP Address:", bg="black", fg="Green", font=normal_font)
lbl_ip.place(relx=0.075,rely=0.470)

#IP addr input box:

text_ip=Entry(main_window, font=input_font, textvariable=ipbox)
text_ip.place(relx=0.480,rely=0.470)

#Start Port:

lbl_port1=Label(main_window, text="👉 Start Port Number:", bg="black", fg="Green", font=normal_font)
lbl_port1.place(relx=0.075,rely=0.570)

#Start port input box:

text_box1=Entry(main_window,font=input_font, width = 7, textvariable=spbox)
text_box1.place(relx=0.480,rely=0.570)
text_box1.delete(0,END)

#End Port:

lbl_port2=Label(main_window, text="👉 End Port Number: ", bg="black", fg="Green", font=normal_font)
lbl_port2.place(relx=0.075,rely=0.670)

#End port input box:

text_box2=Entry(main_window,font=input_font, width = 7, textvariable=epbox)
text_box2.place(relx=0.480,rely=0.670)
text_box2.delete(0,END)


#Frame
button_frame= Frame(main_window, bg="black")
button_frame.place(relx=0.5,rely=0.850, anchor=CENTER)

#buttons:

bt_scan=ttk.Button(button_frame, text="Scan 🔎", command=scan_res)
bt_scan.grid(row=0,column=0,padx=30)   #place(relx=0.185,rely=0.810)

bt_logs=ttk.Button(button_frame, text="View Logs", command= prev_logs)
bt_logs.grid(row=0,column=1,padx=30)

bt_reset=ttk.Button(button_frame, text="Reset", command=re_set)
bt_reset.grid(row=0,column=2,padx=30)    #place(relx=0.440,rely=0.810)

bt_exit=ttk.Button(button_frame, text="Exit", command= exit_prog)
bt_exit.grid(row=0,column=3,padx=30)     #place(relx=0.695,rely=0.810)

#right click pop-up menu:

rt_clk = Menu(main_window, tearoff=0)

rt_clk.add_command(label="New Window")
rt_clk.add_separator()
rt_clk.add_command(label="Scan", command= scan_res)
rt_clk.add_command(label="View Logs", command= prev_logs)
rt_clk.add_command(label="Reset", command= re_set)
rt_clk.add_separator()
rt_clk.add_command(label="Exit", command= exit_prog)

def menupopup(event):
   
   try:
      rt_clk.tk_popup(event.x_root, event.y_root, 0)
   
   finally:
      rt_clk.grab_release()
    
main_window.bind("<Button-3>", menupopup)

#footer:

lbl_CR=Label(main_window, text="Copyright © 2022   Parth Dhungana, All Rights Reserved.", bg="Green", fg="black", padx=150, font=footer_font)
lbl_CR.place(relx=0.5,rely=0.980,anchor=CENTER)

#MenuBar:
menubar=Menu(main_window)

filemenu=Menu(menubar,tearoff=0)
filemenu.add_command(label="View Logs",command=prev_logs)
filemenu.add_separator()
filemenu.add_command(label="Exit",command=exit_prog)

menubar.add_cascade(label="Menu",menu=filemenu)


main_window.config(menu=menubar)

#screen loop:

main_window.mainloop()



