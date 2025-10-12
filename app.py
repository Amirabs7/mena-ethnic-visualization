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
    
    # Enhanced conflict data with duration and impact scale
    conflicts_data = [
        {'year': 1967, 'name': 'Six-Day War', 'duration': 6, 'impact': 'High', 'countries': ['Israel', 'Palestine', 'Egypt', 'Syria', 'Jordan'], 'displaced': 300000},
        {'year': 1973, 'name': 'Yom Kippur War', 'duration': 19, 'impact': 'Medium', 'countries': ['Israel', 'Egypt', 'Syria'], 'displaced': 100000},
        {'year': 1975, 'name': 'Lebanese Civil War', 'duration': 5475, 'impact': 'Very High', 'countries': ['Lebanon'], 'displaced': 900000},
        {'year': 1980, 'name': 'Iran-Iraq War', 'duration': 2887, 'impact': 'Very High', 'countries': ['Iran', 'Iraq'], 'displaced': 2500000},
        {'year': 1990, 'name': 'Gulf War', 'duration': 43, 'impact': 'High', 'countries': ['Iraq', 'Kuwait', 'Saudi Arabia'], 'displaced': 5000000},
        {'year': 2003, 'name': 'Iraq War', 'duration': 3180, 'impact': 'Very High', 'countries': ['Iraq'], 'displaced': 9200000},
        {'year': 2011, 'name': 'Syrian Civil War', 'duration': 4800, 'impact': 'Very High', 'countries': ['Syria'], 'displaced': 13000000},
        {'year': 2014, 'name': 'Yemeni Civil War', 'duration': 3285, 'impact': 'Very High', 'countries': ['Yemen'], 'displaced': 4000000}
    ]
    
    conflicts_df = pd.DataFrame(conflicts_data)
    
    # Create timeline visualization
    st.subheader("Major Conflicts Timeline")
    
    # Color mapping for impact levels
    impact_colors = {
        'Very High': '#8B0000',
        'High': '#FF4500', 
        'Medium': '#FFA500',
        'Low': '#FFD700'
    }
    
    fig_timeline = px.scatter(conflicts_df, 
                             x='year', 
                             y=[1]*len(conflicts_df),
                             size='displaced',
                             color='impact',
                             color_discrete_map=impact_colors,
                             hover_name='name',
                             hover_data={'duration': True, 'displaced': ':,', 'countries': True, 'year': False},
                             size_max=30,
                             title="MENA Conflicts Timeline & Impact Scale (1967-Present)")
    
    fig_timeline.update_layout(
        yaxis={'visible': False, 'range': [0.5, 1.5]},
        xaxis={'title': 'Year', 'tickvals': list(range(1965, 2025, 5))},
        height=400,
        showlegend=True
    )
    
    # Add duration as line segments
    for _, conflict in conflicts_df.iterrows():
        fig_timeline.add_shape(
            type="line",
            x0=conflict['year'],
            y0=0.9,
            x1=conflict['year'] + (conflict['duration'] / 365),
            y1=0.9,
            line=dict(color=impact_colors[conflict['impact']], width=2)
        )
    
    st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Conflict details by country
    st.subheader("Conflict Impact by Country")
    
    # Create country-conflict matrix
    all_conflict_countries = list(set([country for conflict in conflicts_data for country in conflict['countries']]))
    country_conflicts = []
    
    for country in all_conflict_countries:
        country_wars = [conflict['name'] for conflict in conflicts_data if country in conflict['countries']]
        country_displaced = sum([conflict['displaced'] for conflict in conflicts_data if country in conflict['countries']])
        country_conflicts.append({
            'Country': country,
            'Conflicts': ', '.join(country_wars),
            'Total Conflicts': len(country_wars),
            'Estimated Displaced': f"{country_displaced:,}"
        })
    
    country_conflicts_df = pd.DataFrame(country_conflicts).sort_values('Total Conflicts', ascending=False)
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.dataframe(country_conflicts_df, use_container_width=True, hide_index=True)
    
    with col2:
        st.metric("Total Conflicts Tracked", len(conflicts_data))
        total_displaced = sum(conflict['displaced'] for conflict in conflicts_data)
        st.metric("Total Estimated Displaced", f"{total_displaced:,}")
        st.metric("Countries Affected", len(all_conflict_countries))
    
    # Ethnic Migration Patterns with enhanced visualization
    st.subheader("Ethnic Migration Patterns")
    
    migration_patterns = [
        {'group': 'Palestinians', 'period': '1948-present', 'scale': '6.5M+', 'primary_destinations': ['Jordan', 'Lebanon', 'Syria', 'Gulf States']},
        {'group': 'Kurds', 'period': 'Various', 'scale': '3M+', 'primary_destinations': ['Turkey', 'Iraq', 'Syria', 'Iran', 'Europe']},
        {'group': 'Syrians', 'period': '2011-present', 'scale': '6.8M', 'primary_destinations': ['Turkey', 'Lebanon', 'Jordan', 'Europe']},
        {'group': 'Iraqis', 'period': '2003-present', 'scale': '9.2M', 'primary_destinations': ['Syria', 'Jordan', 'Iran', 'Europe']},
        {'group': 'Yemenis', 'period': '2014-present', 'scale': '4M', 'primary_destinations': ['Oman', 'Saudi Arabia', 'Djibouti']},
        {'group': 'Lebanese', 'period': '1975-1990', 'scale': '900K', 'primary_destinations': ['Europe', 'Americas', 'Africa']}
    ]
    
    migration_df = pd.DataFrame(migration_patterns)
    
    fig_migration = px.bar(migration_df.sort_values('scale', ascending=True),
                          x='scale',
                          y='group',
                          orientation='h',
                          title="Major Ethnic Displacement Patterns",
                          hover_data=['period', 'primary_destinations'],
                          color='scale',
                          color_continuous_scale='Reds')
    
    fig_migration.update_layout(
        xaxis_title="Estimated Displaced Population",
        yaxis_title="Ethnic Group"
    )
    
    st.plotly_chart(fig_migration, use_container_width=True)
    
    # Interactive country-selector for conflict details
    st.subheader("Conflict Impact on Specific Countries")
    
    selected_country_conflict = st.selectbox(
        "Select country to view conflict history:",
        sorted(all_conflict_countries),
        key="country_conflict"
    )
    
    country_specific_conflicts = [conflict for conflict in conflicts_data if selected_country_conflict in conflict['countries']]
    
    if country_specific_conflicts:
        st.write(f"**{selected_country_conflict} was involved in {len(country_specific_conflicts)} major conflicts:**")
        
        for conflict in country_specific_conflicts:
            with st.expander(f"{conflict['year']}: {conflict['name']}"):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.metric("Duration", f"{conflict['duration']} days")
                with col2:
                    st.metric("Impact Level", conflict['impact'])
                with col3:
                    st.metric("Displaced", f"{conflict['displaced']:,}")
                
                st.write(f"**Other affected countries:** {', '.join([c for c in conflict['countries'] if c != selected_country_conflict])}")
    
    # Methodology note
    st.info("""
    **Methodology Note**: This dashboard shows 2021 demographic data. Conflict and displacement estimates are based on 
    historical records and UNHCR data. The visualization demonstrates how decades of conflict have shaped current 
    ethnic distributions across the MENA region.
    """)

# CLEAN FOOTER
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates | Gulf citizen data based on demographic studies")
