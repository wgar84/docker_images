import os
import utils
import random
import pandas as pd
import spacy
from spacy.util import minibatch, compounding
import banco_dou as db

spacy.require_gpu()

tset_1 = pd.read_csv('training_set_1.csv', sep='\t')
tset_1 = tset_1.where(~tset_1.isnull(), '')

tset_2 = pd.read_csv('training_set_2.csv', sep='\t')
tset_2 = tset_2.where(~tset_2.isnull(), '')

tset_3 = pd.read_csv('training_set_3.csv', sep='\t')
tset_3 = tset_3.where(~tset_3.isnull(), '')

tset_4 = pd.read_csv('training_set_4.csv', sep='\t')
tset_4 = tset_4.where(~tset_4.isnull(), '')

tset = pd.concat([tset_1, tset_2, tset_3, tset_4]).to_dict(orient='records')

bruto_q = (
    db.session
    .query(db.Bruto)
    )

last_entity = (
    db.session
    .query(db.Entidade)
    .order_by(db.Entidade.id_ent.desc())
    .first()
    )

if last_entity:
    last_id = last_entity.id_ent
else:
    last_id = 0

new_id = last_id + 1

ent_list = []

for d in tset:
    id = d.pop('id')
    bruto = (
        bruto_q
        .filter(db.Bruto.id == id)
        .one_or_none()
        )

    if not bruto:
        continue

    d.pop('sentence')
    for k, v in d.items():

        if v == '':
            continue

        vs = str(v).split('; ')

        for v in vs:
            new_entity = db.Entidade(
                id_ent=new_id,
                categoria=k,
                valor=v,
                fonte='train'
                )

            new_id += 1
            bruto.entidades.append(new_entity)
            ent_list.append(new_entity)

db.session.add_all(ent_list)
db.session.commit()
