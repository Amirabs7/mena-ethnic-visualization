import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('mena_ethnicity_enhanced_final.csv')
    
    # DEBUG: Check original data structure
    st.sidebar.markdown("### DEBUG: Data Structure")
    st.sidebar.write(f"Total rows: {len(df)}")
    st.sidebar.write(f"Year range: {df['from'].min()} - {df['to'].max()}")
    st.sidebar.write(f"Unique years in 'to': {sorted(df['to'].unique())}")
    
    # Check if data actually changes by year for a sample country
    sample_country = df['statename'].iloc[0] if len(df) > 0 else None
    if sample_country:
        country_data = df[df['statename'] == sample_country]
        st.sidebar.write(f"Sample country '{sample_country}' years: {sorted(country_data['to'].unique())}")
        
        # Check if percentages change across years
        for year in sorted(country_data['to'].unique()):
            year_data = country_data[country_data['to'] == year]
            st.sidebar.write(f"  {year}: {len(year_data)} groups")
    
    # UPDATE: Change Berber to Amazigh as requested
    df['group'] = df['group'].replace({'Berbers': 'Amazigh'})
    
    # FIX: Manual data corrections
    # Update Mauritania from Arab-Berber to Arab-Amazigh
    df['group'] = df['group'].replace({'Arab-Berber': 'Arab-Amazigh'})
    
    # Update Palestine data for 2023 - add Israeli settlers
    if 'Palestine' in df['statename'].values:
        settlers_data = {
            'statename': 'Palestine',
            'group': 'Israeli Settlers', 
            'percentage': 15.0,
            'from': 2023,
            'to': 2023
        }
        df = df[~((df['statename'] == 'Palestine') & (df['group'] == 'Israeli Settlers'))]
        settlers_df = pd.DataFrame([settlers_data])
        df = pd.concat([df, settlers_df], ignore_index=True)
    
    # FIX: Tunisia composition - 98% Arab-Amazigh, 2% Others
    if 'Tunisia' in df['statename'].values:
        df = df[df['statename'] != 'Tunisia']
        tunisia_data = [
            {'statename': 'Tunisia', 'group': 'Arab-Amazigh', 'percentage': 98.0, 'from': 2000, 'to': 2021},
            {'statename': 'Tunisia', 'group': 'Others', 'percentage': 2.0, 'from': 2000, 'to': 2021}
        ]
        tunisia_df = pd.DataFrame(tunisia_data)
        df = pd.concat([df, tunisia_df], ignore_index=True)
    
    # FIX: UAE data - ONLY Emiratis vs Foreigners
    if 'UAE' in df['statename'].values:
        df = df[df['statename'] != 'UAE']
        uae_data = [
            {'statename': 'UAE', 'group': 'Emiratis', 'percentage': 11.5, 'from': 2000, 'to': 2021},
            {'statename': 'UAE', 'group': 'Foreigners', 'percentage': 88.5, 'from': 2000, 'to': 2021}
        ]
        uae_df = pd.DataFrame(uae_data)
        df = pd.concat([df, uae_df], ignore_index=True)
    
    return df

df = load_data()

# Streamlit app
st.set_page_config(page_title="MENA Ethnic Diversity", layout="wide")

st.title("🌍 MENA Ethnic Diversity Dashboard")
st.markdown("### Ethnic Composition Across Middle East & North Africa")

# Sidebar
st.sidebar.markdown("## 🧭 Navigation")
year = st.sidebar.slider("**Select Year**", 2000, 2021, 2021)

# Get available countries from dataset
all_countries = sorted(df['statename'].unique())

selected_countries = st.sidebar.multiselect(
    "**Select Countries**", 
    all_countries, 
    default=all_countries
)

# Check data changes by year
st.sidebar.markdown("### Data Changes by Year")
selected_country_check = st.sidebar.selectbox("Check country data:", all_countries)
country_check_data = df[df['statename'] == selected_country_check]

if not country_check_data.empty:
    years_with_data = sorted(country_check_data['to'].unique())
    st.sidebar.write(f"Years with data: {years_with_data}")
    
    # Check if data is identical across years
    if len(years_with_data) > 1:
        first_year = years_with_data[0]
        last_year = years_with_data[-1]
        
        first_data = country_check_data[country_check_data['to'] == first_year].sort_values('group')
        last_data = country_check_data[country_check_data['to'] == last_year].sort_values('group')
        
        if len(first_data) == len(last_data):
            same_data = True
            for (idx1, row1), (idx2, row2) in zip(first_data.iterrows(), last_data.iterrows()):
                if row1['group'] != row2['group'] or abs(row1['percentage'] - row2['percentage']) > 0.1:
                    same_data = False
                    break
            if same_data:
                st.sidebar.warning(f"⚠️ Data identical for {first_year} and {last_year}")
            else:
                st.sidebar.success(f"✅ Data changes between {first_year} and {last_year}")

