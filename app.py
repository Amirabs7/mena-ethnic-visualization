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
    
    # Bahrain - Citizen composition (all Arab Bahraini with religious diversity) - FIXED LABELS
    bahrain_data = [
        {'statename': 'Bahrain', 'group': 'Arab Bahraini - Shia Muslims', 'percentage': 65.0, 'from': 2000, 'to': 2021},
        {'statename': 'Bahrain', 'group': 'Arab Bahraini - Sunni Muslims', 'percentage': 35.0, 'from': 2000, 'to': 2021},
    ]
    
    # Add all Gulf citizen data
    gulf_citizen_data = saudi_data + qatar_data + kuwait_data + oman_data + bahrain_data
    gulf_citizen_df = pd.DataFrame(gulf_citizen_data)
    df = pd.concat([df, gulf_citizen_df], ignore_index=True)
    
    # FIX: Jordan - Update "Christians" to "Arab Christians"
    df['group'] = df['group'].replace({'Christians': 'Arab Christians'})
    
    return df

df = load_data()

# Streamlit app
st.set_page_config(page_title="MENA Ethnic Diversity", layout="wide")

st.title("🌍 MENA Ethnic Diversity Dashboard")
st.markdown("### Ethnic Composition Across Middle East & North Africa")

# ACADEMIC FOCUS NOTE - UPDATED
st.info("""
**Methodological Note**: Gulf state data focuses on **citizen population composition** showing religious diversity within Arab national populations. 
United Arab Emirates shows ethnic diversity within Emirati citizens. This approach provides meaningful comparisons of demographic patterns.
""")

# Sidebar
st.sidebar.markdown("## 🧭 Navigation")

# Get available countries from dataset
all_countries = sorted(df['statename'].unique())

selected_countries = st.sidebar.multiselect(
    "**Select Countries**", 
    all_countries, 
    default=all_countries
)

# QUICK INSIGHTS SIDEBAR
st.sidebar.markdown("## 📈 Quick Insights")

# Calculate diversity for all countries (using 2021 data only)
country_diversity = []
for country in all_countries:
    country_data = df[(df['statename'] == country) & (df['to'] == 2021)]  # Fixed to 2021 only
    if not country_data.empty:
        # Use most recent data for each country
        country_data_recent = country_data
        
        if len(country_data_recent) > 1:
            diversity = 1 - sum((country_data_recent['percentage']/100)**2)
            majority_percentage = country_data_recent['percentage'].max()
            groups_count = len(country_data_recent)
            
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
        group_data = df[(df['group'] == group) & (df['to'] == 2021)]  # Fixed to 2021 only
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

# 5 TABS - ADDED NEW CONFLICT TAB
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏛️ Country Profile", "👥 Ethnic Group Focus", "📊 Diversity Analysis", "🔍 Regional Comparisons", "⚔️ Conflict & Migration"])

