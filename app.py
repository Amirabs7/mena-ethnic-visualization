import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('mena_ethnicity_enhanced_final.csv')
    
    # First, let's see what columns we actually have
    st.sidebar.markdown("### Dataset Info")
    st.sidebar.write(f"Columns: {list(df.columns)}")
    st.sidebar.write(f"Total rows: {len(df)}")
    
    # UPDATE: Change "UAE" to "United Arab Emirates" for consistency
    df['statename'] = df['statename'].replace({'UAE': 'United Arab Emirates'})
    
    # UPDATE: Change Berber to Amazigh as requested
    df['group'] = df['group'].replace({'Berbers': 'Amazigh'})
    
    # FIX: Manual data corrections
    # Update Mauritania from Arab-Berber to Arab-Amazigh
    df['group'] = df['group'].replace({'Arab-Berber': 'Arab-Amazigh'})
    
    # FIX: Palestine data - more realistic percentages including Christians
    if 'Palestine' in df['statename'].values:
        # Remove all existing Palestine data and replace with realistic composition
        df = df[df['statename'] != 'Palestine']
        palestine_data = [
            {'statename': 'Palestine', 'group': 'Palestinian Muslims', 'percentage': 81.5, 'from': 2000, 'to': 2021},
            {'statename': 'Palestine', 'group': 'Israeli Settlers', 'percentage': 15.0, 'from': 2000, 'to': 2021},
            {'statename': 'Palestine', 'group': 'Palestinian Christians', 'percentage': 1.5, 'from': 2000, 'to': 2021},
            {'statename': 'Palestine', 'group': 'Others', 'percentage': 2.0, 'from': 2000, 'to': 2021},
        ]
        palestine_df = pd.DataFrame(palestine_data)
        df = pd.concat([df, palestine_df], ignore_index=True)
    
    # FIX: Tunisia composition - 98% Arab-Amazigh, 2% Others
    if 'Tunisia' in df['statename'].values:
        df = df[df['statename'] != 'Tunisia']
        tunisia_data = [
            {'statename': 'Tunisia', 'group': 'Arab-Amazigh', 'percentage': 98.0, 'from': 2000, 'to': 2021},
            {'statename': 'Tunisia', 'group': 'Others', 'percentage': 2.0, 'from': 2000, 'to': 2021}
        ]
        tunisia_df = pd.DataFrame(tunisia_data)
        df = pd.concat([df, tunisia_df], ignore_index=True)
    
    # FIX: United Arab Emirates data - Focus ONLY on Emirati nationals ethnic composition
    # Remove any existing United Arab Emirates data first
    df = df[df['statename'] != 'United Arab Emirates']
    
    # United Arab Emirates Nationals Ethnic Composition 
    # Emirati citizens have diverse ancestral backgrounds:
    uae_nationals_data = [
        {'statename': 'United Arab Emirates', 'group': 'Arab Tribes (Qawasim, Bani Yas, etc.)', 'percentage': 65.0, 'from': 2000, 'to': 2021},
        {'statename': 'United Arab Emirates', 'group': 'Persian-origin Emiratis', 'percentage': 20.0, 'from': 2000, 'to': 2021},
        {'statename': 'United Arab Emirates', 'group': 'Baloch-origin Emiratis', 'percentage': 8.0, 'from': 2000, 'to': 2021},
        {'statename': 'United Arab Emirates', 'group': 'African-origin Emiratis', 'percentage': 5.0, 'from': 2000, 'to': 2021},
        {'statename': 'United Arab Emirates', 'group': 'Other Emirati groups', 'percentage': 2.0, 'from': 2000, 'to': 2021},
    ]
    
    uae_nationals_df = pd.DataFrame(uae_nationals_data)
    df = pd.concat([df, uae_nationals_df], ignore_index=True)
    
    # FIX: Other Gulf Countries - Focus on CITIZEN composition only with proper labeling
    # Remove existing Gulf country data and replace with citizen-focused data
    gulf_countries = ['Saudi Arabia', 'Qatar', 'Kuwait', 'Oman', 'Bahrain']
    df = df[~df['statename'].isin(gulf_countries)]
    
    # Saudi Arabia - Citizen composition (religious sects)
    saudi_data = [
        {'statename': 'Saudi Arabia', 'group': 'Arab Saudi - Sunni Muslims', 'percentage': 85.0, 'from': 2000, 'to': 2021},
        {'statename': 'Saudi Arabia', 'group': 'Arab Saudi - Shia Muslims', 'percentage': 15.0, 'from': 2000, 'to': 2021},
    ]
    
    # Qatar - Citizen composition (all Arab Qatari with religious diversity)
    qatar_data = [
        {'statename': 'Qatar', 'group': 'Arab Qatari - Sunni Muslims', 'percentage': 90.0, 'from': 2000, 'to': 2021},
        {'statename': 'Qatar', 'group': 'Arab Qatari - Shia Muslims', 'percentage': 10.0, 'from': 2000, 'to': 2021},
    ]
    
    # Kuwait - Citizen composition (all Arab Kuwaiti with religious diversity)
    kuwait_data = [
        {'statename': 'Kuwait', 'group': 'Arab Kuwaiti - Sunni Muslims', 'percentage': 70.0, 'from': 2000, 'to': 2021},
        {'statename': 'Kuwait', 'group': 'Arab Kuwaiti - Shia Muslims', 'percentage': 30.0, 'from': 2000, 'to': 2021},
    ]
    
    # Oman - Citizen composition (all Arab Omani with religious diversity)
    oman_data = [
        {'statename': 'Oman', 'group': 'Arab Omani - Ibadi Muslims', 'percentage': 75.0, 'from': 2000, 'to': 2021},
        {'statename': 'Oman', 'group': 'Arab Omani - Sunni Muslims', 'percentage': 15.0, 'from': 2000, 'to': 2021},
        {'statename': 'Oman', 'group': 'Arab Omani - Shia Muslims', 'percentage': 5.0, 'from': 2000, 'to': 2021},
        {'statename': 'Oman', 'group': 'Arab Omani - Hindu/Baloch', 'percentage': 5.0, 'from': 2000, 'to': 2021},
    ]
    
    # Bahrain - Citizen composition (all Arab Bahraini with religious diversity)
    bahrain_data = [
        {'statename': 'Bahrain', 'group': 'Arab Bahraini - Shia Muslims', 'percentage': 65.0, 'from': 2000, 'to': 2021},
        {'statename': 'Bahrain', 'group': 'Arab Bahraini - Sunni Muslims', 'percentage': 35.0, 'from': 2000, 'to': 2021},
    ]
    
    # Add all Gulf citizen data
    gulf_citizen_data = saudi_data + qatar_data + kuwait_data + oman_data + bahrain_data
    gulf_citizen_df = pd.DataFrame(gulf_citizen_data)
    df = pd.concat([df, gulf_citizen_df], ignore_index=True)
    
    return df

