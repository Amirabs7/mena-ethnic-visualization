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
    
    # Ethnic Migration Patterns - FIXED VERSION
    st.subheader("🚶‍♂️ Major Ethnic Displacement Patterns")
    
    migration_data = [
        {'group': 'Palestinians', 'period': '1948-present', 'scale': 6500000, 'scale_label': '6.5M+', 'primary_destinations': ['Jordan', 'Lebanon', 'Syria', 'Gulf States']},
        {'group': 'Syrians', 'period': '2011-present', 'scale': 6800000, 'scale_label': '6.8M', 'primary_destinations': ['Turkey', 'Lebanon', 'Jordan', 'Europe']},
        {'group': 'Iraqis', 'period': '2003-present', 'scale': 9200000, 'scale_label': '9.2M', 'primary_destinations': ['Syria', 'Jordan', 'Iran', 'Europe']},
        {'group': 'Yemenis', 'period': '2014-present', 'scale': 4000000, 'scale_label': '4M', 'primary_destinations': ['Oman', 'Saudi Arabia', 'Djibouti']},
        {'group': 'Kurds', 'period': 'Various', 'scale': 3000000, 'scale_label': '3M+', 'primary_destinations': ['Turkey', 'Iraq', 'Syria', 'Iran', 'Europe']}
    ]
    
    migration_df = pd.DataFrame(migration_data)
    
    # Use bar chart instead of treemap for better compatibility
    fig_migration = px.bar(migration_df.sort_values('scale', ascending=True),
                          x='scale',
                          y='group',
                          orientation='h',
                          title="Major Ethnic Displacement Patterns in MENA",
                          hover_data=['period', 'primary_destinations', 'scale_label'],
                          color='scale',
                          color_continuous_scale='Reds',
                          labels={'scale': 'Estimated Displaced', 'group': 'Ethnic Group'})
    
    fig_migration.update_layout(
        xaxis_title="Estimated Displaced Population",
        yaxis_title="Ethnic Group"
    )
    
    st.plotly_chart(fig_migration, use_container_width=True)
    
    # Display migration data as table
    st.markdown("#### Detailed Migration Patterns")
    migration_display_df = migration_df[['group', 'period', 'scale_label', 'primary_destinations']].copy()
    migration_display_df['primary_destinations'] = migration_display_df['primary_destinations'].apply(lambda x: ', '.join(x))
    migration_display_df = migration_display_df.rename(columns={
        'group': 'Ethnic Group',
        'period': 'Period',
        'scale_label': 'Estimated Displaced',
        'primary_destinations': 'Primary Destinations'
    })
    
    st.dataframe(migration_display_df, use_container_width=True, hide_index=True)
    
    # Methodology note
    st.info("""
    **Data Sources**: Conflict data compiled from UN OCHA, UNHCR, ACLED, and historical records. 
    Current Gaza war statistics from UN and humanitarian organizations (2023-2025). 
    Displacement figures represent estimates of directly conflict-induced migration.
    """)
