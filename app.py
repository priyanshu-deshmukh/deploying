from flask import Flask, render_template
from datetime import datetime
import pandas as pd

app = Flask(__name__)

# Function to calculate age in years, months, and days
def calculate_age(birthdate):
    today = datetime.today()
    delta = today - birthdate
    years = delta.days // 365
    months = (delta.days % 365) // 30
    days = (delta.days % 365) % 30
    return years, months, days

# Function to calculate days left until the next birthday
def days_until_birthday(birthdate):
    today = datetime.today()
    next_birthday = birthdate.replace(year=today.year)
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year)
    return (next_birthday - today).days

# Function to safely parse dates
def parse_date(date_value):
    """Tries to parse a date string and return a datetime object."""
    try:
        return datetime.strptime(str(date_value), "%d-%m-%Y")
    except ValueError:
        return None

@app.route('/')
def index():
    # Load the Excel file
    df = pd.read_excel('input.xlsx')

    people = []
    for _, row in df.iterrows():
        first_name = row['First Name']
        last_name = row['Last Name']
        dob = row['Date of Birth']

        # Parse and validate the date of birth
        dob_parsed = parse_date(dob)
        if dob_parsed is None:
            continue  # Skip this entry if date is invalid

        # Calculate age and days left for birthday
        age = calculate_age(dob_parsed)
        days_to_birthday = days_until_birthday(dob_parsed)

        people.append({
            'first_name': first_name,
            'last_name': last_name,
            'age': f"{age[0]} Years, {age[1]} Months, {age[2]} Days",
            'days_to_birthday': days_to_birthday
        })

    # Render the template with the processed data
    return render_template('index.html', people=people)

if __name__ == '__main__':
    app.run(debug=True)
