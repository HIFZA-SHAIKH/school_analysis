import streamlit as st
import pandas as pd
import os

import plotly.express as px

# Add a title for the project
st.title("📊 Cost Analysis of Schools")
uploaded_file = st.file_uploader("Upload your Excel file", type=["xlsx", "xls"])
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df.columns = [col.strip().replace("state", "State") for col in df.columns]  # Clean and standardize column names

    st.subheader("📄 Data Preview")
    st.dataframe(df.head())

    # Sidebar Filter: School Name
    st.sidebar.header("🔍 Filter by School Name")
    school_filter = st.sidebar.multiselect(
        "Select School(s):", sorted(df["School Name"].dropna().unique()), default=None
    )

    # Apply filter
    filtered_df = df.copy()
    if school_filter:
        filtered_df = filtered_df[filtered_df["School Name"].isin(school_filter)]

    st.markdown("### Filtered Dataset")
    st.dataframe(filtered_df.head())

    st.divider()

    school_col = "School Name"

    # Chart 1: Bar Chart - Top 10 Schools by Enrollments
    if "total enrolled student" in filtered_df.columns:
        col = "total enrolled student"
        data = filtered_df[[school_col, col]].dropna().sort_values(by=col, ascending=False).head(10)
        fig_bar = px.bar(data, x=col, y=school_col, orientation='h', title="Top 10 Schools by Enrolled Students")
        st.plotly_chart(fig_bar, use_container_width=True)

    # Chart 2: Line Chart - Tuition Fees of Top 10 Schools
    if "textbooks" in filtered_df.columns:
        col = "textbooks"
        data = filtered_df[[school_col, col]].dropna().sort_values(by=col, ascending=False)
        fig_tuition = px.bar(data, x=school_col, y=col, title="Text book Fees of All Schools", labels={school_col: "School Name", col: "Tuition Fees"})
        st.plotly_chart(fig_tuition, use_container_width=True)
    # Chart 3: Funnel Chart - Transportation Options
    if "transportation for students" in filtered_df.columns:
        col = "transportation for students"
        transport_counts = filtered_df[col].fillna("No Info").value_counts().reset_index()
        transport_counts.columns = ["Transportation Option", "Number of Schools"]
        fig_funnel = px.funnel(transport_counts, x="Number of Schools", y="Transportation Option",
                               title="Funnel Chart: Availability of Student Transportation")
        st.plotly_chart(fig_funnel, use_container_width=True)

    # Chart 4: Pie Chart - Schools Providing Meals/Snacks
    if "Are meals or snacks provided? If yes, what is the cost for families?" in filtered_df.columns:
        col = "Are meals or snacks provided? If yes, what is the cost for families?"
        meal_provided = filtered_df[col].fillna("No Info").apply(lambda x: "Yes" if "yes" in str(x).lower() else "No")
        meal_counts = meal_provided.value_counts().reset_index()
        meal_counts.columns = ["Meals Provided", "Number of Schools"]
        fig_pie = px.pie(meal_counts, names="Meals Provided", values="Number of Schools",
                         title="Do Schools Provide Meals or Snacks?")
        st.plotly_chart(fig_pie, use_container_width=True)

    # Chart 5: Scatter Plot - Free Education Eligibility
    if "Are any students eligible for free education programs?" in filtered_df.columns:
        col = "Are any students eligible for free education programs?"
        eligible = filtered_df[col].fillna("No Info").value_counts().reset_index()
        eligible.columns = ["Eligibility", "Number of Schools"]
        fig_scatter = px.scatter(eligible, x="Eligibility", y="Number of Schools",
                                 title="Schools with Free Education Eligibility")
        st.plotly_chart(fig_scatter, use_container_width=True)

    # Chart 6: Column Chart - Location-wise Number of Schools
    if "location" in filtered_df.columns:
        col = "location"
        location_counts = filtered_df[col].value_counts().reset_index()
        location_counts.columns = ["Location", "Number of Schools"]
        fig_column = px.bar(location_counts, x="Location", y="Number of Schools",
                            title="Location-wise Number of Schools")
        st.plotly_chart(fig_column, use_container_width=True)