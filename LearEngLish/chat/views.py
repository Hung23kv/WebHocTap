from django.shortcuts import render,redirect
from .models import Doithoai,Thoai,Traloi,Nguoidung
from datetime import date
from django.db.models import Q

# Create your views here.
def homeChat(request):
    data = Doithoai.objects.all()
    return render(request,'ChatHome.html',{"Listchat": data})
def ChatDetail(request,idQ):
    data = Thoai.objects.filter(id_doithoai=idQ).first()
    id_user = Nguoidung.objects.get(pk=2)
    id_Question = data.id
    
    if request.method == 'POST':
        Chattext = request.POST.get('ChatContent')
        Date = date.today()
        id_Ques = data.id
        Nid_Ques = Traloi.objects.get(pk = id_Ques)
        answer = Traloi.objects.create(id_nguoidung = id_user,id_cauhoi = Nid_Ques,ngaygui = Date,noidung = Chattext)
        answer.save()
        nextQues = Thoai.objects.filter(id_gt = data.id).order_by('id').first()
        if nextQues:
            return redirect('ChatDetail', idQ=nextQues.id)
        else:
            return render(request, 'ChatDetail.html', {
                "Content": None,
                
                "done": True
            })
    return render(request,'ChatDetail.html',{"Content" :data, "chat" : get_chat_user(id_user,id_Question)   ,"done" : False })
def get_chat_user(user, Question):
    r = Traloi.objects.filter(Q(id_nguoidung=user) & Q(id_cauhoi=Question)).first()
    reply = []
    if r:
        reply.append({
            'question': r.id_cauhoi.cauhoi,
            'answer': r.noidung
        })
    return reply
