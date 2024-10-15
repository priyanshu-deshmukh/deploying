def days_until_birthday(birthdate):
    today = datetime.today()
    next_birthday = birthdate.replace(year=today.year)
    if next_birthday < today:
        next_birthday = next_birthday.replace(year=today.year)
    return (next_birthday - today).days