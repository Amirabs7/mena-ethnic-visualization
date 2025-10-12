import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('mena_ethnicity_enhanced_final.csv')
    
    # REMOVE "United Arab Emirates" and keep only "UAE"
    df = df[df['statename'] != 'United Arab Emirates']
    
    # UPDATE: Change Berber to Amazigh as requested
    df['group'] = df['group'].replace({'Berbers': 'Amazigh'})
    
    # FIX: Manual data corrections
    # Update Mauritania from Arab-Berber to Arab-Amazigh
    df['group'] = df['group'].replace({'Arab-Berber': 'Arab-Amazigh'})
    
    # FIX: Palestine data - realistic percentages
    if 'Palestine' in df['statename'].values:
        # Remove all existing Palestine data and replace with realistic composition
        df = df[df['statename'] != 'Palestine']
        palestine_data = [
            {'statename': 'Palestine', 'group': 'Palestinian Arabs', 'percentage': 83.0, 'from': 2000, 'to': 2021},
            {'statename': 'Palestine', 'group': 'Israeli Settlers', 'percentage': 15.0, 'from': 2000, 'to': 2021},
            {'statename': 'Palestine', 'group': 'Others', 'percentage': 2.0, 'from': 2000, 'to': 2021}
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
    
    # FIX: UAE data - Apply Gulf logic with realistic percentages
    # Remove any existing UAE data first
    df = df[df['statename'] != 'UAE']
    
    # Add comprehensive UAE data
    uae_data = [
        # 2021 Data
        {'statename': 'UAE', 'group': 'Emiratis', 'percentage': 11.5, 'from': 2021, 'to': 2021},
        {'statename': 'UAE', 'group': 'South Asians', 'percentage': 59.0, 'from': 2021, 'to': 2021},
        {'statename': 'UAE', 'group': 'Other Arabs', 'percentage': 12.0, 'from': 2021, 'to': 2021},
        {'statename': 'UAE', 'group': 'East Asians', 'percentage': 8.0, 'from': 2021, 'to': 2021},
        {'statename': 'UAE', 'group': 'Westerners', 'percentage': 5.0, 'from': 2021, 'to': 2021},
        {'statename': 'UAE', 'group': 'Others', 'percentage': 4.5, 'from': 2021, 'to': 2021},
    ]
    
    uae_df = pd.DataFrame(uae_data)
    df = pd.concat([df, uae_df], ignore_index=True)
    
    # FIX: Other Gulf Countries - Focus on CITIZEN composition only
    # Remove existing Gulf country data and replace with citizen-focused data
    gulf_countries = ['Saudi Arabia', 'Qatar', 'Kuwait', 'Oman', 'Bahrain']
    df = df[~df['statename'].isin(gulf_countries)]
    
    # Saudi Arabia - Citizen composition (religious sects)
    saudi_data = [
        {'statename': 'Saudi Arabia', 'group': 'Sunni Muslims', 'percentage': 85.0, 'from': 2000, 'to': 2021},
        {'statename': 'Saudi Arabia', 'group': 'Shia Muslims', 'percentage': 15.0, 'from': 2000, 'to': 2021},
    ]
    
    # Qatar - Citizen composition
    qatar_data = [
        {'statename': 'Qatar', 'group': 'Sunni Muslims', 'percentage': 90.0, 'from': 2000, 'to': 2021},
        {'statename': 'Qatar', 'group': 'Shia Muslims', 'percentage': 10.0, 'from': 2000, 'to': 2021},
    ]
    
    # Kuwait - Citizen composition (religious sects and Bedouin/Arab groups)
    kuwait_data = [
        {'statename': 'Kuwait', 'group': 'Sunni Muslims', 'percentage': 70.0, 'from': 2000, 'to': 2021},
        {'statename': 'Kuwait', 'group': 'Shia Muslims', 'percentage': 30.0, 'from': 2000, 'to': 2021},
    ]
    
    # Oman - Citizen composition (Ibadi Islam majority)
    oman_data = [
        {'statename': 'Oman', 'group': 'Ibadi Muslims', 'percentage': 75.0, 'from': 2000, 'to': 2021},
        {'statename': 'Oman', 'group': 'Sunni Muslims', 'percentage': 15.0, 'from': 2000, 'to': 2021},
        {'statename': 'Oman', 'group': 'Shia Muslims', 'percentage': 5.0, 'from': 2000, 'to': 2021},
        {'statename': 'Oman', 'group': 'Hindu/Baloch', 'percentage': 5.0, 'from': 2000, 'to': 2021},
    ]
    
    # Bahrain - Citizen composition (Sunni/Shia divide)
    bahrain_data = [
        {'statename': 'Bahrain', 'group': 'Shia Muslims', 'percentage': 65.0, 'from': 2000, 'to': 2021},
        {'statename': 'Bahrain', 'group': 'Sunni Muslims', 'percentage': 35.0, 'from': 2000, 'to': 2021},
    ]
    
    # Add all Gulf citizen data
    gulf_citizen_data = saudi_data + qatar_data + kuwait_data + oman_data + bahrain_data
    gulf_citizen_df = pd.DataFrame(gulf_citizen_data)
    df = pd.concat([df, gulf_citizen_df], ignore_index=True)
    
    return df

df = load_data()

# Streamlit app
st.set_page_config(page_title="MENA Ethnic Diversity", layout="wide")

st.title("🌍 MENA Ethnic Diversity Dashboard")
st.markdown("### Ethnic Composition Across Middle East & North Africa")

# ACADEMIC FOCUS NOTE - UPDATED
st.info("""
**Methodological Note**: Gulf state data focuses on **citizen population composition** (religious/ethnic groups among nationals). 
Total population figures including foreign residents are shown separately for UAE. This approach provides meaningful 
comparisons of historical and demographic patterns across the region.
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
            
            # Categorize countries
            gulf_countries = ['UAE', 'Saudi Arabia', 'Qatar', 'Kuwait', 'Oman', 'Bahrain']
            if country in gulf_countries:
                if country == 'UAE':
                    category = 'Gulf Total Population'
                else:
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
    
    # Find most widespread ethnic group
    group_distribution = []
    for group in df['group'].unique():
        group_data = df[(df['group'] == group) & (df['to'] >= year)]
        if not group_data.empty:
            countries_with_group = group_data['statename'].nunique()
            total_presence = group_data['percentage'].sum()
            group_distribution.append({
                'group': group, 
                'countries': countries_with_group,
                'total_presence': total_presence
            })

    if group_distribution:
        most_widespread = max(group_distribution, key=lambda x: x['countries'])
        st.sidebar.metric(
            "Most Widespread Group", 
            f"{most_widespread['group']}", 
            f"{most_widespread['countries']} countries"
        )

# 3 tabs
tab1, tab2, tab3 = st.tabs(["🏛️ Country Profile", "👥 Ethnic Group Focus", "📊 Diversity Analysis"])

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
        
        # Add contextual notes for Gulf countries
        gulf_countries = ['Saudi Arabia', 'Qatar', 'Kuwait', 'Oman', 'Bahrain']
        if country_for_details in gulf_countries:
            st.info(f"**Showing citizen population composition for {country_for_details}**")
        elif country_for_details == 'UAE':
            st.info(f"**Showing total population composition for {country_for_details} (includes foreign residents)**")
        
        fig_pie = px.pie(country_data, 
                        values='percentage', 
                        names='group',
                        title=f"Ethnic Composition of {country_for_details}",
                        color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Groups", len(country_data))
        with col2:
            majority_group = country_data.loc[country_data['percentage'].idxmax(), 'group']
            majority_pct = country_data['percentage'].max()
            st.metric("Largest Group", f"{majority_group} ({majority_pct:.1f}%)")
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
        st.warning(f"No data available for {selected_ethnic_group}")

with tab3:
    st.subheader("Diversity Analysis")
    
    st.markdown("""
    ### Population Diversity Across MENA
    
    Diversity analysis distinguishes between Gulf citizen populations and total population compositions
    to provide meaningful comparisons of historical ethnic and religious diversity patterns.
    """)
    
    if country_diversity:
        # Create diversity ranking dataframe
        diversity_df = pd.DataFrame(country_diversity)
        diversity_df = diversity_df.sort_values('diversity', ascending=False)
        diversity_df['diversity'] = diversity_df['diversity'].round(3)
        diversity_df['rank'] = range(1, len(diversity_df) + 1)
        
        # Display ranking
        st.markdown("#### Population Diversity Ranking")
        st.dataframe(
            diversity_df[['rank', 'country', 'diversity', 'groups_count', 'category']].rename(columns={
                'rank': 'Rank',
                'country': 'Country', 
                'diversity': 'Diversity Index',
                'groups_count': 'Groups',
                'category': 'Population Type'
            }),
            use_container_width=True,
            height=500
        )
        
        # Visualize diversity
        st.markdown("---")
        st.markdown("#### Diversity Index Comparison")
        
        fig_diversity = px.bar(
            diversity_df,
            x='diversity', 
            y='country',
            orientation='h',
            title="Population Diversity Across MENA Countries",
            color='category',
            color_discrete_map={
                'Gulf Total Population': '#FFA726',
                'Gulf Citizen Population': '#4ECDC4',
                'Highly Homogeneous': '#B0BEC5', 
                'Moderately Diverse': '#45B7D1',
                'Highly Diverse': '#2E7D32'
            }
        )
        fig_diversity.update_layout(
            yaxis={'categoryorder': 'total ascending'},
            height=600
        )
        st.plotly_chart(fig_diversity, use_container_width=True)
        
        # Explanation
        st.markdown("---")
        st.markdown("**Methodological Notes**:")
        st.markdown("""
        - **Gulf Citizen Populations**: Show religious/ethnic composition among nationals only
        - **UAE**: Shows total population including foreign residents (for comparison)
        - **Other Countries**: Based on total population ethnic composition
        - **Diversity Index**: 1 - Σ(percentage²) | Range: 0 (homogeneous) to 1 (diverse)
        - **Interpretation**: Higher values indicate more diverse populations
        """)
        
    else:
        st.warning("No diversity data available for the selected year")

# CLEAN FOOTER
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates | Gulf citizen data based on demographic studies")
