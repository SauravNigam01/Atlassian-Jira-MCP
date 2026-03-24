import requests
from requests.auth import HTTPBasicAuth
import os
from dotenv import load_dotenv

load_dotenv()

# ── Jira Config ───────────────────────────────────────────────────────────────
JIRA_EMAIL  = os.getenv("JIRA_EMAIL", "your-email@example.com")
JIRA_TOKEN  = os.getenv("JIRA_API_TOKEN", "your-api-token")
BASE_URL    = os.getenv("JIRA_BASE_URL", "https://your-domain.atlassian.net")
PROJECT     = os.getenv("JIRA_PROJECT", "YOUR_PROJECT_KEY")

AUTH    = HTTPBasicAuth(JIRA_EMAIL, JIRA_TOKEN)
HEADERS = {"Accept": "application/json", "Content-Type": "application/json"}


# ── 1. Get Issue Details ──────────────────────────────────────────────────────
def get_issue(ticket_key: str) -> dict:
    """Fetch full details of a Jira issue by key (e.g. SCRUM-42)."""
    resp = requests.get(
        f"{BASE_URL}/rest/api/3/issue/{ticket_key}",
        auth=AUTH, headers=HEADERS
    )
    resp.raise_for_status()
    data = resp.json()
    fields = data["fields"]
    return {
        "key":         data["key"],
        "summary":     fields["summary"],
        "status":      fields["status"]["name"],
        "assignee":    fields.get("assignee", {}).get("displayName", "Unassigned") if fields.get("assignee") else "Unassigned",
        "priority":    fields.get("priority", {}).get("name", "N/A"),
        "description": fields.get("description", ""),
        "url":         f"{BASE_URL}/browse/{data['key']}"
    }


# ── 2. Create Issue ───────────────────────────────────────────────────────────
def create_issue(summary: str, description: str = "", issue_type: str = "Task", priority: str = "Medium") -> dict:
    """Create a new Jira issue in the configured project."""
    payload = {
        "fields": {
            "project":     {"key": PROJECT},
            "summary":     summary,
            "description": {
                "type": "doc", "version": 1,
                "content": [{"type": "paragraph", "content": [{"type": "text", "text": description}]}]
            },
            "issuetype": {"name": issue_type},
            "priority":  {"name": priority}
        }
    }
    resp = requests.post(
        f"{BASE_URL}/rest/api/3/issue",
        json=payload, auth=AUTH, headers=HEADERS
    )
    resp.raise_for_status()
    data = resp.json()
    return {
        "key": data["key"],
        "url": f"{BASE_URL}/browse/{data['key']}",
        "id":  data["id"]
    }


# ── 3. Update Ticket Status ───────────────────────────────────────────────────
def update_ticket_status(ticket_key: str, target_status: str) -> dict:
    """Transition a Jira ticket to a new status (e.g. 'In Progress', 'Done')."""
    # Step 1: fetch available transitions for this ticket
    resp = requests.get(
        f"{BASE_URL}/rest/api/3/issue/{ticket_key}/transitions",
        auth=AUTH, headers=HEADERS
    )
    resp.raise_for_status()
    transitions = resp.json().get("transitions", [])

    # Step 2: find the transition ID that matches target_status (case-insensitive)
    match = next(
        (t for t in transitions if t["name"].lower() == target_status.lower()),
        None
    )
    if not match:
        available = [t["name"] for t in transitions]
        return {"success": False, "error": f"Status '{target_status}' not available. Options: {available}"}

    # Step 3: apply the transition
    resp = requests.post(
        f"{BASE_URL}/rest/api/3/issue/{ticket_key}/transitions",
        json={"transition": {"id": match["id"]}},
        auth=AUTH, headers=HEADERS
    )
    resp.raise_for_status()
    return {"success": True, "ticket": ticket_key, "new_status": target_status}


