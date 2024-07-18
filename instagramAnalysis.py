import json
from datetime import datetime
import os

def extract_usernames_and_timestamps_from_following(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)['relationships_following']
    
    usernames = []
    for entry in data:
        if 'string_list_data' in entry:
            for item in entry['string_list_data']:
                try:
                    if isinstance(item['timestamp'], int):
                        timestamp = datetime.fromtimestamp(item['timestamp']).strftime('%S.%M.%H %d.%m.%Y')
                    else:
                        timestamp = datetime.strptime(item['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%S.%M.%H %d.%m.%Y')
                except (ValueError, KeyError):
                    timestamp = item.get('timestamp', 'N/A')
                
                usernames.append({
                    'username': item['value'],
                    'timestamp': timestamp
                })
    return usernames

def extract_usernames_and_timestamps_from_followers(file_path):
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"{file_path} not found.")
    
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    usernames = []
    for entry in data:
        if 'string_list_data' in entry:
            for item in entry['string_list_data']:
                try:
                    if isinstance(item['timestamp'], int):
                        timestamp = datetime.fromtimestamp(item['timestamp']).strftime('%S.%M.%H %d.%m.%Y')
                    else:
                        timestamp = datetime.strptime(item['timestamp'], '%Y-%m-%dT%H:%M:%S.%fZ').strftime('%S.%M.%H %d.%m.%Y')
                except (ValueError, KeyError):
                    timestamp = item.get('timestamp', 'N/A')
                
                usernames.append({
                    'username': item['value'],
                    'timestamp': timestamp
                })
    return usernames

def find_difference(list1, list2):
    set1 = {item['username'] for item in list1}
    set2 = {item['username'] for item in list2}
    
    difference = set1 - set2
    
    return [item for item in list1 if item['username'] in difference]

def find_intersection(list1, list2):
    set1 = {item['username'] for item in list1}
    set2 = {item['username'] for item in list2}
    
    intersection = set1 & set2
    
    return [item for item in list1 if item['username'] in intersection]

following_json_path = 'following.json'
followers_json_path = 'followers_1.json'

try:
    following = extract_usernames_and_timestamps_from_following(following_json_path)
    followers = extract_usernames_and_timestamps_from_followers(followers_json_path)
except FileNotFoundError as e:
    print(f"Error: {e}")
    exit(1)

not_following_back = find_difference(following, followers)
not_followed_back = find_difference(followers, following)
mutual_follow = find_intersection(following, followers)

html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Follow Analysis</title>
    <link href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" rel="stylesheet">
    <style>
        .user-list {{
            list-style-type: none;
            padding: 0;
        }}
        .user-list li {{
            margin-bottom: 10px;
        }}
        .content-section {{
            display: none;
        }}
        .content-section.active {{
            display: block;
        }}
    </style>
</head>
<body>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <a class="navbar-brand" href="#">Instagram Analysis</a>
        <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
            <ul class="navbar-nav">
                <li class="nav-item">
                    <a class="nav-link" href="#" data-target="#not-following-back-section">Not Following Back</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#" data-target="#not-followed-back-section">Not Followed Back</a>
                </li>
                <li class="nav-item">
                    <a class="nav-link" href="#" data-target="#mutual-follow-section">Mutual Follow</a>
                </li>
            </ul>
        </div>
    </nav>
    <div class="container mt-4">
        <div id="not-following-back-section" class="content-section active">
            <h2>Not Following Back</h2>
            <div class="row">
"""

for index, user in enumerate(not_following_back, start=1):
    html_content += f"""
                <div class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">{index}. <a href="https://www.instagram.com/{user['username']}" target="_blank">{user['username']}</a></h5>
                            <p class="card-text">Date: {user['timestamp']}</p>
                        </div>
                    </div>
                </div>
    """

html_content += """
            </div>
        </div>
        <div id="not-followed-back-section" class="content-section">
            <h2>Not Followed Back</h2>
            <div class="row">
"""

for index, user in enumerate(not_followed_back, start=1):
    html_content += f"""
                <div class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">{index}. <a href="https://www.instagram.com/{user['username']}" target="_blank">{user['username']}</a></h5>
                            <p class="card-text">Date: {user['timestamp']}</p>
                        </div>
                    </div>
                </div>
    """

html_content += """
            </div>
        </div>
        <div id="mutual-follow-section" class="content-section">
            <h2>Mutual Follow</h2>
            <div class="row">
"""

for index, user in enumerate(mutual_follow, start=1):
    html_content += f"""
                <div class="col-md-4 mb-3">
                    <div class="card">
                        <div class="card-body">
                            <h5 class="card-title">{index}. <a href="https://www.instagram.com/{user['username']}" target="_blank">{user['username']}</a></h5>
                            <p class="card-text">Date: {user['timestamp']}</p>
                        </div>
                    </div>
                </div>
    """

html_content += """
            </div>
        </div>
    </div>
    <script>
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', event => {
                event.preventDefault();
                document.querySelectorAll('.content-section').forEach(section => {
                    section.classList.remove('active');
                });
                const targetId = event.target.getAttribute('data-target');
                document.querySelector(targetId).classList.add('active');
            });
        });
    </script>
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/@popperjs/core@2.9.2/dist/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
</body>
</html>
"""

with open('follow_analysis.html', 'w', encoding='utf-8') as file:
    file.write(html_content)

print("The results were saved in HTML format.")
