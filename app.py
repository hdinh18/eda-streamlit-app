import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load dataset
def load_data():
    data = st.sidebar.file_uploader("Upload a CSV file", type='csv')
    if data:
        return pd.read_csv(data)
# Since the Iris dataset is open-source, there is no need to read a csv file
df = load_data()
if df is None:
    df = sns.load_dataset("iris")
# App title
st.title("Interactive Dashboard")
# Sidebar header
st.sidebar.header("Controls")

# Select numeric columns
numeric_columns = df.select_dtypes(include=['float64', 'int64']).columns
# Make the map to setup the clean UI
label_map = {col: col.replace("_", " ").title() for col in numeric_columns}
# Input 1
x_variable = st.sidebar.selectbox(
    "Select X variable",
    numeric_columns,
    format_func=lambda x: label_map[x]
)
# Input 2
y_variable = st.sidebar.selectbox(
    "Select Y variable",
    numeric_columns,
    format_func=lambda x: label_map[x]
)
# Make the label
x_label = label_map[x_variable]
y_label = label_map[y_variable]
# Select hue columns
hue_columns = df.select_dtypes(include=['object']).columns
if len(hue_columns) > 0:
    hue_map = {col: col.replace("_", " ").title() for col in hue_columns}

    hue_variable = st.sidebar.selectbox(
        "Select hue variable",
        hue_columns,
        format_func=lambda x: hue_map[x]
    )
else:
    hue_variable = None

# Plot section
st.subheader("Scatter Plot")
fig, ax = plt.subplots()
sns.scatterplot(data=df, x=x_variable, y=y_variable, hue=hue_variable, ax=ax)
ax.set_title(f"{x_label} vs {y_label}")
ax.set_xlabel(x_label)
ax.set_ylabel(y_label)
st.pyplot(fig)

# Correlation section
st.subheader("Correlation Result")
# Correlation calculation
correlation = df[x_variable].corr(df[y_variable])
# Output results
st.write(f"Correlation between **{x_label}** and **{y_label}**: {correlation:.3f}")
# Compare to understand the relationship
relationship = ''
if correlation >= 0.5:
    relationship = 'strong positive'
elif correlation > 0:
    relationship = 'weak positive'
elif correlation <= -0.5:
    relationship = 'strong negative'
elif correlation < 0:
    relationship = 'weak negative'
else:
    relationship = 'no'
# Output the relationship
st.write(f"**{x_label}** and **{y_label}** have {relationship} relationship")
