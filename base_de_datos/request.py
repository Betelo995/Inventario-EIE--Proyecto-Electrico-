import requests
import json

url = 'https://app.nanonets.com/api/v2/OCR/Model/34353217-1d3f-4511-b86f-e24e842e66e8/LabelFile/?async=false'



data = {'file': open('prueba.jpg', 'rb')}

response = requests.post(url, auth=requests.auth.HTTPBasicAuth('0DeaHQHCf7qAs9n7mFAGmF9gHd6IVMA9', ''), files=data)

response_json = response.text
response_json = json.loads(response_json)
placa = response_json["result"][0]['prediction'][0]['ocr_text']
