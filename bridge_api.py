from flask import Flask, request, jsonify
from service import ApifyService

app = Flask(__name__)

# Initialize the ApifyService
apify_service = ApifyService()

@app.route('/get-instagram-data', methods=['GET'])
def get_instagram_data():
    # Retrieve the 'tag' and 'limit' parameters from the GET request
    tag = request.args.get('tag')
    limit = request.args.get('limit', default=0, type=int)

    if not tag:
        return jsonify({"error": "Tag parameter is required"}), 400

    # Run the hashtag scraper
    results = apify_service.run_hashtag_scraper([tag], limit)

    if results is None:
        return jsonify({"error": "No data retrieved from the scraper"}), 500

    # Filter the data using the extract_instagram_data method
    filtered_data = apify_service.extract_instagram_data(results)

    # Return the filtered data as a JSON response
    return jsonify(filtered_data), 200

if __name__ == '__main__':
    app.run(debug=True)