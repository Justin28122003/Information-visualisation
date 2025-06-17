import pandas as pd
from scipy.stats import pearsonr

# Laad de CSV-bestanden
covid_df = pd.read_csv('owid-covid-data.csv')
onderwijs_df = pd.read_csv('education.csv', encoding='latin1')
# life_expectancy

# "Mortality rate, under-5 (per 1,000)"
# "Prevalence of HIV, total (% of population ages 15-49)"

# Neem het gemiddelde vaccinatiepercentage per land
vaccinatie_per_land = covid_df.sort_values('date').groupby('location', as_index=False)['people_vaccinated_per_hundred'].last()
GDP_per_land = covid_df.sort_values('date').groupby('location',as_index = False)['gdp_per_capita'].last()
handenwassen_per_land = covid_df.sort_values('date').groupby('location', as_index=False)['handwashing_facilities'].last()

# Filter op de juiste indicator
onderwijs_literacy = onderwijs_df[onderwijs_df['Series Code'] == 'SE.ADT.LITR.ZS']
sterfgevallen_jaartal = onderwijs_df[onderwijs_df['Series Code'] == 'SH.DYN.MORT']
hiv_gevallen = onderwijs_df[onderwijs_df['Series Code'] == 'SH.DYN.AIDS.ZS']
onderwijzers = onderwijs_df[onderwijs_df['Series Code'] == 'UIS.QUTP.02']

# Zet de jaarkolommen om naar numeriek (behalve de metadata-kolommen)
jaar_kolommen = [col for col in onderwijs_literacy.columns if '[YR' in col]
onderwijs_literacy[jaar_kolommen] = onderwijs_literacy[jaar_kolommen].replace('..', pd.NA).apply(pd.to_numeric, errors='coerce')
sterfgevallen_jaartal[jaar_kolommen] = sterfgevallen_jaartal[jaar_kolommen].replace('..', pd.NA).apply(pd.to_numeric, errors='coerce')
hiv_gevallen[jaar_kolommen] = hiv_gevallen[jaar_kolommen].replace('..', pd.NA).apply(pd.to_numeric, errors = 'coerce')
onderwijzers[jaar_kolommen] = onderwijzers[jaar_kolommen].replace('..', pd.NA).apply(pd.to_numeric, errors = 'coerce')
# Vind per land de meest recente waarde
onderwijs_literacy['literacy_rate'] = onderwijs_literacy[jaar_kolommen].bfill(axis=1).iloc[:, 0]
sterfgevallen_jaartal['sterfgevallen'] = sterfgevallen_jaartal[jaar_kolommen].bfill(axis=1).iloc[:, 0]
hiv_gevallen['hiv_cases'] = hiv_gevallen[jaar_kolommen].bfill(axis=1).iloc[:,0]
onderwijzers['goede_onderwijzers'] = onderwijzers[jaar_kolommen].bfill(axis=1).iloc[:,0]
# Maak een nieuw dataframe met land en meest recente waarde
onderwijs_literacy_recent = onderwijs_literacy[['Country Name', 'literacy_rate']].rename(columns={'Country Name': 'location'})
sterfgevallen_jaartal_recent = sterfgevallen_jaartal[['Country Name', 'sterfgevallen']].rename(columns={'Country Name': 'location'})
hiv_gevallen = hiv_gevallen[['Country Name', 'hiv_cases']].rename(columns={'Country Name': 'location'})
onderwijzers = onderwijzers[['Country Name', 'goede_onderwijzers']].rename(columns={'Country Name': 'location'})
# Merge op landnaam
merged_df = pd.merge(vaccinatie_per_land, onderwijs_literacy_recent, on='location')
merged_df = pd.merge(merged_df, sterfgevallen_jaartal_recent, on='location')
merged_df = pd.merge(merged_df, GDP_per_land, on='location')
merged_df = pd.merge(merged_df, hiv_gevallen, on='location')
merged_df = pd.merge(merged_df, onderwijzers, on='location')
merged_df = pd.merge(merged_df, handenwassen_per_land, on='location')

# print(merged_df.head(10))
# Toon het resultaat
# print(merged_df.head(30))

correlatie_GDP_literacy = merged_df['gdp_per_capita'].corr(merged_df['literacy_rate'])
correlatie_GDP_sterfgevallen = merged_df['gdp_per_capita'].corr(merged_df['sterfgevallen'])
correlatie_GDP_hiv = merged_df['gdp_per_capita'].corr(merged_df['hiv_cases'])
correlatie_GDP_onderwijzers = merged_df['gdp_per_capita'].corr(merged_df['goede_onderwijzers'])
correlatie_vaccinatie_literacy = merged_df['people_vaccinated_per_hundred'].corr(merged_df['literacy_rate'])
correlatie_vaccinatie_sterfgevallen = merged_df['people_vaccinated_per_hundred'].corr(merged_df['sterfgevallen'])
correlatie_vaccinatie_hiv = merged_df['people_vaccinated_per_hundred'].corr(merged_df['hiv_cases'])
correlatie_vaccinatie_onderwijzers = merged_df['people_vaccinated_per_hundred'].corr(merged_df['goede_onderwijzers'])
correlatie_handenwassen_literacy = merged_df['handwashing_facilities'].corr(merged_df['literacy_rate'])
correlatie_handenwassen_sterfgevallen = merged_df['handwashing_facilities'].corr(merged_df['sterfgevallen'])
correlatie_handenwassen_hiv = merged_df['handwashing_facilities'].corr(merged_df['hiv_cases'])
correlatie_handenwassen_onderwijzers = merged_df['handwashing_facilities'].corr(merged_df['goede_onderwijzers'])
# print(correlatie_GDP_literacy, correlatie_GDP_sterfgevallen, correlatie_GDP_hiv, correlatie_vaccinatie_literacy, correlatie_vaccinatie_sterfgevallen, correlatie_vaccinatie_hiv, correlatie_GDP_onderwijzers,correlatie_vaccinatie_onderwijzers)
# print(correlatie_handenwassen_literacy)