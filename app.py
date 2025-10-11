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
    
    # FIX: UAE data - ONLY Emiratis (9.78%) vs Foreigners (90.22%)
    if 'UAE' in df['statename'].values:
        df = df[df['statename'] != 'UAE']
        uae_data = [
            {'statename': 'UAE', 'group': 'Emiratis', 'percentage': 9.78, 'from': 2000, 'to': 2021},
            {'statename': 'UAE', 'group': 'Foreigners', 'percentage': 90.22, 'from': 2000, 'to': 2021}
        ]
        uae_df = pd.DataFrame(uae_data)
        df = pd.concat([df, uae_df], ignore_index=True)
    
    return df

df = load_data()

# Streamlit app
st.set_page_config(page_title="MENA Ethnic Diversity", layout="wide")

st.title("🌍 MENA Ethnic Diversity Dashboard")
st.markdown("### Ethnic Composition Across Middle East & North Africa")

# ACADEMIC FOCUS NOTE
st.info("""
**Academic Focus Note**: This analysis concentrates on **historical ethnic groups and long-standing diversity patterns**. 
Gulf citizen populations are treated as homogeneous national groups for comparative purposes, reflecting their demographic reality.
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

# Calculate diversity for all countries - PROPER CITIZEN FOCUS
country_diversity = []
gulf_citizen_groups = ['Emiratis', 'Saudis', 'Qataris', 'Kuwaitis', 'Omanis', 'Bahrainis']

for country in all_countries:
    country_data = df[(df['statename'] == country) & (df['to'] >= year)]
    if not country_data.empty:
        # Use most recent data for each country
        most_recent_year = country_data['to'].max()
        country_data_recent = country_data[country_data['to'] == most_recent_year]
        
        # For Gulf countries, we consider the citizen population as one homogeneous group
        gulf_countries = ['UAE', 'Saudi Arabia', 'Qatar', 'Kuwait', 'Oman', 'Bahrain']
        if country in gulf_countries:
            # For Gulf countries, diversity is essentially 0 (homogeneous citizenry)
            diversity = 0.0
            majority_percentage = 100.0  # Citizen population is treated as 100% homogeneous
            groups_count = 1
            category = 'Gulf Citizen Population'
            
        else:
            # For non-Gulf countries, calculate actual ethnic diversity
            if len(country_data_recent) > 1:
                diversity = 1 - sum((country_data_recent['percentage']/100)**2)
                majority_percentage = country_data_recent['percentage'].max()
                groups_count = len(country_data_recent)
                
                # Categorize based on actual ethnic diversity
                if majority_percentage > 90:
                    category = 'Highly Homogeneous'
                elif majority_percentage > 70:
                    category = 'Moderately Homogeneous'
                elif majority_percentage > 50:
                    category = 'Moderately Diverse'
                else:
                    category = 'Highly Diverse'
            else:
                diversity = 0.0
                majority_percentage = 100.0
                groups_count = 1
                category = 'Highly Homogeneous'
        
        country_diversity.append({
            'country': country, 
            'diversity': diversity,
            'groups_count': groups_count,
            'majority_percentage': majority_percentage,
            'category': category
        })

if country_diversity:
    # Filter out Gulf countries for "true diversity" insights
    true_diversity_countries = [c for c in country_diversity if c['category'] != 'Gulf Citizen Population']
    
    if true_diversity_countries:
        most_diverse = max(true_diversity_countries, key=lambda x: x['diversity'])
        least_diverse = min(true_diversity_countries, key=lambda x: x['diversity'])
        
        st.sidebar.metric(
            "Most Ethnically Diverse", 
            f"{most_diverse['country']}", 
            f"{most_diverse['diversity']:.3f}"
        )
        st.sidebar.metric(
            "Most Ethnically Homogeneous", 
            f"{least_diverse['country']}", 
            f"{least_diverse['diversity']:.3f}"
        )
    
    # Find most widespread ethnic group (excluding Gulf citizen groups)
    group_distribution = []
    excluded_groups = ['Foreigners', 'Emiratis', 'Saudis', 'Qataris', 'Kuwaitis', 'Omanis', 'Bahrainis']
    for group in df['group'].unique():
        if group not in excluded_groups:
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

# 3 tabs with proper citizen-focused analysis
tab1, tab2, tab3 = st.tabs(["🏛️ Country Profile", "👥 Ethnic Group Focus", "📊 Ethnic Diversity"])

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
        
        # For Gulf countries, add note about citizen focus
        gulf_countries = ['UAE', 'Saudi Arabia', 'Qatar', 'Kuwait', 'Oman', 'Bahrain']
        if country_for_details in gulf_countries:
            st.info(f"**Note**: {country_for_details} shows citizen population composition. Foreign labor populations are excluded from diversity calculations.")
        
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
            # Get the correct diversity score from our calculation
            country_diversity_data = next((c for c in country_diversity if c['country'] == country_for_details), None)
            if country_diversity_data:
                st.metric("Diversity Index", f"{country_diversity_data['diversity']:.3f}")
            else:
                st.metric("Diversity Index", "N/A")
                
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
    st.subheader("Ethnic Diversity Analysis")
    
    st.markdown("""
    ### Historical Ethnic Diversity Analysis
    
    This analysis focuses on **long-standing ethnic diversity patterns** rather than temporary demographic features.
    Gulf citizen populations are treated as homogeneous for comparative purposes, reflecting their demographic reality.
    """)
    
    if country_diversity:
        # Create diversity ranking dataframe
        diversity_df = pd.DataFrame(country_diversity)
        diversity_df = diversity_df.sort_values('diversity', ascending=False)
        diversity_df['diversity'] = diversity_df['diversity'].round(3)
        diversity_df['rank'] = range(1, len(diversity_df) + 1)
        
        # Display the ranking
        st.markdown("#### Ethnic Diversity Ranking")
        st.dataframe(
            diversity_df[['rank', 'country', 'diversity', 'groups_count', 'category']].rename(columns={
                'rank': 'Rank',
                'country': 'Country', 
                'diversity': 'Diversity Index',
                'groups_count': 'Ethnic Groups',
                'category': 'Type'
            }),
            use_container_width=True,
            height=500
        )
        
        # Visualize true ethnic diversity (excluding Gulf as homogeneous)
        st.markdown("---")
        st.markdown("#### Historical Ethnic Diversity Comparison")
        
        fig_diversity = px.bar(
            diversity_df,
            x='diversity', 
            y='country',
            orientation='h',
            title="Ethnic Diversity Across MENA (Gulf as Homogeneous)",
            color='category',
            color_discrete_map={
                'Gulf Citizen Population': '#B0BEC5',  # Gray for homogeneous
                'Highly Homogeneous': '#4ECDC4', 
                'Moderately Homogeneous': '#45B7D1',
                'Moderately Diverse': '#96CEB4',
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
        st.markdown("**Methodological Note**:")
        st.markdown("""
        - **Gulf States**: Treated as ethnically homogeneous citizen populations (diversity = 0)
        - **Other Countries**: Diversity calculated from actual ethnic group distributions
        - **Focus**: Long-standing historical diversity patterns, not temporary demographics
        - **Diversity Index**: 1 - Σ(percentage²) | 0 = homogeneous, 1 = maximum diversity
        """)
        
    else:
        st.warning("No diversity data available for the selected year")

# SIMPLE FOOTER
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates | **Focus**: Historical Ethnic Diversity")
# SIMPLE FOOTER
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates | **Focus**: Citizen Population Analysis")