# ── 4. Add Comment ────────────────────────────────────────────────────────────
def add_comment(ticket_key: str, comment_text: str) -> dict:
    """Add a comment to an existing Jira ticket."""
    payload = {
        "body": {
            "type": "doc", "version": 1,
            "content": [{"type": "paragraph", "content": [{"type": "text", "text": comment_text}]}]
        }
    }
    resp = requests.post(
        f"{BASE_URL}/rest/api/3/issue/{ticket_key}/comment",
        json=payload, auth=AUTH, headers=HEADERS
    )
    resp.raise_for_status()
    data = resp.json()
    return {
        "comment_id": data["id"],
        "ticket":     ticket_key,
        "author":     data["author"]["displayName"],
        "url":        f"{BASE_URL}/browse/{ticket_key}"
    }


# ── 5. Search Tickets by Keyword ──────────────────────────────────────────────
def search_tickets_by_keyword(keyword: str, status: str = None, assignee_email: str = None) -> list[dict]:
    """Search tickets using JQL — searches summary, description, and comments."""
    conditions = [
        f'project = {PROJECT}',
        f'text ~ "{keyword}"'
    ]
    if status:
        conditions.append(f'status = "{status}"')
    if assignee_email:
        conditions.append(f'assignee = "{assignee_email}"')

    jql = " AND ".join(conditions) + " ORDER BY updated DESC"

    resp = requests.get(
        f"{BASE_URL}/rest/api/3/search",
        params={"jql": jql, "maxResults": 30, "fields": "summary,status,assignee,priority"},
        auth=AUTH, headers=HEADERS
    )
    resp.raise_for_status()
    issues = resp.json().get("issues", [])

    return [{
        "key":      i["key"],
        "summary":  i["fields"]["summary"],
        "status":   i["fields"]["status"]["name"],
        "assignee": i["fields"].get("assignee", {}).get("displayName", "Unassigned") if i["fields"].get("assignee") else "Unassigned",
        "priority": i["fields"].get("priority", {}).get("name", "N/A"),
        "url":      f"{BASE_URL}/browse/{i['key']}"
    } for i in issues]


# ── 6. List All Issues in Project ─────────────────────────────────────────────
def list_project_issues(status: str = None, max_results: int = 50) -> list[dict]:
    """List all issues in the configured project, optionally filtered by status."""
    conditions = [f'project = {PROJECT}']
    if status:
        conditions.append(f'status = "{status}"')

    jql = " AND ".join(conditions) + " ORDER BY updated DESC"

    resp = requests.get(
        f"{BASE_URL}/rest/api/3/search",
        params={"jql": jql, "maxResults": max_results, "fields": "summary,status,assignee,priority"},
        auth=AUTH, headers=HEADERS
    )
    resp.raise_for_status()
    issues = resp.json().get("issues", [])

    return [{
        "key":      i["key"],
        "summary":  i["fields"]["summary"],
        "status":   i["fields"]["status"]["name"],
        "assignee": i["fields"].get("assignee", {}).get("displayName", "Unassigned") if i["fields"].get("assignee") else "Unassigned",
        "priority": i["fields"].get("priority", {}).get("name", "N/A"),
        "url":      f"{BASE_URL}/browse/{i['key']}"
    } for i in issues]


# ── 7. Assign Issue ───────────────────────────────────────────────────────────
def assign_issue(ticket_key: str, assignee_account_id: str) -> dict:
    """Assign a Jira issue to a user by their accountId."""
    resp = requests.put(
        f"{BASE_URL}/rest/api/3/issue/{ticket_key}/assignee",
        json={"accountId": assignee_account_id},
        auth=AUTH, headers=HEADERS
    )
    resp.raise_for_status()
    return {"success": True, "ticket": ticket_key, "assigned_to": assignee_account_id}


# ── 8. Delete Issue ───────────────────────────────────────────────────────────
def delete_issue(ticket_key: str) -> dict:
    """Permanently delete a Jira issue. Use with caution."""
    resp = requests.delete(
        f"{BASE_URL}/rest/api/3/issue/{ticket_key}",
        auth=AUTH, headers=HEADERS
    )
    resp.raise_for_status()
    return {"success": True, "deleted": ticket_key}