with tab1:
    st.subheader("Country Profile - Ethnic Composition")
    
    country_for_details = st.selectbox(
        "Select Country for Details", 
        all_countries,
        key="country_details"
    )
    
    country_data = df[(df['statename'] == country_for_details) & (df['to'] == 2021)]  # Fixed to 2021 only
    
    if not country_data.empty:
        # Use most recent data
        country_data_recent = country_data
        
        # Add contextual note for Gulf countries
        gulf_countries = ['United Arab Emirates', 'Saudi Arabia', 'Qatar', 'Kuwait', 'Oman', 'Bahrain']
        if country_for_details in gulf_countries:
            st.info("**Showing citizen population composition only**")
        
        # Create two columns for pie chart and stats
        col_chart, col_stats = st.columns([2, 1])
        
        with col_chart:
            fig_pie = px.pie(country_data_recent, 
                            values='percentage', 
                            names='group',
                            title=f"Ethnic Composition of {country_for_details} (2021)",
                            color_discrete_sequence=px.colors.qualitative.Set3)
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col_stats:
            st.metric("Data Year", "2021")
            st.metric("Total Groups", len(country_data_recent))
            majority_group = country_data_recent.loc[country_data_recent['percentage'].idxmax(), 'group']
            majority_pct = country_data_recent['percentage'].max()
            st.metric("Largest Group", f"{majority_pct:.1f}%")
            
            if len(country_data_recent) > 1:
                diversity = 1 - sum((country_data_recent['percentage']/100)**2)
                st.metric("Diversity Index", f"{diversity:.3f}")
            else:
                st.metric("Diversity Index", "0.000")
                
        st.markdown("#### Detailed Composition")
        display_data = country_data_recent[['group', 'percentage']].sort_values('percentage', ascending=False)
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
    
    ethnic_data = df[(df['group'] == selected_ethnic_group) & (df['to'] == 2021)]  # Fixed to 2021 only
    
    if not ethnic_data.empty:
        # Use most recent data for each country
        most_recent_data = ethnic_data
        
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
                        title=f"'{selected_ethnic_group}' Distribution Across MENA (2021)",
                        color='percentage',
                        color_continuous_scale='Blues')
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
            
        st.markdown("#### Country-by-Country Distribution")
        display_ethnic_data = most_recent_data[['statename', 'percentage']].sort_values('percentage', ascending=False)
        display_ethnic_data['percentage'] = display_ethnic_data['percentage'].round(1)
        display_ethnic_data = display_ethnic_data.rename(columns={
            'statename': 'Country', 
            'percentage': 'Percentage'
        })
        st.dataframe(display_ethnic_data, use_container_width=True, hide_index=True)
        
    else:
        st.warning(f"No data available for {selected_ethnic_group}")

