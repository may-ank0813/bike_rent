from unicodedata import name
from django.shortcuts import render, get_object_or_404,redirect
from .models import *
from .forms import *
from django.core.mail import send_mail
from django.contrib import messages
import itertools 
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, logout, login
from json import dumps 
from datetime import datetime, timedelta, date
from django.db.models import Count, Sum, Max
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def home(request):
    faqs            = Faq.objects.all()
    bikes           = Bike.objects.all()
    # #2 row list under the search
    bikeLatest       = Bike.objects.all()[0:3]
    bikeLatestSecond = Bike.objects.all()[4:10]
    current  = request.user

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
    

    context={'bikes':bikes,
    'bikeLatest':bikeLatest,
    'bikeLatestSecond':bikeLatestSecond,
    'faqs':faqs,
    'current':current
    }
    return render(request,'home.html', context)

def registerPage(request):
    current = request.user
    forms = createUserForm()
    if request.method == 'POST':
        forms = createUserForm(request.POST)
        
        if forms.is_valid():
            forms.save()
            user = forms.cleaned_data.get('username')
            messages.success(request, 'Account was created for' + user +', log in' )
            return redirect('home')
  
    context={
        'forms'     :forms,
        'current'   :current
         }
    return render(request,'register.html', context)

@login_required(login_url='home.html')
def logoutPage(request):
    logout(request)
    return redirect('home')

def bike_list(request):
    current = request.user
    bike = Bike.objects.all()
    print(bike)
    query = request.GET.get('q')
    if query:
        bike = bike.filter(
                     Q(name__icontains=query) |
                     Q(model__icontains = query) |
                     Q(price__icontains=query)
                            )
    
    # pagination
    paginator = Paginator(bike, 12)  # Show 15 contacts per page
    page = request.GET.get('page')
    try:
        bike = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        bike = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        bike = paginator.page(paginator.num_pages)
    context = {
        'bike': bike,
        'current'   :current
    }
    
    return render(request, 'bikelist.html', context)

def bikePage(request,id=None):
    current  = request.user
    bikepage = get_object_or_404(Bike,id=id)
    # bikepage= Bike.objects.get(Bike,id=id)

    if request.method  == 'POST':
        message_name    =   request.POST['name'] +' '   + " "+request.POST['number']
        message_email   =   request.POST['email']
        message   =   request.POST['message']
        send_mail(
            message_name,
            message,
            message_email,
            ['mayanksaini0813@gmail.com'],
            fail_silently=False
        )
    context = {'bikepage': bikepage,'current'   :current}
    return render(request,'bike.html',context)


@login_required(login_url='home.html')
def createOrder(request,id):
    dataHolder  = []
    dataClean   = []
    current     = request.user
    bikeData     = Bike.objects.get(id=id)
    pickupPlace = Location.objects.all()
    rawData     = Order.objects.filter(automobileId=id)
    
    
    #making a list of blocked days for date picker 
    for x in rawData:
        if x.endRent > datetime.now().date():
            sdate = x.startRent
            edate = x.endRent
            delta = edate - sdate
            dataHolder = [ (sdate + timedelta(days=i)) for i in range(delta.days + 1) ]
    
    dataClean = [ x.strftime("%Y/%m/%d") for x in dataHolder]
    dataClean = dumps(dataClean)
      
    context={
        'current':current,
        'bikeData':bikeData,
        'dataClean':dataClean,
        'pickupPlace':pickupPlace,
        }
    return render ( request, 'renting.html', context,)

@login_required(login_url='home.html')
def customerPage(request,id):
    
    current     = request.user
    dataHolder  = Order.objects.filter(customerID=current.id)
    totalPrice  = list(dataHolder.aggregate(Sum('price')).values())[0]
    orderList   = reversed(dataHolder)
    lastOrder   = dataHolder.last()
    favCar      = dataHolder.values('bikeModel').annotate(car_count=Count('bikeModel'))
    if not favCar:
        favCarList  = "Rent something ;)"
    else:
        favCarList  = list(favCar.aggregate(Max('bikeModel')).values())
        favCarList  = favCarList[0].replace("['']",'')

    
    context = {
        'current'    :current,
        'orderList'  :orderList,
        'lastOrder'  :lastOrder,
        'totalPrice' :totalPrice,
        'favCarList' :favCarList,
        'dataHolder' :dataHolder,
    }
    return render(request,'order.html',context)

@login_required(login_url='home.html')
def makeOrder(request, id):
   
    bike       = Bike.objects.get(id=id)
    startDate = request.POST['startDate']
    endDate   = request.POST['endDate']
    current   = request.user
    
    
    format    = "%Y/%m/%d"
    if (request.method == 'POST' and endDate > startDate):
        sdate       = datetime.strptime(startDate, format)
        edate       = datetime.strptime(endDate, format)
        daysTotal   = edate - sdate
        priceTotal       = int(daysTotal.days)*int(bike.price)
        place       = Location.objects.get(id=request.POST['pickUpPlace'])


        addingToBase  = Order(customer=current,customerID=current.id,bikeModel=bike.model,automobileId=bike.id,price=priceTotal,startRent=sdate ,endRent=edate ,pickUp=place)
        addingToBase.save()
        currentOrder = addingToBase.id
            

    context={
        'bike'         :bike, 
        'place'        :place,
        'endDate'      :endDate,
        'current'      :current,
        'startDate'    :startDate,
        'currentOrder' :currentOrder,
        'priceTotal' : priceTotal,
        }
    return render ( request, 'confirm.html', context,)

            

@login_required(login_url='home.html')
def cancelOrder(request,id):
   
    order           = Order.objects.get(id=id)
    orderForCancel  = canceledOrders(customerID=order.customerID,price=order.price,automobileId=order.automobileId)
    orderForCancel.save()
    order.delete()

   
    return redirect ('home')


def gallery(request):
    current     = request.user
    picList = ['bike1','bike2','bike3']
    pictureList = []
    
    for x in picList:
        photo = Bike.objects.values_list(x)
        pictureList.append(photo)
   
    data = list(itertools.chain(*pictureList)) 
    data = list(itertools.chain(*data)) 
    data = list(filter(None, data))

    context = {
        'data':data[::-1],
        'current' : current
    }

    return render ( request, 'gallery.html', context)

