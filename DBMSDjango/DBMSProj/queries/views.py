from django.shortcuts import render
from django.http import HttpResponse
from django.http import JsonResponse
from django.template import loader
import mariadb


# try:
#     conn = mariadb.connect(
#         user="roobtj11",
#         password="tr4003",
#         host="washington.uww.edu",
#         port=3306,
#         database="cs366-2231_roobtj11"
#     )
#     print("connection successful??") #REMOVE
# except mariadb.Error as e:
#     print(f"Error connecting to MariaDB Platform: {e}")

# curr = conn.cursor()

def index(request):
    print('iiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii') #REMOVE 
    return render(request, 'index.html')

# def display_content(request):
#     print("HHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHHH")
#     # if request.is_ajax() and request.methof == "GET":
#     resp_data = {
#         'html' : 'stuff'
#     }
#     print(resp_data)
#     return JsonResponse(resp_data, status=200)



    option = request.POST.get('option')
    #run query, etc
    # option = option + 'jjjjjjjjjjj'
    updatedContent = '<p>Updated content: {}</p>'.format(option)
    return HttpResponse({'content': updatedContent})

# curr.execute(
#     "SELECT PlayerName FROM Player LIMIT 10"
# )

# for(PlayerName) in curr:
#     print(PlayerName[0])

# def queries(request):
#     template = loader.get_template('home.html')
#     # return HttpResponse(template.render())
    
#     curr.execute(
#         "SELECT PlayerName FROM Player LIMIT 10"
#     )

#     results = ''.join([f'<div>{PlayerName[0]}</div>' for PlayerName in curr])
#     for(PlayerName) in curr:
#         results = results + PlayerName[0] + '\n'

#     return HttpResponse(results)


    # return HttpResponse("Hello world!")
# Create your views here.
