from django.shortcuts import render

# Create your views here.
def login_page(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        password= request.POST.get('password')
        print(email,password)
    return render(request, 'auth/login.html')

def register(request):
    if request.method == 'POST':
        email= request.POST.get('email')
        password= request.POST.get('password')
        print(email,password)
    return render(request, 'auth/register.html')