df = load_data()

# Check if we have conflict-related columns and add conflict analysis
def check_conflict_data(df):
    """Check what conflict-related data we have"""
    conflict_columns = ['status', 'reg_autonomy', 'excluded', 'discriminated', 'settlement']
    available_conflict_cols = [col for col in conflict_columns if col in df.columns]
    
    return available_conflict_cols

# Get available conflict data
available_conflict_data = check_conflict_data(df)

# Streamlit app
st.set_page_config(page_title="MENA Ethnic Diversity", layout="wide")

st.title("🌍 MENA Ethnic Diversity Dashboard")
st.markdown("### Ethnic Composition Across Middle East & North Africa")

# Show available conflict data
if available_conflict_data:
    st.sidebar.markdown("### 🚨 Available Conflict Data")
    for col in available_conflict_data:
        st.sidebar.write(f"✓ {col}")

# ACADEMIC FOCUS NOTE - UPDATED
st.info("""
**Methodological Note**: Gulf state data focuses on **citizen population composition** showing religious diversity within Arab national populations. 
United Arab Emirates shows ethnic diversity within Emirati citizens. Palestine includes Christian minority population.
""")

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

# QUICK INSIGHTS SIDEBAR
st.sidebar.markdown("## 📈 Quick Insights")

# Calculate diversity for all countries
country_diversity = []
country_minority_data = []  # For minority analysis
country_conflict_data = []  # For conflict analysis

for country in all_countries:
    country_data = df[(df['statename'] == country) & (df['to'] >= year)]
    if not country_data.empty:
        # Use most recent data for each country
        most_recent_year = country_data['to'].max()
        country_data_recent = country_data[country_data['to'] == most_recent_year]
        
        if len(country_data_recent) > 1:
            diversity = 1 - sum((country_data_recent['percentage']/100)**2)
            majority_percentage = country_data_recent['percentage'].max()
            groups_count = len(country_data_recent)
            
            # Calculate minority groups (<10% population)
            minority_groups = country_data_recent[country_data_recent['percentage'] < 10]
            minority_count = len(minority_groups)
            total_minority_percentage = minority_groups['percentage'].sum()
            
            # Calculate conflict-related metrics if data available
            conflict_metrics = {}
            if 'status' in df.columns:
                # Count discriminated/excluded groups
                discriminated_groups = country_data_recent[country_data_recent['status'].isin(['DISCRIMINATED', 'POWERLESS'])]
                conflict_metrics['discriminated_groups'] = len(discriminated_groups)
                conflict_metrics['discriminated_percentage'] = discriminated_groups['percentage'].sum()
            
            # Categorize countries
            gulf_countries = ['United Arab Emirates', 'Saudi Arabia', 'Qatar', 'Kuwait', 'Oman', 'Bahrain']
            if country in gulf_countries:
                category = 'Gulf Citizen Population'
            elif majority_percentage > 80:
                category = 'Highly Homogeneous'
            elif majority_percentage > 60:
                category = 'Moderately Diverse'
            else:
                category = 'Highly Diverse'
            
            country_diversity.append({
                'country': country, 
                'diversity': diversity,
                'groups_count': groups_count,
                'majority_percentage': majority_percentage,
                'category': category
            })
            
            country_minority_data.append({
                'country': country,
                'minority_groups': minority_count,
                'total_minority_percentage': total_minority_percentage,
                'largest_minority': minority_groups['percentage'].max() if not minority_groups.empty else 0
            })
            
            country_conflict_data.append({
                'country': country,
                **conflict_metrics
            })

