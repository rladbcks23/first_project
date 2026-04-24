from django.db import models
from django.conf import settings

# 폴더 역할
class Notebook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 유저 확인
    name = models.CharField(max_length=100, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 페이지 구분
class Post(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='posts') # 상속
    title = models.CharField(max_length=200, null=False) # 제목
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):  
        return self.title

# 노트북 파일의 경우 한 페이지당 여러 셀(본문?)이 있는데 그 블록 역할
class Block(models.Model):
    # 블록 종류 정의 ) 한 블록당 한가지 형태의 파일만 들어가도록.
    BLOCK_TYPES = [
        ('text', '텍스트'),
        ('image', '이미지'),
        ('video', '동영상'),
    ]

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='blocks') # 상속
    block_type = models.CharField(max_length=10, choices=BLOCK_TYPES, default='text') # 블록의 유형
    content = models.TextField(blank=True)          # text 내용 / image URL / video URL
    image_file = models.ImageField(upload_to='blocks/images/', blank=True, null=True)
    video_file = models.FileField(upload_to='blocks/videos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0) # 순서

    def __str__(self):
        return f'{self.post.title} - {self.block_type}'
