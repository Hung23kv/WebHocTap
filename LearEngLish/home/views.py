from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from chat.models import Nguoidung,Tientrinh,Baihoc,Khoahoc,Tuvung,Ontap
from django.core.mail import send_mail
from django.conf import settings
import random
from datetime import date

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
                return redirect('Customadmin')
            elif role == 'lecturer':
                return redirect('lecturer')
            else:  # student hoặc role khác
                tien_trinh = Tientrinh.objects.filter(id_nguoidung=nguoidung).first()
                if not tien_trinh:
                    return redirect('chon_cap_do')
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
        return redirect('dang_ky')
    khoahoc = Khoahoc.objects.get(id=tien_trinh.id_khoahoc.id)
    next_lv = int(khoahoc.thutu) + 1
    cap_do_tiep_theo = get_cap_do_tiep_theo(next_lv)
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

def dang_ky(request):
    if request.method == 'POST':
        if 'send_otp' in request.POST:
            # Get form data
            ten = request.POST.get('ten')
            email = request.POST.get('email')
            matkhau = request.POST.get('matkhau')
            sdt = request.POST.get('sdt')
            
            # Check if email already exists
            if Nguoidung.objects.filter(email=email).exists():
                messages.error(request, 'Email đã tồn tại. Vui lòng sử dụng email khác.')
                return render(request, 'dangky.html')
            
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            
            # Store data in session
            request.session['registration_data'] = {
                'ten': ten,
                'email': email,
                'matkhau': matkhau,
                'sdt': sdt,
                'otp': otp
            }
            
            # Send OTP email
            try:
                send_mail(
                    'Mã OTP - Đăng ký tài khoản EnglishMaster',
                    f'Mã OTP của bạn là: {otp}. Mã này có hiệu lực trong 5 phút.',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Mã OTP đã được gửi đến email của bạn.')
                return render(request, 'dangky.html', {'otp_sent': True})
            except Exception as e:
                messages.error(request, f'Không thể gửi email. Lỗi: {str(e)}')
                return render(request, 'dangky.html')
                
        elif 'verify_otp' in request.POST:
            user_otp = request.POST.get('otp')
            registration_data = request.session.get('registration_data')
            
            if not registration_data:
                messages.error(request, 'Phiên đăng ký đã hết hạn. Vui lòng thử lại.')
                return redirect('dang_ky')
            
            if user_otp == registration_data['otp']:
                new_user = Nguoidung(
                    ten=registration_data['ten'],
                    email=registration_data['email'],
                    matkhau=registration_data['matkhau'],
                    quyen='student',
                    ngaytao=date.today(),
                    otp=user_otp,
                    verotp=user_otp
                )
                new_user.save()
                
                # Clear session
                del request.session['registration_data']
                
                messages.success(request, 'Đăng ký thành công! Vui lòng đăng nhập.')
                return redirect('dang_nhap')
            else:
                messages.error(request, 'Mã OTP không đúng hoặc đã hết hạn!')
                return render(request, 'dangky.html', {'otp_sent': True})
    
    return render(request, 'dangky.html')

def quen_mat_khau(request):
    if request.method == 'POST':
        if 'send_otp' in request.POST:
            email = request.POST.get('email')
            user = Nguoidung.objects.filter(email=email).first()
            
            if not user:
                messages.error(request, 'Email không tồn tại trong hệ thống.')
                return render(request, 'quenmatkhau.html')
            
            # Generate OTP
            otp = str(random.randint(100000, 999999))
            
            # Store data in session
            request.session['reset_data'] = {
                'email': email,
                'otp': otp
            }
            
            # Send OTP email
            try:
                send_mail(
                    'Mã OTP - Đặt lại mật khẩu EnglishMaster',
                    f'Mã OTP của bạn là: {otp}. Mã này có hiệu lực trong 5 phút.',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Mã OTP đã được gửi đến email của bạn.')
                return render(request, 'quenmatkhau.html', {'otp_sent': True})
            except Exception as e:
                messages.error(request, f'Không thể gửi email. Lỗi: {str(e)}')
                return render(request, 'quenmatkhau.html')
                
        elif 'verify_otp' in request.POST:
            user_otp = request.POST.get('otp')
            reset_data = request.session.get('reset_data')
            
            if not reset_data:
                messages.error(request, 'Phiên đặt lại mật khẩu đã hết hạn. Vui lòng thử lại.')
                return redirect('quen_mat_khau')
            
            if user_otp == reset_data['otp']:
                return render(request, 'quenmatkhau.html', {'otp_sent': True, 'reset_password': True})
            else:
                messages.error(request, 'Mã OTP không đúng hoặc đã hết hạn!')
                return render(request, 'quenmatkhau.html', {'otp_sent': True})
                
        elif 'reset_password' in request.POST:
            reset_data = request.session.get('reset_data')
            if not reset_data:
                messages.error(request, 'Phiên đặt lại mật khẩu đã hết hạn. Vui lòng thử lại.')
                return redirect('quen_mat_khau')
                
            new_password = request.POST.get('new_password', '').strip()
            confirm_password = request.POST.get('confirm_password', '').strip()
            
            if len(new_password) < 6:
                messages.error(request, '❌ Mật khẩu mới phải có ít nhất 6 ký tự!')
                return render(request, 'quenmatkhau.html', {'otp_sent': True, 'reset_password': True})
                
            if new_password != confirm_password:
                messages.error(request, '❌ Mật khẩu mới không khớp!')
                return render(request, 'quenmatkhau.html', {'otp_sent': True, 'reset_password': True})
                
            user = Nguoidung.objects.get(email=reset_data['email'])
            user.matkhau = new_password
            user.save()
            
            # Clear session
            del request.session['reset_data']
            
            messages.success(request, '✅ Đặt lại mật khẩu thành công! Vui lòng đăng nhập.')
            return redirect('dang_nhap')
    
    return render(request, 'quenmatkhau.html')

def chon_cap_do(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')

    if request.method == 'POST':
        khoahoc_id = request.POST.get('khoahoc_id')
        if not khoahoc_id:
            messages.error(request, 'Vui lòng chọn cấp độ của bạn.')
            return redirect('chon_cap_do')

        try:
            khoahoc = Khoahoc.objects.get(id=khoahoc_id)
            # Tạo tiến trình học cho người dùng
            tien_trinh = Tientrinh.objects.create(
                id_nguoidung=nguoidung,
                id_khoahoc=khoahoc,
                diemtong=0,
                tudahoc=0
            )
            messages.success(request, f'Chào mừng bạn đến với {khoahoc.ten}! Hãy bắt đầu học ngay.')
            return redirect('trang_chu')
        except Khoahoc.DoesNotExist:
            messages.error(request, 'Không tìm thấy khóa học phù hợp. Vui lòng liên hệ hỗ trợ.')
            return redirect('chon_cap_do')

    khoahoc = Khoahoc.objects.all()
    return render(request, 'choncapdo.html', {'khoahoc': khoahoc})