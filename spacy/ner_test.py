import declare as db
import pandas as pd

Q = (
    db.session
    .query(db.Bruto, db.Entidade)
    .join(db.Bruto.entidades)
    .filter(db.Entidade.categoria == 'NUMBER')
    )

test_df = pd.read_sql(Q.statement, db.connect)
