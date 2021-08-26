from django.shortcuts import render

# Create your views here.

def search(request):

    if request.method == 'GET':        
        return render(request, 'search.html')
        
        

        
    
