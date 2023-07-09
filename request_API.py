import requests

url = 'http://127.0.0.1:8000/predict'
params_dict = {'vidPath':r'F:\PyCode\face_rec\sample_vid.mp4', 
               'weightsPath':r'F:\PyCode\face_rec\data.pt',
               'csvPath':r'F:\PyCode\face_rec\students.csv'}

resp = requests.post(url, params=params_dict)
# resp = requests.post(url, params={'v_Path':"/content/drive/MyDrive/DemoVideos/testvid18.mp4"})

print(resp.content)