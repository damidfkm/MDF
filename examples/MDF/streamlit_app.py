import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from modeci_mdf.execution_engine import EvaluableGraph
from modeci_mdf.utils import simple_connect
from modeci_mdf.mdf import *

# Define the MDF model creation and execution function
def execute_biology_model():
    # Create the MDF model
    mod = Model(id="BiologyModel")
    mod_graph = Graph(id="biology_example")
    mod.graphs.append(mod_graph)

    # Create nodes and connect them
    population_node = Node(id="Population")
    interaction_node = Node(id="Interaction")

    simple_connect(population_node, interaction_node, mod_graph)

    # Set parameters for nodes
    population_growth_rate = Parameter(id="growth_rate", value=0.1)
    interaction_rate = Parameter(id="interaction_rate", value=0.05)

    population_node.parameters.append(population_growth_rate)
    interaction_node.parameters.append(interaction_rate)

    # Set conditions for nodes
    population_condition = Condition(type="Always")
    interaction_condition = Condition(type="EveryNCalls", dependencies=population_node.id, n=5)
    mod_graph.conditions = ConditionSet(
        node_specific={population_node.id: population_condition, interaction_node.id: interaction_condition}
    )

    # Execute the graph
    eg = EvaluableGraph(mod_graph, verbose=False)
    eg.evaluate()

    # Get output values
    population_size = eg.enodes["Population"].evaluable_outputs["population_size"].curr_value
    predator_size = eg.enodes["Interaction"].evaluable_outputs["predator_size"].curr_value

    return population_size, predator_size


# Create Streamlit app
def main():
    st.title("Simple Biology Model Execution")

    # Execute the model when button is clicked
    if st.button("Execute Model"):
        st.write("Executing model...")
        population_size, predator_size = execute_biology_model()

        # Plot the output
        plt.figure(figsize=(10, 5))
        plt.plot(population_size, label="Population Size")
        plt.plot(predator_size, label="Predator Size")
        plt.xlabel("Time")
        plt.ylabel("Size")
        plt.title("Population and Predator Size Over Time")
        plt.legend()
        st.pyplot(plt)

# Run the app
if __name__ == "__main__":
    main()