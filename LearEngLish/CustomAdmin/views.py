from django.shortcuts import render, redirect
from chat.models import Nguoidung, Khoahoc, Tientrinh, Ontap, Tuvung
from home.views import nguoidung_dang_nhap
from django.contrib import messages
from datetime import date
from django.db.models import Sum, Count
# Create your views here.

def homeAdmin(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    if nguoidung.quyen.strip() != 'admin':
        return redirect('dang_nhap') 
    users = Nguoidung.objects.exclude(quyen='admin')
    return render(request,'HomeAdmin.html',{'users':users})

def track_users(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung or nguoidung.quyen.strip() != 'admin':
        return redirect('dang_nhap')
        
    # Get all users except admins
    users = Nguoidung.objects.exclude(quyen='admin')
    
    # Get learning progress for each user
    for user in users:
        # Get current course and total score
        progress = Tientrinh.objects.filter(id_nguoidung=user).order_by('-diemtong').first()
        if progress:
            user.current_course = progress.id_khoahoc
            user.total_score = progress.diemtong
            user.words_learned = progress.tudahoc
        else:
            user.current_course = None
            user.total_score = 0
            user.words_learned = 0
            
        # Get learning history
        user.learning_progress = []
        progress_history = Tientrinh.objects.filter(id_nguoidung=user).order_by('-diemtong')
        for p in progress_history:
            user.learning_progress.append({
                'course_name': p.id_khoahoc.ten,
                'score': p.diemtong,
                'words_learned': p.tudahoc,
                'date': p.id_khoahoc.ngaytao
            })
            
    return render(request, 'TrackUsers.html', {'users': users})

def addLecturer(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung or nguoidung.quyen.strip() != 'admin':
        return redirect('dang_nhap')
        
    if request.method == 'POST':
        ten = request.POST.get('ten')
        email = request.POST.get('email')
        matkhau = request.POST.get('matkhau')
        
        # Kiểm tra email đã tồn tại chưa
        if Nguoidung.objects.filter(email=email).exists():
            messages.error(request, 'Email này đã được sử dụng!')
            return redirect('addLecturer')
            
        # Tạo giảng viên mới
        new_lecturer = Nguoidung(
            ten=ten,
            email=email,
            matkhau=matkhau,
            quyen='lecturer',
            ngaytao=date.today()
        )
        new_lecturer.save()
        messages.success(request, 'Thêm giảng viên thành công!')
        return redirect('Customadmin')
        
    return render(request, 'AddLecturer.html')

def addCourse(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung or nguoidung.quyen.strip() != 'admin':
        return redirect('dang_nhap')
        
    if request.method == 'POST':
        ten = request.POST.get('ten')
        diemlencap = request.POST.get('diemlencap')
        thutu = request.POST.get('thutu')
        mota = request.POST.get('mota')
        
        # Kiểm tra tên khóa học đã tồn tại chưa
        if Khoahoc.objects.filter(ten=ten).exists():
            messages.error(request, 'Tên khóa học này đã tồn tại!')
            return redirect('addCourse')
            
        # Tạo khóa học mới
        new_course = Khoahoc(
            ten=ten,
            diemlencap=diemlencap,
            thutu=thutu,
            mota=mota,
            ngaytao=date.today()
        )
        new_course.save()
        messages.success(request, 'Thêm khóa học thành công!')
        return redirect('manage-coures')
        
    return render(request, 'AddCourse.html')

def manageCoures(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    if nguoidung.quyen.strip() != 'admin':
        return redirect('dang_nhap')
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    coures = Khoahoc.objects.all()
    return render(request,'ManageCoures.html',{'coures':coures})

