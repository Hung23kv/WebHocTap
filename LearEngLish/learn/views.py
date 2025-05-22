from django.shortcuts import render
from home.views import nguoidung_dang_nhap
from chat.models import Tientrinh,Baihoc,Tuvung,Ontap
from datetime import date
# Create your views here.

def homeLear(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    
    tien_trinh = Tientrinh.objects.filter(id_nguoidung=nguoidung).first()
    cap_do = tien_trinh.id_khoahoc.ten 
    lesson = Baihoc.objects.filter(id_khoahoc=tien_trinh.id_khoahoc).order_by('id')
    return render(request, 'homeLear.html',{"lesson" : lesson, "cap_do" : cap_do})
def vocab(request,lesson_id):
    vocabulary = Tuvung.objects.filter(id_baihoc=lesson_id)
    return render(request, 'vocab.html',{"vocabulary" : vocabulary})
def complete_lesson(request,lesson_id):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    lesson = Baihoc.objects.get(id=lesson_id)
    tien_trinh = Tientrinh.objects.get(id_nguoidung=nguoidung, id_khoahoc=lesson.id_khoahoc)
    vocab_count = Tuvung.objects.filter(id_baihoc=lesson_id).count()

    tien_trinh.diemtong = tien_trinh.diemtong + lesson.diem
    tien_trinh.tudahoc = tien_trinh.tudahoc + vocab_count
    tien_trinh.save()

    Ontap.objects.create(
        id_nguoidung = nguoidung,
        id_baihoc = lesson,
        ketqua = lesson.diem,
        ngaylam = date.today()
    )
    return render(request, 'complete_lesson.html',{"lesson" : lesson})
