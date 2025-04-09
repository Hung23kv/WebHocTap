from django.shortcuts import render

# Create your views here.
def homeChat(request):
    return render(request,'ChatHome.html')
def ChatDetail(request):
    return render(request,'ChatDetail.html')