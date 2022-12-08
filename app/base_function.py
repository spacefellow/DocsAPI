import csv


def parse_csv():
    result = []
    with open("./posts.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append({'text': row['text'], 'created_date': row['created_date'], 'rubrics': row['rubrics']})
    return result


def model_to_dict(model):
    res = {
        'id': model.id,
        'text': model.text,
        'rubrics': model.rubrics,
        'created_date': model.created_date
    }
    return res
