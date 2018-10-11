from django.shortcuts import render

def index(request):
    #return render(request,"Layout.html")
    return render(request,"App_Dashboard/content.html")
