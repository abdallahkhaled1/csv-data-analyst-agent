import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import gradio as gr
import seaborn as sns
from smolagents import CodeAgent, FinalAnswerTool,tool,InferenceClientModel,DuckDuckGoSearchTool,VisitWebpageTool,GradioUI

# Model initial

load_dotenv()

model = InferenceClientModel(
    model_id="Qwen/Qwen2.5-Coder-32B-Instruct",
    stream =False,
    token=os.getenv("HF_TOKEN")
)

# Create Tool
@tool
def inspect_csv_data(file_path: str) -> str:
    """
    Provides a quick inspection summary of a CSV file, including total rows, columns, data types, and the first 3 rows.

    Args:
        file_path: The file path of the CSV file to inspect.
    """
    try:
        df = pd.read_csv(file_path)
        info = f"Rows: {df.shape[0]}, Columns: {df.shape[1]}\n\n"
        info += "Column Names & Data Types:\n" + str(df.dtypes) + "\n\n"
        info += "First 3 rows sample:\n" + str(df.head(3))
        return info
    except Exception as e:
        return f"Error reading CSV file: {str(e)}"



# Create Agent
agent = CodeAgent(
    model=model,
    tools=[FinalAnswerTool(),DuckDuckGoSearchTool(),VisitWebpageTool(),inspect_csv_data],
    additional_authorized_imports=['pandas','matplotlib.pyplot','seaborn','numpy','os'],
    max_steps=6

)


'''
/* Lunch Agent
demo = GradioUI(agent)
demo.launch(share=True)'''

#Function to link Gradio UI with CodeAgent
def analyze_csv(file_obj, user_query):
    if file_obj is None:
        return "Please upload a CSV file first.", None
    
    # Gradio stores uploaded file in file_obj.name
    file_path = file_obj.name
    
    prompt = f"""
    You are given a CSV file located at: '{file_path}'.
    Task: {user_query}

    Instructions:
    1. First, inspect the file structure or read it with pandas.
    2. Perform the required analysis and logic to answer the task.
    3. If a chart/graph is required, save it as 'output_plot.png'.
    4. Return a clear and direct summary answer.
    """
    
    try:
        response = agent.run(prompt)
        # Check if plot was saved
        plot_image = "output_plot.png" if os.path.exists("output_plot.png") else None
        return str(response), plot_image
    except Exception as e:
        return f"Error during execution: {str(e)}", None

#Custom Gradio Interface with File Upload Box
with gr.Blocks(title="CSV Data Analyst AI Agent") as demo:
    gr.Markdown("# 📊 CSV Data Analyst AI Agent")
    gr.Markdown("Upload your CSV file, type your request, and the agent will analyze data and generate plots!")
    
    with gr.Row():
        with gr.Column(scale=1):
            file_input = gr.File(label="Upload CSV File", file_types=[".csv"])
            query_input = gr.Textbox(
                label="Your Analysis Request / Question",
                placeholder="e.g., Show top 5 rows and plot a bar chart of class survival rates."
            )
            submit_btn = gr.Button("Analyze 🚀", variant="primary")
            
        with gr.Column(scale=1):
            text_output = gr.Textbox(label="Agent Response / Result", lines=10)
            image_output = gr.Image(label="Generated Chart")

    # Clean up old output plot before new run
    def pre_process_run(file_obj, user_query):
        if os.path.exists("output_plot.png"):
            os.remove("output_plot.png")
        return analyze_csv(file_obj, user_query)

    submit_btn.click(
        fn=pre_process_run,
        inputs=[file_input, query_input],
        outputs=[text_output, image_output]
    )

if __name__ == "__main__":
    demo.launch()















