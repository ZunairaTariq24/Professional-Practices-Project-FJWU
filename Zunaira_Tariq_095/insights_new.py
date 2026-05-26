import pandas as pd

# 1. Load your dataset
file_path = 'cleaned_data_with_insights.xlsx'  # Update if your file name is different
df = pd.read_excel(file_path)

# Clean column names (strip whitespace just in case)
df.columns = df.columns.str.strip()

# 2. Define the columns needed for this analysis
col_behavior = "Be honest, what describes you the best?"
col_internship = "Respond to the following Questions. [Completed any internship?]"
col_projects = "Respond to the following Questions. [Worked on real-world projects (outside coursework)?]"
col_freelancing = "Respond to the following Questions. [Done freelancing or any paid work?]"
col_skills_lacking = "What skills do you think you are lacking for a job?"
col_university_change = "If you could change one thing in your university system to better prepare students for jobs, what would it be?"

# 3. Create a function to classify students into Persona A or Persona B
def classify_persona(row):
    # Check if they have done any practical out-of-class work
    has_practical_exp = (
        str(row[col_internship]).strip().lower() == 'yes' or
        str(row[col_projects]).strip().lower() == 'yes' or
        str(row[col_freelancing]).strip().lower() == 'yes'
    )
    
    # Check their mindset statement
    is_active_mindset = "actively work on skills" in str(row[col_behavior]).lower()
    
    # Classification Logic
    if has_practical_exp and is_active_mindset:
        return "Persona B: Proactive Agile"
    else:
        return "Persona A: Passive-Dependent"

# Apply the persona classification to the dataframe
df['Student_Persona'] = df.apply(classify_persona, axis=1)

# 4. Separate the open-ended text based on these Personas to analyze them
print("--- ANALYSIS COMPLETED ---\n")
print(f"Total Students Segmented:")
print(df['Student_Persona'].value_counts())
print("-" * 50)

# 5. Let's look at what Persona A vs Persona B actually say they are lacking
for persona in ["Persona A: Passive-Dependent", "Persona B: Proactive Agile"]:
    print(f"\n💡 SAMPLE RESPONSES FROM [{persona.upper()}]:")
    subset = df[df['Student_Persona'] == persona].head(5) # Look at top 5 examples
    
    for idx, row in subset.iterrows():
        print(f"\n- Mindset/Behavior: {row[col_behavior]}")
        print(f"  Says they lack: '{row[col_skills_lacking]}'")
        print(f"  Wants University to change: '{row[col_university_change]}'")

# 6. Save this segmented data to a new spreadsheet for your report
df.to_excel('behavioral_integrity_analysis.xlsx', index=False)