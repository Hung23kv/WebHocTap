from django.shortcuts import render,redirect
from .models import Doithoai,Thoai,Traloi,Nguoidung
from datetime import date
from django.contrib import messages
import json

# Create your views here.
def homeChat(request):
    data = Doithoai.objects.all()
    return render(request,'ChatHome.html',{"Listchat": data})
def Login(request):
    if request.method == "POST":
        EmailLog = request.POST.get('user')
        password = request.POST.get('passw')
        Log = Nguoidung.objects.filter(email = EmailLog,matkhau = password).first()
        if Log:
            request.session['name'] = Log.ten
            role  = Log.quyen
            role = role.strip()
            request.session['role'] = role  
            if role == 'admin':
                return redirect('/admin/')
            return redirect('homeChat')
        else:
            messages.error(request, 'Nhập sai thông tin tài khoản!')
        
    return render(request,'Login.html')
def ChatDetail(request, id):
    user = request.session.get('name')
    if not user:
        return redirect('Login')
    dataDoiThoai = Doithoai.objects.get(id=id)
    ngay = date.today().strftime('%Y-%m-%d')
    id_user = Nguoidung.objects.get(ten = user) 
    cauhois = Thoai.objects.filter(id_doithoai=id).order_by('id')
    
    current_index = int(request.POST.get('current_index', 0))
    reply_json = request.POST.get('reply_data', '[]')
    reply = json.loads(reply_json)

    if request.method == 'POST':
        user_answer = request.POST.get('ChatContent')
        if current_index < cauhois.count():
            current_question = cauhois[current_index]
            
            reply.append({
                'question': current_question.cauhoi,
                'id_user': id_user.id,
                'answer': user_answer,
                'time': ngay,
                'id_question': current_question.id,
            })
            
            current_index += 1
            
            if current_index < cauhois.count():
                return render(request, 'ChatDetail.html', {
                    "Chat": dataDoiThoai,
                    "chat": reply,
                    "Content": cauhois[current_index],
                    "done": False,
                    "current_index": current_index,
                    "reply_data": json.dumps(reply),
                    "remaining_questions": cauhois.count() - current_index
                })
            else:
                return render(request, 'ChatDetail.html', {
                    "Chat": dataDoiThoai, 
                    "chat": reply,
                    "Content": None,
                    "done": True,
                    "reply_data": json.dumps(reply)
                })

    return render(request, 'ChatDetail.html', {
        "Chat": dataDoiThoai,
        "chat": [],
        "Content": cauhois[0] if cauhois else None,
        "done": False,
        "current_index": 0,
        "reply_data": json.dumps([]),
        "remaining_questions": cauhois.count()
})
def save(request):
    if request.method == 'POST':
        data = json.loads(request.POST.get('reply_data', '[]'))
        for item in data:
            id_user = item['id_user']
            id_question = item['id_question']
            answer = item['answer']
            time = item['time']
            
            thoai = Thoai.objects.get(id=id_question)
            nguoi_dung = Nguoidung.objects.get(id=id_user)
            
            traloi = Traloi(id_nguoidung=nguoi_dung, id_cauhoi=thoai,ngaygui=time, noidung=answer)
            traloi.save()
            
        return redirect('homeChat')
    return redirect('homeChat')
def creatChat(request):
    user = request.session.get('name')
    if not user:
        return redirect('Login')
    id_user = Nguoidung.objects.get(ten = user) 
    
    if request.method == 'POST':
        title = request.POST.get('title')
        purpose = "Trò chuyện"
        doiThoai = Doithoai(tieude=title, muctieu=purpose,nguoitao = id_user)
        doiThoai.save()
        return redirect('chatuser', id = doiThoai.id )
    return render(request, 'creatChat.html')
def ChatUser(request,id):
    user = request.session.get('name')
    data = Doithoai.objects.get(id = id)
    id_user = Nguoidung.objects.get(ten = user)
    return render(request,"ChatUser.html",{"detail":data,"host":id_user})