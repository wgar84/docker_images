import re
import spacy
import banco_dou as db
from cupy.cuda.memory import OutOfMemoryError

spacy.require_gpu()

def register_ents(doc):
    global new_id

    for ent in doc.ents:

        new_entity = db.Entidade(
            id_ent=new_id,
            categoria=ent.label_,
            fonte='ner',
            valor=ent.text
        )
        new_id += 1
        entry.entidades.append(new_entity)

        db.session.add(new_entity)

        if not new_id % 100:
            print(new_id)
            db.session.commit()

nlp = spacy.load('model/')

# entries without entities
Q_bruto = (
    db.session
    .query(db.Bruto)
    .filter(~db.Bruto.entidades.any())
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

for entry in Q_bruto.all():
    sen = entry.conteudo

    if len(sen) > 1000000:
        print('BIG: {}'.format(entry.id))

        sents = sen.split('.')
        docs = [nlp(s) for s in sents]
        docs = [d for d in docs if d.ents]
        for d in docs:
            register_ents(d)

        continue

    try:
        doc = nlp(sen)
    except OutOfMemoryError:
        print('OOM: {}'.format(entry.id))

        sents = sen.split('.')
        docs = [nlp(s) for s in sents]
        docs = [d for d in docs if d.ents]
        for d in docs:
            register_ents(d)

        continue

    if not doc.ents:
        continue

    register_ents(doc)

db.session.commit()
db.session.close()
