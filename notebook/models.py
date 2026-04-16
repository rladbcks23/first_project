from django.db import models
from django.conf import settings

# 폴더 역할
class Notebook(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) # 유저 확인
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

# 페이지 구분
class Post(models.Model):
    notebook = models.ForeignKey(Notebook, on_delete=models.CASCADE, related_name='posts') # 상속
    title = models.CharField(max_length=200) # 제목
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return self.title

# 노트북 파일의 경우 한 페이지당 여러 셀(본문?)이 있는데 그 블록 역할    
class Block(models.Model):
    # 블록 종류 정의 ) 한 블록당 한가지 형태의 파일만 들어가도록.
    BLOCK_TYPE_CHOICES = (
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='blocks') # 상속
    type = models.CharField(max_length=10, choices=BLOCK_TYPE_CHOICES) # 해당 블록의 종류
    content = models.TextField(blank=True)  # 텍스트용
    file = models.FileField(upload_to='blocks/', blank=True, null=True)  # 이미지/영상
    order = models.IntegerField(default=0)  # 블록의 순서
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