with tab3:
    st.subheader("Diversity Analysis")
    
    st.markdown("""
    ### Population Diversity Across MENA (2021 Data)
    
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
            title="Population Diversity Across MENA Countries (2021)",
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
        
        # Explanation
        st.markdown("---")
        st.markdown("**Methodological Notes**:")
        st.markdown("""
        - **United Arab Emirates**: Shows ethnic diversity within Emirati citizens
        - **Other Gulf States**: Show religious diversity within Arab citizen populations
        - **Non-Gulf Countries**: Based on total population ethnic composition
        - **Diversity Index**: 1 - Σ(percentage²) | Range: 0 (homogeneous) to 1 (diverse)
        - **Kuwait's high score**: Reflects balanced Sunni (70%) - Shia (30%) citizen distribution
        """)
        
    else:
        st.warning("No diversity data available")

with tab4:
    st.subheader("Regional Comparisons")
    
    st.markdown("### Compare Multiple Countries (2021 Data)")
    
    # FIX: Only use countries that actually exist in the dataset
    available_for_comparison = [country for country in all_countries if country in ['Lebanon', 'Israel', 'Kuwait', 'United Arab Emirates', 'Iran', 'Egypt', 'Saudi Arabia']]
    
    # Country comparison selector - FIXED: Only use countries that exist
    compare_countries = st.multiselect(
        "Select countries to compare:",
        all_countries,
        default=available_for_comparison[:3],  # Only use first 3 available countries
        key="compare_countries"
    )
    
    if compare_countries:
        compare_data = df[(df['statename'].isin(compare_countries)) & (df['to'] == 2021)]  # Fixed to 2021 only
        if not compare_data.empty:
            # Use most recent data for each country
            compare_recent = compare_data
            
            # Grouped bar chart comparison
            fig_compare = px.bar(compare_recent, 
                               x='statename', y='percentage', color='group',
                               title="Ethnic Composition Comparison (2021)",
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
    st.header("⚔️ Conflict & Migration Patterns (1967-Present)")
    
    st.markdown("""
    ### How Major Conflicts Shaped MENA's Ethnic Landscape
    
    Understanding contemporary ethnic distributions requires looking at the forced migrations 
    and displacements caused by decades of conflict.
    """)

    # Enhanced conflict data with detailed casualty information
    conflicts_data = [
        # Israeli-Palestinian conflicts since 1967 with detailed casualty data
        {
            'year': 1967, 'name': 'Six-Day War', 'duration': 6, 'impact': 'Very High', 
            'countries': ['Israel', 'Palestine', 'Egypt', 'Syria', 'Jordan'], 
            'displaced': 300000, 'type': 'Interstate War',
            'casualties': '~20,000 total', 'description': 'Israel captures West Bank, Gaza, Golan Heights, Sinai'
        },
        {
            'year': 1973, 'name': 'Yom Kippur War', 'duration': 19, 'impact': 'Very High', 
            'countries': ['Israel', 'Egypt', 'Syria'], 
            'displaced': 100000, 'type': 'Interstate War',
            'casualties': '~15,000 total', 'description': 'Egypt and Syria launch surprise attack on Israel'
        },
        {
            'year': 1982, 'name': 'First Lebanon War', 'duration': 105, 'impact': 'Very High', 
            'countries': ['Israel', 'Lebanon', 'Syria'], 
            'displaced': 600000, 'type': 'Interstate War',
            'casualties': '~20,000 total', 'description': 'Israel invades Lebanon to remove PLO'
        },
        {
            'year': 1987, 'name': 'First Intifada', 'duration': 1825, 'impact': 'High', 
            'countries': ['Israel', 'Palestine'], 
            'displaced': 150000, 'type': 'Uprising',
            'casualties': '~2,000 total', 'description': 'Palestinian uprising against Israeli occupation'
        },
        {
            'year': 2000, 'name': 'Second Intifada', 'duration': 1825, 'impact': 'Very High', 
            'countries': ['Israel', 'Palestine'], 
            'displaced': 350000, 'type': 'Uprising',
            'casualties': '~4,000 total', 'description': 'Violent Palestinian uprising following failed peace talks'
        },
        {
            'year': 2006, 'name': 'Second Lebanon War', 'duration': 34, 'impact': 'High', 
            'countries': ['Israel', 'Lebanon'], 
            'displaced': 1000000, 'type': 'Interstate War',
            'casualties': '~1,500 total', 'description': 'Hezbollah cross-border raid triggers war with Israel'
        },
        {
            'year': 2008, 'name': 'Gaza War (Cast Lead)', 'duration': 22, 'impact': 'High', 
            'countries': ['Israel', 'Palestine'], 
            'displaced': 150000, 'type': 'Military Operation',
            'casualties': '~1,400 total', 'description': 'Israeli operation against Hamas in Gaza'
        },
        {
            'year': 2012, 'name': 'Operation Pillar of Defense', 'duration': 8, 'impact': 'Medium', 
            'countries': ['Israel', 'Palestine'], 
            'displaced': 75000, 'type': 'Military Operation',
            'casualties': '~170 total', 'description': 'Israeli operation against Hamas military targets'
        },
        {
            'year': 2014, 'name': 'Gaza War (Protective Edge)', 'duration': 50, 'impact': 'Very High', 
            'countries': ['Israel', 'Palestine'], 
            'displaced': 500000, 'type': 'Military Operation',
            'casualties': '~2,200 total', 'description': 'Major conflict following Hamas rocket attacks'
        },
        {
            'year': 2021, 'name': 'Gaza Conflict (May 2021)', 'duration': 11, 'impact': 'High', 
            'countries': ['Israel', 'Palestine'], 
            'displaced': 75000, 'type': 'Military Operation',
            'casualties': '~260 total', 'description': 'Conflict sparked by tensions in Jerusalem'
        },
        {
            'year': 2023, 'name': 'Israel-Hamas War (2023-2025)', 'duration': 800, 'impact': 'Catastrophic', 
            'countries': ['Israel', 'Palestine'], 
            'displaced': 1900000, 'type': 'War',
            'casualties': '85,530+ total', 'description': 'Ongoing war following Hamas October 7 attacks'
        },
        
        # Other regional conflicts
        {
            'year': 1975, 'name': 'Lebanese Civil War', 'duration': 5475, 'impact': 'Very High', 
            'countries': ['Lebanon'], 
            'displaced': 900000, 'type': 'Civil War',
            'casualties': '~150,000 total', 'description': 'Sectarian conflict with regional involvement'
        },
        {
            'year': 1980, 'name': 'Iran-Iraq War', 'duration': 2887, 'impact': 'Very High', 
            'countries': ['Iran', 'Iraq'], 
            'displaced': 2500000, 'type': 'Interstate War',
            'casualties': '~1,000,000 total', 'description': 'Longest conventional war of 20th century'
        },
        {
            'year': 1990, 'name': 'Gulf War', 'duration': 43, 'impact': 'High', 
            'countries': ['Iraq', 'Kuwait', 'Saudi Arabia'], 
            'displaced': 5000000, 'type': 'Interstate War',
            'casualties': '~50,000 total', 'description': 'Coalition forces liberate Kuwait from Iraq'
        },
        {
            'year': 2003, 'name': 'Iraq War', 'duration': 3180, 'impact': 'Very High', 
            'countries': ['Iraq'], 
            'displaced': 9200000, 'type': 'Interstate War',
            'casualties': '~300,000 total', 'description': 'US-led invasion and subsequent insurgency'
        },
        {
            'year': 2011, 'name': 'Syrian Civil War', 'duration': 4800, 'impact': 'Very High', 
            'countries': ['Syria'], 
            'displaced': 13000000, 'type': 'Civil War',
            'casualties': '~600,000 total', 'description': 'Ongoing multi-sided civil war'
        },
        {
            'year': 2014, 'name': 'Yemeni Civil War', 'duration': 3285, 'impact': 'Very High', 
            'countries': ['Yemen'], 
            'displaced': 4000000, 'type': 'Civil War',
            'casualties': '~377,000 total', 'description': 'Civil war with Saudi-led intervention'
        }
    ]
    
    conflicts_df = pd.DataFrame(conflicts_data)
    
    # Create an interactive timeline with enhanced visualization
    st.subheader("📅 Major Conflicts Timeline (1967-Present)")
    
    # Color mapping for impact levels
    impact_colors = {
        'Catastrophic': '#8B0000',
        'Very High': '#FF0000', 
        'High': '#FF4500',
        'Medium': '#FFA500',
        'Low': '#FFD700'
    }
    
    # Create a bubble chart timeline
    fig_timeline = px.scatter(conflicts_df, 
                             x='year', 
                             y='impact',
                             size='displaced',
                             color='impact',
                             color_discrete_map=impact_colors,
                             hover_name='name',
                             hover_data={
                                 'duration': True, 
                                 'displaced': ':,', 
                                 'casualties': True,
                                 'year': False,
                                 'impact': False
                             },
                             size_max=40,
                             title="MENA Conflicts Timeline: Impact & Scale (1967-Present)",
                             labels={'impact': 'Conflict Impact', 'year': 'Year'})
    
    fig_timeline.update_layout(
        yaxis={'categoryorder': 'array', 'categoryarray': ['Low', 'Medium', 'High', 'Very High', 'Catastrophic']},
        xaxis={'title': 'Year', 'tickvals': list(range(1965, 2030, 5))},
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Current Gaza War Detailed Analysis
    st.markdown("---")
    st.subheader("🎯 Current Conflict: Israel-Hamas War (2023-2025)")
    
    col1, col2, col3 = st.columns([1, 1, 1])
    
    with col1:
        st.metric("Total Reported Killed", "85,530+", "Ongoing")
        st.metric("Duration", "800+ days", "Since Oct 7, 2023")
        st.metric("Displaced", "1.9M+", "Gaza Population")
    
    with col2:
        st.metric("Gaza Strip Deaths", "77,467+", "67,967 killed + 9,500 missing")
        st.metric("West Bank Deaths", "1,000+", "Ongoing violence")
        st.metric("Wounded", "170,179+", "Gaza Strip")
    
    with col3:
        st.metric("Israeli Deaths", "2,084+", "1,005 civilians + 1,079 security forces")
        st.metric("Israeli Wounded", "13,500+", "Civilians and soldiers")
        st.metric("Detained/Abducted", "12,000+", "Palestinians detained")
    
    # Conflict details in expandable sections
    st.subheader("📊 Conflict Details")
    
    selected_conflict = st.selectbox(
        "Select conflict for detailed analysis:",
        sorted([f"{c['year']}: {c['name']}" for c in conflicts_data], reverse=True),
        key="conflict_selector"
    )
    
    # Find the selected conflict
    selected_year = int(selected_conflict.split(":")[0])
    selected_conflict_data = next((c for c in conflicts_data if c['year'] == selected_year), None)
    
    if selected_conflict_data:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"**{selected_conflict_data['name']} ({selected_conflict_data['year']})**")
            st.write(f"**Type:** {selected_conflict_data['type']}")
            st.write(f"**Duration:** {selected_conflict_data['duration']} days")
            st.write(f"**Description:** {selected_conflict_data['description']}")
            
        with col2:
            st.metric("Impact Level", selected_conflict_data['impact'])
            st.metric("Displaced", f"{selected_conflict_data['displaced']:,}")
            st.metric("Casualties", selected_conflict_data['casualties'])
    
    # Conflict frequency analysis
    st.subheader("📈 Conflict Frequency Analysis")
    
    # Calculate conflicts per decade
    decades = []
    for year in range(1960, 2030, 10):
        decade_conflicts = [c for c in conflicts_data if year <= c['year'] < year + 10]
        decades.append({
            'Decade': f"{year}s",
            'Conflicts': len(decade_conflicts),
            'Total Displaced': sum([c['displaced'] for c in decade_conflicts]),
            'Major Conflicts': len([c for c in decade_conflicts if c['impact'] in ['Very High', 'Catastrophic']])
        })
    
    decades_df = pd.DataFrame(decades)
    
    fig_decades = px.bar(decades_df, 
                        x='Decade', 
                        y='Conflicts',
                        title="MENA Conflicts by Decade",
                        color='Total Displaced',
                        color_continuous_scale='Reds')
    
    st.plotly_chart(fig_decades, use_container_width=True)
    
    # Israeli-Palestinian conflict focus
    st.subheader("🇮🇱🇵🇸 Israeli-Palestinian Conflict Analysis")
    
    ip_conflicts = [c for c in conflicts_data if 'Israel' in c['countries'] and 'Palestine' in c['countries']]
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Conflicts", len(ip_conflicts))
    
    with col2:
        total_ip_displaced = sum([c['displaced'] for c in ip_conflicts])
        st.metric("Total Displaced", f"{total_ip_displaced:,}")
    
    with col3:
        total_ip_casualties = "100,000+"
        st.metric("Estimated Casualties", total_ip_casualties)
    
    with col4:
        years_span = 2025 - 1967
        st.metric("Years of Conflict", f"{years_span}+")
    
    # Ethnic Migration Patterns
    st.subheader("🚶‍♂️ Major Ethnic Displacement Patterns")
    
    migration_data = [
        {'group': 'Palestinians', 'period': '1948-present', 'scale': '6.5M+', 'primary_destinations': ['Jordan', 'Lebanon', 'Syria', 'Gulf States']},
        {'group': 'Syrians', 'period': '2011-present', 'scale': '6.8M', 'primary_destinations': ['Turkey', 'Lebanon', 'Jordan', 'Europe']},
        {'group': 'Iraqis', 'period': '2003-present', 'scale': '9.2M', 'primary_destinations': ['Syria', 'Jordan', 'Iran', 'Europe']},
        {'group': 'Yemenis', 'period': '2014-present', 'scale': '4M', 'primary_destinations': ['Oman', 'Saudi Arabia', 'Djibouti']},
        {'group': 'Kurds', 'period': 'Various', 'scale': '3M+', 'primary_destinations': ['Turkey', 'Iraq', 'Syria', 'Iran', 'Europe']}
    ]
    
    migration_df = pd.DataFrame(migration_data)
    
    fig_migration = px.treemap(migration_df, 
                              path=['group'], 
                              values='scale',
                              title="Ethnic Displacement Scale in MENA",
                              color='scale',
                              color_continuous_scale='Reds')
    
    st.plotly_chart(fig_migration, use_container_width=True)
    
    # Methodology note
    st.info("""
    **Data Sources**: Conflict data compiled from UN OCHA, UNHCR, ACLED, and historical records. 
    Current Gaza war statistics from UN and humanitarian organizations (2023-2025). 
    Displacement figures represent estimates of directly conflict-induced migration.
    """)

# CLEAN FOOTER
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates | Gulf citizen data based on demographic studies")