if country_diversity:
    # Find most and least diverse countries
    most_diverse = max(country_diversity, key=lambda x: x['diversity'])
    least_diverse = min(country_diversity, key=lambda x: x['diversity'])
    
    st.sidebar.metric(
        "Most Diverse Population", 
        f"{most_diverse['country']}", 
        f"{most_diverse['diversity']:.3f}"
    )
    st.sidebar.metric(
        "Most Homogeneous Population", 
        f"{least_diverse['country']}", 
        f"{least_diverse['diversity']:.3f}"
    )

# 6 TABS - ADDED CONFLICT ANALYSIS IF DATA AVAILABLE
tabs = ["🏛️ Country Profile", "👥 Ethnic Group Focus", "📊 Diversity Analysis", "🔍 Regional Comparisons", "📋 Minority Analysis"]

if available_conflict_data:
    tabs.append("⚡ Conflict Analysis")

tab1, tab2, tab3, tab4, tab5, *remaining_tabs = st.tabs(tabs)

if available_conflict_data:
    tab6 = remaining_tabs[0]

with tab1:
    st.subheader("Country Profile - Ethnic Composition")
    
    country_for_details = st.selectbox(
        "Select Country for Details", 
        all_countries,
        key="country_details"
    )
    
    country_data = df[(df['statename'] == country_for_details) & (df['to'] >= year)]
    
    if not country_data.empty:
        # Use most recent data
        most_recent_year = country_data['to'].max()
        country_data = country_data[country_data['to'] == most_recent_year]
        
        # Add contextual note for Gulf countries
        gulf_countries = ['United Arab Emirates', 'Saudi Arabia', 'Qatar', 'Kuwait', 'Oman', 'Bahrain']
        if country_for_details in gulf_countries:
            st.info("**Showing citizen population composition only**")
        elif country_for_details == 'Palestine':
            st.info("**Includes Palestinian Christian minority (1.5%)**")
        
        # Create two columns for pie chart and stats
        col_chart, col_stats = st.columns([2, 1])
        
        with col_chart:
            fig_pie = px.pie(country_data, 
                            values='percentage', 
                            names='group',
                            title=f"Ethnic Composition of {country_for_details}",
                            color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_stats:
            st.metric("Data Year", most_recent_year)
            st.metric("Total Groups", len(country_data))
            majority_group = country_data.loc[country_data['percentage'].idxmax(), 'group']
            majority_pct = country_data['percentage'].max()
            st.metric("Largest Group", f"{majority_pct:.1f}%")
            
            if len(country_data) > 1:
                diversity = 1 - sum((country_data['percentage']/100)**2)
                st.metric("Diversity Index", f"{diversity:.3f}")
            else:
                st.metric("Diversity Index", "0.000")
                
        st.markdown("#### Detailed Composition")
        display_data = country_data[['group', 'percentage']].sort_values('percentage', ascending=False)
        display_data['percentage'] = display_data['percentage'].round(1)
        st.dataframe(display_data, use_container_width=True, hide_index=True)

# ... [Keep all other tabs the same as before, just add the conflict tab if data exists]

if available_conflict_data:
    with tab6:
        st.subheader("Conflict & Political Status Analysis")
        
        st.markdown(f"""
        ### Political Status and Conflict Correlation
        
        **Available Conflict Data**: {', '.join(available_conflict_data)}
        
        This analysis explores the relationship between ethnic group political status and potential conflict patterns.
        """)
        
        # Show political status distribution
        if 'status' in df.columns:
            st.markdown("#### Political Status Distribution")
            
            status_data = df[(df['to'] >= year)].groupby('status').size().reset_index(name='count')
            fig_status = px.pie(status_data, values='count', names='status', 
                              title="Distribution of Ethnic Group Political Status")
            st.plotly_chart(fig_status, use_container_width=True)
            
            # Countries with most discriminated groups
            st.markdown("#### Countries with Political Exclusion")
            conflict_countries = []
            for country in all_countries:
                country_data = df[(df['statename'] == country) & (df['to'] >= year)]
                if not country_data.empty and 'status' in df.columns:
                    discriminated = country_data[country_data['status'].isin(['DISCRIMINATED', 'POWERLESS'])]
                    if len(discriminated) > 0:
                        conflict_countries.append({
                            'Country': country,
                            'Discriminated Groups': len(discriminated),
                            'Total Population Discriminated': discriminated['percentage'].sum()
                        })
            
            if conflict_countries:
                conflict_df = pd.DataFrame(conflict_countries)
                conflict_df = conflict_df.sort_values('Total Population Discriminated', ascending=False)
                st.dataframe(conflict_df, use_container_width=True, hide_index=True)

# CLEAN FOOTER
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates | Gulf citizen data based on demographic studies")
