from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notebook, Post, Block
from .forms import NotebookForm

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ MAIN ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@login_required # 로그인 확인
# 메인 화면
def index(request):
    # 로그인 성공시
    notebooks = Notebook.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'notebooks': notebooks,
    }
    return render(request, 'notebook/index.html', context)
    
# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ MAIN ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ



# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ NOTEBOOK ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# 노트북 생성
@login_required
def notebook_create(request):
    # POST 요청이 들어오면
    if request.method == 'POST':
        form = NotebookForm(request.POST)
        # 유효성 검사
        if form.is_valid():
            # Notebook을 만들고 메인화면으로 이동
            notebook = form.save(commit=False)
            notebook.user = request.user
            notebook.save()
            return redirect('notebooks:index')
    # GET요청이 들어오면
    else:
        # Notebook 하나 생성
        form = NotebookForm()
        context = {
            'form': form,
        }
        return render(request, 'notebook/notebook_create.html', context)

# 노트북 안에 있는 Post들 보기
def notebook_detail(request, notebook_id):
    return

# 노트북 수정( 뭐 순서라든가, 안에 Post 삭제라든가, Post Notebook 옮기기라든가)
def notebook_update(request, notebook_id):
    return

# 노트북 삭제 ( 동시에 안에 있는 Post 모두 삭제)
def notebook_delete(request, notebook_id):
    return

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ NOTEBOOK ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ




# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ POST ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# Post 생성
@login_required
def post_create(request, notebook_id):
    # 맞지 않는 값이 있으면 404반환
    notebook = get_object_or_404(Notebook, id=notebook_id, user=request.user)
    # 흐름 : Notebook → Post → Block        
    # 그래서 Post를 먼저 만들고 Post의 pk에 block을 만듦
    if request.method == 'POST':
        # 값 받아오기
        title = request.POST.get('title')
        block_types = request.POST.getlist('block_type')
        block_contents = request.POST.getlist('block_content')

        # Post 객체 생성( Block은 반드시 Post에 속해야 한다 )
        post = Post.objects.create(notebook=notebook, title=title)

        # 받아온 값 순회해서 block 객체 생성
        for i, (b_type, b_content) in enumerate(zip(block_types, block_contents)):
            if b_content.strip():   # 빈 블록 제거
                # block 생성
                Block.objects.create(post=post, type=b_type, content=b_content, order=i)

        return redirect('notebooks:index')
    # 
    else:
        form = NotebookForm()
        context = {
            'form' : form
        }
        return render(request, 'notebook/post_create.html', context)

# Post 세부정보 보기 ( 정리해놓은 block들 보기 )
def post_detail(request, post_id):
    return

# Post 수정 ( 뭐 block들 위치를 바꾼다던가, 이미지를 바꾸거나 글을 수정한다던가... )
def post_update(request, post_id):
    return

# Post 삭제( 동시에 안에있는 block들까지 모두 삭제 )
def post_delete(request, post_id):
    return

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ POST ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
