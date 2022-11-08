import csv


def parse_csv():
    result = []
    with open("./posts.csv", encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            result.append({'text': row['text'], 'created_date': row['created_date'], 'rubrics': row['rubrics']})
    return result
