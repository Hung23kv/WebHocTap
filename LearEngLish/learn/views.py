from django.shortcuts import render,redirect
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
    lesson = Baihoc.objects.filter(id_khoahoc=tien_trinh.id_khoahoc).exclude(
        id__in=Ontap.objects.filter(id_nguoidung=nguoidung).values_list('id_baihoc', flat=True)
    ).order_by('id')
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
def takeTest(request, lesson_id):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    vocabulary = list(Tuvung.objects.filter(id_baihoc=lesson_id))
    lesson = Baihoc.objects.get(id=lesson_id)
    if not vocabulary:
        return render(request, 'takeTest.html', {'error': 'Không có từ vựng nào cho bài học!'})

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
            # Nếu không có answer (từ step 1 chuyển sang) thì giữ nguyên step = 2
        elif step == 3:  # Test 2
            answer = request.POST.get('answer')        
            # Remove both types of ellipsis and clean the strings
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
                    return render(request, 'takeTest.html', {'done': True, 'lesson': lesson})
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
    return render(request, 'takeTest.html', context)