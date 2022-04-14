from tensorflow.keras.models import load_model
import numpy as np
import librosa
import os
class livePredictions:

    def __init__(self, path=r"..\Interviewer\static\model\testing10_model.h5"):
        self.path = path
        # self.file = file
        print("loading Model ...")
        self.loaded_model =load_model(self.path)
        # print(self.loaded_model.summary())


    # def load_model(self):
    #     self.loaded_model = keras.models.load_model(self.path)
    #     return self.loaded_model.summary()

    def makepredictions(self,file):
        data, sampling_rate = librosa.load(file)
        mfccs = np.mean(librosa.feature.mfcc(y=data, sr=sampling_rate, n_mfcc=40).T, axis=0)
        x = np.expand_dims(mfccs, axis=1)
        x = np.expand_dims(x, axis=0)
        # predictions = self.loaded_model.predict_classes(x)
        predictions = np.argmax(self.loaded_model.predict(x), axis=-1)
        # print("Prediction is", " ", self.convertclasstoemotion(predictions))
        pred = self.convertclasstoemotion(predictions)
        # print(pred)
        return pred

    @staticmethod
    def convertclasstoemotion(pred):        
        label_conversion = {'0': 'neutral',
                            '1': 'calm',
                            '2': 'happy',
                            '3': 'sad',
                            '4': 'angry',
                            '5': 'fearful',
                            '6': 'disgust',
                            '7': 'surprised'}

        for key, value in label_conversion.items():
            if int(key) == pred:
                label = value
        return label

# pred = livePredictions()
# path='testing10_model.h5',file='angry.wav'
# pred.load_model()
# (?# file_path =r"E:\Project-Testing\Virtual_interviewer\temporary_folder\Interviewer\media\audioData")
# files = os.listdir(file_path)

# for file in files:
#     pred.makepredictions(file_path+"\\"+file)
