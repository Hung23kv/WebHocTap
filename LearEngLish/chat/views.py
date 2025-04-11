from django.shortcuts import render,redirect
from .models import Doithoai,Thoai,Traloi,Nguoidung
from datetime import date
from django.db.models import Q

# Create your views here.
def homeChat(request):
    data = Doithoai.objects.all()
    return render(request,'ChatHome.html',{"Listchat": data})
def ChatDetail(request, idQ):
    
    dataDoiThoai = Doithoai.objects.get(id=idQ)
    
   
    cauhois = Thoai.objects.filter(id_doithoai=idQ).order_by('id')
    
    current_index = request.session.get('current_index', 0)
    reply = request.session.get('reply', [])

    if request.method == 'POST':
        user_answer = request.POST.get('ChatContent')

        if current_index < cauhois.count():
            current_question = cauhois[current_index]

            reply.append({
                'question': current_question.cauhoi,
                'answer': user_answer
            })

           
            request.session['reply'] = reply
            request.session['current_index'] = current_index + 1

           
            if current_index + 1 < cauhois.count():
                return redirect('detailChat', idQ=idQ)
            else:
                request.session.pop('reply', None)
                request.session.pop('current_index', None)
                return render(request, 'ChatDetail.html', {
                    "Chat": dataDoiThoai,
                    "chat": reply,
                    "Content": None,
                    "done": True
                })

    current_question = None
    if current_index < cauhois.count():
        current_question = cauhois[current_index]

    return render(request, 'ChatDetail.html', {
        "Chat": dataDoiThoai,
        "chat": reply,
        "Content": current_question,
        "done": False
    })