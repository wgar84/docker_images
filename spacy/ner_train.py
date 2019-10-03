import re
import random
import pandas as pd
import spacy
from spacy.util import minibatch, compounding
import banco_dou as db

spacy.require_gpu()

# train set

training_q = (
    db.session
    .query(db.Bruto, db.Entidade)
    .join(db.Bruto.entidades)
    .filter(db.Entidade.fonte == 'train')
    )

train_df = pd.read_sql(training_q.statement, db.connect)

train_data = []

for _, df in train_df.groupby('id'):
    sentence = df.conteudo.tolist()[0]
    # sentence = re.sub('-(?![^0-9])', ' ', sentence)
    ents = []
    for row in df.itertuples():
        cat = row.categoria
        val = row.valor
        # val = re.sub('-(?![^0-9])', ' ', val)
        begin = sentence.find(val)
        end = begin + len(val)
        entity = (begin, end, cat)
        ents.append(entity)
    datum = (sentence, {'entities': ents})
    train_data.append(datum)

# for _, df in train_df.groupby('id'):
#     sentence = df.conteudo.tolist()[0]
#     excertos = sentence.split('. ')
#     for e in excertos:
#         ents = []
#         for row in df.itertuples():
#             cat = row.categoria
#             val = row.valor
#             begin = sentence.find(val)
#             if begin == -1:
#                 continue
#             end = begin + len(val)
#             entity = (begin, end, cat)
#             ents.append(entity)
#             datum = (e, {'entities': ents})
#     train_data.append(datum)

nlp = spacy.blank('pt')

ner = nlp.create_pipe('ner')

nlp.add_pipe(ner, last=True)

for _, annotations in train_data:
    for ent in annotations.get('entities'):
        ner.add_label(ent[2])

n_iter = 100

optimizer = nlp.begin_training()

for itn in range(n_iter):
    random.shuffle(train_data)
    losses = {}
    # batch up the examples using spaCy's minibatch
    batches = minibatch(train_data, size=compounding(4., 32., 1.001))
    for batch in batches:
        texts, annotations = zip(*batch)
        nlp.update(
            texts,  # batch of texts
            annotations,  # batch of annotations
            drop=0.5,  # dropout - make it harder to memorise data
            sgd=optimizer,  # callable to update weights
            losses=losses)
    print('Losses', losses)

# ITS ALIVE!!!!
nlp.to_disk('model/')
