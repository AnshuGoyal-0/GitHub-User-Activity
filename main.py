import json
import sys
from urllib import request, error

# Function to fetch and display GitHub user activity
def fetch_github_activity(username):
    url = f"https://api.github.com/users/{username}/events"

    try:
        # Making a GET request to the GitHub API
        response = request.urlopen(url)
        data = json.loads(response.read())

        # Parsing and displaying relevant events
        if data:
            for event in data:
                event_type = event.get("type")
                repo_name = event.get("repo", {}).get("name", "Unknown repository")
                
                if event_type == "PushEvent":
                    commits = event.get("payload", {}).get("commits", [])
                    commit_count = len(commits)
                    print(f"Pushed {commit_count} commit(s) to {repo_name}")
                elif event_type == "IssuesEvent":
                    action = event.get("payload", {}).get("action", "Unknown action")
                    print(f"{action.capitalize()} a new issue in {repo_name}")
                elif event_type == "WatchEvent":
                    print(f"Starred {repo_name}")
                else:
                    print(f"Performed {event_type} on {repo_name}")
        else:
            print(f"No recent activity found for user: {username}")

    except error.HTTPError as e:
        if e.code == 404:
            print(f"Error: User '{username}' not found.")
        else:
            print(f"Error: Unable to fetch data (HTTP {e.code}).")
    except error.URLError as e:
        print(f"Error: Network issue ({e.reason}).")
    except json.JSONDecodeError:
        print("Error: Failed to decode the response from GitHub API.")

# Main function to handle command-line arguments
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: github-activity <username>")
        sys.exit(1)

    username = sys.argv[1]
    fetch_github_activity(username)
