import streamlit as st
import time
from tasks.task import create_workflow
from tasks.state import WorkflowState # Import WorkflowState

# Define the function to start the workflow with progress updates using streaming
def start_workflow_streamed(subreddit_name):
    if not subreddit_name:
        raise ValueError("Subreddit name must be provided.")

    workflow_input = {"subreddit": subreddit_name}
    workflow = create_workflow()

    # Map node names to user-friendly status messages
    status_map = {
        "scraper": "🕵️‍♀️ Scraping data...",
        "insights": "🧠 Analyzing data and extracting insights...",
        "solution_architect": "💡 Generating MVP solution idea...",
        "risk_assessor": "⚠️ Assessing risks for the proposed idea...",
        "presentor": "📄 Preparing the final presentation..."
    }

    st.write("✨ Starting workflow...")

    # Use a placeholder for the dynamic status message
    status_placeholder = st.empty()
    # Use another placeholder for accumulating output/state if desired
    # output_placeholder = st.empty()

    final_output = None
    accumulated_state = {} # To build up the final state

    try:
        for chunk in workflow.stream(workflow_input):
            # >>> Add these debug prints <<<
            print("-" * 20)
            print(f"Received Chunk Type: {type(chunk)}")
            print(f"Received Chunk Value: {chunk}")
            print("-" * 20)
            # >>> End Debug Prints <<<

            # Add a safety check for None chunks
            if chunk is None:
                print("Warning: Skipping None chunk received from stream.")
                continue # Skip to the next chunk if None

            # Find which node just finished in this chunk
            finished_node = None
            node_output = None
            # The chunk should be a dictionary, so .items() should work if it's not None
            for key, value in chunk.items():
                 if key in status_map:
                      finished_node = key
                      # In streaming mode, the value for a node key is often the
                      # *output dictionary* returned by that node.
                      # Let's assume this structure for now.
                      node_output = value
                      break

            if finished_node:
                # Update the status message
                status_placeholder.info(f"{status_map[finished_node]} Done.")
                # You could optionally show partial output here, e.g.,
                # output_placeholder.json({finished_node: node_output})

                # Accumulate the state updates (merge the node's output into the state)
                # Ensure node_output is actually a dictionary before updating
                if isinstance(node_output, dict):
                   accumulated_state.update(node_output)
                else:
                   print(f"Warning: Node {finished_node} returned non-dict output: {node_output}")
                   # Decide how to handle non-dict output - maybe store it under a special key?
                   # accumulated_state[f"{finished_node}_output"] = node_output


            time.sleep(0.1) # Keep the small delay for visibility

        # After the loop, the workflow is complete
        status_placeholder.empty() # Clear the last status message/spinner
        st.success("✅ Workflow completed successfully!")

        # The final state is the accumulated_state
        # Extract the final presentation from the accumulated state
        final_output = accumulated_state.get("final_presentation")

        if final_output is None:
             st.warning("⚠️ Workflow completed, but the final presentation output ('final_presentation' key) was not generated.")
             st.markdown("### Final State for Debugging:")
             st.json(accumulated_state) # Show the full state if final output is missing
             return None # Indicate no final output

        return final_output # Return the successfully retrieved final presentation text

    except Exception as e:
        status_placeholder.error(f"🚫 An error occurred during workflow execution: {e}")
        print(f"An error occurred: {e}") # Also print to console for server-side debugging
        return None # Indicate failure

# Streamlit UI starts here
st.set_page_config(page_title="📊 Agentic Market Analyzer", layout="wide")

# --- Header ---
st.markdown("<h1 style='text-align: center;'>📊 Autonomous Market Opportunity Discoverer</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: gray;'>Uncover startup opportunities by analyzing trends in online communities.</p>", unsafe_allow_html=True)
st.markdown("---") # Separator

# --- Input Section ---
st.header("⚙️ Configuration")
subreddit = st.text_input("Enter Subreddit Name (e.g., 'technology')", value="technology", help="Specify the subreddit for analysis.")

# Run button
run_button = st.button("🚀 Discover Opportunities!")

st.markdown("---") # Separator

# --- Output Section ---
st.header("📈 Analysis Results")

if run_button:
    if not subreddit:
        st.error("❌ Please enter a subreddit name to start the analysis.")
    else:
        # Use the streaming function
        final_presentation_text = start_workflow_streamed(subreddit)

        if final_presentation_text:
            st.markdown("### ✨ Final Opportunity Report")
            # Assuming the output is markdown formatted text
            st.markdown(final_presentation_text)
        # Error/Warning messages are handled within the streaming function now

























