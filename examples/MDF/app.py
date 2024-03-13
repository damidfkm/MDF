import streamlit as st
import numpy as np
from modeci_mdf.execution_engine import EvaluableGraph
from modeci_mdf.mdf import Model, Graph, Node, Parameter, OutputPort


def create_biology_model():
    # Create a model for a simple biology example
    biology_model = Model(id="BiologyModel")

    # Create a graph for the biology model
    biology_graph = Graph(id="biology_example")
    biology_model.graphs.append(biology_graph)

    # Create a node representing a biological entity
    biological_node = Node(id="BiologicalEntity")
    biology_graph.nodes.append(biological_node)

    # Add stateless and stateful parameters to the biological entity node
    # Stateless parameter
    increment_parameter = Parameter(id="increment", value=1.0)
    biological_node.parameters.append(increment_parameter)

    # Stateful parameter
    count_parameter = Parameter(id="count", value="count + increment")
    biological_node.parameters.append(count_parameter)

    # Add an output port for the biological entity node
    output_port = OutputPort(id="output", value="count")
    biological_node.output_ports.append(output_port)

    return biology_model


def execute_model(model):
    # Execute the graph
    eg = EvaluableGraph(model.graphs[0], verbose=False)
    eg.evaluate()
    return eg.enodes["BiologicalEntity"].evaluable_outputs["output"].curr_value


def main():
    st.title("Simple Biology Model Execution")

    # Create a button to execute the model
    if st.button("Execute Model"):
        st.write("Executing model...")

        # Create and execute the model
        model = create_biology_model()
        output_value = execute_model(model)

        # Display the output value
        st.write("Output:", output_value)

        # Optionally, plot the output at multiple time points
        time_points = np.linspace(0, 10, 11)  # Example time points
        output_values = [execute_model(model) for _ in time_points]
        st.line_chart(output_values, time_points)


if __name__ == "__main__":
    main()
