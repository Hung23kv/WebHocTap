import json
import random
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from chat.models import Nguoidung,Tientrinh,Baihoc,Khoahoc,Tuvung,Ontap
from datetime import date




def nguoidung_dang_nhap(request):
    nguoidung_id = request.session.get('nguoidung_id')
    return get_object_or_404(Nguoidung, id=nguoidung_id) if nguoidung_id else None



def get_cap_do_tiep_theo(diem):
    return Khoahoc.objects.filter(diemlencap__gt=diem).order_by('diemlencap').first()




def dang_nhap(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        matkhau = request.POST.get('matkhau')
        nguoidung = Nguoidung.objects.filter(email=email, matkhau=matkhau).first()

        if nguoidung:
            request.session['nguoidung_id'] = nguoidung.id
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

    cap_do_tiep_theo = get_cap_do_tiep_theo(tien_trinh.diemtong)
    cap_do = tien_trinh.id_khoahoc.ten 
    diem_hien_tai = tien_trinh.diemtong
    diem_toi_da = cap_do_tiep_theo.diemlencap if cap_do_tiep_theo else diem_hien_tai
    progress_percent = min((diem_hien_tai / diem_toi_da) * 100, 100) if diem_toi_da else 100

    context = {
        'nguoidung': nguoidung,
        'cap_do': cap_do,
        'diem': diem_hien_tai,
        'diem_toi_da': diem_toi_da,
        'progress_percent': round(progress_percent, 2),
        'tuvung_hoc': tien_trinh.tudahoc,
    }
    return render(request, 'home.html', context)




def hoctumoi(request, bai_hoc_id):
    bai_hoc = get_object_or_404(Baihoc, id=bai_hoc_id)
    tu_vung_list = Tuvung.objects.filter(id_baihoc=bai_hoc)

    data = [
        {
            'Tu': tv.Tu,
            'Dich': tv.Dich,
            'HinhAnh': str(tv.HinhAnh),
            'PhatAm': str(tv.PhatAm),
            'BaiHoc_id': tv.id_baihoc.id
        } for tv in tu_vung_list
    ]

    return render(request, 'hoctumoi.html', {
        'bai_hoc': bai_hoc,
        'tu_vung_list': json.dumps(data, ensure_ascii=False)
    })




def hoan_thanh_bai_hoc(request, bai_hoc_id):
    bai_hoc = get_object_or_404(Baihoc, id=bai_hoc_id)
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')

    tien_trinh = Tientrinh.objects.filter(
        id_nguoidung=nguoidung,
        id_khoahoc=bai_hoc.id_khoahoc.id
    ).first()

    if not tien_trinh:
        messages.error(request, "Bạn chưa có tiến trình học. Vui lòng liên hệ hỗ trợ.")
        return redirect('trang_chu')

    # Cộng điểm và kiểm tra lên cấp
    tien_trinh.diem_tong += bai_hoc.Diem

    # Xác định cấp độ mới dựa trên điểm mới
    # cap_do_moi = get_cap_do_hien_tai(tien_trinh.diem_tong)

    # if cap_do_moi and tien_trinh.id_khoahoc != cap_do_moi.id:
    #     tien_trinh.id_khoahoc = cap_do_moi.id  # Gán id thay vì đối tượng
    #     messages.success(request, f'🎉 Bạn đã lên cấp {cap_do_moi.Ten}!')

    tien_trinh.save()

    # Lưu vào bảng OnTap nếu chưa có
    if not Ontap.objects.filter(id_nguoidung=nguoidung.id, id_baihoc=bai_hoc.id).exists():
        Ontap.objects.create(
            id_nguoidung=nguoidung.id,
            id_baihoc=bai_hoc.id,
            ngayLam=date.today(),
            ketQua=0
        )

    tong_baihoc = Baihoc.objects.filter(id_khoahoc=bai_hoc.id_khoahoc).count()
    bai_da_hoan_thanh = Ontap.objects.filter(id_nguoidung=nguoidung.id, id_baihoc__in=Baihoc.objects.filter(id_khoahoc=bai_hoc.id_khoahoc).values_list('id', flat=True)).count()

    return render(request, 'hoanthanh.html', {
        'bai_hoc': bai_hoc,
        'diem_thuong': bai_hoc.Diem,
        'diem_hien_tai': tien_trinh.diem_tong,
        'tong_baihoc': tong_baihoc,
        'bai_da_hoan_thanh': bai_da_hoan_thanh,
    })


def ontap(request):
    user = nguoidung_dang_nhap(request)
    ontap_qs = Ontap.objects.filter(id_nguoidung=user.id)
    tu_vung_ids = ontap_qs.values_list('id_baihoc', flat=True)
    tu_vung_list = list(Tuvung.objects.filter(id_baihoc__in=tu_vung_ids))
    random.shuffle(tu_vung_list)
    tu_vung_list = tu_vung_list[:10]
    data = [
        {
            'Tu': tv.Tu,
            'Dich': tv.Dich,
            'HinhAnh': str(tv.HinhAnh),
            'PhatAm': str(tv.PhatAm),
        } for tv in tu_vung_list
    ]
    return render(request, 'ontap.html', {'tu_vung_list': json.dumps(data, ensure_ascii=False)})


def hoan_thanh_ontap(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')

    tien_trinh = Tientrinh.objects.filter(id_nguoidung=nguoidung).first()
    if tien_trinh:
        tien_trinh.diem_tong += 20
        tien_trinh.save()

    return render(request, 'hoanthanh.html', {
        'bai_hoc': None,
        'diem_thuong': 20,
        'diem_hien_tai': tien_trinh.diem_tong if tien_trinh else 0,
        'tong_baihoc': 0,
        'ontap': True
    })

# ======================= BỎ QUAN BÀI HỌC =======================

def bo_qua_bai_hoc(request, bai_hoc_id):
    bai_hoc = get_object_or_404(Baihoc, id=bai_hoc_id)
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')

    tien_trinh = Tientrinh.objects.filter(
        id_nguoidung=nguoidung,
        id_khoahoc=bai_hoc.id_khoahoc.id
    ).first()

    if not tien_trinh:
        tien_trinh = Tientrinh.objects.create(
            id_nguoidung=nguoidung,
            id_khoahoc=bai_hoc.id_khoahoc.id,
            diem_tong=0,
            tuvung_hoc=0
        )

    # Nếu chưa hoàn thành thì cộng điểm
    if not Ontap.objects.filter(id_nguoidung=nguoidung.id, id_baihoc=bai_hoc.id).exists():
        tien_trinh.diem_tong += bai_hoc.Diem
        tien_trinh.save()
        Ontap.objects.create(
            id_nguoidung=nguoidung.id,
            id_baihoc=bai_hoc.id,
            ngayLam=date.today(),
            ketQua=0
        )

    tong_baihoc = Baihoc.objects.filter(id_khoahoc=bai_hoc.id_khoahoc).count()
    bai_da_hoan_thanh = Ontap.objects.filter(id_nguoidung=nguoidung.id, id_baihoc__in=Baihoc.objects.filter(id_khoahoc=bai_hoc.id_khoahoc).values_list('id', flat=True)).count()

    return render(request, 'hoanthanh.html', {
        'bai_hoc': bai_hoc,
        'diem_thuong': bai_hoc.Diem,
        'diem_hien_tai': tien_trinh.diem_tong,
        'tong_baihoc': tong_baihoc,
        'bai_da_hoan_thanh': bai_da_hoan_thanh,
    })
