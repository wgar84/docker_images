import os
import banco_dou as db
import spacy
import codecs
import sys
from sqlalchemy.sql.expression import func

spacy.require_gpu()

nlp = spacy.load('model/')

sys.stdout = open(sys.stdout.fileno(), mode='w', encoding='utf8', buffering=1)

sys.stdin = codecs.getreader('cp1252')(sys.stdin)

# sys.stdin.encoding


def processa_entrada(text, options):
    output = ''
    while output not in options:
        output = input(text)

    return output


query = (
    db.session
    .query(db.Bruto)
    .filter(~db.Bruto.entidades.any())
    .order_by(func.random())
    .limit(100)
    )

map_cats = {
    'a': 'ACT',
    'n': 'NAME',
    'p': 'POS',
    'i': 'INST',
    'd': 'DOCTYPE',
    'r': 'NUMBER'
    }

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

for entry in query.all():

    entries = entry.conteudo.split('. ')

    for e in entries:
        dec_text = e
        doc = nlp(e)

        if not doc.ents:
            continue

        for ent in doc.ents:

            sys.stdout.write(str(entry.id) + ': ' + dec_text)
            sys.stdout.write('\n')
            sys.stdout.write(ent.label_ + ": " + ent.text)
            sys.stdout.write('\n')

            # cat = input('Categoria [a/n/p/i/d/r/q(next)]: ')
            action = processa_entrada(
                '[Accept/Modify/Remove]: ',
                ['a', 'm', 'r']
                )

            if action == 'r':
                continue

            elif action == 'm':
                cat = processa_entrada(
                    'Categoria [a/n/p/i/d/r/q(next)]: ',
                    ['a', 'n', 'p', 'i', 'd', 'r', 'q']
                    )

                cat_entry = map_cats[cat]

                excerto = input('Texto: ')
                sys.stdout.write('\n')

                new_entity = db.Entidade(
                        id_ent=new_id,
                        categoria=cat_entry,
                        fonte='train',
                        valor=excerto
                        )
                new_id += 1
                entry.entidades.append(new_entity)
                ent_list.append(new_entity)

                dec_text = dec_text.replace(excerto, '')

            elif action == 'a':

                new_entity = db.Entidade(
                        id_ent=new_id,
                        categoria=ent.label_,
                        fonte='train',
                        valor=ent.text
                        )
                new_id += 1
                entry.entidades.append(new_entity)
                ent_list.append(new_entity)

                dec_text = dec_text.replace(ent.text, '')

        extra = processa_entrada('Anything Else? [y/n]: ', ['y', 'n'])

        if extra == 'y':
            while 1:
                sys.stdout.write(dec_text)
                sys.stdout.write('\n')

                cat = processa_entrada(
                    'Categoria [a/n/p/i/d/r/q(next)]: ',
                    ['a', 'n', 'p', 'i', 'd', 'r', 'q']
                    )

                if cat == 'q':
                    break

                cat_entry = map_cats[cat]

                excerto = input('Texto: ')
                sys.stdout.write('\n')

                new_entity = db.Entidade(
                        id_ent=new_id,
                        categoria=cat_entry,
                        fonte='train',
                        valor=excerto
                        )
                new_id += 1
                entry.entidades.append(new_entity)
                ent_list.append(new_entity)

                dec_text = dec_text.replace(excerto, '')

        db.session.add_all(ent_list)
        db.session.commit()
        ent_list = []

    quit = processa_entrada('Quit? [y/n]: ', ['y', 'n'])
    sys.stdout.write('\n')
    os.system('clear')
    if quit == 'y':
        break
