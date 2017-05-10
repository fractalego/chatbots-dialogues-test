Simple code to generate dialogues according to the shortest path in the conversation
====================================================================================

This is the code related [this blog
page](https://fractalego.github.io/chatbot/2017/05/10/hurried-dialogues.html).

In order to create the data you must first train the doc2vec model

```bash
$ python3 train_word2vec_model.py
```
```bash
$ python3 create_tsne_vectors.py
```
```bash
$ python3 clustering.py
```


Then you can generate the dialogues using


```bash
$ python3 generate_dialogues.py
```