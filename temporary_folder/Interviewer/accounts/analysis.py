import cv2
from deepface import DeepFace
import json
# from . import queue
def analyze(queue):
    temp = []
    res = {}
    while len(queue) > 0:

        # if len(queue)>0 :

        # analysis
        data = queue.pop(-1)
        cap = cv2.VideoCapture(data[1])

        di = {}
        flag = True
        f = open("emotions.txt", "w")
        count =0
        di ={"happy":0, "sad":0, "angry":0, "neutral":0, "surprise":0, "fear":0, "disgust":0}
        while flag:
            ret, frame = cap.read()
            # print(ret)
            # print(count)
            if ret:
                if count %8 ==0:
                    result = DeepFace.analyze(frame, actions = ['emotion'], enforce_detection=False)
                    f.write(result['dominant_emotion'])
                    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                    # cv2.imshow('Original video', frame)
                    emotions = result['dominant_emotion']
                    di[emotions] += 1
                    # di.append(result['dominant_emotion'])
            else:
                flag = False
                # continue

            count +=1
            
            if cv2.waitKey(2) & 0xFF == ord('q'):
                break
            # print(result['dominant_emotion'])
        cap.release()
        cv2.destroyAllWindows()
        # print(data[0])
        res[data[0]] = di
        with open("result.json","w") as file :
            json.dump(res,file)
        temp.append((data[0],di))

            
        # else:
        #     break
    # return temp
    