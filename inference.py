import torch
from PIL import Image
from facenet_pytorch import MTCNN, InceptionResnetV1
import pandas as pd
import cv2 as cv
from mailthon import postman, email
from fastapi import FastAPI
from tqdm import tqdm
import uvicorn
import time

def face_match(img_arr, data_path): # img_path= location of photo, data_path= location of data.pt
    # getting embedding matrix of the given img
    img = Image.fromarray(img_arr)
    mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20)
    resnet = InceptionResnetV1(pretrained='vggface2').eval()
    face, prob = mtcnn(img, return_prob=True) # returns cropped face and probability
    emb = resnet(face.unsqueeze(0)).detach() # detech is to make required gradient false

    # data_path = 'data.pt'
    saved_data = torch.load(data_path) # loading data.pt file
    embedding_list = saved_data[0] # getting embedding data
    name_list = saved_data[1] # getting list of names
    dist_list = [] # list of matched distances, minimum distance is used to identify the person

    for idx, emb_db in enumerate(embedding_list):
        dist = torch.dist(emb, emb_db).item()
        dist_list.append(dist)

    # print(dist_list)
    idx_min = dist_list.index(min(dist_list))
    return (name_list[idx_min], min(dist_list))

app = FastAPI()
@app.post('/predict')
def main(vidPath=None, weightsPath=None, csvPath=None):
    if weightsPath is None or csvPath is None:
        raise ValueError('Either Weights Path or CSV Path was not provided, it cannot be none.')
    
    wt_pth = weightsPath
    pth = vidPath if vidPath != None else 0
    csv_pth = csvPath
    # pth = '/content/sample_vid.mp4'
    # wt_pth = '/content/data.pt'
    # csv_pth = '/content/students.csv'

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    mtcnn = MTCNN(image_size=160, margin=0, min_face_size=20, device=device)
    df = pd.read_csv(csv_pth)
    df['name'] = df['name'].str.lower()

    done = []
    minutes = 2
    max_time = 60 * minutes 
    start_time = time.time()
    cap = cv.VideoCapture(pth)

    if (cap.isOpened() == False):
        print("Error opening video stream or file")

    # Read until video is completed
    # all_frames = int(cap.get(cv.CAP_PROP_FRAME_COUNT))
    # progress_bar = iter(tqdm(range(all_frames)))
    while (time.time() - start_time) < max_time:
        # Capture frame-by-frame
        Frame = cap.get(cv.CAP_PROP_POS_FRAMES)
        ret, frame = cap.read()
        if ret:
            frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            name, conf = face_match(frame, wt_pth)
            if not (name in done):
                #Lesser distance means a better prediction. So we need to discard predictions with 
                #distance greater than some threshold, threshold = 0.8
                print(f"{name.replace('_', ' ').title()} recognized. Distance Score: {conf}")
                if conf < 0.8:
                    done.append(name)
                    if any(df['name'].str.contains(name.replace('_', ' ').lower())):
                        df.loc[df['name'] == name.replace('_', ' ').lower(), 'presence'] = 'P'
        else:
            print('Error reading frame#{}'.format(Frame))
            break
    cap.release()


    print()
    print('Timer Ended.')
    print()
    df.loc[df['presence'] != 'P', 'presence'] = 'A'
    absentees = list(df.loc[df['presence'] == 'A', 'email'].values)

    absent_names = list(df.loc[df['presence'] == 'A', 'name'].values)
    for abs in absent_names:
        print(f"{abs.replace('_', ' ').title()} is absent.")

    p = postman(host='smtp.gmail.com', auth=('awaisnawaz2000@gmail.com', 'fbcabwnopmdugkhx'))
    r = p.send(email(
            content=u'<p>This user is absent</p>',
            subject='Absentee Report',
            sender='Awais <awaisnawaz2000@gmail.com>',
            receivers=absentees,
        ))
    
    print()
    print('Email sent to absentees.')
    
if __name__ == '__main__':
    uvicorn.run(app='inference:app', host='127.0.0.1', port=8000, reload=True)
    # v_Path = r'F:\PyCode\face_rec\sample_vid.mp4'
    # wt_Path = r'F:\PyCode\face_rec\data.pt'
    # csv_Path = r'F:\PyCode\face_rec\students.csv'
    # main(v_Path, wt_Path, csv_Path)

