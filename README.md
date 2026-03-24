🚀 Jira MCP Server

A lightweight and extensible Jira MCP (Model Context Protocol) Server that enables seamless integration between AI tools and Jira. This project allows AI agents (like Claude, ChatGPT, or VS Code extensions) to create, manage, and track Jira tickets programmatically.

📌 Features
✅ Create Jira tickets using API
✅ Update and fetch issues
✅ MCP-compatible server for AI integration
✅ Secure authentication using API Token
✅ Easy setup with environment variables
✅ Clean and modular Python architecture
🛠️ Tech Stack
Python
Jira REST API
MCP (Model Context Protocol)
python-dotenv

📂 Project Structure

├── main.py # Entry point of MCP server

├── jira.py            # Jira API handling logic

├── requirements.txt   # Project dependencies

├── .env               # Environment variables (not included)

⚙️ Setup Instructions

1️⃣ Clone the Repository
git clone https://github.com/your-username/jira-mcp-server.git
cd jira-mcp-server

2️⃣ Create Virtual Environment
python -m venv venv
venv\Scripts\activate   # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure Environment Variables

Create a .env file in the root directory and add:

JIRA_BASE_URL=https://your-domain.atlassian.net
JIRA_EMAIL=your-email@example.com
JIRA_API_TOKEN=your-api-token

▶️ Running the Server
python main.py

🔐 Authentication

This project uses Jira API Token-based authentication.
You can generate your API token from your Jira account settings.

🔧 File Descriptions

📄 jira.py

Handles all Jira-related operations such as authentication and API calls for creating, updating, and retrieving tickets.

📄 main.py

Main server file that initializes the MCP server and connects AI tools with Jira functionalities.

📄 requirements.txt

Contains all required Python libraries for the project.

💡 Use Cases

Automate Jira ticket creation using AI
Integrate Jira with Claude Desktop or VS Code
Build AI-powered developer tools
Streamline bug tracking workflows

🚀 Future Improvements

Add support for Jira comments & attachments
Implement ticket search & filtering
Add logging and error handling
Docker support for easy deployment

🤝 Contributing
Contributions are welcome! Feel free to fork the repo and submit a pull request.
