# 📊 Autonomous CSV Data Analyst AI Agent

An AI-powered Data Analyst Agent built with **smolagents** and **Qwen2.5-Coder-32B-Instruct**. The agent autonomously inspects CSV datasets, executes Python code for data analysis, and generates visualization charts dynamically via a Gradio UI.

## 🚀 Key Features
- **Autonomous Code Execution:** Writes and executes Pandas/Python code to perform data manipulation.
- **Custom Inspection Tool:** Includes a custom `@tool` (`inspect_csv_data`) to parse metadata, column dtypes, and samples before deep analysis.
- **Visualizations:** Automatically generates and outputs plots using Matplotlib & Seaborn.
- **Interactive UI:** Built with Gradio for seamless CSV uploads and real-time query responses.

## 🛠️ Tech Stack
- **Framework:** `smolagents` (CodeAgent)
- **Model:** `Qwen/Qwen2.5-Coder-32B-Instruct` (via `HfApiModel`)
- **Frontend:** Gradio (`gr.Blocks`)
- **Environment & Dependency Management:** `uv`

## 📦 Local Setup & Run

1. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/data-analyst-agent.git](https://github.com/YOUR_USERNAME/data-analyst-agent.git)
   cd data-analyst-agent