# 2 tabs only
tab1, tab2 = st.tabs(["🏛️ Country Profile", "👥 Ethnic Group Focus"])

with tab1:
    st.subheader("Country Profile - Ethnic Composition")
    
    country_for_details = st.selectbox(
        "Select Country for Details", 
        all_countries,
        key="country_details"
    )
    
    country_data = df[(df['statename'] == country_for_details) & (df['to'] >= year)]
    
    if not country_data.empty:
        # Show which year's data we're actually displaying
        actual_years = country_data['to'].unique()
        if len(actual_years) == 1:
            st.info(f"Showing data from {actual_years[0]} (selected year: {year})")
        else:
            st.warning(f"Multiple years of data found: {sorted(actual_years)}. Using most recent.")
            # Use most recent year's data
            most_recent_year = max(actual_years)
            country_data = country_data[country_data['to'] == most_recent_year]
        
        fig_pie = px.pie(country_data, 
                        values='percentage', 
                        names='group',
                        title=f"Ethnic Composition of {country_for_details}",
                        color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Ethnic Groups", len(country_data))
        with col2:
            majority_group = country_data.loc[country_data['percentage'].idxmax(), 'group']
            majority_pct = country_data['percentage'].max()
            st.metric("Majority Group", f"{majority_group} ({majority_pct:.1f}%)")
        with col3:
            if len(country_data) > 1:
                diversity = 1 - sum((country_data['percentage']/100)**2)
                st.metric("Diversity Index", f"{diversity:.2f}")
            else:
                st.metric("Diversity Index", "0.00")
                
        st.markdown("#### Detailed Composition")
        display_data = country_data[['group', 'percentage']].sort_values('percentage', ascending=False)
        display_data['percentage'] = display_data['percentage'].round(1)
        st.dataframe(display_data, use_container_width=True)
        
        # Show data availability for this country across years
        st.markdown("#### Data Availability Across Years")
        country_all_years = df[df['statename'] == country_for_details]
        year_counts = country_all_years.groupby('to').size()
        st.write("Records per year:")
        st.dataframe(year_counts.reset_index().rename(columns={0: 'Records', 'to': 'Year'}))

with tab2:
    st.subheader("Ethnic Group Focus - Regional Distribution")
    
    all_ethnic_groups = sorted(df['group'].unique())
    selected_ethnic_group = st.selectbox(
        "Select Ethnic Group for Analysis",
        all_ethnic_groups,
        key="ethnic_analysis"
    )
    
    ethnic_data = df[(df['group'] == selected_ethnic_group) & (df['to'] >= year)]
    
    if not ethnic_data.empty:
        # Use most recent data for each country
        most_recent_data = ethnic_data.loc[ethnic_data.groupby('statename')['to'].idxmax()]
        
        fig_bar = px.bar(most_recent_data.sort_values('percentage', ascending=True),
                        y='statename', x='percentage', orientation='h',
                        title=f"'{selected_ethnic_group}' Distribution Across MENA",
                        color='percentage',
                        color_continuous_scale='Blues')
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Countries Present", most_recent_data['statename'].nunique())
        with col2:
            total_presence = most_recent_data['percentage'].sum()
            st.metric("Total Regional Presence", f"{total_presence:.1f}%")
        with col3:
            max_country = most_recent_data.loc[most_recent_data['percentage'].idxmax(), 'statename']
            max_pct = most_recent_data['percentage'].max()
            st.metric("Largest Population", f"{max_country} ({max_pct:.1f}%)")
            
        st.markdown("#### Country-by-Country Distribution")
        display_ethnic_data = most_recent_data[['statename', 'percentage', 'to']].sort_values('percentage', ascending=False)
        display_ethnic_data['percentage'] = display_ethnic_data['percentage'].round(1)
        st.dataframe(display_ethnic_data, use_container_width=True)
        
    else:
        st.warning(f"No data available for {selected_ethnic_group} in {year}")

# SIMPLE FOOTER
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates")
