import streamlit as st
import pandas as pd
import altair as alt
import Task1.Task1 as dsp
import matplotlib.pyplot as plt


st.set_page_config(page_title="Task 1 — Signal Operations", layout="wide")

st.title("Task 1 — Signal Operations")

st.markdown(
    """
    This GUI uses your **Task1.py** project functions to perform signal operations.

    **Supported operations:**
    - Add two signals
    - Subtract two signals
    - Multiply a signal by a constant
    - Shift (advance/delay)
    - Fold (time reversal)
    """
)

# Sidebar: choose operation
st.sidebar.header("Operations")
operation = st.sidebar.selectbox(
    "Choose operation",
    ["Add", "Subtract", "Multiply by constant", "Shift", "Fold"]
)

const_val = st.sidebar.number_input("Constant (for multiply)", value=2.0,step=1.0)
shift_val = st.sidebar.number_input("Shift amount", value=1)

# Run operation using Task1 functions
result = None
if operation == "Add":
    indices, values = dsp.AddingSignals()
    result = pd.DataFrame({"n": indices, "x": values})
elif operation == "Subtract":
    indices, values = dsp.SubSignals()
    result = pd.DataFrame({"n": indices, "x": values})
elif operation == "Multiply by constant":
    indices, values = dsp.MultiplySignals(const_val)
    result = pd.DataFrame({"n": indices, "x": values})
elif operation == "Shift":
    indices, values = dsp.ShiftSignal(shift_val)
    result = pd.DataFrame({"n": indices, "x": values})
elif operation == "Fold":
    indices, values = dsp.Fold()
    result = pd.DataFrame({"n": indices, "x": values})

# Display results
if result is None or result.empty:
    st.warning("No result yet.")
else:
    st.subheader("Resulting Signal")
    horizontal = pd.DataFrame([result["x"].values], columns=result["n"].values,index=["x[n]"])
    horizontal.index.name = "n"
    st.write(horizontal)

    # # Plot as a DSP stem plot (discrete-time signal)
    # st.sidebar.header("Plot options")
    # show_points = st.sidebar.checkbox("Show sample points", value=True)

    # if result is not None and not result.empty:
    #     fig, ax = plt.subplots()

    #     # Classic DSP-style stem plot
    #     markerline, stemlines, baseline = ax.stem(result["n"], result["x"])

    #     # Style the stems and markers
    #     plt.setp(markerline, marker='o', markersize=6, color='blue', markerfacecolor='blue')
    #     plt.setp(stemlines, color='blue')
    #     plt.setp(baseline, color='black', linewidth=1)

    #     # Axes styling
    #     ax.axhline(0, color='black', linewidth=1)   # horizontal axis
    #     ax.axvline(0, color='black', linewidth=1)   # vertical axis
    #     ax.set_xlabel("n")
    #     ax.set_ylabel("x[n]")

    #     st.pyplot(fig)
        
    # Plot 
    st.sidebar.header("Plot options") 
    show_points = st.sidebar.checkbox("Show sample points", value=True) 
    base = alt.Chart(result.reset_index()).encode( x=alt.X('n:Q', title="n"), y=alt.Y('x:Q', title="x(n)"), tooltip=['n', 'x'] ) 
    line = base.mark_line(point=show_points) 
    st.altair_chart(line.interactive(), use_container_width=True)
    
st.markdown("---")
st.caption("Created for DSP Task 1 — Streamlit GUI powered by Task1.py")
