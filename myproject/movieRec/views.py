from django.shortcuts import render, HttpResponse
from . import main
import csv
from io import StringIO
from django.http import JsonResponse

def home(request):
    return render(request, 'index.html')

def input(request):
    if request.method == 'POST':
        uploaded_file = request.FILES.get('csv_file')
        if uploaded_file:
            # You can read the file content if needed
            file_data = uploaded_file.read().decode('utf-8')
            print("uploaded successfully.")
            csv_reader = csv.reader(StringIO(file_data))
            rows = [row for row in csv_reader]
            liked_movies = [row[0] for row in rows if row] 
            results = main.recommend_for_user(
                liked_movies,  # pass as a list of strings
                main.top_neighbors,
                top_n=5
            )
            #return HttpResponse(f"File '{uploaded_file.name}' uploaded successfully!<br>Content:<br>{file_data[:200]}...")
            #return HttpResponse(results.html())

            data = results.to_dict(orient='records')
            return JsonResponse({'results': data})

        else:
            print("No file uploaded.")
            return HttpResponse("No file uploaded.")
    return HttpResponse("Invalid request method.")
