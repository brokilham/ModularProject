from django.shortcuts import render
from django.contrib.auth import authenticate, login,logout
from django.http import JsonResponse,HttpResponseRedirect

def index(request):
    #return render(request,"Layout.html")
    return render(request,"App_Accounts/index.html")


def login_process(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return JsonResponse({'status':'s','result':'now you login'})
        else:
            data = 'username or password in not valid'
            return JsonResponse({'status':'e','result':data})
    except ValueError  as Argument: 
        return JsonResponse({'status':'e','result':Argument})

def logout_process(request):
    try:
        logout(request)
        return HttpResponseRedirect('login')
    except ValueError as Argument:
        return JsonResponse({'status':'e','result':Argument})    
   
   

