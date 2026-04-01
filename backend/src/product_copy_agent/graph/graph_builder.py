from langgraph.graph import StateGraph

from product_copy_agent.graph.state import AgentState
from product_copy_agent.graph.nodes import (
    check_prompt_history_node,
    ask_user_update_node,
    upload_instructions_node,
    upload_input_file_node,
    process_bedrock_node,
    generate_output_link_node,
)

def build_graph():
    graph = StateGraph(AgentState)

    graph.add_node("check_prompt_history", check_prompt_history_node)
    graph.add_node("ask_user_update", ask_user_update_node)
    graph.add_node("upload_instructions", upload_instructions_node)
    graph.add_node("upload_input_file", upload_input_file_node)
    graph.add_node("process_bedrock", process_bedrock_node)
    graph.add_node("generate_output_link", generate_output_link_node)

    graph.set_entry_point("check_prompt_history")

    graph.add_conditional_edges(
        "check_prompt_history",
        lambda s: "ask_user_update"
    )
    graph.add_conditional_edges(
        "ask_user_update",
        lambda s: "upload_instructions" if s.get("user_choice") == "yes" else "upload_input_file"
    )

    graph.add_edge("upload_instructions", "upload_input_file")
    graph.add_edge("upload_input_file", "process_bedrock")
    graph.add_edge("process_bedrock", "generate_output_link")

    graph.set_finish_point("generate_output_link")
    return graph.compile()
