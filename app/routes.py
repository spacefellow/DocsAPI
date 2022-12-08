from flask import url_for, request, redirect, current_app, jsonify
from init import create_app, db, PER_PAGE
from config import app_config
from models import Document
from base_function import parse_csv, model_to_dict
from flask_swagger_ui import get_swaggerui_blueprint

app = create_app(app_config)

SWAGGER_URL = '/swagger'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Todo List API"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix=SWAGGER_URL)


@app.route("/", methods=["GET", "POST"], defaults={"page": 1})
@app.route("/<int:page>", methods=["GET", "POST"])
def allDocs(page):
    docs = Document.query.paginate(page=page, per_page=PER_PAGE)
    data = []

    for doc in docs.items:
        data.append(model_to_dict(doc))

    meta = {
        "page": docs.page,
        'pages': docs.pages,
        'total_count': docs.total,
        'prev_page': docs.prev_num,
        'next_page': docs.next_num,
        'has_next': docs.has_next,
        'has_prev': docs.has_prev,

    }
    return jsonify({'data': data, "meta": meta})


@app.route("/doc/<int:id>", methods=["GET", "POST"])
def doc_detail(id):
    doc = Document.query.get_or_404(id)
    res = model_to_dict(doc)
    return jsonify(res)


@app.route("/search", methods=["GET", "POST"])
def search():
    q = request.args["q"].lower()
    data = current_app.elasticsearch.search(index="documents", size=20,
                                            body={"query":
                                                      {"multi_match":
                                                           {"query": q,
                                                            "fields": ["text"]
                                                            }
                                                       }
                                                  }
                                            )

    res = []
    for doc in data['hits']['hits']:
        buf = Document.query.filter_by(text=doc['_source']['text']).first_or_404()
        res.append({
            'text': doc['_source']['text'],
            'rubrics': buf.rubrics,
            'created_date': buf.created_date
        })
    res.sort(key=lambda obj: obj['created_date'], reverse=True)
    return jsonify(res[:20])


@app.route("/delete/<int:id>", methods=["DELETE"])
def delete(id):
    try:
        doc = Document.query.get_or_404(id)
        db.session.delete(doc)
        current_app.elasticsearch.delete(index="documents", id=id, ignore=404)
        db.session.commit()
        return f'Document was successfully deleted'
    except Exception as e:
        return f'Cannot delete document because of {e}'


@app.route("/add", methods=["GET", "POST"])
def add():
    elements = parse_csv()
    doc_id = 1
    for elem in elements:
        if not Document.query.filter_by(id=doc_id,
                                        created_date=elem['created_date'],
                                        text=elem['text'],
                                        rubrics=elem['rubrics']).first():
            document = Document(created_date=elem['created_date'],
                                text=elem['text'],
                                rubrics=elem['rubrics'],
                                id=doc_id)
            db.session.add(document)
            db.session.commit()
        doc_id += 1
    docs = Document.query.all()
    current_app.elasticsearch.indices.delete(index="documents", ignore=404)
    current_app.elasticsearch.indices.create(index="documents", ignore=400)
    id = 1
    for doc in docs:
        data = {
            "text": doc.text
        }
        current_app.elasticsearch.index(index="documents", id=id, body=data)
        id += 1
    current_app.elasticsearch.indices.refresh(index="documents")
    return redirect(url_for("allDocs"))
