# AttendanceMarker

## Data Preparation

Please keep your iamges in this format, and the folder should be named according to the student's name in csv, For example if student's name in CSV is 'Ali Raza' then the folder should be name 'ali_raza' and accordingly.

```
|
|__Train
        |__name1_name2
        |__name1_name2
        |__name1_name2
```

## Instructions 
- After setting up the data, run the train.py file once, this should generate a weights file ```data.pt```, which will be used for inference.
- Then pass the path to ```students.csv``` file which contains records of name, email, and presence. The presence column will be filled by the program automatically and all the absent students will receive an email notifying them.
- The ```inference.py``` file contains an attirbute to control how long the function will run, basically a timer.
    


