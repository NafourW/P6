from gensim.models import Word2Vec
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
import pandas as pd
import time
import os
import re

class modelSetup:

    def train_model(sent):
        print('[+] Training the model')
        start_training = time.time()

        # Train the model with the given(sent) text corpus
        model = Word2Vec(sent, min_count=1, size=100, workers=4, window=4, sg=0)

        end_training = time.time()
        print('     ..Total time (s) for preparing data = ' + str(end_training - start_training))

        # Save the model after training
        saved_model = model.save("trainedModel/word2vec.model")

        return saved_model


    def dataManipulation():
        with open("logfiles/test_c.rcl", "r") as file:
            listOfLine = []
            listOfList = []
            counter = 0
            for line in file:
                l = re.split(r"[\t \n ( ) ' , :]+", line)
                print(l)
                listOfLine.append(l)
             
                counter += 1

                print("Lines loaded: " + str(counter), end="\r")
        
        print("Lines loaded: " + str(counter))
        

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

        plt.show()

        print('     ..Done loading model\n')

        print(df)
        print(model.wv.most_similar('bye',topn=10))
        
t = modelSetup.dataManipulation()
q = modelSetup.loadModel()