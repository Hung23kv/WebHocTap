from django.shortcuts import render, get_object_or_404
from chat.models import Khoahoc,Baihoc,Tuvung,Doithoai,Thoai
from django.urls import reverse
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
import os
from django.utils import timezone
from home.views import nguoidung_dang_nhap

# Create your views here.
def homeLecturer(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    if nguoidung.quyen != 'lecturer':
        return redirect('dang_nhap')
    return render(request,'HomeLecturer.html')

def manageLession(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    if nguoidung.quyen != 'lecturer':
        return redirect('dang_nhap')
    coures = Khoahoc.objects.all()
    context = {
        'coures':coures,
        'select_course':None,
        'listLession':None,
    }
    if request.method == 'POST':
        course_id = request.POST.get('cboLession')
        if course_id:
            lessons = Baihoc.objects.filter(id_khoahoc=course_id)
            context.update({
                "selected_lesstion": int(course_id),
                "listLession": lessons
            })
    return render(request,'ManageLession.html',context)
def manage_vocab(request, lesson_id):

    lesson = Baihoc.objects.get(id=lesson_id)
    vocab_list = Tuvung.objects.filter(id_baihoc=lesson)
    
    # Check if lesson has no vocabulary words
    if not vocab_list.exists():
        return redirect('add_vocab', lesson_id=lesson_id) 
        
    if request.method == 'POST':
        vocab_id = request.POST.get('vocab_id')
        tu = request.POST.get('tu')
        dich = request.POST.get('dich')
        phatam = request.POST.get('phatam')
        
        if vocab_id: 
            vocab = Tuvung.objects.get(id=vocab_id)
            vocab.tu = tu
            vocab.dich = dich
            vocab.phatam = phatam
            
            # Handle image upload for existing vocab
            if 'hinhanh' in request.FILES:
                # Delete old image if exists
                if vocab.hinhanh:
                    old_image_path = os.path.join('media', vocab.hinhanh)
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)
                # Save new image
                fs = FileSystemStorage()
                image = request.FILES['hinhanh']
                filename = fs.save(f'vocab_images/{image.name}', image)
                vocab.hinhanh = filename
                
            vocab.save()
        else:  
            # Handle image upload for new vocab
            hinhanh = None
            if 'hinhanh' in request.FILES:
                fs = FileSystemStorage()
                image = request.FILES['hinhanh']
                filename = fs.save(f'vocab_images/{image.name}', image)
                hinhanh = filename
                
            Tuvung.objects.create(
                id_baihoc=lesson,
                tu=tu,
                dich=dich,
                phatam=phatam,
                hinhanh=hinhanh
            )
            
        return redirect(reverse('manage_vocab', args=[lesson_id]))
        
    return render(request, 'manage_vocab.html', {'lesson': lesson, 'vocab_list': vocab_list})

def add_vocab(request, lesson_id):
    lesson = Baihoc.objects.get(id=lesson_id)
    
    if request.method == 'POST':
        print("POST request received")
        print("POST data:", request.POST)
        print("FILES data:", request.FILES)
        
        # Get the number of vocabulary items from the form
        count = 0
        while f'tu_{count}' in request.POST:
            tu = request.POST.get(f'tu_{count}')
            dich = request.POST.get(f'dich_{count}')
            phatam = request.POST.get(f'phatam_{count}')
            
            # Handle image upload
            hinhanh = None
            if f'hinhanh_{count}' in request.FILES:
                fs = FileSystemStorage()
                image = request.FILES[f'hinhanh_{count}']
                filename = fs.save(f'vocab_images/{image.name}', image)
                hinhanh = filename
            
            # Create new vocabulary item
            Tuvung.objects.create(
                id_baihoc=lesson,
                tu=tu,
                dich=dich,
                phatam=phatam,
                hinhanh=hinhanh
            )
            count += 1
        
        return redirect('manage_vocab', lesson_id=lesson_id)
    
    return render(request, 'add_vocab.html', {'lesson': lesson})

def add_lesson(request):
    course_id = request.GET.get('course_id')
    if course_id:
        course = Khoahoc.objects.get(id=course_id)
        
        if request.method == 'POST':
            try:
                # Lấy dữ liệu từ form
                tieude = request.POST.get('ten')  # Lấy từ name="ten" trong form
                thutu = request.POST.get('thutu')
                diem = request.POST.get('diem')
                
                # Tạo bài học mới
                Baihoc.objects.create(
                    id_khoahoc=course,
                    tieude=tieude,
                    thutu=thutu,
                    diem=diem
                )
                return redirect('manage-lession')
            except Exception as e:
                print(f"Error: {str(e)}")  # In lỗi để debug
                context = {
                    'course': course,
                    'error': str(e)
                }
                return render(request, 'add_lesson.html', context)
                
        return render(request, 'add_lesson.html', {'course': course})
    return redirect('manage-lession')

def manage_conversation(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    if nguoidung.quyen != 'lecturer':
        return redirect('dang_nhap')
    conversations = Doithoai.objects.exclude(muctieu='Trò chuyện')
    return render(request, 'manage_conversation.html', {'conversations': conversations})

def add_conversation(request):
    if request.method == 'POST':
        try:
            tieude = request.POST.get('tieude')
            muctieu = request.POST.get('muctieu')
            hinhanh = None
            
            if 'hinhanh' in request.FILES:
                fs = FileSystemStorage()
                image = request.FILES['hinhanh']
                filename = fs.save(f'conversation_images/{image.name}', image)
                hinhanh = filename
            
            Doithoai.objects.create(
                tieude=tieude,
                muctieu=muctieu,
                hinhanh=hinhanh,
                # nguoitao=request.user  # Giả sử đã có user đăng nhập
            )
            return redirect('manage-conversation')
        except Exception as e:
            return render(request, 'add_conversation.html', {'error': str(e)})
            
    return render(request, 'add_conversation.html')

def manage_dialogue(request, conversation_id):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    if nguoidung.quyen != 'lecturer':
        return redirect('dang_nhap')
    conversation = Doithoai.objects.get(id=conversation_id)
    dialogues = Thoai.objects.filter(id_doithoai=conversation)
    
    # Check if conversation has no dialogue questions
    if not dialogues.exists():
        if request.method == 'POST':
            # Get the number of dialogue items from the form
            count = 0
            while f'cauhoi_{count}' in request.POST:
                cauhoi = request.POST.get(f'cauhoi_{count}')
                
                # Create new dialogue item
                Thoai.objects.create(
                    id_doithoai=conversation,
                    cauhoi=cauhoi,
                    ngaytao=timezone.now()
                )
                count += 1
            
            return redirect('manage_dialogue', conversation_id=conversation_id)
            
        return render(request, 'add_dialogue.html', {'conversation': conversation})
    
    if request.method == 'POST':
        dialogue_id = request.POST.get('dialogue_id')
        cauhoi = request.POST.get('cauhoi')
        
        if dialogue_id:
            dialogue = Thoai.objects.get(id=dialogue_id)
            dialogue.cauhoi = cauhoi
            dialogue.save()
        else:
            Thoai.objects.create(
                id_doithoai=conversation,
                cauhoi=cauhoi,
                ngaytao=timezone.now()
            )
            
        return redirect('manage_dialogue', conversation_id=conversation_id)
        
    return render(request, 'manage_dialogue.html', {
        'conversation': conversation,
        'dialogues': dialogues
    })

def delete_dialogue(request, dialogue_id):
    dialogue = get_object_or_404(Thoai, id=dialogue_id)
    conversation_id = dialogue.id_doithoai.id
    dialogue.delete()
    return redirect('manage_dialogue', conversation_id=conversation_id)

def delete_vocab(request, vocab_id):
    vocab = get_object_or_404(Tuvung, id=vocab_id)
    lesson_id = vocab.id_baihoc.id
    
    # Delete the image file if it exists
    if vocab.hinhanh:
        image_path = os.path.join('media', vocab.hinhanh)
        if os.path.exists(image_path):
            os.remove(image_path)
    
    vocab.delete()
    return redirect('manage_vocab', lesson_id=lesson_id)