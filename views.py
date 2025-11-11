import math
import random

import razorpay
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from .forms import  questionForm
import nltk
from string import punctuation
import re
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


from .models import user, categry, expert_tbl, question, Pending, tbl_answer, tbl_chat


def indez(request):

    return render(request, "indez.html")


def login(request):
    request.session['email'] = 'null'
    request.session['password'] = 'null'
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        if user.objects.filter(email=email, password=password, status=1).exists():
            request.session['email'] = email
            request.session['password'] = password
            return redirect('user/')
        elif expert_tbl.objects.filter(email=email, password=password, status=1).exists():
            request.session['email'] = email
            request.session['password'] = password
            return redirect('expert/')
        else:
            messages.error(request, '!!!invaild login credentials')
            return redirect('/login/')

    return render(request, "LOGIN.html")


def reg1(request):
    request.session['email'] = 'null'
    request.session['password'] = 'null'
    category = {
        'c_det': categry.objects.all(),
    }

    if request.method == "POST":
        f_name = request.POST.get("f_name")

        mobile = request.POST.get("m_number")
        email = request.POST.get("email")
        password = request.POST.get("password")
        category1 = request.POST.get("category1")
        interest = request.POST.get("interest")
        fileToUpload = request.FILES.get("fileToUpload")
        if expert_tbl.objects.filter(email=email).exists():
            messages.info(request, "email already exist")
            redirect('/reg1/')
        else:

            new_reg = expert_tbl.objects.create(f_name=f_name, mobile=mobile, password=password, email=email,
                                                interest=interest, cat=category1, fileToUpload=fileToUpload)
            new_reg.save()
            messages.info(request, "successfully registered")
            return redirect('/')

    return render(request, "REGISTER1.html", category)


def reg2(request):
    if request.method == "POST":
        f_name = request.POST.get("f_name")
        l_name = request.POST.get("l_name")
        mobile = request.POST.get("m_number")
        email = request.POST.get("email")
        password = request.POST.get("password")
        # gender = request.POST.get("gender")
        if user.objects.filter(email=email, status=1).exists():
            messages.info(request, "email already exist")
            redirect('/reg2/')
        else:
            new_reg = user(f_name=f_name, l_name=l_name, mobile=mobile, password=password, email=email,
                           status=0)
            new_reg.save()

            request.session['email'] = email
            return redirect('/payment_user/')
    return render(request, "REGISTER2.html")


