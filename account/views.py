from django.shortcuts import render, redirect
from django.contrib.auth import login, logout 
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.core.files.storage import default_storage

from notebook.models import Block # 삭제를 위해서

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

# 프로필 보기
@login_required
def profile_view(request):
    return render(request, 'account/profile.html')

# 정보 수정하기
@login_required
def update(request):
    if request.method == 'POST':
        # 바꿀 때 유저네임만 바꾸도록 가져오기
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('accounts:profile')
    else:
        # 기존 아이디는 들어가 있어야지
        form = UserUpdateForm(instance=request.user)

    context = {
        'form': form,
    }
    return render(request, 'account/update.html', context)

# 회원 탈퇴
@login_required
def delete(request):
    if request.method == 'POST':
        # 현재 유저 가져오기
        user = request.user
        # 현재 유저의 블록들 가져오기
        # 유저가 올려놓은 S3에 올라간 이미지, 영상들을 같이 삭제하기 위해서
        # 왜 why? 블록들에 있는 이미지나 영상들의 path를 가져오기 위해서
        user_blocks = Block.objects.filter(post__notebook__user=user)
        file_names = []

        for block in user_blocks:
            if getattr(block, 'image', None):
                if block.image:
                    file_names.append(block.image.name)

            if getattr(block, 'video', None):
                if block.video:
                    file_names.append(block.video.name)
        
        # 중복 으로 가져온 파일 제거
        file_names = list(set(file_names))
        
        # DB 작업 안전하게 묶기
        with transaction.atomic():
            user.delete()
            # 유저와 연결된 DB 데이터 삭제

            # S3 파일 삭제용 "함수"
            def delete_files():
                for file_name in file_names:
                    if default_storage.exists(file_name):
                        default_storage.delete(file_name)

            # DB 삭제 성공하면 그때만 파일 삭제
            transaction.on_commit(delete_files)

        logout(request)
        return redirect('accounts:login')
    else:
        return redirect('accounts:profile')
