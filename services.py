import requests

API_URL = "https://jsonplaceholder.typicode.com/todos"

_cache = None  # simple in-memory cache

def fetch_todos():
    global _cache

    if _cache is not None:
        return _cache

    response = requests.get(API_URL, timeout=5)

    if response.status_code != 200:
        raise Exception("API returned non-200 status.")

    data = response.json()

    if not isinstance(data, list):
        raise Exception("Unexpected JSON format.")

    _cache = data
    return data


def get_user_summary(user_id: int):
    todos = fetch_todos()

    user_todos = [t for t in todos if t.get("userId") == user_id]

    total = len(user_todos)

    if total == 0:
        return None

    completed = sum(1 for t in user_todos if t.get("completed"))
    pending = total - completed
    percentage = (completed / total) * 100 if total > 0 else 0

    first_5_titles = [t["title"] for t in user_todos[:5]]

    return {
        "total": total,
        "completed": completed,
        "pending": pending,
        "percentage": round(percentage, 2),
        "titles": first_5_titles,
    }
