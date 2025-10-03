#  MENA Ethnic Diversity Dashboard

https://mena-ethnic-visualization-chbree9gc8fzao7ijvkmfr.streamlit.app/

Interactive satellite-view dashboard exploring ethnic composition across 20 Middle East & North Africa countries (1946-2021). 

##  Overview
This project visualizes ethnic distributions across the MENA region with:
- **Satellite & Political maps** - Toggle between visualization styles
- **Historical analysis** - Data from 1946 to 2021
- **Regional focus** - Maghreb, Mashriq, and Gulf States
- **Country profiles** - Detailed ethnic breakdowns

##  Features
- **Interactive choropleth maps** with ethnic group coloring
- **Time slider** (1946-2021) for historical comparison
- **Regional filtering** (Maghreb, Mashriq, Gulf States)
- **Country-specific analysis** with treemap visualizations
- **Ethnic group spotlight** across multiple countries

##  Tech Stack
- **Frontend**: Streamlit, Plotly, Matplotlib
- **Data Processing**: Pandas, NumPy
- **Visualization**: Choropleth maps, treemaps, area charts

## Data Sources

### Primary Source
**Ethnic Power Relations (EPR) Core Dataset 2021**
- **URL**: https://icr.ethz.ch/data/epr/core/
- **Coverage**: 1946-2021, 181 countries
- **Academic credibility**: Used in peer-reviewed research

### Estimation Sources (for missing countries)
**CIA World Factbook**
- https://www.cia.gov/the-world-factbook/field/ethnic-groups/
- Used for Yemen, Mauritania, Sudan estimates

**World Population Review**
- https://worldpopulationreview.com/country-rankings/ethnicity-by-country
- Current demographic estimates

### Academic Research References
- Alesina et al. (2003) - Fractionalization paper
- Minorities at Risk Project
- World Values Survey

## Dataset
- **20 MENA countries** including Yemen, Mauritania, Sudan estimates
- **54 ethnic groups** from Arabs and Amazigh to Kurds and various minorities
- **75-year span** from post-WWII (1946) to present (2021)

##  Local Development
```bash
# Clone repository
git clone https://github.com/yourusername/mena-ethnic-dashboard.git

# Install dependencies
pip install -r requirements.txt

# Run locally
streamlit run app.py
