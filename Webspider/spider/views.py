
from spider.utils import main_func
from django.shortcuts import render
from spider.forms import UrlForm



def linkview(request):
    if request.method == 'POST':
        urlform = UrlForm(request.POST)
        urlform.is_valid()
        Urls=set()
        main_dic={}
        relations= []
        url= urlform.cleaned_data['url']
        results=main_func(url,5,Urls,1,main_dic,relations)
        context= {'form':urlform, 'Urls':results}
        return render(request, "spider/linkview.html", context)
    else:
        urlform = UrlForm()
        return render(request, 'spider/index.html',{'form':urlform})
    