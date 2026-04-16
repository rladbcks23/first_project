from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notebook, Post, Block

# Create your views here.
@login_required
# 메인 화면
def index(request):
    if request.user.is_authenticated:
        notebooks = Notebook.objects.filter(user=request.user).order_by('-created_at')

        context = {
            'notebooks': notebooks,
        }
        return render(request, 'notebook/index.html', context)
    else:
    # 로그인이 안 되어 있을 때 ( 로그인 화면(아직 안만듦)으로 이동 )
        return redirect('account:login')

def create(request):
    return

def update(request, pk):
    return

def delete(request, pk):
    return

