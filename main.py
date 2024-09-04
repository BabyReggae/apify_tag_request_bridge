import json
from service import ApifyService

def main():
    apify_service = ApifyService()
    
    # Run the hashtag scraper and get the results
    results = apify_service.run_hashtag_scraper()

    if results is not None:
        # Extract Instagram data from the results
        filtered = apify_service.extract_instagram_data(results)
        print(json.dumps(filtered, indent=2))
    else:
        print("No data was retrieved.")

if __name__ == "__main__":
    main()
