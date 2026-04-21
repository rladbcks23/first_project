from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notebook, Post, Block
from .forms import NotebookForm, PostForm
import re

# @login_required
# 이 문자는 로그인확인을 위한 데코레이터로
# 포스트나 노트북은 각 계정마다 본인의 노트북과 포스트가 보여야 하기때문에 
# 넣었음 

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ MAIN ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ

@login_required
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
    # POST 요청이 들어오면(값이 들어왔다는 뜻)
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
@login_required
def notebook_detail(request, notebook_id):
    notebook = get_object_or_404(Notebook, id=notebook_id, user=request.user)
    posts = notebook.posts.all().order_by('-created_at')
    # notebook : 해당 유저의 노트북 가져오기 (title이랑 id 가져와야지)
    # posts : 해당 notebook에 있는 posts 가져오기 

    context = {
        'notebook': notebook,
        'posts': posts,
    }
    return render(request, 'notebook/notebook_detail.html', context)

# 노트북 수정( 뭐 순서라든가, 안에 Post 삭제라든가, Post Notebook 옮기기라든가)
@login_required
def notebook_update(request, notebook_id):
    notebook = get_object_or_404(Notebook, id=notebook_id, user=request.user)
    # notebook : 수정할 노트북 가져오기

    # POST 요청일 시(수정 완료시) 유효성 검사 후 저장 밑 반환
    if request.method == 'POST':
        form = NotebookForm(request.POST, instance=notebook)
        # 유효성검사
        if form.is_valid():
            form.save()
            return redirect('notebooks:notebook_detail', notebook.id)
    # 그게 아니면 생성할 때 넣어놓은 기본값을 불러오기
    else:
        form = NotebookForm(instance=notebook)
        # instance=notebook : 생성할 때 넣어놓은 기본값을 불러오기
        context = {
            'form': form,
            'notebook': notebook,
        }
        return render(request, 'notebook/notebook_update.html', context)

# 노트북 삭제 ( 동시에 안에 있는 Post 모두 삭제 )
@login_required
def notebook_delete(request, notebook_id):
    notebook = get_object_or_404(Notebook, id=notebook_id, user=request.user)

    # POST 요청이 있을때만 삭제 가능
    if request.method == 'POST':
        notebook.delete()
        return redirect('notebooks:index')
    # GET요청 제한 ( 그냥 직접 url치고 들어오면 detail로 반환 )
    else:
        return redirect('notebooks:notebook_detail', notebook.id)

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ NOTEBOOK ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ




# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ POST ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
# Post 생성
@login_required
def post_create(request, notebook_id):
    # 노트북 가져오기
    notebook = get_object_or_404(Notebook, id=notebook_id, user=request.user)

    if request.method == 'POST':
        form = PostForm(request.POST)

        if form.is_valid():
            post = form.save(commit=False)
            post.notebook = notebook
            post.save()

            block_data = {}

            for key, value in request.POST.items():
                match = re.match(r'^blocks\[(\d+)\]\[(type|content)\]$', key)
                if match:
                    idx, field = match.groups()
                    idx = int(idx)
                    block_data.setdefault(idx, {})
                    block_data[idx][field] = value

            for key, uploaded_file in request.FILES.items():
                match = re.match(r'^blocks\[(\d+)\]\[(image|video)\]$', key)
                if match:
                    idx, field = match.groups()
                    idx = int(idx)
                    block_data.setdefault(idx, {})
                    block_data[idx][field] = uploaded_file

            for order, idx in enumerate(sorted(block_data.keys())):
                item = block_data[idx]
                block_type = item.get('type')

                if block_type == 'text':
                    content = item.get('content', '').strip()
                    if not content:
                        continue
                    Block.objects.create(
                        post=post,
                        block_type='text',
                        content=content,
                        order=order
                    )

                elif block_type == 'image':
                    image = item.get('image')
                    if not image:
                        continue
                    Block.objects.create(
                        post=post,
                        block_type='image',
                        image_file=image,
                        order=order
                    )

                elif block_type == 'video':
                    video = item.get('video')
                    if not video:
                        continue
                    Block.objects.create(
                        post=post,
                        block_type='video',
                        video_file=video,
                        order=order
                    )

            return redirect('notebooks:post_detail', post.id)

    else:
        form = PostForm()

    return render(request, 'post/post_create.html', {
        'notebook': notebook,
        'form': form,
    })

