from flask import Blueprint, jsonify, request
from document_retrieval.get_documents import get_documents

document_retrieval_bp = Blueprint("document_retrieval_bp", __name__)

@document_retrieval_bp.route("/documents/<tckr>", methods=["POST"])
def documents(tckr):
    data = request.get_json(silent=True) or {}
    from_date = data.get("from_date")
    to_date = data.get("to_date")
    if not from_date or not to_date:
        return jsonify({"error": "from_date and to_date are required"}), 400

    found = get_documents(tckr, from_date, to_date)
    if not found:
        return jsonify({"error": f"no company found for ticker: {tckr}"}), 404

    return jsonify({"status": "ok", "ticker": tckr}), 200