## [BlackboxAI Agent](https://github.com/Coral-Protocol/Coral-BlackboxAI-Agent)
 
BLACKBOX AI is a coding-focused AI platform that delivers precise, context-aware support to streamline software development and tackle complex programming challenges efficiently.

## Responsibility

The BlackboxAI agent can help you solve any code-related task.

## Details
- **Framework**: LangChain
- **Tools used**: Coral Server Tools
- **AI model**: OpenAI GPT-4.1-mini
- **Date added**: 06/07/25
- **Reference**: [BlackboxAI](https://www.blackbox.ai/)
- **License**: MIT

## Setup the Agent

### 1. Clone & Install Dependencies

<details>  

```bash
# In a new terminal clone the repository:
git clone https://github.com/Coral-Protocol/Coral-BlackboxAI-Agent.git

# Navigate to the project directory:
cd Coral-BlackboxAI-Agent

# Download and run the UV installer, setting the installation directory to the current one
curl -LsSf https://astral.sh/uv/install.sh | env UV_INSTALL_DIR=$(pwd) sh

# Create a virtual environment named `.venv` using UV
uv venv .venv

# Activate the virtual environment
source .venv/bin/activate

# install uv
pip install uv

# Install dependencies from `pyproject.toml` using `uv`:
uv sync
```

</details>

### 2. Configure Environment Variables

Get the API Keys:
- [BlackboxAI API Key](https://www.blackbox.ai/dashboard)

<details>

```bash
# Create .env file in project root
cp -r .env.example .env
```
</details>

## Run the Agent

You can run in either of the below modes to get your system running.  

- The Executable Model is part of the Coral Protocol Orchestrator which works with [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio).  
- The Dev Mode allows the Coral Server and all agents to be seaprately running on each terminal without UI support.  

### 1. Executable Mode

Checkout: [How to Build a Multi-Agent System with Awesome Open Source Agents using Coral Protocol](https://github.com/Coral-Protocol/existing-agent-sessions-tutorial-private-temp) and update the file: `coral-server/src/main/resources/application.yaml` with the details below, then run the [Coral Server](https://github.com/Coral-Protocol/coral-server) and [Coral Studio UI](https://github.com/Coral-Protocol/coral-studio). You do not need to set up the `.env` in the project directory for running in this mode; it will be captured through the variables below.

<details>

For Linux or MAC:

```bash
# PROJECT_DIR="/PATH/TO/YOUR/PROJECT"

applications:
  - id: "app"
    name: "Default Application"
    description: "Default application for testing"
    privacyKeys:
      - "default-key"
      - "public"
      - "priv"

registry:
  blackboxai_agent:
    options:
      - name: "BLACKBOXAI_API_KEY"
        type: "string"
        description: "API key for the service"
    runtime:
      type: "executable"
      command: ["bash", "-c", "${PROJECT_DIR}/run_agent.sh main.py"]
      environment:
        - name: "BLACKBOXAI_API_KEY"
          from: "BLACKBOXAI_API_KEY"
        - name: "BLACKBOXAI_URL"
          value: "https://api.blackbox.ai"
        - name: "MODEL_NAME"
          value: "blackboxai/openai/gpt-4.1-mini"
        

```

For Windows, create a powershell command (run_agent.ps1) and run:

```bash
command: ["powershell","-ExecutionPolicy", "Bypass", "-File", "${PROJECT_DIR}/run_agent.ps1","main.py"]
```

</details>

### 2. Dev Mode

Ensure that the [Coral Server](https://github.com/Coral-Protocol/coral-server) is running on your system and run below command in a separate terminal.

<details>

```bash
# Run the agent using `uv`:
uv run python main.py
```
</details>


## Example

<details>


```bash
# Input:
help me design a simple front end

# Output:
Here is a simple front end example provided by BlackboxAI agent:

---

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Simple Front End</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            background-color: #f4f4f4;
        }
        h1 {
            color: #333;
        }
        button {
            padding: 10px 15px;
            background-color: #007BFF;
            color: white;
            border: none;
            border-radius: 5px;
            cursor: pointer;
        }
        button:hover {
            background-color: #0056b3;
        }
    </style>
</head>
<body>
    <h1>Welcome to Simple Front End!</h1>
    <button onclick="showMessage()">Click Me</button>
    <p id="message"></p>

    <script>
        function showMessage() {
            document.getElementById('message').innerText = 'Hello! You clicked the button.';
        }
    </script>
</body>
</html>

---

This creates a basic web page with a heading, a button, and a message that appears when you click the button. Would you like to customize this further or need help with something more specific?
```
</details>


## Creator Details
- **Name**: Xinxing
- **Affiliation**: Coral Protocol
- **Contact**: [Discord](https://discord.com/invite/Xjm892dtt3)
