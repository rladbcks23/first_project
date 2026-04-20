from django.shortcuts import render
from django.core.files.storage import default_storage

def image(request):
    if request.method == 'POST':        # 이미지 파일
        if request.FILES.get('image'):
            file = request.FILES['image']
            
            filename = default_storage.save(file.name, file)
            file_url = default_storage.url(filename)
            print(filename)
            print(file_url)
            print(type(default_storage))

            return render(request, 'index.html', {
                'file_url': file_url,
            })
        
        elif request.FILES.get('video'):    # 영상파일
            file = request.FILES['video']

            filename = default_storage.save(file.name, file)
            file_url = default_storage.url(filename)
            print(filename)
            print(file_url)
            print(type(default_storage))

            return render(request, 'index.html', {
                'file_url': file_url,
            })

    return render(request, 'index.html')
