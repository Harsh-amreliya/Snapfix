from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,redirect
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from stores.models import storedata
from servicestore.models import servicestoredata
from stores.forms import addstoreform
from servicestore.forms import addservicestoreform
from servicestore.models import servicestoredata
from client.forms import liststorerequestform
from client.models import liststorerequest
from client.models import towingrequest
from client.models import productrequest
from . import forms
# Create your views here.


User = get_user_model()


# Create your views here.

def registerowner(request):
    admin_user = request.user
    admin_user2 = admin_user
    print(admin_user)
    form=forms.storedetail(request.POST)
    if request.method=='POST':
        if request.POST.get('username') and request.POST.get('email') and request.POST.get('password') and request.POST.get('user_role') :
            psd=request.POST.get('password')
            user_role = request.POST.get('user_role')
            is_store_owner = user_role == 'is_store_owner'
            is_service_store_owner = user_role == 'is_service_store_owner'
            username = request.POST.get('username')
            password = request.POST.get('password')

            if request.POST.get('password') == request.POST.get('password1'):
                try:
                    User.objects.get(username=request.POST.get('username'))
                    return render(request,'ad/Registerstoreuser.html',{'msg':'User Already Exists !!!'})
                except User.DoesNotExist:
                    user=User.objects.create_user(username=request.POST.get('username'),password=request.POST.get('password'), email=request.POST.get('email'))
                    user.is_store_owner = is_store_owner
                    user.is_service_store_owner = is_service_store_owner
                    user.save()

                    send_registration_email(user,psd,user_role)
                    return redirect(index)
            else:
                return render(request,'ad/Registerstoreuser.html',{'msg':'Password Doesnot Match !!!'})
        else:
            return render(request,'ad/Registerstoreuser.html',{'msg':'Please Enter Valid Credentials !!!'})

    return render(request,'ad/Registerstoreuser.html')

def send_registration_email(user,psd,user_role):
    subject = 'Registration Successful'
    role=" ".join(user_role.split("_")[1:])
    message = f'Thank you for registering on Snapfix!  Mr.{user.username}\n You can now join us using these Credentials:\n\nUsername: {user.username}\nPassword: {psd}\nYour Role: {role}'
    from_email = 'amreliyaharsh55@gmail.com'  # Replace with your email
    recipient_list = [user.email]

    send_mail(subject, message, from_email, recipient_list)

@login_required(login_url='/adminh/')
def index(request):
    listrequest = liststorerequest.objects.all()
    store=storedata.objects.count()
    inactivestore=storedata.objects.filter(is_activee=False).count()
    activestore=storedata.objects.filter(is_activee=True).filter(is_deleted=False).count()
    servicestore=servicestoredata.objects.count()
    inactiveservice=servicestoredata.objects.filter(is_activee=False).count()
    activeservice=servicestoredata.objects.filter(is_activee=True).filter(is_deleted=False).count()
    name=request.user
    servicerequests=towingrequest.objects.filter(completed=True).count()
    productorders=productrequest.objects.filter(completed=True).count()

    return render(request,'ad/index.html',{'store':store,'service':servicestore,'actstore':inactivestore,'actservice':inactiveservice,'activestore':activestore,'activeservice':activeservice,'request':listrequest,'name':name,'servicerequest':servicerequests,'productorders':productorders})

def addstore(request):
    return render(request,'ad/addstore.html')

def addservice(request):
    return render(request,'ad/addservice.html')

def managestore(request):
    data=storedata.objects.filter(is_deleted=False)
    return render(request,'ad/managestore.html',{'data':data})

def manageservice(request):
    data=servicestoredata.objects.filter(is_deleted=False)
    return render(request,'ad/manageservicestore.html',{'data':data})

def editservice(request,id):
    data=servicestoredata.objects.get(id=id)
    return render(request,'ad/editservice.html',{'data':data})

def editstore(request,id):
    data=storedata.objects.get(id=id)
    return render(request, 'ad/editstore.html', {'data': data})

def deleteservice(request,id):
    data=servicestoredata.objects.get(id=id)
    data.is_deleted=True
    data.save()
    return redirect(manageservice)

def deletestore(request,id):
    data=storedata.objects.get(id=id)
    data.is_deleted=True
    data.save()
    return redirect(managestore)

def storerequest(request):
    data=liststorerequest.objects.all()
    return render(request,'ad/storerequest.html',{'data':data})

def addnow(request,id):
    data=liststorerequest.objects.get(id=id)
    form = forms.storedetail(request.POST)
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('email') and request.POST.get(
                'password') and request.POST.get('user_role'):
            psd = request.POST.get('password')
            user_role = request.POST.get('user_role')
            is_store_owner = user_role == 'is_store_owner'
            is_service_store_owner = user_role == 'is_service_store_owner'
            username = request.POST.get('username')
            password = request.POST.get('password')

            if request.POST.get('password') == request.POST.get('password1'):
                try:
                    User.objects.get(username=request.POST.get('username'))
                    return render(request, 'ad/Registerstoreuser.html', {'msg': 'User Already Exists !!!','data':data})
                except User.DoesNotExist:
                    user = User.objects.create_user(username=request.POST.get('username'),password=request.POST.get('password'),email=request.POST.get('email'))
                    user.is_store_owner = is_store_owner
                    user.is_service_store_owner = is_service_store_owner
                    user.save()
                    data.listed=True
                    data.save()

                    send_registration_email(user, psd, user_role)
                    return redirect(index)
            else:
                return render(request, 'ad/Registerstoreuser.html', {'msg': 'Password Doesnot Match !!!','data':data})
        else:
            return render(request, 'ad/Registerstoreuser.html', {'msg': 'Please Enter Valid Credentials !!!','data':data})
    return render(request,'ad/Registerstoreuser.html',{'data':data})

def adupdatestore(request,id):
    data=storedata.objects.get(id=id)
    form=addstoreform(request.POST,request.FILES,instance=data)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect(managestore)
        else:
            return render(request,'ad/editstore.html',{'msg':'Invalid Input'})
    return render(request,'ad/editstore.html',{'data':data})

def adupdateservice(request,id):
    data=servicestoredata.objects.get(id=id)
    form=addservicestoreform(request.POST,request.FILES,instance=data)
    if request.method=='POST':
        if form.is_valid():
            form.save()
            return redirect(manageservice)
        else:
            return render(request,'ad/editservice.html',{'msg':'Invalid Input'})
    return render(request,'ad/editservice.html',{'data':data})

def addstoreuser(request):
    return render(request,'ad/registerstoreuser.html')

def removerequest(request,id):
    data=liststorerequest.objects.filter(id=id)
    data.delete()
    return redirect(storerequest)

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)

        if user is not None:

            if user.is_admin:
                auth.login(request,user)
                return redirect(index)
            else:
                return render(request,'ad/login.html',{'msg':'No Role defined'})
        else:
            return render(request,'ad/login.html',{'msg':'Invalid Credentials !!'})
    return render(request,'ad/login.html')

def logout(request):
    auth.logout(request)
    return redirect(login)
