import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('mena_ethnicity_enhanced_final.csv')
    
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

# Streamlit app
st.set_page_config(page_title="MENA Ethnic Diversity", layout="wide")

st.title("🌍 MENA Ethnic Diversity Dashboard")
st.markdown("### Ethnic Composition Across Middle East & North Africa")

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
    
    # Find country with most minority groups
    if country_minority_data:
        most_minorities = max(country_minority_data, key=lambda x: x['minority_groups'])
        st.sidebar.metric(
            "Most Minority Groups", 
            f"{most_minorities['country']}", 
            f"{most_minorities['minority_groups']} groups"
        )

# 5 TABS - ADDED MINORITY ANALYSIS TAB
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏛️ Country Profile", "👥 Ethnic Group Focus", "📊 Diversity Analysis", "🔍 Regional Comparisons", "📋 Minority Analysis"])

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
        
        # Create metrics and chart
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Countries Present", most_recent_data['statename'].nunique())
        with col2:
            total_presence = most_recent_data['percentage'].sum()
            st.metric("Total Regional Presence", f"{total_presence:.1f}%")
        with col3:
            max_country = most_recent_data.loc[most_recent_data['percentage'].idxmax(), 'statename']
            max_pct = most_recent_data['percentage'].max()
            st.metric("Largest Population", f"{max_country}")
        with col4:
            avg_presence = most_recent_data['percentage'].mean()
            st.metric("Average Presence", f"{avg_presence:.1f}%")
        
        fig_bar = px.bar(most_recent_data.sort_values('percentage', ascending=True),
                        y='statename', x='percentage', orientation='h',
                        title=f"'{selected_ethnic_group}' Distribution Across MENA",
                        color='percentage',
                        color_continuous_scale='Blues')
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
            
        st.markdown("#### Country-by-Country Distribution")
        display_ethnic_data = most_recent_data[['statename', 'percentage', 'to']].sort_values('percentage', ascending=False)
        display_ethnic_data['percentage'] = display_ethnic_data['percentage'].round(1)
        display_ethnic_data = display_ethnic_data.rename(columns={
            'statename': 'Country', 
            'percentage': 'Percentage',
            'to': 'Data Year'
        })
        st.dataframe(display_ethnic_data, use_container_width=True, hide_index=True)
        
    else:
        st.warning(f"No data available for {selected_ethnic_group}")

with tab3:
    st.subheader("Diversity Analysis")
    
    st.markdown("""
    ### Population Diversity Across MENA
    
    **Note on Kuwait's Diversity**: Kuwait shows high diversity due to its balanced Sunni-Shia citizen composition (70-30 split).
    Countries like Lebanon and Israel have more complex ethnic diversity but different distribution patterns.
    """)
    
    if country_diversity:
        # Create diversity ranking dataframe
        diversity_df = pd.DataFrame(country_diversity)
        diversity_df = diversity_df.sort_values('diversity', ascending=False)
        diversity_df['diversity'] = diversity_df['diversity'].round(3)
        diversity_df['rank'] = range(1, len(diversity_df) + 1)
        
        # Display ranking
        st.markdown("#### Population Diversity Ranking")
        
        # Add explanation for high diversity countries
        st.markdown("""
        **Understanding High Diversity Scores**:
        - **Kuwait**: Balanced religious diversity within citizen population
        - **Lebanon**: Complex multi-ethnic and multi-religious composition  
        - **Israel**: Jewish-Arab diversity with multiple subgroups
        - **Gulf States**: Religious diversity within ethnically Arab populations
        """)
        
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
        
    else:
        st.warning("No diversity data available for the selected year")

with tab4:
    st.subheader("Regional Comparisons")
    
    st.markdown("### Compare Multiple Countries")
    
    # FIX: Only use countries that actually exist in the dataset
    available_for_comparison = [country for country in all_countries if country in ['Lebanon', 'Israel', 'Kuwait', 'United Arab Emirates', 'Iran', 'Egypt', 'Saudi Arabia', 'Palestine']]
    
    # Country comparison selector - FIXED: Only use countries that exist
    compare_countries = st.multiselect(
        "Select countries to compare:",
        all_countries,
        default=available_for_comparison[:3],  # Only use first 3 available countries
        key="compare_countries"
    )
    
    if compare_countries:
        compare_data = df[(df['statename'].isin(compare_countries)) & (df['to'] >= year)]
        if not compare_data.empty:
            # Use most recent data for each country
            compare_recent = compare_data.loc[compare_data.groupby(['statename', 'group'])['to'].idxmax()]
            
            # Grouped bar chart comparison
            fig_compare = px.bar(compare_recent, 
                               x='statename', y='percentage', color='group',
                               title="Ethnic Composition Comparison",
                               barmode='stack',
                               color_discrete_sequence=px.colors.qualitative.Bold)
            st.plotly_chart(fig_compare, use_container_width=True)
            
            # Diversity comparison table
            st.markdown("#### Diversity Metrics Comparison")
            comparison_metrics = []
            for country in compare_countries:
                country_data = compare_recent[compare_recent['statename'] == country]
                if len(country_data) > 1:
                    diversity = 1 - sum((country_data['percentage']/100)**2)
                    majority_pct = country_data['percentage'].max()
                    groups_count = len(country_data)
                    comparison_metrics.append({
                        'Country': country,
                        'Diversity Index': round(diversity, 3),
                        'Majority Group %': round(majority_pct, 1),
                        'Number of Groups': groups_count
                    })
            
            if comparison_metrics:
                comparison_df = pd.DataFrame(comparison_metrics)
                comparison_df = comparison_df.sort_values('Diversity Index', ascending=False)
                st.dataframe(comparison_df, use_container_width=True, hide_index=True)

with tab5:
    st.subheader("Minority Group Analysis")
    
    st.markdown("### Analysis of Minority Populations (<10% of population)")
    
    if country_minority_data:
        minority_df = pd.DataFrame(country_minority_data)
        minority_df = minority_df.sort_values('total_minority_percentage', ascending=False)
        
        # Display minority analysis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Countries with Highest Minority Populations")
            st.dataframe(
                minority_df[['country', 'minority_groups', 'total_minority_percentage', 'largest_minority']].rename(columns={
                    'country': 'Country',
                    'minority_groups': 'Minority Groups',
                    'total_minority_percentage': 'Total Minority %',
                    'largest_minority': 'Largest Minority %'
                }),
                use_container_width=True,
                height=400
            )
        
        with col2:
            st.markdown("#### Minority Group Insights")
            st.markdown("""
            **Key Findings**:
            - Countries with high minority percentages often have complex ethnic histories
            - Large minority populations can indicate historical migration patterns
            - Some countries have many small minority groups rather than few large ones
            - Gulf states show religious minorities within ethnically homogeneous populations
            """)
        
        # Visualize minority distribution
        st.markdown("---")
        st.markdown("#### Total Minority Population by Country")
        
        fig_minority = px.bar(
            minority_df.head(15),
            x='total_minority_percentage', 
            y='country',
            orientation='h',
            title="Total Minority Population Percentage (Groups <10%)",
            color='minority_groups',
            color_continuous_scale='Viridis'
        )
        fig_minority.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_minority, use_container_width=True)


# CLEAN FOOTER
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates | Gulf citizen data based on demographic studies")
