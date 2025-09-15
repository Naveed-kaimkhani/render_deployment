

# server.py
from flask import Flask, request, jsonify
from scraper import scrape_daraz

app = Flask(__name__)

@app.route("/products", methods=["GET"])
def get_products():
    query = request.args.get("q", "shoes")  # default = shoes if not provided
    data = scrape_daraz(query)  # scrape fresh data
    return jsonify({"query": query, "results": data})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)


# scraper.py
import requests
import re
import json

def scrape_daraz(query, page=1):
    url = f"https://www.daraz.pk/catalog/?q={query}&page={page}"
    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    r = requests.get(url, headers=headers)
    if r.status_code != 200:
        return {"error": f"Failed to fetch page {page}"}

    # Extract embedded JSON
    match = re.search(r"window\.pageData=(\{.*?\});", r.text)
    if not match:
        return {"error": "No JSON found in page"}

    data = json.loads(match.group(1))
    products = []

    for item in data.get("mods", {}).get("listItems", []):
        products.append({
            "title": item.get("name"),
            "price": item.get("priceShow"),
            "rating": item.get("ratingScore"),
            "link": "https:" + item.get("productUrl"),
            "image": item.get("image")
        })

    return products




# from flask import Flask, request, jsonify
# from scraper import scrape_daraz

# app = Flask(__name__)

# @app.route("/products")
# def products():
#     query = request.args.get("q", "")
#     page = request.args.get("page", "1")
#     if not query:
#         return jsonify({"error": "missing query"}), 400
    
#     results = scrape_daraz(query, page)
#     return jsonify({"query": query, "results": results})

# if __name__ == "__main__":
#     app.run(debug=True)
