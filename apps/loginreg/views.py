from django.shortcuts import render, redirect, HttpResponse
from .models import User, Trip
from django.contrib import messages
# Create your views here.
def index(request):
    # request.session.delete()
    request.session['magic'] = 'nhgbhnv'
    return render(request, 'loginreg/index.html')

def process(request):
    if request.method == "GET":
        messages.success(request, "Nice try!")
        return redirect('/')
    user = User.objects.register(request.POST)
    print user
    if user[0] == True:
        messages.success(request, 'Successful Registration! Please Log in')
        data = User.objects.filter(id=user[1].id)
        # print "this is the id: ", data
        request.session['id'] = data[0].id
        request.session['magic'] = 'registered'
    else:
        for i in user[1]:
            print i
            messages.success(request, i)
        return redirect('/')
    return redirect('/travels')

def loginProcess(request):
    if request.method == "GET":
        messages.success(request, "Nice try!")
        return redirect("/")
    frogs = User.objects.login(request.POST['emailLogin'], request.POST['pwLogin'])
    if frogs[0] == True:
        # print frogs[1], "="*50
        messages.success(request, 'Successful Logged In!')
        request.session['id'] = frogs[2].id
        request.session['magic'] = 'loggedin'
    else:
        for i in frogs[1]:
            # print i
            messages.success(request, i)
        return redirect('/')
    return redirect('/travels')

def travels(request):
    if "id" not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['id'])
        context = {
            "user": user
        }
    return render(request, 'loginreg/success.html', context)


def addplan(request):
    return render(request, "loginreg/addtravels.html")

def addProcess(request):
    userTrip = Trip.objects.addTrip(request.POST)
    if userTrip[0] == True:
        # print "="*50, userTrip[1], "="*50
        messages.success(request, 'Successful Added New Trip!')

        context = {
            "trip": Trip.objects.all()
        }

        return render(request, 'loginreg/success.html', context)
    else:
        for i in userTrip[1]:
            messages.success(request, i)
        return redirect('/add')
    return redirect('/travels')

def destroy(request, id):
    data = {
    'tripId': Trip.objects.get(id=id),
    "trips": Trip.objects.filter(id=id)
    }
    return render(request, 'loginreg/destroy.html', data)

def remove(request, id):
    # tripId = Trip.objects.get(id=id),
    trips = Trip.objects.filter(id=id).delete()
    return redirect('/travels')









def logout(request):
    if request.method == "GET":
        messages.success(request, "Nice try!")
        return redirect("/")

    request.session.clear()
    return redirect('/')
