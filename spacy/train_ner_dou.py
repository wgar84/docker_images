import utils
import random
import pandas as pd
import spacy
from spacy.util import minibatch, compounding
import banco_dou as db

spacy.require_gpu()

# tset_1 = pd.read_csv('training_set_1.csv', sep='\t')
# tset_1 = tset_1.where(~tset_1.isnull(), '')
#
# tset_2 = pd.read_csv('training_set_2.csv', sep='\t')
# tset_2 = tset_2.where(~tset_2.isnull(), '')
#
# tset_3 = pd.read_csv('training_set_3.csv', sep='\t')
# tset_3 = tset_3.where(~tset_3.isnull(), '')
#
# TRAIN_DATA = (
#     utils.generate_train_set(tset_1) +
#     utils.generate_train_set(tset_2) +
#     utils.generate_train_set(tset_3)
#     )
#
# nlp = spacy.blank('pt')
#
# ner = nlp.create_pipe('ner')
#
# nlp.add_pipe(ner, last=True)
#
# for _, annotations in TRAIN_DATA:
#     for ent in annotations.get('entities'):
#         ner.add_label(ent[2])
#
# n_iter = 100
#
# optimizer = nlp.begin_training()
#
# for itn in range(n_iter):
#     random.shuffle(TRAIN_DATA)
#     losses = {}
#     # batch up the examples using spaCy's minibatch
#     batches = minibatch(TRAIN_DATA, size=compounding(4., 32., 1.001))
#     for batch in batches:
#         texts, annotations = zip(*batch)
#         nlp.update(
#             texts,  # batch of texts
#             annotations,  # batch of annotations
#             drop=0.5,  # dropout - make it harder to memorise data
#             sgd=optimizer,  # callable to update weights
#             losses=losses)
#     print('Losses', losses)
#
# for text, _ in TRAIN_DATA:
#     doc = nlp(text)
#     print('Entities', [(ent.text, ent.label_) for ent in doc.ents])
#     print('Tokens', [(t.text, t.ent_type_, t.ent_iob) for t in doc])
#
# # ITS ALIVE!!!!
# nlp.to_disk('model/')

nlp = spacy.load('model/')

# db.session.rollback()

# vamo pegar tudo
Q = (
    db.session
    .query(db.Bruto)
    .order_by(db.Bruto.id)
    )

full_docs = []

for entry in Q.all():
    sentences = entry.conteudo.split('. ')
    id = entry.id
    print(id)
    for s in sentences:
        df_entry = {
            'id': str(id),
            'sentence': s,
            'ACT': [],
            'NAME': [],
            'POS': [],
            'INST': [],
            'DOCTYPE': [],
            'NUMBER': []
            }
        doc = nlp(s)
        if doc.ents:
            for ent in doc.ents:
                df_entry[ent.label_].append(ent.text)

        clean_entry = {}

        for k, v in df_entry.items():
            if k not in ['id', 'sentence']:
                clean_entry[k] = '; '.join(v)
            else:
                clean_entry[k] = v

        full_docs.append(clean_entry)

docs_df = pd.DataFrame(full_docs)

docs_df.tail(20)

(
    docs_df
    [['id', 'sentence', 'ACT', 'NAME', 'POS', 'INST', 'DOCTYPE', 'NUMBER']]
    .to_csv('attempt_with_docs.csv', sep='\t')
    )
