import json
from typing import Dict, List, Optional
from apify_client import ApifyClient

class ApifyService:
    def __init__(self, config_path='parameters/config.json'):
        with open(config_path, 'r') as f:
            self.config = json.load(f)

        # Initialize the ApifyClient with your API token
        self.client = ApifyClient(self.config["api_token"])

        # # Prepare the Actor input
        # self.config["run_input"] = {
        #     "hashtags": self.config["hashtags"],
        #     "resultsLimit": self.config["results_limit"],
        # }

    def run_hashtag_scraper(self, hashtags, limit = 0) -> Optional[List[Dict]]:
        
        if limit == 0: 
            limit = self.config("results_limit")
            
        run_input = {
            "hashtags": hashtags,
            "resultsLimit": limit,
        }
        
        try:
            # Run the Actor and wait for it to finish
            run = self.client.actor(self.config["actor_id"]).call(run_input=run_input)

            # Fetch the Actor results from the run's dataset
            results = []
            for item in self.client.dataset(run["defaultDatasetId"]).iterate_items():
                results.append(item)

            return results if results else None
        
        except Exception as e:
            print(f"An error occurred while running the hashtag scraper: {e}")
            return None

    def extract_instagram_data(self, json_data: List[Dict]) -> List[Dict]:
        extracted_data = []
        # print(json.dumps(json_data, indent=2))
        for post in json_data:
            # Extract the required information
            post_data = {
                "ownerId": post.get("ownerId", []),
                "ownerUsername": post.get("ownerUsername", []),
                "fullName": post.get("fullName", []),
                "timestamp": post.get("timestamp", []),
                "hashtags": post.get("hashtags", {}),
                
                "id": post.get("id"),
                "commentsCount": post.get("commentsCount", {}),
                "likesCount": post.get("likesCount", []),
                "type": post.get("type"),
            }
            
            # Add the extracted data to the list
            extracted_data.append(post_data)
        
        return extracted_data
