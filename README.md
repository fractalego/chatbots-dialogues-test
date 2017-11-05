Simple code to generate dialogues according to the shortest path in the conversation
====================================================================================

Install a virtual environment
-----------------------------

```bash
virtualenv env/ --python=/usr/bin/python3

source env/bin/activate

pip install -r requirements.txt
```



Execute the code
----------------

This is the code related [this blog
page](https://fractalego.github.io/chatbot/2017/05/10/hurried-dialogues.html).

In order to create the data you must first train the doc2vec model

```bash
$ python train_word2vec_model.py
```
```bash
$ python create_tsne_vectors.py
```
```bash
$ python clustering.py
```


Then you can generate the dialogues using


```bash
$ python3 generate_dialogues.py
```


DISCLAIMER
----------
This code is merely a toy dialogue generator.
The dialogue generator uses lines from the [Cornell movie corpus](https://www.cs.cornell.edu/~cristian/Cornell_Movie-Dialogs_Corpus.html) and arranges them in different order.
These are lines taken from real movies. I did not modify these lines, nor looked for offensive content.
I completely disassociate myself from any offensive lines that might be randomly chosen and printed out.

