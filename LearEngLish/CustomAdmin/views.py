from django.shortcuts import render, redirect
from chat.models import Nguoidung,Khoahoc
from home.views import nguoidung_dang_nhap
# Create your views here.

def homeAdmin(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    if nguoidung.quyen != 'admin':
        return redirect('dang_nhap') 
    users = Nguoidung.objects.exclude(quyen='admin')
    return render(request,'HomeAdmin.html',{'users':users})
def manageCoures(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    if nguoidung.quyen != 'admin':
        return redirect('dang_nhap')
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    coures = Khoahoc.objects.all()
    return render(request,'ManageCoures.html',{'coures':coures})
