import banco_dou as db
import pandas as pd

all_q = (
    db.session
    .query(db.Bruto)
    .order_by(db.Bruto.id.desc())
    )

sent_list = []

for entry in all_q.limit(1000).all():
    content = entry.conteudo
    sentences = content.split('. ')
    for s in sentences:
        sent_list.append({'id': entry.id, 'sentence': s})

pd.DataFrame(sent_list).to_csv('to_train.csv')
