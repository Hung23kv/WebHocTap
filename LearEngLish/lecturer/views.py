from django.shortcuts import render
from chat.models import Khoahoc,Baihoc,Tuvung
from django.urls import reverse
from django.shortcuts import redirect
from django.core.files.storage import FileSystemStorage
import os

# Create your views here.
def homeLecturer(request):
    return render(request,'HomeLecturer.html')

def manageLession(request):
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
        
    vocab_list = Tuvung.objects.filter(id_baihoc=lesson)
    return render(request, 'manage_vocab.html', {'lesson': lesson, 'vocab_list': vocab_list})