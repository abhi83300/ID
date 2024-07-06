from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import qrcode
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import json
import requests

def index(request):
    return render(request, 'index.html')

@csrf_exempt
def scan_qr(request):
    if request.method == "POST":
        qr_image = request.FILES.get('qrcodeimage')
        
        # Convert the uploaded image to a numpy array
        nparr = np.fromstring(qr_image.read(), np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Decode the QR code
        decoded_objects = decode(img)
        
        if decoded_objects:
            qr_data = decoded_objects[0].data.decode('utf-8')
            
            # Verify data with server
            try:
                response = requests.get(f"https://issuer.ngrok.io/api/v1/enrollee-from-id/{qr_data}")
                if response.status_code == 200:
                    data = response.json()
                    return JsonResponse({
                        "status": "verified",
                        "data": data
                    })
                else:
                    return JsonResponse({"status": "not_verified", "message": "Data not found or invalid"})
            except requests.RequestException:
                return JsonResponse({"status": "error", "message": "Failed to connect to the server"})
        else:
            return JsonResponse({"status": "error", "message": "Unable to decode QR code"})
    
    return JsonResponse({"status": "error", "message": "Invalid request method"})

def generate_qr(request):
    if request.method == "POST":
        data = json.loads(request.body)
        qr_data = str(data['id'])
        
        qr = qrcode.QRCode(version=1, box_size=10, border=5)
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")
        
        response = HttpResponse(content_type="image/png")
        img.save(response, "PNG")
        return response
    
    return JsonResponse({"status": "error", "message": "Invalid request method"})