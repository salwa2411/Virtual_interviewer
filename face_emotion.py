import cv2
from deepface import DeepFace
cap = cv2.VideoCapture(1)
if not cap.isOpened():
    cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise IOError("Cannot open webcam")
di ={"happy":0, "sad":0, "angry":0, "neutral":0, "surprise":0, "fear":0}
count = 0
while True:
    ret, frame = cap.read()
    result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
    emotions = result['dominant_emotion']
    di[emotions] += 1
    count += 1
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.imshow('Original video', frame)
    if cv2.waitKey(2) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
maximum = max(di.items(), key=lambda x:x[1])
print(di)
print("Emotion",maximum[0])



