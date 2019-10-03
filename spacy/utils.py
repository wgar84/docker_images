def generate_train_set(df):
    df = df.drop('id', axis=1)
    df = df.where(~df.isnull(), '')
    d_list = df.to_dict(orient='records')
    train_list = []
    for d in d_list:
        sentence = d.pop('sentence')
        entity_list = []
        for k, v in d.items():
            if v is '':
                continue
            if '; ' in v:
                v_list = v.split('; ')
                for va in v_list:
                    begin = sentence.find(va)
                    end = begin + len(va)
                    entity = (begin, end, k)
                    entity_list.append(entity)
            else:
                begin = sentence.find(v)
                end = begin + len(v)
                entity = (begin, end, k)
                entity_list.append(entity)

        if entity_list:
            train_set = (sentence, {'entities': entity_list})
            train_list.append(train_set)

    return train_list
