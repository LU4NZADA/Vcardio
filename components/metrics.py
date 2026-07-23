import streamlit as st


def metric_row(metrics):
    cols = st.columns(len(metrics))
    for col, (label, valor, delta) in zip(cols, metrics):
        with col:
            st.metric(label=label, value=valor, delta=delta)