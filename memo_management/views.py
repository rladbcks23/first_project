from django.shortcuts import redirect


def index(request):
    # 기본화면으로 이동
    return redirect('notebooks:index')