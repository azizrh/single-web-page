from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect


from main.models import List,Item
from .forms import CreateNewList
from django.contrib.auth.decorators import login_required

@login_required(login_url='/login/')
# Create your views here.
def index(response, name):
    ls = List.objects.get(name=name)
 
    if response.method == "POST":
        print(response.POST)
        if response.POST.get("save"):
            for item in ls.item_set.all():
                item.save()

        elif response.POST.get("newItem"):
            txt = response.POST.get("new")
            lnk = response.POST.get("newLink")
    
            if len(txt) > 2:
                ls.item_set.create(text=txt, link=lnk)
            else:
                print("invalid")

    return render(response, "main/list.html", {"ls":ls})

@login_required(login_url='/login/')
def home(response):
    return render(response, "main/home.html",{"name":"test"})

@login_required(login_url='/login/')
def create(response):
    if response.method == "POST":
        form = CreateNewList(response.POST)
        #validating and creating new list

        if form.is_valid(): 
            n = form.cleaned_data["name"]
            t = List(name=n)
            t.save()

        return HttpResponseRedirect("/%i" %t.id)
    else: 
        form = CreateNewList()


    return render(response, "main/create.html",{"form":form})


