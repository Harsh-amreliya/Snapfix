import json
from django.contrib import auth
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,HttpResponse,redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from geopy.exc import GeocoderTimedOut
from stores.models import storedata, productlisting
from . import forms,models
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from .utils import convert_amount_to_words
from geopy import distance as geopy_distance
# from geopy.distance import vincenty ------------------------- another function to calculate distance
from servicestore.models import servicestoredata
from servicestore.models import servicelisting
from math import radians, sin, cos, sqrt, atan2
from django.forms.models import model_to_dict



from . import models
from .models import UserLocation
User = get_user_model()

# Create your views here.
# @login_required(login_url='/client/')
def index(request):

    # data=storedata.objects.filter(is_activee=True)
    totalservices=[]
    service=servicestoredata.objects.filter(is_activee=True).filter(is_deleted=False)

    try: 
        for d in service:
            data=models.servicelisting.objects.filter(store=d).filter(active=True).count()
            totalservices.append(data)
    except:
        print("no stores found")

    store = []
    if len(service) > 5:
        for i in range(5):
           store.append(service[i])
    else:
        store=service

    # if len(data) > 5:
    #     for i in range(5):
    #        store.data(service[i])
    # else:
    #     store=data
    maindata=zip(store,totalservices)
    return render(request,'cl/index.html',{'maindata':maindata})

def fetchstore(request,storetype):
    totalproducts=[]


    if storetype=="product":
        data=storedata.objects.filter(is_activee=True).filter(is_deleted=False)
        try:
            for d in data:
                tproduct=models.productlisting.objects.filter(store=d).filter(active=True).count()
                totalproducts.append(tproduct)
        except:
            print("no productstores listed")

    elif storetype=="service":

        data=servicestoredata.objects.filter(is_activee=True).filter(is_deleted=False)
        try:
            for d in data:
                tservice = models.servicelisting.objects.filter(store=d).filter(active=True).count()
                totalproducts.append(tservice)

        except:
            print("no servicestores listed")


    if totalproducts:

        data_list= {}
        for index,dataObj in enumerate(data):
            data_list[index] = {"storename":dataObj.storename,"storecontact":dataObj.storecontact,"email":dataObj.email,"storeaddress":dataObj.storeaddress,"id":dataObj.id,"imageofstore":dataObj.imageofstore.url, "totalproducts":totalproducts[index]}

    else:
        data_list = {}
        for index, dataObj in enumerate(data):
            data_list[index] = {"storename": dataObj.storename, "storecontact": dataObj.storecontact,
                                "email": dataObj.email, "storeaddress": dataObj.storeaddress, "id": dataObj.id,
                                "imageofstore": dataObj.imageofstore.url, "totalproducts": totalproducts[index]}

    return JsonResponse(data_list)

