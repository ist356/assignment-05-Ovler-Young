import pandas as pd
import streamlit as st
import pandaslib as pl

# TODO: Write your transformation code here

# 1. Load the data from the cache
states_data = pd.read_csv("cache/states.csv")
survey_data = pd.read_csv("cache/survey.csv")

# Create a unique list of years from the survey data
years = survey_data["year"].unique()

# Load cost of living data for each year
col_dataframes = []
for year in years:
    col_df = pd.read_csv(f"cache/col_{year}.csv")
    col_dataframes.append(col_df)
col_data = pd.concat(col_dataframes, ignore_index=True)

# 2. Merge the survey data with the cost of living data
survey_data["_country"] = survey_data["What country do you work in?"].apply(
    pl.clean_country_usa
)

# Join states data to map state names to codes
survey_data = survey_data.merge(
    states_data,
    left_on="If you're in the U.S., what state do you work in?",
    right_on="State",
    how="inner",
)

# Engineer the full city column
survey_data["_full_city"] = (
    survey_data["What city do you work in?"]
    + ", "
    + survey_data["Abbreviation"]
    + ", "
    + survey_data["_country"]
)

# Merge with cost of living data
combined = survey_data.merge(
    col_data, left_on=["year", "_full_city"], right_on=["year", "City"], how="inner"
)

# 3. Normalize the annual salary based on cost of living
combined["__annual_salary_cleaned"] = combined[
    "What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"
].apply(pl.clean_currency)
combined["_annual_salary_adjusted"] = (
    100 / combined["Cost of Living Index"]
) * combined["__annual_salary_cleaned"]

# 4. Produce the reports
# Save the engineered dataset
combined.to_csv("cache/survey_combined.csv", index=False)

# Create and save the first report
location_age_report = pd.pivot_table(
    combined,
    values="_annual_salary_adjusted",
    index="_full_city",
    columns="How old are you?",
    aggfunc="mean",
)
location_age_report.to_csv("cache/annual_salary_adjusted_by_location_and_age.csv")

# Create and save the second report
location_education_report = pd.pivot_table(
    combined,
    values="_annual_salary_adjusted",
    index="_full_city",
    columns="What is your highest level of education completed?",
    aggfunc="mean",
)
location_education_report.to_csv(
    "cache/annual_salary_adjusted_by_location_and_education.csv"
)


st.header("Annual Salary Adjusted by Location Education")
st.scatter_chart(location_education_report, size=30)
st.download_button(
    "Download Location and Education Report",
    "cache/annual_salary_adjusted_by_location_and_education.csv",
)

st.header("Annual Salary Adjusted by Location and Age")
st.scatter_chart(location_age_report, size=30)
st.download_button(
    "Download Location and Age Report",
    "cache/annual_salary_adjusted_by_location_and_age.csv",
)