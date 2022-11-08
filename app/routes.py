from flask import render_template, url_for, request, redirect, current_app
from init import create_app, db, PER_PAGE
from config import app_config
from models import Document
from base_function import parse_csv
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
    return render_template("docs.html", docs=docs)


@app.route("/doc/<int:id>", methods=["GET", "POST"])
def doc_detail(id):
    doc = Document.query.get_or_404(id)
    return render_template("doc_detail.html", doc=doc)


@app.route("/search", methods=["GET", "POST"])
def search():
    q = request.args["q"].lower()
    res = current_app.elasticsearch.search(index="documents", size=20,
                                           body={"query": {"multi_match": {"query": q,
                                                                           "fields": ["text"]}}}
                                           )
    res['hits']['hits'].sort(key=lambda d: d['_source']['created_date'], reverse=True)
    return render_template('search.html', res=res, term=q)


@app.route("/delete/<int:id>", methods=["GET", "POST"])
def delete(id):
    try:
        doc = Document.query.get_or_404(id)
        current_app.elasticsearch.delete(index="documents", id=id, ignore=404)
        db.session.delete(doc)
        db.session.commit()
        return redirect(url_for("allDocs"))
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
            "text": doc.text,
            "rubrics": doc.rubrics,
            "created_date": doc.created_date
        }
        current_app.elasticsearch.index(index="documents", id=id, body=data)
        id += 1
    current_app.elasticsearch.indices.refresh(index="documents")
    return redirect(url_for("allDocs"))
