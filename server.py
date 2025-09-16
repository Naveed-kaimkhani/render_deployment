


from flask import Flask, request, jsonify
from scraper import scrape_daraz

app = Flask(__name__)

@app.route("/products")
def products():
    query = request.args.get("q", "")
    # page = request.args.get("page", "1")
    if not query:
        return jsonify({"error": "missing query"}), 400
    
    results = scrape_daraz(query, 1)
    return jsonify({"query": query, "results": results})

if __name__ == "__main__":
    app.run(debug=True)