def payment_user(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    else:
        client = razorpay.Client(auth=("rzp_test_8omlEOoshWBlBg", "pKnHdNim8b24slqDCc6gLDmy"))
        email = request.session['email']
        digits = "0123456789"
        token = ""
        for i in range(6):
            token += digits[math.floor(random.random() * 10)]

        subject = "QA World Registration "
        from_email = settings.EMAIL_HOST_USER
        recepient_list = [email]
        htmlgen = 'The otp for successfull registration to QA World is :' + token + ''
        send_mail(subject, htmlgen, from_email, recepient_list)
        DATA = {
            "amount": 20000,
            "currency": "INR",

        }
        client.order.create(data=DATA)
        content = {
            'token': token
        }

    return render(request, "user_payment.html", content)

def payment_done(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    else:
       email=request.session['email']
       person=user.objects.get(email=email)
       person.status=1
       person.save()
       return redirect('/login/')

def payment_done1(request,id):
    if request.session['email'] == 'null':
        return redirect('/login/')
    else:
       email=request.session['email']
       person=user.objects.get(email=email)
       if id==1:
           person.credit_balance=person.credit_balance+400
           person.save()
       if id==2:
           person.credit_balance = person.credit_balance + 1000
           person.save()
       if id==3:
           person.credit_balance = person.credit_balance + 1800
           person.save()
       return redirect('/public_profile/')

def users_payment(request):
    if request.session['email'] == 'null':
        return redirect('/home/')

    elif 'email' in request.session:
        email = request.session['email']
        public = user.objects.get(email=email)
        messages.info(request, "successfully registered")
        public.status = 1
        public.save()

        return render(request, "user_credit.html")




def expert(request):
    if request.session['email'] == 'null':
        return redirect('/login/')

    elif 'email' in request.session:
        email = request.session['email']
        user =expert_tbl.objects.get(email=email)
        if user.type == "user" or user.status==0:
            return redirect('/login/')
        else:
            email = request.session['email']
            content = {
                'email': email
            }
            return render(request, "expert_index.html", content)


def expert_profile(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        user = expert_tbl.objects.get(email=email)
        if user.type == "user" or user.status == 0:
            return redirect('/login/')
        else:

            email = request.session['email']
            content = {
                'r_det': expert_tbl.objects.get(email=email)
            }

            return render(request, "expert_profile.html", content)


def expert_eprofile(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        user = expert_tbl.objects.get(email=email)
        if user.type == "user" or user.status == 0:
            return redirect('/login/')
        else:

            email = request.session['email']
            if request.method == "POST":
                f_name = request.POST.get("f_name")
                mobile = request.POST.get("m_number")
                interest = request.POST.get("interest")
                category1 = request.POST.get("category1")
                person1 = expert_tbl.objects.get(email=email)
                person1.f_name = f_name
                person1.mobile = mobile
                person1.interest = interest
                person1.category1=category1
                person1.save()
                return redirect('/expert_profile/')
            content = {
                'r_det': expert_tbl.objects.get(email=email)
            }
            return render(request, "expert_eprofile.html", content)



def question_list(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        user = expert_tbl.objects.get(email=email)
        if user.type == "user" or user.status == 0:
            return redirect('/login/')
        else:

            email = request.session['email']
            exp = expert_tbl.objects.get(email=email)
            a = exp.cat
            b = categry.objects.get(cat=a)
            qs = question.objects.filter(categry=b, question_status=0)
            content = {
                'qs_list': qs

            }

            return render(request, "qs_list.html", content)


def pending(request, id):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        user = expert_tbl.objects.get(email=email)
        if user.type == "user" or user.status == 0:
            return redirect('/login/')
        else:

                email = request.session['email']
                exp = expert_tbl.objects.get(email=email)
                question1 = question.objects.get(id=id)
                pen = Pending(expert=exp, question=question1)
                pen.save()
                return redirect('/question_list/')


def pending_question(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        user = expert_tbl.objects.get(email=email)
        if user.type == "user" or user.status == 0:
            return redirect('/login/')
        else:

            email = request.session['email']
            exp = expert_tbl.objects.get(email=email)
            # a = exp.cat
            # b = categry.objects.get(cat=a)
            qs = Pending.objects.filter(expert=exp, status=1)
            # final_qs = Pending.objects.filter(expert=exp,question=qs)

            content = {
                'qs_list': qs

            }

            return render(request, "pending_question.html", content)


def qs_approve(request, id):
    if request.session['email'] == 'null':
        return redirect('/login/')

    else:

            # email = request.session['email']
            # exp = expert_tbl.objects.get(email=email)

            p_qs = Pending.objects.get(id=id)
            p_qs.status = 0
            p_qs.save()
            qs = p_qs.question
            qs.question_status = 1
            qs.expert = p_qs.expert.email
            qs.save()
            new_ans = tbl_answer.objects.create(pending=p_qs)
            new_ans.save()
            # qs = Pending.objects.filter(expert=exp)
            # final_qs = Pending.objects.filter(expert=exp,question=qs)
            return redirect('/user_req_ques/')


def approved_qs(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        user = expert_tbl.objects.get(email=email)
        if user.type == "user" or user.status == 0:
            return redirect('/login/')
        else:
                email = request.session['email']
                exp = expert_tbl.objects.get(email=email)
                qs = tbl_answer.objects.filter(pending__expert=exp)
                content = {
                    'qs_list': qs
                }

                return render(request, "qs_approved.html", content)


def answering(request, id):
    if request.session['email'] == 'null':
        return redirect('/login/')
    qs = tbl_answer.objects.get(id=id)
    if request.method == "POST":
        ans = request.POST.get("ans")
        qs.answer = ans
        qs.status = 1
        qs.save()

    return redirect('/approved_qs/')



def delete_pending_question(request, id):
    if request.session['email'] == 'null':
        return redirect('/login/')
    else:
        Pending.objects.get(id=id).delete()
        return redirect('/pending_question/')


def logout(request):
    request.session['email'] = 'null'
    request.session['password'] = 'null'
    return redirect('/login/')


def passwrd(request):
    if request.method == "POST":
        email = request.POST.get("user_email")
        request.session['email'] = email
        print(email)
        return redirect('/co_ver/')
    return render(request, "passwrd.html")


def co_ver(request):
    n_pass = request.POST.get("n_pass")
    email = request.session['email']
    digits = "0123456789"
    token = ""
    for i in range(6):
        token += digits[math.floor(random.random() * 10)]

    subject = "QA World Forgot password "
    from_email = settings.EMAIL_HOST_USER
    recepient_list = [email]
    htmlgen = 'The otp for changing the password in QA World is :' + token + ''
    send_mail(subject, htmlgen, from_email, recepient_list)

    content = {
        'token': token
    }
    if request.method == "POST":
        usr = user.objects.get(email=email)
        usr.password = n_pass
        usr.save()
        return redirect("/")
    return render(request, "ver_code.html", content)


def user1(request):
    email = request.session['email']
    category = {
        'r_det': user.objects.get(email=email),
    }

    return render(request, "index.html", category)


# def answer(request):
#     if request.session['email'] == 'null':
#         return redirect('/login/')
#     else:
#         email = request.session['email']
#         if request.method == "POST":
#             user1 = user.objects.get(email=email)
#             catgry = request.POST.get("category1")
#             cate = categry.objects.get(cat=catgry)
#             qus = request.POST.get("questions")
#
#             datee = request.POST.get("duration")
#
#             new_qs = question(person=user1, question=qus, e_date=datee, categry=cate)
#             new_qs.save()
#             return redirect('/answer/')
#         cat = {
#             'c_det': categry.objects.all(),
#         }
#
#     return render(request, "answer.html", cat)
def answer(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        User = user.objects.get(email=email)
        if User.type == "expert" or User.status == 0:
            return redirect('/login/')
        else:

            email = request.session['email']
            user1=user.objects.get(email=email)

            if request.method == "POST":
                if User.credit_balance <=100:
                    return redirect('/users_payment/')

                form = questionForm(request.POST)
                if form.is_valid():
                    per=form.save(commit=False)
                    per.person=user1
                    per.save()
                    form.catgry = form.cleaned_data['categry']
                    form.e_date = form.cleaned_data['e_date']
                    form.question = form.cleaned_data['question']
                    form.save()
                    user1.credit_balance=user1.credit_balance-100
                    user1.save()
                else:
                    return redirect('/answer/')
                return redirect('/answer/')

            form =questionForm
            mydict = {
               'form':form,
                'c_det': categry.objects.all(),
                'user':user1
            }
            return render(request,'answer.html',context=mydict)


def user_added_questions(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        User = user.objects.get(email=email)
        if User.type == "expert" or User.status == 0:
            return redirect('/login/')
        else:
            email = request.session['email']
            person = user.objects.get(email=email)
            qs = {
                "ques": question.objects.filter(person=person)
            }

            return render(request, "user_added_qs.html", qs)


def de_user_ques(request, id):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        User = user.objects.get(email=email)
        if User.type == "expert" or User.status == 0:
            return redirect('/login/')
        else:
            question.objects.get(id=id).delete()
            return redirect('/user_added_questions/')


def user_req_ques(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        User = user.objects.get(email=email)
        if User.type == "expert" or User.status == 0:
            return redirect('/login/')
        else:
            email = request.session['email']
            person = user.objects.get(email=email)





            nltk.download('stopwords')
            set(stopwords.words('english'))
            stop_words = stopwords.words('english')
            experts_list=expert_tbl.objects.all();
            for expert in experts_list:
                review_list=[]
                if tbl_answer.objects.filter(pending__expert=expert).exists():
                                answer_attended=tbl_answer.objects.filter(pending__expert=expert)
                                answer_count=answer_attended.count()

                                rating_sum=0
                                for answer in answer_attended:
                                    text1=str(answer.review)

                                    text_final = ''.join(c for c in text1 if not c.isdigit())

                                    processed_doc1 = ' '.join([word for word in text_final.split() if word not in stop_words])

                                    sa = SentimentIntensityAnalyzer()
                                    dd = sa.polarity_scores(text=processed_doc1)
                                    compound = round((1 + dd['compound']) / 2, 2)
                                    rating_sum=rating_sum+compound
                                rating=rating_sum/answer_count
                                rating=rating*100
                                expert.rating=rating
                                expert.count=answer_count
                                if answer_count>10 and expert.rating>50:
                                    reminder=answer_count%10

                                    amount=(answer_count-reminder)/10*300
                                    expert.payment_received=amount
                                    expert.save()

                                expert.save()












            qs = {
                "ques": Pending.objects.filter(question__person=person,status=1)
            }

            return render(request, "user_req_ques.html", qs)




def user_ans_ques(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        User = user.objects.get(email=email)
        if User.type == "expert" or User.status == 0:
            return redirect('/login/')
        else:
            email = request.session['email']
            person = user.objects.get(email=email)
            qs = {
                "ques": tbl_answer.objects.filter(pending__question__person=person, status=1)
            }
            return render(request, "user_ans_ques.html", qs)


def user_review(request,id):
    if request.session['email'] == 'null':
        return redirect('/login/')
    else:
        email = request.session['email']
        person = user.objects.get(email=email)
        answer=tbl_answer.objects.get(id=id)

        if request.method == "POST":
            review = request.POST.get("review")
            answer.review=review
            answer.save()

        return redirect("/user_ans_ques/")


def public_profile(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        User = user.objects.get(email=email)
        if User.type == "expert" or User.status == 0:
            return redirect('/login/')
        else:

            email = request.session['email']
            content = {
                'r_det': user.objects.get(email=email)
            }

            return render(request, "public_profile.html", content)


def public_eprofile(request):
    if request.session['email'] == 'null':
        return redirect('/login/')
    elif 'email' in request.session:
        email = request.session['email']
        User = user.objects.get(email=email)
        if User.type == "expert" or User.status == 0:
            return redirect('/login/')

        else:

            email = request.session['email']
            if request.method == "POST":
                f_name = request.POST.get("f_name")
                l_name = request.POST.get("l_name")
                mobile = request.POST.get("m_number")


                person = user.objects.get(email=email)
                person.f_name = f_name
                person.l_name = l_name
                person.mobile = mobile


                person.save()
                return redirect('/public_profile/')
            content = {
                'r_det': user.objects.get(email=email)
            }

            return render(request, "public_eprofile.html", content)


def user_chat(request, id):
    if request.session['email'] == 'null':
        return redirect('/login/')
    else:
        email = request.session['email']

        ans = tbl_answer.objects.get(id=id)
        print(ans)
        pend = ans.pending
        expert = pend.expert
        public = pend.question.person
        ques = pend.question
        chat = tbl_chat.objects.filter(public=public, expert=expert)
        if request.method == "POST":
            msg = request.POST.get("msg")
            print(msg)
            if msg != "0000":
                new = tbl_chat(public=public, expert=expert, question=pend, msg=msg, person=email)
                new.save()
                msg = "0000"
        content = {
            # 'chat':tbl_chat.objects.get(expert=expert,public=public,question=pend)
            'chat': chat,
            'email':email
        }

        return render(request, "chat.html", content)


def exp_chat(request, id):
    if request.session['email'] == 'null':
        return redirect('/login/')
    else:
        email = request.session['email']

        ans = tbl_answer.objects.get(id=id)
        print(ans)
        pend = ans.pending
        expert = pend.expert
        public = pend.question.person
        ques = pend.question
        chat = tbl_chat.objects.filter(public=public, expert=expert)
        if request.method == "POST":
            msg = request.POST.get("msg")
            print(msg)
            if msg != "0000":
                new = tbl_chat(public=public, expert=expert, question=pend, msg=msg, person=email)
                new.save()
                msg = "0000"
        content = {
            # 'chat':tbl_chat.objects.get(expert=expert,public=public,question=pend)
            'chat': chat,
            'email':email
        }

        return render(request, "chatexp.html", content)


def Expert_payment(request):
        experts=expert_tbl.objects.filter(payment_status=1)
        for expert in experts :
            if expert.rating<50 :
                expert.payment_status=0
                expert.save()
        experts = expert_tbl.objects.filter(payment_status=0)
        for expert in experts:
            if expert.rating >= 50:
                expert.payment_status = 1
                expert.save()



        experts=expert_tbl.objects.filter(payment_status=1)
        for expert in experts:
            money=int(expert.count/10)*300
            expert.payment_pending=money-expert.payment_received
            expert.save()
        total_money=0
        experts=expert_tbl.objects.filter(payment_status=1)
        for expert in experts:
            total_money=total_money+expert.payment_pending

        experts=expert_tbl.objects.all()


        if total_money>0:
            client = razorpay.Client(auth=("rzp_test_8omlEOoshWBlBg", "pKnHdNim8b24slqDCc6gLDmy"))

            DATA = {
                "amount": total_money*100,
                "currency": "INR",

            }

            client.order.create(data=DATA)

        content={
            'total_money':total_money*100,
            'total':total_money,
            'experts':experts
        }


        return render(request,'admin/expertpayment.html',content)

def payment_success(request):
    experts=expert_tbl.objects.all()

    for expert in experts:
        expert.payment_pending=0
        expert.payment_received=int(expert.count/10)*300
        expert.save()
    return redirect('/Expert_payment/')