# Post 세부정보 보기 ( 정리해놓은 block들 보기 )
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, notebook__user=request.user)
    # order 기준 정렬
    blocks = post.blocks.all().order_by('order')
    notebook = post.notebook
    # 값 가져오기

    context = {
        'post': post,
        'blocks': blocks,
        'notebook': notebook,
    }
    # 값 넘기기
    return render(request, 'post/post_detail.html', context)

# Post 수정 ( 뭐 block들 위치를 바꾼다던가, 이미지를 바꾸거나 글을 수정한다던가... )
# 수정 완료시 원래 block들을 전부 삭제하고 수정할때 만든 block들을 다시 load
@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id, notebook__user=request.user)

    if request.method == 'POST':
        title = request.POST.get('title', '').strip()

        if not title:
            blocks = post.blocks.all().order_by('order')
            context = {
                'post': post,
                'blocks': blocks,
            }
            return render(request, 'post/post_update.html', context)

        post.title = request.POST.get('title', '').strip()
        post.save()

        index = 0
        kept_block_ids = []

        while True:
            block_type = request.POST.get(f'blocks[{index}][type]')
            if block_type is None:
                break

            block_id = request.POST.get(f'blocks[{index}][id]')
            delete_flag = request.POST.get(f'blocks[{index}][delete]', '0')

            # 삭제 요청이면 기존 블록 삭제
            if delete_flag == '1':
                if block_id:
                    Block.objects.filter(id=block_id, post=post).delete()
                index += 1
                continue

            # 기존 블록 수정 or 새 블록 생성
            if block_id:
                block = get_object_or_404(Block, id=block_id, post=post)
            else:
                block = Block(post=post)

            block.block_type = block_type
            block.order = index

            if block_type == 'text':
                block.content = request.POST.get(f'blocks[{index}][content]', '')
                # 텍스트 블록이면 파일 필드는 비움
                block.image_file = None
                block.video_file = None

            elif block_type == 'image':
                new_image = request.FILES.get(f'blocks[{index}][image]')

                # 새 이미지가 있을 때만 교체
                if new_image:
                    block.image_file = new_image

                # 이미지 블록이면 content는 비워도 됨
                block.content = ''
                block.video_file = None

            elif block_type == 'video':
                new_video = request.FILES.get(f'blocks[{index}][video]')

                # 새 동영상이 있을 때만 교체
                if new_video:
                    block.video_file = new_video

                block.content = ''
                block.image_file = None

            block.save()
            kept_block_ids.append(block.id)
            index += 1

        # 현재 폼에 없는 기존 블록 정리하고 싶으면 아래 사용
        # 단, delete 플래그 방식이면 보통 없어도 됨
        # Block.objects.filter(post=post).exclude(id__in=kept_block_ids).delete()

        return redirect('notebooks:post_detail', post.id)

    blocks = post.blocks.all().order_by('order')
    context = {
        'post': post,
        'blocks': blocks,
    }
    return render(request, 'post/post_update.html', context)

# Post 삭제( 동시에 안에있는 block들까지 모두 삭제 )
@login_required
def post_delete(request, post_id):
    post = get_object_or_404(Post, id=post_id, notebook__user=request.user)
    # notebook__user : 언더바가 2개인 이유는 관계를 따라간다는 뜻
    # --> Post의 notebook의 user가 request.user인 것만 가져와라( == 본인인증 )

    notebook_id = post.notebook.id
    # post 삭제하면 notebook으로 돌아가야하는데 그 id 받아오기

    # POST 요청이 있을때만 삭제 가능
    if request.method == 'POST':
        post.delete()
        return redirect('notebooks:notebook_detail', notebook_id)
    # GET요청 제한 ( 그냥 직접 url치고 들어오면 detail로 반환 )
    else:
        return redirect('notebooks:post_detail', post.id)

# ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ POST ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ
