from django.shortcuts import render
from .forms import NewRegistration,ChiefUserLogin
from .models import ChiefuserDetail   # for fetching admin details 
from django.contrib import messages
import cv2 as cv 
import os 
import numpy as np
import re
# from django.core import validators
# from django import forms

# Create your views here.


def admin_panel(request):
    return render(request, 'ChiefUser/admin_panel.html', {'title': "Admin Panel"})


# name of employee as global ..
nm = 'N'
def addANewEmp(request):
    # form_obj = NewRegistration()
    is_error = False
    if request.method == 'POST':
        form_obj = NewRegistration(request.POST)  # obj of class NewRegistration
        if form_obj.is_valid():
            global nm
            nm = form_obj.cleaned_data['name']
            em = form_obj.cleaned_data['email']
            ph = form_obj.cleaned_data['phone_no']
            pss = form_obj.cleaned_data['password']
            cpss = form_obj.cleaned_data['confirm_password']
            address = form_obj.cleaned_data['address']
            
            # print(nm)
            # print(em)
            # print(psswd)
            # print(cpass)
            
            
            # Name Validation 
            if nm.replace(" ", "").isalpha():
                pass
            else:
                is_error = True
                messages.error(request,"Have You forgotten the Name Huh? It's Invalid!")
                
            # Email Validation 
            if '@' in em:
                regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
                if(re.fullmatch(regex, em)):
                    pass
                else:
                    is_error = True
                    messages.error(request,'Invalid Email!')
            else:
                is_error = True
                messages.error(request,'Invalid Email!')

            #Phone no validation
            if len(ph) > 10 or len(ph) < 10:
                is_error = True
                messages.error(request,'Invalid Phone Number!')
            else:
                if ph.isdigit() == False:
                    is_error = True
                    messages.error(request,'Invalid Phone Number!')

            # password verification
            if len(pss) == 6 and len(cpss) == 6:
                if pss != cpss:
                    is_error = True
                    messages.error(request,'Password is not Matching!')
            else:
                is_error = True
                messages.error(request,'Password should Be 6 chars long!')

            # Address Validation 
            if len(address) < 3:
                is_error = True
                messages.error(request,'Invalid Address!')
            else:
                unwanted = ['@','#','$','%','^','*','!']
                for i in unwanted:
                    if i in address:
                        is_error = True
                        messages.error(request,'Invalid Address!')

            # If there is no error then save to database.
            if is_error == False:
                form_obj.save()
                print('successfully saved to the database.')


            # New Employee form validations Here....
            if len(nm) > 2 and not is_error:
                return render(request,'ChiefUser/faceSample.html',{'title':'faceSample'})
                # raise forms.ValidationError('Name should be greater than 2 Chars')
            
    else:
        form_obj = NewRegistration()
    return render(request,'ChiefUser/addNew.html',{'title': 'New employee Attachment','form':form_obj})



def admin_login(request):
    original_id = ""
    original_pass = ""
    if request.method == 'POST':
        fobj = ChiefUserLogin(request.POST)
        if fobj.is_valid():
            ide = fobj.cleaned_data['chiefUserId']
            pas = fobj.cleaned_data['password']
            
            # print(ide)
            # print(pas)
            chiefuserData = ChiefuserDetail.objects.all()   # fetching admin data from dB
            for i in chiefuserData:
                original_id = i.chiefUserId
                original_pass = i.password
            #validations on admin login id and password!!
            if ide == original_id and pas == original_pass:
                return render(request,'ChiefUser/admin_panel.html',{'title':'Admin_Panel'})
            else:
                # pass
                return render(request,'ChiefUser/adminLogin.html',{'title':'Admin Login','form':fobj,'error':True})   
    else:
        fobj = ChiefUserLogin()
    return render(request,'ChiefUser/adminLogin.html',{'title':'Admin Login','form':fobj})




def faceSamplePage(request):
    return render(request,'ChiefUser/faceSample.html',{'title':'Collecting Face Samples'})



def takeFaceSample(request):
    # print('The camera will start taking your picture.')

    import cv2 

    key = cv2. waitKey(1)
    webcam = cv2.VideoCapture(0)
    while True:
        try:
            check, frame = webcam.read()
            # print(check) #prints true as long as the webcam is running
            # print(frame) #prints matrix values of each framecd 
            cv2.imshow("Capturing", frame)
            key = cv2.waitKey(1)
            if key == ord('s'):
                fileName_path = f"/home/abhishek/dj/proje/core/static/core/sample_images/{nm}.jpg" 
                # cv2.imwrite(filename=f'{nm}.jpg', img=frame)
                cv2.imwrite(fileName_path, img=frame)
                # print(os.getcwd()) 
                # print(nm)
                webcam.release()
                # img_new = cv2.imread(f'{nm}.jpg', cv2.IMREAD_GRAYSCALE)
                # img_new = cv2.imshow("Captured Image", img_new)
                cv2.waitKey(1650)
                cv2.destroyAllWindows()
            
                print("Image saved!")
            
                break
            elif key == ord('q'):
                print("Turning off camera.")
                webcam.release()
                print("Camera off.")
                print("Program ended.")
                cv2.destroyAllWindows()
                break
            
        except(KeyboardInterrupt):
            print("Turning off camera.")
            webcam.release()
            print("Camera off.")
            print("Program ended.")
            cv2.destroyAllWindows()
            break

            # After collecting the face sample return back to admin home page
    return render(request,'ChiefUser/admin_panel.html',{'title':'after collecting face sample'})







