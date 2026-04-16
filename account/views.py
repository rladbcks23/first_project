from django.shortcuts import render, redirect
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm

# 회원가입
def signup(request):
    # 로그인이 성공했다면 바로 index로 연결하기
    if request.user.is_authenticated:
        return redirect('notebooks:index')
    # POST 요청이 들어왔다면 회원가입 진행 및 바로 로그인 후 index 연결
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('notebooks:index')
    # GET 요청이 들어왔다면?
    else:
        form = SignUpForm()

    context = {
        'form': form,
    }
    return render(request, 'account/signup.html', context)

# 로그인
def login_views(request):
    # 로그인이 성공했다면 바로 index로 연결하기
    if request.user.is_authenticated:
        return redirect('notebooks:index')

    # POST 요청이 들어왔다면 로그인 시도
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('notebooks:index')
    # GET 요청이 들어왔다면 login으로 연결
    else:
        form = AuthenticationForm()

    context = {
        'form': form,
    }
    return render(request, 'account/login.html', context)

# 로그아웃
def logout_views(request):
    # 로그아웃 후 로그인 화면 연결
    if request.method == 'POST':
        logout(request)
        return redirect('accounts:login')
    # 로그아웃 진행
    return render(request, 'account/logout.html')