def requeststorelisting(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        type = request.POST.get('type')
        storename = request.POST.get('storename')

        data=models.liststorerequest
        data.objects.create(
            username=username,
            email=email,
            type=type,
            storename=storename,
            listed=False
        )


        return JsonResponse({'message' : 'Your request has been submitted successfully!!'})

    return JsonResponse({1 : 1})

def about(request):
    return render(request,'cl/about.html')

def service(request):
    data=servicestoredata.objects.filter(is_activee=True).filter(is_deleted=False)
    totalproducts=[]
    try:
        for d in data:
            tservice = models.servicelisting.objects.filter(store=d).filter(active=True).count()
            totalproducts.append(tservice)
    except:
        print("no servicestores listed")
    maindata=zip(data,totalproducts)
    return render(request,'cl/service.html',{'maindata':maindata})

def contact(request):
    return render(request,'cl/contact.html')
@login_required(login_url='/cl-login/')
def cartdetails(request,id,storeid):
    servempty = 0
    servicesincart = models.mycart.objects.filter(user=id).filter(serviceid__store__id=storeid)
    newstoreid=storeid



    data=models.mycart.objects.filter(user=id)
    cartdata=models.mycart.objects.filter(user=id).filter(serviceid__isnull=False)
    servempty=len(cartdata)
    # cartdata2={}
    # for i, a in enumerate(cartdata):
    #     cartdata2[i]={'serviceid': a.serviceid.id,'serviceimage': a.serviceid.serviceimage,'servicename': a.serviceid.servicename,'serviceprice': a.serviceid.serviceprice,'towable': a.serviceid.towable,'store':a.serviceid.store.id}

    # ----------------------------------------------.filter(serviceid__store__id = 1 )---------------------for multiple foreignkey value------------------------

    storeid=models.mycart.objects.filter(user=id).filter(serviceid__isnull=False).values('serviceid__store_id')
    storeidlist=[]
    for d in storeid:
        storeidlist.append(d["serviceid__store_id"])

    storeidlist=list(set(storeidlist))

    if len(servicesincart) == 0 and len(storeidlist) > 0:
        newstoreid=storeidlist[0]

    storeservicesdetails={}
    for d in storeidlist:
        a=servicestoredata.objects.get(id=d)
        storename=a.storename
        storeservicesdetails[d]= {'services':0,'storename':storename,'towing':0}

    for storeid in storeidlist:
        for service in cartdata:
            if service.serviceid.store.id == storeid:
                a=servicelisting.objects.get(id=service.serviceid.id)
                towing=a.towable
                if towing:
                    storeservicesdetails[storeid]['towing'] = 1
                storeservicesdetails[storeid]['services']+=1



    # servempty=len(storeservicesdetails)
    # storeservicesdetails['servempty']=servempty

    if newstoreid:
        return render(request, 'cl/cart.html',{'data': data, 'storeobj': storeservicesdetails, 'storeid': newstoreid, 'servempty':servempty})
    try:
        return render(request,'cl/cart.html',{'data':data,'storeobj':storeservicesdetails,'storeid':storeidlist[0], 'servempty':servempty})
    except:
        return render(request,'cl/cart.html',{'data':data,'storeobj':storeservicesdetails, 'servempty':servempty})


def dynamiccartdata(request,id,storeid):
    cartdata=models.mycart.objects.filter(user=id).filter(serviceid__store__id = storeid)
    cartdata2 = models.mycart.objects.filter(user=id).filter(serviceid__isnull=False)
    servempty = len(cartdata2)



    listdetails={}
    noservice={}
    for i, a in enumerate(cartdata):

        listdetails[i]={'serviceid':a.serviceid.id,'serviceimage':a.serviceid.serviceimage.url,'servicename':a.serviceid.servicename,'serviceprice':a.serviceid.serviceprice,'towable':a.serviceid.towable,'avgtime':a.serviceid.avgtime,'storeid':a.serviceid.store.id}

    noservice['servempty']=servempty

    if servempty > 0 and storeid == 0:
        print(storeid)
        storeid=listdetails[0]['storeid']

        dynamiccartdata(request,id,storeid)



    combined_data = {
        'listdetails': listdetails,
        'noservice': noservice
    }
    return JsonResponse(combined_data)

def dynamicproductdata(request,id,type):
    isempty=0
    if type == 'product':
        cartdata = models.mycart.objects.filter(user=id).filter(productid__isnull=False)

        listdetails = {}
        for i, a in enumerate(cartdata):

            listdetails[i] = {'cartid':a.id,'productid': a.productid.id, 'productimage': a.productid.productimage.url,
                              'productname': a.productid.productname, 'productprice': a.productid.productprice,
                              'storeid': a.productid.store.id,'quantity':a.quantity}
        isempty=len(listdetails)
        listdetails['isempty']=isempty
        return JsonResponse(listdetails)
    else:
        return redirect(cartdetails,id,0)


@login_required(login_url='/cl-login/')
def payment(request,storeid,type):

    if type == "service":
        cartdata = models.mycart.objects.filter(user=request.user).filter(serviceid__store__id=storeid)

        amount=0
        items=0
        istowable=0
        for d in cartdata:
            storename=d.serviceid.store.storename
            amount+=(d.serviceid.serviceprice)*(d.quantity)
            items+=1
            if d.serviceid.towable:
                istowable=1
        isservice=1
        return render(request,'cl/payment.html',{'totalamount':amount,'totalitems':items,'istowable':istowable,'storename':storename,'isservice':isservice,'storeid':storeid})
    elif type == "product":
        cartdata = models.mycart.objects.filter(user=request.user).filter(productid__isnull=False)
        amount = 0
        items = 0
        storename=[]
        for d in cartdata:
            storename.append(d.productid.store.storename)
            amount += (d.productid.productprice) * (d.quantity)
            items += 1
        productstorename=list(set(storename))
        isproduct=1
        return render(request,'cl/payment.html',{'totalamount':amount,'totalitems':items,'productstorename':productstorename,'isproduct':isproduct,'storeid':storeid})

def login(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=auth.authenticate(username=username,password=password)

        if user is not None:

            if user.is_store_owner:
                return render(request,'cl/login.html',{'msg':'Sorry you Cannot login with Store id'})
            elif user.is_service_store_owner:
                return render(request,'cl/login.html',{'msg':'Sorry you Cannot login with Servicestore id'})
            elif user.is_admin:
                return render(request,'cl/login.html',{'msg':'Sorry you Cannot login with admin id'})
            else:
                auth.login(request,user)
                return redirect(index)
        else:
            return render(request,'cl/login.html',{'msg':'Invalid Credentials !!'})

    return render(request,'cl/login.html')

def register(request):
    if request.method == 'POST':
        if request.POST.get('username') and request.POST.get('email') and request.POST.get('password'):
            if request.POST.get('password') == request.POST.get('password1'):
                try:
                    User.objects.get(username=request.POST.get('username'))
                    return render(request, 'cl/register.html', {'msg': 'User Already Exists!!!'})
                except User.DoesNotExist:
                    user = User.objects.create_user(username=request.POST.get('username'),password=request.POST.get('password'), email=request.POST.get('email'))
                    return redirect(login)
            else:
                return render(request, 'cl/register.html', {'msg': 'Password Doesnot Match !!!'})
        else:
            return render(request, 'cl/register.html', {'msg': 'Invalid Input!!!'})

    return render(request, 'cl/register.html')

def stores(request,id):
    data=servicestoredata.objects.get(id=id)
    servicedata=servicelisting.objects.filter(store=id).filter(active=True)
    try:
        cart=models.mycart.objects.filter(user=request.user)
        cartid=[]
        for serviceid in cart:
            try:
                if serviceid.id:
                    cartid.append(serviceid.serviceid.id)
            except:
                print('success')
    except:
        cartid=[]
    return render(request,'cl/store.html',{'data':data, 'servicedata':servicedata,'storeid':id,'cart':cartid})

def products(request,id):
    data=storedata.objects.get(id=id)
    productdata=productlisting.objects.filter(store=id).filter(active=True)
    try:
        cart=models.mycart.objects.filter(user=request.user)
        cartid = []
        for productid in cart:
            try:
                if productid.id:
                    cartid.append(productid.productid.id)
            except:
                print('success')
    except:
        cartid=[]
    return render(request, 'cl/store.html', {'data': data, 'productdata': productdata, 'cart': cartid, 'storeid': id})

neareststores={}
@csrf_exempt
def nearbystore(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        user_latitude = data.get('latitude')
        user_longitude = data.get('longitude')

        # Find stores near the entered location (you can customize the logic)
        user_location = (user_latitude, user_longitude)

        geolocator = Nominatim(user_agent="Harsh55")
        nearby_stores = []

        # Create a list to store stores with their distances
        stores_with_distances = []

        for store in storedata.objects.filter(is_activee = True).filter(is_deleted=False):
            store_address = store.storeaddress
            try:
                store_location = geolocator.geocode(store_address)
                store_latitude, store_longitude = store_location.latitude, store_location.longitude

                # Extract the city from the geocoded address
                city = store_location.raw.get('address', {}).get('city', '')
            except (AttributeError, GeocoderTimedOut):
                continue

            store_coords = (store_latitude, store_longitude)
            distance = calculate_distance(user_location, store_coords)

            # Append the store, its distance, and city to the list
            stores_with_distances.append({'store_id': store.id, 'distance': round(distance,2)})

        # Sort stores by city and then by distance within each city
        stores_with_distances.sort(key=lambda x: ( x['distance']))

        # Extract the sorted store information for rendering
        sorted_stores_info = [{'store_id': store_info['store_id'], 'distance': store_info['distance']} for store_info in stores_with_distances]
        km=float(25)

        nearest=[]
        for i in range(len(sorted_stores_info)):
            if sorted_stores_info[i]['distance'] < km:
                nearest.append(stores_with_distances[i])

        global neareststores
        neareststores['product']=nearest
        print(neareststores)

        stores_with_distances=[]
        for store in servicestoredata.objects.filter(is_activee = True).filter(is_deleted=False):
            store_address = store.storeaddress
            try:
                store_location = geolocator.geocode(store_address)
                store_latitude, store_longitude = store_location.latitude, store_location.longitude

                # Extract the city from the geocoded address
                city = store_location.raw.get('address', {}).get('city', '')
            except (AttributeError, GeocoderTimedOut):
                continue

            store_coords = (store_latitude, store_longitude)
            distance = calculate_distance(user_location, store_coords)

            # Append the store, its distance, and city to the list
            stores_with_distances.append({'store_id': store.id, 'distance': round(distance,2)})

        # Sort stores by city and then by distance within each city
        stores_with_distances.sort(key=lambda x: (x['distance']))

        # Extract the sorted store information for rendering
        sorted_stores_info = [{'store_id': store_info['store_id'], 'distance': store_info['distance']} for store_info in stores_with_distances]
        km=float(25)

        nearest2=[]
        for i in range(len(sorted_stores_info)):
            if sorted_stores_info[i]['distance'] < km:
                nearest2.append(stores_with_distances[i])

        neareststores['service']=nearest2
        print(neareststores)

        return render(request, 'cl/nearbystore.html', {'store_info': sorted_stores_info})

    return render(request, 'cl/nearbystore.html')


def nearbystore_active(request,storetype):
    data=[]
    distance={}
    if storetype.lower() == "product store":
        target = "product"
        for a in neareststores[target]:
            data.append(storedata.objects.get(id=a['store_id']))
            tproduct = models.productlisting.objects.filter(store=a['store_id']).filter(active=True).count()
            temp_list=[a['distance'],tproduct]
            distance[a['store_id']]=temp_list

    else:
        target = "service"
        for a in neareststores[target]:
            data.append(servicestoredata.objects.get(id=a['store_id']))
            tproduct = models.servicelisting.objects.filter(store=a['store_id']).filter(active=True).count()
            temp_list = [a['distance'], tproduct]
            distance[a['store_id']] = temp_list

    data_list = {}
    for index, dataObj in enumerate(data):
        data_list[index] = {"storename": dataObj.storename, "storecontact": dataObj.storecontact,
                            "email": dataObj.email, "storeaddress": dataObj.storeaddress, "id": dataObj.id,
                            "imageofstore": dataObj.imageofstore.url, "totalproducts": distance[dataObj.id][1],'distance':distance[dataObj.id][0]}

    return JsonResponse(data_list)

def calculate_distance(coord1, coord2):
    # Radius of the Earth in kilometers
    R = 6371.0

    # Convert latitude and longitude from degrees to radians
    lat1, lon1 = radians(coord1[0]), radians(coord1[1])
    lat2, lon2 = radians(coord2[0]), radians(coord2[1])

    # Calculate differences in coordinates
    dlat = lat2 - lat1
    dlon = lon2 - lon1

    # Haversine formula to calculate distance
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    # Distance in kilometers
    distance = R * c
    # return vincenty(coord1, coord2).km -----------------another method to calculate distance
    return distance

def logout(request):
    auth.logout(request)
    return redirect(login)

@login_required(login_url='/cl-login/')
def addtocartproduct(request,id,storeid):
    form=forms.cartform(request.POST)
    product=productlisting.objects.get(id=id)

    # if request.method=='POST':
    #     if form.is_valid():
    #         data=form.save(commit=False)                          
    #         data.user=request.user
    #         data.productid=product
    #         data.save()
    #     else:
    #         print(form.errors)
    #         return HttpResponse('Invalid!!')
    idofproduct = productlisting.objects.get(id=id)
    service = models.mycart
    try:
        service.objects.create(productid=idofproduct, user=request.user)
        return JsonResponse({"message" : 'added'})
    except:
        print('except block')
    return JsonResponse({1:1})

@login_required(login_url='/cl-login/')
def addtocartservice(request,id,storeid):
    # form=forms.cartform(request.POST) ----------------------another method using form-------------------------------
    # if request.method=='POST':
    #     if form.is_valid():
    #         data=form.save(commit=False)
    #         data.user=request.user
    #         data.serviceid=service
    #         data.save()
    idofservice=servicelisting.objects.get(id=id)
    service=models.mycart
    try:
        service.objects.create(serviceid=idofservice,user=request.user)
        return JsonResponse({"message" : 'added'})
    except:
        print('except block')
    return JsonResponse({1:1})

def removeservice(request,id,storeid):
    userid=request.user.id
    data=models.mycart.objects.filter(serviceid=id)
    data.delete()

    return redirect(cartdetails,userid,storeid)

def removeproduct(request,id,storeid):
    userid=request.user.id
    data=models.mycart.objects.filter(productid=id)
    data.delete()

    return redirect(cartdetails,userid,storeid)

def servicelistinfo(request):
    data=models.mycart.objects.filter(user=request.user)
    print(data)

def updatequantity(request,cartid,type):

    if type =='increment':
        data=models.mycart.objects.get(id=cartid)
        data.quantity +=1
        data.save()

    elif type == 'decrement':
        data = models.mycart.objects.get(id=cartid)
        if data.quantity == 1:
            return JsonResponse({1:1})
        data.quantity -= 1
        data.save()
    return JsonResponse({'1':'1'})

def towingorder(request,storeid,istowable):
    serviceid=models.mycart.objects.filter(user=request.user).filter(serviceid__store=storeid)
    # servicequantity=models.mycart.objects.filter(user=request.user).filter(serviceid__store=storeid).values('quantity')

    # quantityy=[]
    # for value in servicequantity:
    #    quantityy.append(value['quantity'])

    serviceidlist=""
    for id in serviceid:
        serviceidlist=serviceidlist+str((id.serviceid.id))+"-"

    idfordelete=serviceidlist.split('-')
    idfordelete.pop()
    totlprice=0
    for a in idfordelete:

        cartdata=models.mycart.objects.filter(user=request.user).filter(serviceid=a)
        cartdata.delete()

        price=models.servicelisting.objects.get(id=a)
        totlprice+=price.serviceprice
    s=0
    if request.method=='POST':

        a=models.towingrequest
        a.objects.create(contact=request.POST.get('contact'),additionalprobleminfo=request.POST.get('additionalprobleminfo'),clientlocation=request.POST.get('clientlocation'),email=request.POST.get('email'),name=request.POST.get('name'),user=request.user,serviceid=serviceidlist,storeid=storeid,totalprice=totlprice,istowable=istowable)
        s=1
        return render(request,'cl/confirmed.html',{'s':s})
    else:
        return HttpResponse('error')

def productorder(request):
    productdtid=models.mycart.objects.filter(user=request.user).filter(productid__isnull=False)
    productiddict={}
    totalprice=0
    for a in productdtid:
        totalprice+=a.productid.productprice
        productiddict[a.productid.id]=a.quantity
    p=0
    if request.method=='POST':

        a=models.productrequest
        a.objects.create(contact=request.POST.get('contact'),address=request.POST.get('address'),name=request.POST.get('name'),email=request.POST.get('email'),productid=productiddict,totalprice=totalprice,user=request.user)
        productdtid.delete()
        p=1
        return render(request,'cl/confirmed.html',{'p':p})
    else:
        return HttpResponse('error')

@login_required(login_url='/cl-login/')
def myorders(request,id):
    orderdata=models.towingrequest.objects.filter(user=id)
    serviceidlist=[]
    servicedetails={}

    try:
        for a in orderdata:
            serviceidlist.clear()

            serviceidlist=a.serviceid.split('-')
            serviceidlist.pop()
            services=[]

            for s in serviceidlist:
                service = servicelisting.objects.get(id=s)
                services.append(service)
                servicedetails[a.id]=services

    except:
        print('hello')
    return render(request,'cl/myorders.html',{'orderdata':orderdata,'servicedetails':servicedetails})

@login_required(login_url='/cl-login/')
def productorders(request,id):
    orderdata=models.productrequest.objects.filter(user=id)
    order = {}

    for index in orderdata:
        product_id_dict = eval(index.productid)
        for key in product_id_dict:
            pid = models.productlisting.objects.get(id=key)
            if index not in order:
                order[index] = []  # Initialize the list if it doesn't exist
            order[index].append(pid)

    return render(request,'cl/myproductorders.html',{'productdetails':order})
#
# def myorders(request, id):
#     orderdata = models.towingrequest.objects.filter(user=id)
#     servicedetails = {}
#
#     try:
#         for order in orderdata:
#             serviceidlist = order.serviceid.split('-')
#             serviceidlist.pop()
#             services = []  # Create a new list for each order
#
#             for service_id in serviceidlist:
#                 service = servicelisting.objects.get(id=service_id)
#                 services.append(service)
#
#             servicedetails[order.id] = services
#         print(orderdata)
#         print(servicedetails)
#         orderdetails = zip(orderdata, servicedetails.values())
#         return render(request, 'cl/myorders.html', {'orderdata': orderdetails})
#
#     except Exception as e:
#         print('Error:', e)
#         # Handle the exception gracefully
#         return HttpResponse("An error occurred while processing your request.")

def confirmed(request):
    return render(request,'cl/confirmed.html')

def myorderinvoice(request,orderid):

        orderdata=models.towingrequest.objects.get(id=orderid)

        serviceidlist=orderdata.serviceid.split('-')
        serviceidlist.pop()
        servicedata=[]
        amount=0
        towing=0
        for i in serviceidlist:
            s=models.servicelisting.objects.get(id=i)
            amount+=s.serviceprice
            if s.towable:
                towing=1
            servicedata.append(s)
        totlamount=0
        if towing:
            totlamount=amount+300
            gst = ((amount+300) * 18) / 100
            amtwithgst = totlamount + gst
        else:
            gst = (amount * 18) / 100
            amtwithgst = amount + gst
        word = convert_amount_to_words(int(amtwithgst))

        storedetails=servicestoredata.objects.get(id=orderdata.storeid)

        return render(request,'cl/myorderinvoice.html',{'orderdata':orderdata,'servicedata':servicedata,'amount':amount,'words':word,'towing':towing,'amount':amount,'gst':gst,'amtwithgst':amtwithgst,'totlamount':totlamount,'storedetails':storedetails})

def product_invoice(request,orderid):
    orderdata = models.productrequest.objects.get(id=orderid)
    order = []
    amount = 0
    product_id_dict = eval(orderdata.productid)
    storeid=[]
    for key in product_id_dict:
        pid = models.productlisting.objects.get(id=key)
        storeid.append(pid.store)
        pid.quantity = product_id_dict[key]
        amount += pid.productprice * pid.quantity
        order.append(pid)

    gst = (amount * 18) / 100
    amtwithgst = amount + gst
    words = convert_amount_to_words(int(amtwithgst))
    storeid1=set(storeid)
    storeid=list(storeid1)
    return render(request, 'cl/my_product_invoice.html',
                  {'words': words, 'amount': amount, 'gst': gst, 'amtwithgst': amtwithgst, 'order': order,
                    'storeid':storeid, 'orderdata': orderdata})



def update_location(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        latitude = data.get('latitude')
        longitude = data.get('longitude')

        # Reverse geocoding using Nominatim
        geolocator = Nominatim(user_agent="your_application_name")
        location = geolocator.reverse((latitude, longitude))

        if location:
            formatted_address = location.address
            # Do something with formatted address, such as saving to the database
            return JsonResponse({'status': 'Location updated successfully', 'formatted_address': formatted_address})
        else:
            return JsonResponse({'error': 'Failed to reverse geocode the location'})
    else:
        return JsonResponse({'error': 'Invalid request method'})

