import requests
import csv

def fetch_and_print_posts():
    """
    Fetch posts from JSONPlaceholder and print titles
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            posts = response.json()
            for post in posts:
                print(post['title'])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

def fetch_and_save_posts():
    """
    Fetch posts from JSONPlaceholder and save to CSV
    """
    url = "https://jsonplaceholder.typicode.com/posts"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            posts = response.json()
            
            # Structure data into list of dictionaries
            structured_posts = [
                {
                    'id': post['id'],
                    'title': post['title'],
                    'body': post['body']
                }
                for post in posts
            ]
            
            # Write to CSV file
            with open('posts.csv', 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'title', 'body']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerows(structured_posts)
                
            print("Data saved to posts.csv")
            
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
    except Exception as e:
        print(f"Error saving to CSV: {e}")
