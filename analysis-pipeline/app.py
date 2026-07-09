from flask import Flask, jsonify
from document_retrieval.get_documents import get_documents

app = Flask(__name__)


@app.route("/health")
def health():
    return jsonify(status="ok")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
