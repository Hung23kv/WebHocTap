from django.shortcuts import render
from chat.models import Nguoidung,Khoahoc
# Create your views here.

def homeAdmin(request):
    users = Nguoidung.objects.exclude(quyen='admin')
    return render(request,'HomeAdmin.html',{'users':users})
def manageCoures(request):
    coures = Khoahoc.objects.all()
    return render(request,'ManageCoures.html',{'coures':coures})
