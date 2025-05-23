from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from chat.models import Nguoidung,Tientrinh,Baihoc,Khoahoc,Tuvung,Ontap

def nguoidung_dang_nhap(request):
    nguoidung_id = request.session.get('nguoidung_id')
    return get_object_or_404(Nguoidung, id=nguoidung_id) if nguoidung_id else None

def get_cap_do_tiep_theo(thutu):
    return Khoahoc.objects.filter(thutu=thutu).first()
def dang_xuat(request):
    request.session.clear()
    return redirect('dang_nhap')

def dang_nhap(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        matkhau = request.POST.get('matkhau')
        nguoidung = Nguoidung.objects.filter(email=email, matkhau=matkhau).first()

        if nguoidung:
            request.session['nguoidung_id'] = nguoidung.id
            request.session['name'] = nguoidung.ten
            role  = nguoidung.quyen
            role = role.strip()
            request.session['role'] = role  
            if role == 'admin':
                return redirect('/Customadmin/')
            elif role == 'lecturer':
                return redirect('/lecturer/')
            else:
                return redirect('trang_chu')
        return render(request, 'dangnhap.html', {'error': 'Email hoặc mật khẩu không đúng'})

    return render(request, 'dangnhap.html')


def hoso(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')

    if request.method == 'POST':
        # Xử lý đổi mật khẩu
        if request.POST.get('change_password'):
            old_password = request.POST.get('old_password', '').strip()
            new_password = request.POST.get('new_password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()

            # Kiểm tra mật khẩu cũ
            if not old_password or nguoidung.matkhau.strip() != old_password:
                messages.error(request, '❌ Mật khẩu cũ không đúng!', extra_tags='password')
                return redirect('hoso')

            # Kiểm tra mật khẩu mới
            if len(new_password) < 6:
                messages.error(request, '❌ Mật khẩu mới phải có ít nhất 6 ký tự!', extra_tags='password')
                return redirect('hoso')

            if new_password != confirm_password:
                messages.error(request, '❌ Mật khẩu mới không khớp!', extra_tags='password')
                return redirect('hoso')

            nguoidung.matkhau = new_password
            nguoidung.save()
            messages.success(request, '✅ Đổi mật khẩu thành công!', extra_tags='password')
            return redirect('hoso')

        # Xử lý cập nhật thông tin cá nhân
        ten = request.POST.get('Ten')
        email = request.POST.get('Email')
        if ten and email:
            nguoidung.ten = ten
            nguoidung.email = email
            nguoidung.save()
            messages.success(request, '✅ Cập nhật thành công!')
        else:
            messages.error(request, '❌ Vui lòng nhập đầy đủ thông tin!')
        return redirect('hoso')

    # Xóa tất cả thông báo khi load lại trang
    storage = messages.get_messages(request)
    storage.used = True
    return render(request, 'hoso.html', {'user': nguoidung})


def trang_chu(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')

    tien_trinh = Tientrinh.objects.filter(id_nguoidung=nguoidung).first()
    if not tien_trinh:
        first_course = Khoahoc.objects.order_by('diemlencap').first()
        if first_course:
            tien_trinh = Tientrinh.objects.create(
                id_nguoidung=nguoidung,
                id_khoahoc=first_course,
                diemtong=0,
                tudahoc=0
            )
        else:
            messages.error(request, "Không tìm thấy khóa học nào. Vui lòng liên hệ hỗ trợ.")
            return redirect('dang_nhap')
    khoahoc = Khoahoc.objects.get(id=tien_trinh.id_khoahoc.id)
    next = int(khoahoc.thutu) + 1
    cap_do_tiep_theo = get_cap_do_tiep_theo(next)
    cap_do = tien_trinh.id_khoahoc.ten 
    diem_hien_tai = tien_trinh.diemtong
    diem_toi_da = tien_trinh.id_khoahoc.diemlencap if tien_trinh.id_khoahoc.diemlencap else 1
    progress_percent = min((diem_hien_tai / diem_toi_da) * 100, 100) if diem_toi_da else 100
    ontap = Ontap.objects.filter(id_nguoidung=nguoidung)

    # Kiểm tra nếu người dùng đã đạt đủ điểm để lên cấp
    if cap_do_tiep_theo and diem_hien_tai >= tien_trinh.id_khoahoc.diemlencap:
        tien_trinh.id_khoahoc = cap_do_tiep_theo
        tien_trinh.diemtong = 0  
        tien_trinh.save()
        messages.success(request, f'🎉 Chúc mừng! Bạn đã lên {cap_do_tiep_theo.ten}!')
        return redirect('trang_chu')

    context = {
        'nguoidung': nguoidung,
        'cap_do': cap_do,
        'diem': diem_hien_tai,
        'ontap': ontap,
        'diem_toi_da': diem_toi_da,
        'progress_percent': round(progress_percent, 2),
        'tuvung_hoc': tien_trinh.tudahoc,
    }
    return render(request, 'home.html', context)

def ontap(request):
    nguoidung = nguoidung_dang_nhap(request)
    listLession = []
    if not nguoidung:
        return redirect('dang_nhap')
    ontap = Ontap.objects.filter(id_nguoidung=nguoidung)
    for i in ontap:
        lesson = Baihoc.objects.get(id=i.id_baihoc.id)
        listLession.append({
            "idLession": lesson.id,
            "title": lesson.tieude,
            "day" : i.ngaylam, 
        })
    return render(request, 'ontap.html', {'ontap': ontap, 'listLession': listLession})

def reviewTest(request, lesson_id):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    vocabulary = list(Tuvung.objects.filter(id_baihoc=lesson_id))
    lesson = Baihoc.objects.get(id=lesson_id)
    
    # Lấy trạng thái từ POST hoặc mặc định
    current_index = int(request.POST.get('current_index', 0))
    step = int(request.POST.get('step', 1))
    test1_passed = request.POST.get('test1_passed', '0') == '1'

    current_word = vocabulary[current_index]

    if request.method == 'POST':
        if step == 2:  # Test 1
            answer = request.POST.get('answer')
            if answer:  # Nếu có answer thì kiểm tra
                if answer == current_word.tu:
                    test1_passed = True
                    step = 3
                else:
                    step = 1
           
        elif step == 3:  # Test 2
            answer = request.POST.get('answer')        
           
            clean_answer = answer.replace("...", "").replace("…", "").strip().lower().replace(" ", "") if answer else ""
            clean_word = current_word.tu.replace("...", "").replace("…", "").strip().lower().replace(" ", "")
            if answer and clean_answer == clean_word:
                # Đúng cả 2 test, sang từ mới
                if current_index + 1 < len(vocabulary):
                    current_index += 1
                    step = 1
                    current_word = vocabulary[current_index]
                    test1_passed = False
                else:
                    return render(request, 'reviewTest.html', {'done': True, 'lesson': lesson})
            else:
                step = 1
    context = {
        'lesson': lesson,
        'current_word': current_word,
        'current_index': current_index,
        'step': step,
        'test1_passed': test1_passed,
        'vocabulary': vocabulary,
        'total': len(vocabulary),
    }
    return render(request, 'reviewTest.html', context)
