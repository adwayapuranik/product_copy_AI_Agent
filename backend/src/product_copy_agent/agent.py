from product_copy_agent.state import initial_state
from product_copy_agent.graph.graph_builder import build_graph

def main():
    print("\nStarting Product Copy Validation Agent\n")
    app = build_graph()
    final_state = app.invoke(initial_state())

    print("\nAgent run complete!\n")

if __name__ == "__main__":
    main()
