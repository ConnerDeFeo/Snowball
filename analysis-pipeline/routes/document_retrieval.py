from flask import Blueprint, jsonify, request
from document_retrieval.get_documents import get_documents

document_retrieval_bp = Blueprint("document_retrieval_bp", __name__)

MAX_YEARS = 6

@document_retrieval_bp.route("/documents/<tckr>", methods=["POST"])
def documents(tckr):
    data = request.get_json() or {}
    from_date = data.get("from_date")
    to_date = data.get("to_date")
    if not from_date or not to_date:
        return jsonify({"error": "from_date and to_date are required"}), 400

    from_year, to_year = int(from_date[:4]), int(to_date[:4])
    if to_year < from_year or to_year - from_year >= MAX_YEARS:
        return jsonify({"error": f"date range may span at most {MAX_YEARS} years"}), 400

    found = get_documents(tckr, from_date, to_date)
    if not found:
        return jsonify({"error": f"no company found for ticker: {tckr}"}), 404

    return jsonify({"status": "ok", "ticker": tckr}), 200