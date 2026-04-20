from django.shortcuts import render
from django.core.files.storage import default_storage

def image(request):
    if request.method == 'POST' and request.FILES.get('image'):
        file = request.FILES['image']
        # file = request.FILES['image']

        filename = default_storage.save(file.name, file)
        file_url = default_storage.url(filename)
        print(filename)
        print(file_url)
        print(type(default_storage))
        # saved_path = default_storage.save(f'uploads/{file.name}', file)
        # file_url = default_storage.url(saved_path)


        return render(request, 'index.html', {
            'file_url': file_url,
            # 'saved_path': saved_path,
        })

    return render(request, 'index.html')
