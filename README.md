# Automatic-number-plate-recognition-using-open-cv-python
It can detect the number plate and checks the fine/tax have to be paid for that particular number plate id vehicle


Requirements : 
1) tesseract.exe file ( for text extracting supporter )
2) pytesseract package (for text extracting )
3) numpy package ( for utility extraction and rectangle subtraction )
4) pandas package ( for excel file comparison )
5) cv2 package (for video capture )
6) PIL package ( for image display )
7) fpdf package (to add data into pdf and download the pdf )
8) tkinter package (for gui display )
9) time package ( for current time display )



Usage : -

After installing run command "python3 main.py" in command prompt of same directory
After running , You get the gui interface describing to select the image or video, If you select 

 a) Image option , it detects single image and returns the number plate number and checks the id in the excel sheet ( DUMMY NP ) and compares the number plate id with tax of that particular id whether they paid or not , and it shows the data in the interface

b) Video Option , it divides video into photo frames and detects all vehicle numbers existed in the video. Lists the all numbers paid amount/tax have to be pay amound in the interface.






