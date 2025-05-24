from django.shortcuts import render,redirect
from .models import Doithoai,Thoai,Traloi,Nguoidung,Dtnguoidung
from datetime import date
from django.contrib import messages
import json
from deep_translator import GoogleTranslator
from decouple import config
import openai
import traceback
from home.views import nguoidung_dang_nhap
from django.http import JsonResponse

# Create your views here.
def homeChat(request):
    nguoidung = nguoidung_dang_nhap(request)
    if not nguoidung:
        return redirect('dang_nhap')
    data = Doithoai.objects.all()
    completed_chats = set(Traloi.objects.filter(id_nguoidung=nguoidung).values_list('id_cauhoi__id_doithoai', flat=True))
    return render(request,'ChatHome.html',{"Listchat": data,"completed_chats": completed_chats})
def get_gpt_suggestions(question):
    try:
        openai.api_key = config('OPENAI_API_KEY')
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "user",
                    "content": f"Provide 3 different ways to answer this question: '{question}'. Format as: answer1 @ answer2 @ answer3"
                }
            ],
            temperature=0.7,
            max_tokens=150
        )
        suggestion_raw = response.choices[0].message['content'].strip()
        # Tách chuỗi ra danh sách
        suggestion_list = [s.strip() for s in suggestion_raw.split('@') if s.strip()]
        return suggestion_list if suggestion_list else ["Example 1", "Example 2", "Example 3"]
    except Exception as e:
        print(f"OpenAI API Error: {str(e)}")
        traceback.print_exc()
        return ["Could not generate suggestions", "Please try again", "Check your API key"]


def ChatDetail(request, id):
    user = request.session.get('name')
    dataDoiThoai = Doithoai.objects.get(id=id)
    ngay = date.today().strftime('%Y-%m-%d')
    id_user = Nguoidung.objects.get(ten=user)
    cauhois = Thoai.objects.filter(id_doithoai=id).order_by('id')

    current_index = int(request.POST.get('current_index', 0))
    reply_json = request.POST.get('reply_data', '[]')
    reply = json.loads(reply_json)

    # POST request: xử lý câu trả lời và gợi ý tiếp theo
    if request.method == 'POST':
        user_answer = request.POST.get('ChatContent')
        if current_index < cauhois.count():
            current_question = cauhois[current_index]
            suggestions = get_gpt_suggestions(current_question.cauhoi)

            reply.append({
                'question': current_question.cauhoi,
                'id_user': id_user.id,
                'answer': user_answer,
                'time': ngay,
                'id_question': current_question.id,
                'suggestions': suggestions,
            })

            current_index += 1

        if current_index < cauhois.count():
            next_question = cauhois[current_index]
            next_suggestions = get_gpt_suggestions(next_question.cauhoi)

            return render(request, 'ChatDetail.html', {
                "Chat": dataDoiThoai,
                "chat": reply,
                "Content": next_question,
                "done": False,
                "current_index": current_index,
                "reply_data": json.dumps(reply),
                "remaining_questions": cauhois.count() - current_index,
                "suggestions": next_suggestions,
            })
        else:
            return render(request, 'ChatDetail.html', {
                "Chat": dataDoiThoai,
                "chat": reply,
                "Content": None,
                "done": True,
                "reply_data": json.dumps(reply),
                "suggestions": [],  # Không cần gợi ý khi hoàn thành
            })

    # GET request: hiển thị câu hỏi đầu tiên
    if cauhois.exists():
        first_question = cauhois[0]
        suggestions = get_gpt_suggestions(first_question.cauhoi)
    else:
        first_question = None
        suggestions = []

    return render(request, 'ChatDetail.html', {
        "Chat": dataDoiThoai,
        "chat": [],
        "Content": first_question,
        "done": False,
        "current_index": 0,
        "reply_data": json.dumps([]),
        "remaining_questions": cauhois.count(),
        "suggestions": suggestions,
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
def ChatUser(request, id):
    user = request.session.get('name')
    if not user:
        return redirect('dang_nhap')
    
    data = Doithoai.objects.get(id=id)
    id_user = Nguoidung.objects.get(ten=user)
    messages = Dtnguoidung.objects.filter(id_doithoai=data).order_by('ngay')
    
    if request.method == 'POST':
        chat_content = request.POST.get('ChatContent')
        try:
            # Dịch tin nhắn sang tiếng Anh
            translated_text = GoogleTranslator(source='vi', target='en').translate(chat_content)
            
            # Lưu tin nhắn đã dịch vào database
            new_message = Dtnguoidung(
                nguoigui=id_user,
                tinnhan=translated_text,  # Lưu bản dịch tiếng Anh
                ngay=date.today(),
                id_doithoai=data
            )
            new_message.save()
            
            # Return JSON response for AJAX requests
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'translated_message': translated_text,  # Gửi bản dịch tiếng Anh
                    'user_id': id_user.id,
                    'username': id_user.ten
                })
                
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'status': 'error', 'message': str(e)})
            messages.error(request, f"Translation error: {str(e)}")
    
    return render(request, "ChatUser.html", {
        "detail": data,
        "host": id_user,
        "messages": messages,
        "room_id": id
    })

def chat_results(request, id):
    user = request.session.get('name')
    
    dataDoiThoai = Doithoai.objects.get(id=id)
    id_user = Nguoidung.objects.get(ten=user)
    
    cauhois = Thoai.objects.filter(id_doithoai=id).order_by('id')
    
    tralois = Traloi.objects.filter(
        id_nguoidung=id_user,
        id_cauhoi__in=cauhois
    ).order_by('id_cauhoi')
    
    results = []
    for cauhoi in cauhois:
        traloi = tralois.filter(id_cauhoi=cauhoi).first()
        results.append({
            'question': cauhoi.cauhoi,
            'answer': traloi.noidung if traloi else None,
            'date': traloi.ngaygui if traloi else None
        })
    
    return render(request, 'ChatResults.html', {
        "Chat": dataDoiThoai,
        "results": results,
        "has_completed": len(tralois) > 0
    })


