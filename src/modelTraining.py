from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pandas as pd
import time
import json
import os
import re

class modelSetup:

    def train_model(sent):
        print('[+] Training the model')
        start_training = time.time()

        # Train the model with the given(sent) text corpus
        model = Word2Vec(sent, min_count=10, size=42, workers=4, window=1, sg=1)

        end_training = time.time()
        print('     ..Total time (s) for preparing data = ' + str(end_training - start_training))

        # Save the model after training
        saved_model = model.save("trainedModel/word2vec.model")

        return saved_model


    def dataManipulation():
        with open("output.txt", "r") as file:
            listOfLine = []

            for line in file:
                res = re.split("[\D]", line)
                listOfLine.append(list(filter(None, res)))
            
       
        modelSetup.train_model(listOfLine)
    
    def loadModel():
        similarities = []
        print('[+] Load model')
        model = Word2Vec.load('trainedModel/word2vec.model')
        vocab = list(model.wv.vocab)
        X = model[vocab]
        tsne = TSNE(n_components=2)
        X_tsne = tsne.fit_transform(X)
        df = pd.DataFrame(data=X_tsne, index=vocab, columns=['x','y'])
        fig = plt.figure()
        ax = fig.add_subplot(1,1,1)
        ax.scatter(df['x'], df['y'])
        for word, pos in df.iterrows():
            ax.annotate(word, pos)

        #plt.show()

        print('     ..Done loading model\n')

        print(df)
        print(model.wv.most_similar('8',topn=3))
        
t = modelSetup.dataManipulation()
q = modelSetup.loadModel()