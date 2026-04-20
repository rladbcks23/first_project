from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Notebook, Post, Block
from .forms import NotebookForm
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
        title = request.POST.get('title', '').strip()

        # post 가져오기
        post = Post.objects.create(notebook=notebook, title=title)

        # blocks 데이터를 index 기준으로 묶기 위한 dict
        block_data = {}

        # 1. POST 데이터 파싱
        for key, value in request.POST.items():
            # blocks[num][type], blocks[num][content] 같은 구조
            # 여기서 num은 몇번째 블록인지를 뜻함
            match = re.match(r'^blocks\[(\d+)\]\[(type|content)\]$', key)
            if match:
                idx, field = match.groups()
                idx = int(idx)

                block_data.setdefault(idx, {})
                block_data[idx][field] = value

        # 2. FILE 데이터 파싱
        for key, uploaded_file in request.FILES.items():
            # blocks[0][image] or blocks[0][video]
            match = re.match(r'^blocks\[(\d+)\]\[(image|video)\]$', key)
            if match:
                idx, field = match.groups()
                idx = int(idx)
                # default값 삽입 후 값 사입
                block_data.setdefault(idx, {})
                block_data[idx][field] = uploaded_file

        # 3. 각 블록의 유형에 따라 순서대로 block 생성
        for order, idx in enumerate(sorted(block_data.keys())):
        # order는 block 순서를 뜻함 --> 순서대로 block 생성
            item = block_data[idx]
            block_type = item.get('type')

            # 텍스트 블록
            if block_type == 'text':
                content = item.get('content', '').strip()
                if not content:
                    continue

                Block.objects.create(post=post, block_type='text', content=content, order=order)

            # 이미지 블록
            elif block_type == 'image':
                image = item.get('image')
                if not image:
                    continue

                Block.objects.create(post=post, block_type='image', image_file=image, order=order)

            # 비디오 블록
            elif block_type == 'video':
                video = item.get('video')
                if not video:
                    continue

                # # 용량 제한 예시
                # if video.size > 50 * 1024 * 1024:
                #     continue

                Block.objects.create(post=post, block_type='video', video_file=video, order=order)
        # 저장 후 detail화면 반환
        return redirect('notebooks:post_detail', post.id)
    # GET 요청으로 들어올 시
    else:
        return render(request, 'post/post_create.html', {'notebook': notebook})

# Post 세부정보 보기 ( 정리해놓은 block들 보기 )
@login_required
def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id, notebook__user=request.user)
    # order 기준 정렬 
    blocks = post.blocks.all().order_by('order')
    # post랑 post에 있는 block들 불러오기

    context = {
        'post': post,
        'blocks': blocks,
    }
    # 값 넘기기
    return render(request, 'post/post_detail.html', context)

# Post 수정 ( 뭐 block들 위치를 바꾼다던가, 이미지를 바꾸거나 글을 수정한다던가... )
# 수정 완료시 원래 block들을 전부 삭제하고 수정할때 만든 block들을 다시 load
@login_required
def post_update(request, post_id):
    post = get_object_or_404(Post, id=post_id, notebook__user=request.user)

    if request.method == 'POST':
        post.title = request.POST.get('title', '').strip()
        post.save()

        block_data = {}

        # 1. text / hidden 값 파싱
        # blocks[0][type], blocks[0][content], blocks[0][current_image_url], blocks[0][current_video_url]
        for key, value in request.POST.items():
            match = re.match(
                r'^blocks\[(\d+)\]\[(type|content|current_image_url|current_video_url)\]$',
                key
            )
            if match:
                idx, field = match.groups()
                idx = int(idx)
                block_data.setdefault(idx, {})
                block_data[idx][field] = value

        # 2. 새로 업로드한 파일 파싱
        # blocks[0][image], blocks[0][video]
        for key, uploaded_file in request.FILES.items():
            match = re.match(r'^blocks\[(\d+)\]\[(image|video)\]$', key)
            if match:
                idx, field = match.groups()
                idx = int(idx)
                block_data.setdefault(idx, {})
                block_data[idx][field] = uploaded_file

        # 기존 블록 삭제
        # 주의: 아래에서 기존 파일 URL을 hidden input으로 받아서 다시 재생성함
        post.blocks.all().delete()

        # 3. block 재생성
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
                    order=order,
                )

            elif block_type == 'image':
                image = item.get('image')

                # 새 파일이 있으면 그걸 저장
                if image:
                    Block.objects.create(
                        post=post,
                        block_type='image',
                        image_file=image,
                        order=order,
                    )
                    continue

                # 새 파일이 없으면 기존 이미지 URL 유지
                current_image_url = item.get('current_image_url', '').strip()
                if current_image_url:
                    Block.objects.create(
                        post=post,
                        block_type='image',
                        content=current_image_url,
                        order=order,
                    )

            elif block_type == 'video':
                video = item.get('video')

                # 새 파일이 있으면 그걸 저장
                if video:
                    Block.objects.create(
                        post=post,
                        block_type='video',
                        video_file=video,
                        order=order,
                    )
                    continue

                # 새 파일이 없으면 기존 비디오 URL 유지
                current_video_url = item.get('current_video_url', '').strip()
                if current_video_url:
                    Block.objects.create(
                        post=post,
                        block_type='video',
                        content=current_video_url,
                        order=order,
                    )

        return redirect('notebooks:post_detail', post.id)

    else:
        blocks = post.blocks.all().order_by('order')
        context = {
            'post': post,
            'blocks': blocks,   # 여기 중요: block 이 아니라 blocks
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
