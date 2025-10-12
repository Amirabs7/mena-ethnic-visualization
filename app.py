# ADD THIS TO YOUR TABS SECTION (replace the current 4 tabs with 5 tabs)
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🏛️ Country Profile", "👥 Ethnic Group Focus", "📊 Diversity Analysis", "🔍 Regional Comparisons", "⚔️ Conflict & Migration"])

# ... keep all your existing tab1-tab4 code exactly as is ...

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