# import streamlit as st
# from tasks.task import create_workflow  # Make sure this is the correct import path

# # Define the function to start the workflow
# def start_workflow(subreddit_name):
#     if not subreddit_name:
#         raise ValueError("Subreddit name must be provided.")

#     workflow_input = {
#         "subreddit": subreddit_name
#     }

#     workflow = create_workflow()
#     output = workflow.invoke(workflow_input)
#     return output["final_presentation"]

# # Streamlit UI starts here
# st.set_page_config(page_title="📊 Agentic Market Analyzer", layout="wide")
# st.title("📊 Autonomous Market Opportunity Discoverer")
# st.markdown("This app uses AI agents to scrape Reddit and generate a summarized opportunity report.")

# # Subreddit input
# subreddit = st.text_input("Enter Subreddit Name (e.g., 'technology')", value="technology")

# # Run button
# if st.button("🛠 Run Autonomous Agent"):
#     if not subreddit:
#         st.error("❌ Please enter a subreddit name.")
#     else:
#         with st.spinner("🔍 Working... Please wait while agents do their job."):
#             try:
#                 output = start_workflow(subreddit)
#                 st.success("✅ Workflow completed successfully!")
#                 st.markdown("### 🧾 Final Summary Output")
              
#                 st.write("Full Output:", output)
#  # Debug line to inspect actual keys
#             except Exception as e:
#                 st.error(f"🚫 An error occurred: {e}")





















# import streamlit as st
# import sys
# import os
# from langgraph.graph import StateGraph
# from langchain_core.runnables import RunnableLambda
# from tasks.state import WorkflowState  # <-- Import this!
# from tasks.task import create_workflow
# import time
# # Initialize session state for progress tracking
# if "progress" not in st.session_state:
#     st.session_state.progress = []  # Initialize progress list

# def show_progress():
#     """ Display progress based on the session state """
#     if len(st.session_state.progress) > 0:
#         for step in st.session_state.progress:
#             st.write(f"🟢 {step} completed")
#     else:
#         st.write("No progress yet.")

# def progress_callback(state, step_name: str):
#     """ This callback is used to update the progress after each task """
#     print(f"Progress Update: {step_name}")
#     st.session_state.progress.append(step_name)  # Append the step to track the progress

# # def start_workflow():
# #     """ Start the workflow and track the progress """
# #     # Create the workflow graph
# #     result = create_workflow()

# #     # Assuming graph.run() doesn't exist, find an appropriate method to execute the graph
# #     # result = graph.run()  # This will start running the tasks and update progress automatically
# #     # result = "Workflow completed successfully, but no actual processing was done"  # Placeholder result

# #     # When workflow completes, show the progress
# #     st.session_state.progress.append("Workflow Completed!")
# #     st.write(f"🟢 Workflow Completed Successfully!")

# #     return result  # Ensure you return something that can be used as a report


# def start_workflow( subreddit_name=None):
#     workflow_input = {}
#     workflow_input["subreddit"] = subreddit_name
#     # Add others similarly

#     workflow = create_workflow()
#     output = workflow.invoke(workflow_input)
#     st.write(output)
#     return output["report"]
#  # Make sure this key holds the string report

# def clear_progress():
#     """ Clear progress updates """
#     st.session_state.progress.clear()

# # Streamlit UI layout
# st.set_page_config(
#     page_title="Market Opportunity Agent",
#     page_icon="🚀",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # Sidebar
# with st.sidebar:
#     st.title("⚙️ Settings")

#     # Data source selection first
#     data_source = st.selectbox(
#         "Select Data Source", 
#         ["Reddit", "Product Hunt", "Hacker News", "Amazon Reviews", "LinkedIn"]
#     )
#     subreddit = None
#     if data_source == "Reddit":
#         subreddit = st.text_input("Enter Subreddit", value="technology")
#     # Keyword label and input box with info icon next to it
#     st.markdown("""
#         <style>
#             .info-icon {
#                 cursor: pointer;
#                 color: #1E90FF;
#                 font-size: 16px;
#                 font-weight: normal;
#                 display: inline-block;
#                 margin-left: 5px;
#                 position: relative;
#             }
#             .info-tooltip {
#                 visibility: hidden;
#                 width: 250px;
#                 background-color: rgba(0, 0, 0, 0.75);
#                 color: white;
#                 text-align: center;
#                 border-radius: 8px;
#                 padding: 8px;
#                 position: absolute;
#                 z-index: 1;
#                 top: 25px;
#                 left: 50%;
#                 margin-left: -125px;
#                 font-size: 12px;
#                 box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
#                 transition: visibility 0.2s ease;
#             }
#             .info-icon:hover .info-tooltip {
#                 visibility: visible;
#             }

