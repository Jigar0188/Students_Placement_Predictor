import numpy as np
import pandas as pd

df = pd.read_csv('students_record.csv')

print("file has been read")

# print(df.head(5))

# print(df.info())


#Sanity check----> if values is out of range

# print(df.describe())


# column_names = df.columns.tolist()
# print(column_names)

# target = df["placed"]
# print(target.unique())
# print(target.value_counts())

# branch_variety = df["branch"].unique()
# print(branch_variety)

# print(df.shape)

duplicated_values = df.duplicated()
# print(duplicated_values.sum())


#  drop duplicates
df.drop_duplicates(inplace=True)

# print(df.shape)

# categorical_columns = df.select_dtypes(include=['object']).columns.tolist()
# print(categorical_columns)


#  drop the unnecessary columns
columns_to_drop = ["student_id", "name", "registration_date"]

model_df = df.drop(columns=columns_to_drop)

# print(model_df.shape)
# print(model_df["branch"].unique())

# print(model_df.isnull().sum())

#  fix the branch names

canonical_branch_names = {
        "cse": "CSE",
        "Cse": "CSE",
        "Computer Science": "CSE",
        "C.S.E": "CSE",
        "it": "IT",
        "i.t.": "IT",
        "I.T": "IT",
        "Information Technology": "IT",
        "ece": "ECE",
        "E.C.E": "ECE",
        "electronics": "ECE",
        "Electronics": "ECE",
        "eee": "EEE",
        "e.e.e": "EEE",
        "electrical": "EEE",
        "Electrical": "EEE",
        "mech": "MECH",
        "Mechanical": "MECH",
        "Civil": "CIVIL",
        "civil": "CIVIL"
}

model_df["branch"] = (
    df["branch"]
    .astype(str)
    .str.strip()
    .str.lower()
    .replace(canonical_branch_names)
)
model_df["branch"] = df["branch"].replace(canonical_branch_names)

# print("----------")
# print(model_df["branch"].unique())

# cgpa has to be numeric value, but it's showing object nature because of " , " instead of " . " on some places-- 

model_df["cgpa"] = model_df["cgpa"].str.replace(",", ".").astype(float)


# print(model_df["cgpa"].isna().sum())
# print(model_df[model_df["cgpa"].isna()])

model_df["cgpa"] = pd.to_numeric(model_df["cgpa"], errors="coerce")
# print(type(model_df["cgpa"].iloc[0]))



# remove the impossible values--

model_df.loc[(model_df["cgpa"] < 0 )| (model_df["cgpa"] > 10), "cgpa"] = np.nan
model_df.loc[(model_df["attendance_percent"] < 0 )| (model_df["attendance_percent"] > 100), "attendance_percent"] = np.nan
model_df.loc[(model_df["coding_problems_solved"]>2500), "coding_problems_solved"] = np.nan
model_df.loc[(model_df["salary_expectation"]>5000000), "salary_expectation"] = np.nan


# fill numeric columns using median

numeric_columns_with_gaps = ["attendance_percent","communication_skill","tech_events_attended","salary_expectation", "cgpa","coding_problems_solved" ]

for columns in numeric_columns_with_gaps:
    column_median = model_df[columns].median()
    model_df[columns] = model_df[columns].fillna(column_median)


# fill categorical columns 
model_df["city"] = model_df["city"].fillna("Unknown")
# print(model_df.isnull().sum())


# print(model_df["tech_events_attended"].describe())

# students_record_cleaned = model_df.to_csv("students_record_cleaned.csv", index=False)
# print("Cleaned dataset saved to 'students_record_cleaned.csv'")

# Target Distribution tests

# print(model_df["placed"].value_counts())
# print(model_df["placed"].value_counts(normalize=True))

# print("cgpa:", model_df.groupby("placed")["cgpa"].mean())
# print("technical_skills:", model_df.groupby("placed")["technical_skills"].mean())
# print("projects_completed:", model_df.groupby("placed")["projects_completed"].mean())
# print("communication_skill:", model_df.groupby("placed")["communication_skill"].mean())
# print("coding_problems_solved:", model_df.groupby("placed")["coding_problems_solved"].mean())
# print("tech_events_attended:", model_df.groupby("placed")["tech_events_attended"].mean())


# for categorical variables
print(
    pd.crosstab(
        model_df["branch"],
        model_df["placed"],
        normalize="index"
    )
)