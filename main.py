from fastmcp import FastMCP
from jira_client import (
    create_issue,
    list_project_issues,
    get_issue
)

mcp = FastMCP("Jira MCP Server")


@mcp.tool()
def jira_create_ticket(
    summary: str,
    description: str,
    issue_type: str = "Task"
) -> str:
    result = create_issue(summary, description, issue_type)
    return f"Ticket created: {result['key']} → {result['url']}"


@mcp.tool()
def jira_list_all_tickets(status: str = None) -> str:
    tickets = list_project_issues(status)

    if not tickets:
        return "No tickets found."

    lines = [f"Total tickets: {len(tickets)}\n"]
    for t in tickets:
        lines.append(f"[{t['key']}] {t['summary']}")
        lines.append(f"Assignee: {t['assignee']} | Status: {t['status']} | Priority: {t['priority']}\n")

    return "\n".join(lines)


@mcp.tool()
def jira_get_ticket(ticket_key: str) -> str:
    t = get_issue(ticket_key)

    return (
        f"Ticket: {t['key']}\n"
        f"Summary: {t['summary']}\n"
        f"Status: {t['status']}\n"
        f"Assignee: {t['assignee']}\n"
        f"Priority: {t['priority']}\n"
        f"URL: {t['url']}"
    )


if __name__ == "__main__":
    mcp.run()
