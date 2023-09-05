import requests
from django.shortcuts import render
from .models import Parcel

INPOST_API_URL = ''

def create_parcel(request):
    if request.method == 'POST':
        parcel_data = {
            'name': request.POST['name'],
            'address': request.POST['address'],
            # inne dane przesyłki
        }

        # Wywołaj API InPost, aby utworzyć przesyłkę
        response = requests.post(f'{INPOST_API_URL}/parcels', json=parcel_data, headers={'Authorization': 'Bearer API_KEY'})
        
        if response.status_code == 201:
            # Przetwórz odpowiedź i zapisz dane przesyłki w bazie danych
            Parcel.objects.create(number=response.json()['parcel_number'], status='Created', location='')
            return render(request, 'create_parcel.html')
    

def parcel_status(request, parcel_number):
    # Wywołaj API InPost, aby sprawdzić status przesyłki
    response = requests.get(f'{INPOST_API_URL}/parcels/{parcel_number}', headers={'Authorization': 'Bearer API_KEY'})
    
    if response.status_code == 200:
        # Przetwórz odpowiedź i zwróć status przesyłki
        return render(request, 'parcel_status.html', {'status': response.status_code})

def parcels(request):
    return render(request, 'parcels.html', {
        "parcels": {}
    })