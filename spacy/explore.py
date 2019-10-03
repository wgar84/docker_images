import random
import pandas as pd
import banco_dou as db

predicted_q = (
    db.session
    .query(db.Bruto, db.Entidade)
    .join(db.Bruto.entidades)
    .filter(db.Entidade.fonte == 'ner')
    .order_by(db.Bruto.id)
    )

predicted_df = pd.read_sql(predicted_q.statement, db.connect)