#             .input-field {
#                 width: 100%;
#                 padding: 8px;
#                 border-radius: 5px;
#                 border: 1px solid #ccc;
#                 font-size: 16px;
#             }

#             .styled-button {
#                 background-color: #4CAF50;
#                 color: white;
#                 padding: 12px 25px;
#                 border: none;
#                 border-radius: 8px;
#                 font-size: 16px;
#                 font-weight: bold;
#                 cursor: pointer;
#                 text-align: center;
#                 width: 100%;
#                 transition: background-color 0.3s ease;
#             }
#             .styled-button:hover {
#                 background-color: #45a049;
#             }
#         </style>
#         <div>
#             <span>Keyword</span>
#             <span class="info-icon"> (i)
#                 <div class="info-tooltip">
#                     You can enter a custom data source if you want to search for something like a startup or any other topic.
#                 </div>
#             </span>
#             <input type="text" placeholder="Enter a custom data source" class="input-field"/>
#         </div>
#     """, unsafe_allow_html=True)

#     # Timeframe selection
#     timeframe = st.select_slider(
#         "Timeframe", 
#         options=["Last 24h", "Last 3 days", "Last week", "Last month"]
#     )

#     st.markdown("---")

#     button = st.button("🔄 Refresh Data")
#     if button:
#         st.write("Refreshing data...")

# # Main Content
# st.markdown(
#     """
#     <div style="text-align: center; padding: 3rem;">
#         <h1 style="font-size: 3.5rem; color: #333; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;">🚀 Autonomous Market Opportunity Agent</h1>
#         <p style="font-size: 1.3rem; color: #888; font-family: 'Arial', sans-serif;">Discover hidden market gaps and customer pain points, automatically.</p>
#     </div>
#     """, 
#     unsafe_allow_html=True
# )

# st.markdown("---")

# # Progress Tracker
# st.subheader("📈 Progress Tracker")
# progress_steps = ["Collecting Data", "Generating Insights", "Evaluating Opportunities", "Writing Final Report"]

# current_step = 0

# for step in progress_steps:
#     with st.container():
#         step_index = progress_steps.index(step)
#         progress_color = '#4CAF50' if step_index <= current_step else '#e0e0e0'
#         text_color = 'white' if step_index <= current_step else 'black'
        
#         st.markdown(
#             f"""
#             <div style="background-color: {progress_color}; color: {text_color}; padding: 1.2rem; border-radius: 12px; margin-bottom: 0.6rem; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);">
#                 <strong>{step}</strong>
#             </div>
#             """, 
#             unsafe_allow_html=True
#         )
#     time.sleep(0.3)

# st.markdown("---")

# # Generate Report Button
# if st.button("🛠 Run Autonomous Agent"):
#     presentation_report = start_workflow()  # This will call create_workflow() and automatically handle the sequence

#     st.success('✅ All steps completed! Report ready.')
# if st.button("🛠 Run Autonomous Agent"):
#     if data_source == "Reddit" and not subreddit:
#         st.error("Please enter a subreddit name.")
#     else:
#         presentation_report = start_workflow(subreddit)
#         st.success("✅ Workflow completed")
#         st.write(presentation_report)

#     st.markdown("---")

#     # Final Report
#     st.header("📄 Market Opportunity Report")

#     st.markdown(
#         f"""
#         <div style="background-color: #f9f9f9; padding: 2.5rem; border-radius: 12px; box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);">
#             <pre style="font-family: 'Courier New', monospace; color: #333; font-size: 1rem; white-space: pre-wrap; word-wrap: break-word;">{presentation_report}</pre>
#         </div>
#         """, 
#         unsafe_allow_html=True
#     )

#     # Download Button
#     st.download_button("📥 Download Report", data=presentation_report, file_name="market_opportunity_report.txt", help="Click to download the generated report.")
# else:
#     st.info("👆 Click the button above to generate a new report!")
