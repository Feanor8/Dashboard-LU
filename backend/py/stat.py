# Komplette Population | Done
def num_population(df):
    return len(df)

# Hauptwohnsitz (Code: 40) | Done
def num_population_main_household(df):
    total = df.shape[0]
    if total == 0:
        return "Keine Daten"
    m = df[df["einWohnsitzart"] == 40].shape[0]
    return m

# Sekundärwohnsitz (Code: 20) | Done
def num_population_secondary_household(df):
    total = df.shape[0]
    if total == 0:
        return "Keine Daten"
    m = df[df["einWohnsitzart"] == 20].shape[0]
    return m

# Männliche Population | Done
def per_population_male(df):
    total = df.shape[0]
    if total == 0:
        return "Keine Daten"
    m = df[df["Geschlecht"] == 1].shape[0]
    return f"{(m / total * 100):.1f} %"

# Weibliche Population |  Done
def per_population_female(df):
    total = df.shape[0]
    if total == 0:
        return "Keine Daten"
    w = df[df["Geschlecht"] == 2].shape[0]
    return f"{(w / total * 100):.1f} %"

# Eingezogen | Done
def num_population_moved_in(df):
    return "Daten benötigt"

# Ausgezogen | Done
def num_population_moved_out(df):
    return "Daten benötigt"

# Ein-und-Auszug Saldo 
def diff_population_moved(df):
    return "Daten benötigt"

# Altersdurchschnitt | Done
def num_population_average_age(df):
    return round(df["einAlter"].mean(), 2)

# Geburten | Daten benötigt
def num_population_births(df):
    return "Daten benötigt"

# Tode | Daten benötigt
def num_population_deaths(df):
    return "Daten benötigt"

# Geburten-Tode-Saldo | Daten benötigt
def diff_population_births_and_deaths(df):
    return "Daten benötigt"

# Sozialversicherungspflichtige | Daten benötigt
def num_population_social_insurance_subject(df):
    return "Daten benötigt"

# Arbeitende Population in Prozent | Daten benötigt
def per_population_with_jobs(df):
    return "Daten benötigt"

# Arbeitssuchende Population | Daten benötigt
def num_population_no_jobs(df):
    return "Daten benötigt"

# Arbeitssuchende Population in Prozent | Daten benötigt
def per_population_no_jobs(df):
    return "Daten benötigt"
    
# Durchschnittliche Kaufkraft pro Person in Euro | Daten benötigt
def num_population_buying_average_person(df):
    return "Daten benötigt"

# Durchschnittliche Kaufkraft pro Haushalt in Euro | Daten benötigt
def num_population_buying_average_household(df):
    return "Daten benötigt" 

# Kaufkraftindex pro Person | Daten benötigt 
def num_population_buying_index_person(df):
    return "Daten benötigt"

# Kaufkraftindex pro Haushalt | Daten benötigt
def num_population_buying_index_household(df):
    return "Daten benötigt"