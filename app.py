import streamlit as st
import pandas as pd
import altair as alt
import matplotlib.pyplot as plt
from wordcloud import WordCloud


# Load data
url = "California_Fire_Incidents.csv"
df = pd.read_csv(url)
#list data columns
a = list(df)
print(a)

st.write("# California Fire Incidents ")

# Sidebar filters
st.sidebar.title("Filters")
year_range = st.sidebar.slider("Year Range", min_value=2013, max_value=2020, value=(2013, 2020))
county = st.sidebar.selectbox("County", df["Counties"].unique())

# Filter data - Pandas Feature
df_filtered = df[(df["AcresBurned"] > 0) & (df["ArchiveYear"].between(*year_range)) & (df["Counties"] == county)]

# Top 10 largest wildfires table
largest_wildfires = df_filtered.nlargest(10, "AcresBurned")[["Name", "Started", "Extinguished", "AcresBurned"]]
st.write("### Top 10 Largest Wildfires in", county, "County between", year_range[0], "and", year_range[1])
st.table(largest_wildfires)

# Total acres burned chart
st.write("### Total acres burned chart")
# Sum of Elements Aggrigation - Pandas Feature
total_acres_burned = df_filtered.groupby("ArchiveYear")["AcresBurned"].sum().reset_index()
total_acres_burned_chart = alt.Chart(total_acres_burned).mark_bar().encode(
    x="ArchiveYear",
    y="AcresBurned",
    tooltip=["ArchiveYear", "AcresBurned"]
).properties(width=600)
st.altair_chart(total_acres_burned_chart)

st.write("### Year with highest Incidents Reported")

# Group by year and count - Pandas Feature
yearly_counts = df.groupby("ArchiveYear")["Name"].count().reset_index()

# Create line chart
line_chart = alt.Chart(yearly_counts).mark_line().encode(
    x="ArchiveYear",
    y="Name"
)

# Display line chart
st.altair_chart(line_chart, use_container_width=True)

st.write("### Wildfires by Year")
# Group by year and count
yearly_counts = df.groupby("ArchiveYear")["Name"].count().reset_index()

# Create bar chart using Altair
chart = alt.Chart(yearly_counts).mark_bar().encode(
    x="ArchiveYear",
    y="Name",
    tooltip=["ArchiveYear", "Name"]
).properties(
    title="Number of Wildfires in California by Year",
    width=alt.Step(20)
)

# Display chart using Streamlit
st.altair_chart(chart, use_container_width=True)


st.write("### Search Description WordCloud")
descriptions = df["SearchDescription"].str.cat(sep=" ")

# Create word cloud
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="inferno").generate(descriptions)

# Display word cloud
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot()

st.write("## Control Statement WordCloud")
descriptions = df["ControlStatement"].str.cat(sep=" ")

# Create word cloud
wordcloud = WordCloud(width=800, height=400, background_color="white", colormap="inferno").generate(descriptions)

# Display word cloud
st.set_option('deprecation.showPyplotGlobalUse', False)
plt.figure(figsize=(12, 6))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
st.pyplot()

