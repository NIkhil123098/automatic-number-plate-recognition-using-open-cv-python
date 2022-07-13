from tkinter import ttk

import cv2
import pytesseract
import numpy as np
from tkinter import *
import pandas as pd
from PIL import Image,ImageTk
import datetime as dt
import time
from datetime import datetime
from fpdf import FPDF




df=pd.read_excel("Dummy NP.xlsx",engine='openpyxl')
print(df['Name'][df['ID']==15635512].values[0])

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

cascade= cv2.CascadeClassifier("haarcascade_russian_plate_number2.xml")
licensePlate = list()
excel=[]
excel1=[]

def extract_num(img_name, enableVideo):
    inc=0
    if enableVideo:
        img = img_name.copy()
    else:
        img = cv2.imread(img_name) ## Reading Image
    # Converting into Gray
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    cv2.imshow('Gray Image', gray)
    # Detecting plate
    #nplate = cascade.detectMultiScale(gray,1.1,4)
    nplate = cascade.detectMultiScale(gray, scaleFactor = 1.05, minNeighbors = 5, minSize = (40,40))

    for (x,y,w,h) in nplate:


        a,b = (int(0.02*img.shape[0]), int(0.025*img.shape[1]))
        plate = img[y+a:y+h-a, x+b:x+w-b, :]

        kernel = np.ones((1, 1), np.uint8)
        plate = cv2.dilate(plate, kernel, iterations=1)
        plate = cv2.erode(plate, kernel, iterations=1)
        plate_gray = cv2.cvtColor(plate,cv2.COLOR_BGR2GRAY)

        read = pytesseract.image_to_string(plate)
        read = ''.join(e for e in read if e.isalnum())
        #print("=====>", read)
        flagA, flag1 = 0, 0
        for character in read:
            if(character.isalpha()):
                flagA = 1
            if(character.isdigit()):
                flag1 = 1
            if flagA == 1 and flag1== 1:
                break

        if(flagA == 1 and flag1 == 1):

            if(read not in licensePlate):


                time_string = time.strftime('%H:%M:%S')
                im1="result{}.jpg".format(len(licensePlate))
                inc=inc+1
                cv2.imwrite(im1, img)

                licensePlate.append(read)
                top = Tk()

                width = top.winfo_screenwidth()

                height = top.winfo_screenheight()
                h1 = int((0.6) * height)

                top.geometry("%dx%d" % (width, height))
                canvas = Canvas(top, width=width, height=h1)
                canvas.place(x=0, y=0)

                img1 = (Image.open("backi.jpg"))

                resized_image = img1.resize((width, h1), Image.ANTIALIAS)
                new_image = ImageTk.PhotoImage(resized_image)

                canvas.create_image(10, 10, anchor=NW, image=new_image)
                labelframe = Frame(top, width=int(0.7 * width), height=int(0.7 * height), bg='lightgray')
                w1 = Label(labelframe, text=f"{dt.datetime.now():%a, %b %d %Y}     "+time_string, fg="gray", bg="lightgray",font=("helvetica", 9))
                width1 = labelframe.winfo_screenwidth()
                height1 = labelframe.winfo_screenheight()
                w1.place(x=int(0.55 * width1), y=65)
                labelframe.place(x=int(0.25 * width), y=int(0.1 * height))
                def onclick(event):
                    selected=tv.identify('item',event.y,event.y)
                    temp = tv.item(selected, 'values')

                    if(temp[1]=='-'):
                        image5 = Image.open("result.png")
                        resized_image5 = image5.resize((420, 380), Image.ANTIALIAS)
                        test5 = ImageTk.PhotoImage(resized_image5)

                        labelim5 = Label(labelframe, image=test5, bg='lightgray')
                        labelim5.image = test5
                        labelim5.place(x=20, y=80)
                    else:
                        im="result{}.jpg".format(selected)
                        image5 = Image.open(im)
                        resized_image5 = image5.resize((420, 380), Image.ANTIALIAS)
                        test5 = ImageTk.PhotoImage(resized_image5)

                        labelim5 = Label(labelframe, image=test5, bg='lightgray')
                        labelim5.image = test5
                        labelim5.place(x=20, y=80)


                tv = ttk.Treeview(labelframe, columns=(1, 2, 3,4), show='headings', height=8)
                tv.column("#1",width=120)
                tv.column("#2", width=120)
                tv.column("#3", width=120)
                tv.column("#4",width=120)
                tv.heading(1, text="Number")
                tv.heading(2, text="ID")
                tv.heading(3, text="Fine Amount")
                tv.heading(4,text="Recent date")
                tv.bind('<Button-1>',onclick)
                i1=0

                if(read in df.Number_Plate.values):
                 excel.append(read)



                for i in excel:

                    val1=i
                    val2=df['ID'][df['Number_Plate']==i].values[0]
                    val3 = df['Amount '][df['Number_Plate'] == i].values[0]
                    val4 = str(df['Recent_Fined_Date'][df['Number_Plate'] == i].values[0])
                    year, month, day = val4.split('-')
                    date="/".join([year,month,day[0:2]])




                    tv.insert(parent='', index=i1, iid=i1, values=(val1,val2,val3,date))
                    i1=i1+1
                if(read not in df.Number_Plate.values):
                    excel1.append(read)
                for i2 in excel1:
                    tv.insert(parent='', index=i1, iid=i1, values=(i2,"-","-","-"))
                    i1=i1+1



                tv.focus_set()
                children = tv.get_children()
                tv.focus(children[-1])
                tv.selection_set(children[-1])


                tv.place(x=460, y=160)
                image1 = Image.open("logo.png")
                resized_image1 = image1.resize((90, 90), Image.ANTIALIAS)
                test = ImageTk.PhotoImage(resized_image1)

                label1 = Label(labelframe, image=test, bg='lightgray')
                label1.image = test
                image2 = Image.open(im1)
                resized_image2 = image2.resize((420,380), Image.ANTIALIAS)
                test2 = ImageTk.PhotoImage(resized_image2)

                def open_view():
                    top_view = Toplevel(top)
                    top_view.geometry("500x500")
                    top_view.configure(bg='lightgray')
                    selected = tv.focus()
                    temp = tv.item(selected, 'values')
                    if (temp[1] == '-'):
                        image5 = Image.open("result.png")
                        resized_image5 = image5.resize((500, 500), Image.ANTIALIAS)
                        test5 = ImageTk.PhotoImage(resized_image5)

                        labelim5 = Label(top_view, image=test5, bg='lightgray')
                        labelim5.image = test5
                        labelim5.place(x=0, y=0)
                    else:

                     imagelog = Image.open("logo.png")
                     resized_imagelog = imagelog.resize((40, 40), Image.ANTIALIAS)
                     testlog = ImageTk.PhotoImage(resized_imagelog)

                     labellog = Label(top_view, image=test, bg='lightgray')
                     labellog.imagelog = testlog
                     labellog.place(x=1,y=10)
                     print(selected)
                     l4 = Label(top_view, text="Health Security & Environment Department  Parahashan UIP ,\nSmart Panik",bg='lightgray')
                     l4.place(x=90, y=20)
                     l1=Label(top_view,text="Name :   "+df['Name'][df['Number_Plate']==temp[0]].values[0],bg='lightgray')
                     l1.place(x=10,y=80)
                     l2 = Label(top_view, text="Vehicle Number :   " + temp[0],
                                bg='lightgray')
                     l2.place(x=10, y=100)
                     l3 = Label(top_view, text="ID : " + temp[1],
                                bg='lightgray',fg='gray')
                     l3.place(x=360, y=80)
                     fr=Frame(top_view,width=300,height=400)
                     fr.configure(bg='lightgray')
                     fr.place(x=25,y=200)
                     list=[("Date","Amount"),(temp[3],temp[2]),("",""),("Total",temp[2])]
                     for row in range(4):
                         for col in range(2):
                             e=Entry(fr,width=30,bg='lightgray',fg='black')

                             e.grid(row=row,column=col)
                             e.insert(END,list[row][col])
                             e.configure(state='readonly',bg='lightgray')
                    l5=Label(top_view,text="You have a pending amountat Can -Stop cantina or 1580222",bg='lightgray')
                    l5.place(x=80, y=430)
                def down_pdf():
                    selected = tv.focus()
                    temp = tv.item(selected, 'values')
                    pdf = FPDF()
                    pdf.add_page()
                    pdf.image("logo.png", x=5, y=2, w=20, h=20, type='', link='')
                    pdf.set_font("Arial", size=15)
                    pdf.cell(200, 5, txt="Automated Number Plate", ln=1,
                             align='C')
                    pdf.cell(200, 20, txt="Name :   "+df['Name'][df['Number_Plate']==temp[0]].values[0],ln=2, align='L')
                    pdf.cell(200, 10, txt="Vehicle Number :   " + temp[0],ln=3, align='L')
                    pdf.cell(200, 1, txt="ID : " + temp[1], align='R')
                    epw = pdf.w - 2 * pdf.l_margin

                    # Set column width to 1/4 of effective page width to distribute content
                    # evenly across table and page
                    col_width = epw / 2

                    # Since we do not need to draw lines anymore, there is no need to separate
                    # headers from data matrix.

                    data = [["Date","Amount"],[temp[3],temp[2]],["",""],["Total",temp[2]]]



                    # Text height is the same as current font size
                    th = pdf.font_size



                    pdf.set_font('Times', 'B', 14.0)
                    pdf.cell(epw, 0.0, '', align='C',ln=5)
                    pdf.set_font('Times', '', 10.0)
                    pdf.ln(7)

                    # Here we add more padding by passing 2*th as height
                    for row in data:
                        for datum in row:
                            # Enter data in colums
                            pdf.cell(col_width, 2 * th, str(datum), border=1)

                        pdf.ln(2 * th)
                    pdf.cell(200, 80, txt="You have a pending amountat Can -Stop cantina or 1580222", ln=8, align='C')
                    pdf.cell(200, 10, txt="---------   THANKYOU   --------", ln=8, align='C')
                    pdf_name=""+temp[0]+".pdf"

                    pdf.output(pdf_name)



                button_view=Button(labelframe,text="      View      ",bg='blue',fg='white',command=open_view)
                button_view.place(x=740, y=360)
                button_down = Button(labelframe, text="   Download  ", bg='blue', fg='white',command=down_pdf)
                button_down.place(x=840, y=360)
                button_next = Button(labelframe, text="Next Vehicle ->", bg='green', fg='white',padx=7,pady=7, command=top.destroy)
                button_next.place(x=840, y=470)



                labelim2 = Label(labelframe, image=test2, bg='lightgray')
                labelim2.image = test2
                labelim2.place(x=20,y=80)

                label2 = Label(labelframe, text="Fine History Monitor", font=("Arial", 24), bg='lightgray')
                label2.place(x=int(0.2 * width1), y=10)

                label2 = Label(labelframe, text="Automated Number Plate Recognition", font=("Arial", 10),bg='lightgray')
                label2.place(x=int(0.225 * width1), y=50)
                label1.place(x=10, y=10)
                style = ttk.Style()
                style.theme_use("default")
                style.map("Treeview")

                top.mainloop()

        else:
            break

        if(len(read) != 0):
            cv2.rectangle(img, (x,y), (x+w, y+h), (51,51,255), 2)
            cv2.rectangle(img, (x, y - 40), (x + w, y),(51,51,255) , -1)
        cv2.putText(img,read, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
        cv2.imshow('Plate',plate)
        cv2.imwrite('./resultFolder/plate.jpg', plate)

    cv2.imshow("Result", img)



if(__name__ == "__main__"):

    i = int(input("Video Format => Press '1' \nImage Format => Press '2'"))
    if(i==1):
        j = int(input("Saved Video => Press '1' \nWebCam Video => Press '2'"))
        if(j==1):
            cap = cv2.VideoCapture("video2.mp4")
            frameCount = 1
            while True:
                ret,frame= cap.read()
                #image = frame
                frameCount += 1
                if ret is False:
                    break

                if(frameCount%30 == 0):
                    #print(frameCount)
                    extract_num(frame, True)

                key = cv2.waitKey(1)
                if key == 27:
                    break
        else:
            cap = cv2.VideoCapture(0)
            frameCount = 1
            while True:
                ret,frame= cap.read()
                #image = frame
                frameCount += 1
                if ret is False:
                    break

                if(frameCount%30 == 0):
                    #print(frameCount)
                    extract_num(frame, True)
                key = cv2.waitKey(1)
                if key == 27:
                    break

        #shutdown the VideoCapture
        cap.release()

    else:
        extract_num('download.jpg', False)
        cv2.waitKey(0)

    cv2.destroyAllWindows()
