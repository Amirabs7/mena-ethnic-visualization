import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    return pd.read_csv('mena_ethnicity_enhanced_final.csv')

df = load_data()

# Streamlit app
st.set_page_config(page_title="MENA Ethnic Mosaic", layout="wide")

st.title("🗺️ MENA Ethnic Mosaic")
st.markdown("### Satellite View of Ethnic Groups in the Middle East & North Africa")

# Sidebar
st.sidebar.markdown("## 🧭 MENA Navigation")
year = st.sidebar.slider("**Select Year**", 1946, 2021, 2021)

# MENA regions - ISRAEL ADDED TO MASHRIQ
subregions = {
    'Maghreb': ['Morocco', 'Algeria', 'Tunisia', 'Libya', 'Mauritania'],
    'Mashriq': ['Egypt', 'Sudan', 'Jordan', 'Lebanon', 'Syria', 'Iraq', 'Palestine', 'Israel'],
    'Gulf States': ['Saudi Arabia', 'Yemen', 'Oman', 'UAE', 'Qatar', 'Kuwait', 'Bahrain'],
    'All MENA': list(df['statename'].unique())
}

selected_region = st.sidebar.selectbox("**MENA Sub-Region**", list(subregions.keys()))
selected_countries = subregions[selected_region]

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["🌍 Satellite Map", "🏛️ Country Profile", "📜 Historical Trends", "🎯 Ethnic Focus"])

with tab1:
    st.subheader("MENA Ethnic Geography - Satellite View")
    region_data = df[(df['statename'].isin(selected_countries)) & (df['to'] >= year)]
    
    # Enhanced colors for historical years
    if year == 1946:
        colors = px.colors.sequential.Viridis
        title = f"🛰️ 1946 Post-WWII - {selected_region}"
    elif year == 1990:
        colors = px.colors.sequential.Plasma
        title = f"🛰️ 1990 Pre-Gulf War - {selected_region}"
    elif year == 2021:
        colors = px.colors.sequential.Inferno
        title = f"🛰️ 2021 Current - {selected_region}"
    else:
        colors = px.colors.qualitative.Set3
        title = f"🛰️ {year} - {selected_region}"
    
    # Create the map - SIMPLE & WORKING SATELLITE
    if not region_data.empty:
        fig = px.choropleth(region_data,
                           locations="statename",
                           locationmode="country names",
                           color="group",
                           scope="asia",
                           hover_name="statename",
                           hover_data={"percentage": ":.1f%", "group": True},
                           color_discrete_sequence=colors,
                           title=title)
        
        # WORKING SATELLITE STYLE - NO BLACK BACKGROUND
        fig.update_geos(
            visible=True,
            showcountries=True,
            countrycolor="white",
            countrywidth=0.5,
            showcoastlines=True,
            coastlinecolor="cyan",
            showocean=True,
            oceancolor="rgba(0, 100, 200, 0.3)",
            showlakes=True,
            lakecolor="blue",
            projection_type="natural earth",
            landcolor="lightgray",
            bgcolor='rgba(173, 216, 230, 0.1)',  # Light blue, not black
            lonaxis_range=[-20, 60],
            lataxis_range=[0, 45]
        )
        
        fig.update_layout(
            height=600,
            paper_bgcolor='white',  # White background
            plot_bgcolor='white',
            font=dict(color='black', size=12),
            title_font_color='black',
            margin=dict(l=0, r=0, t=50, b=0)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    # Historical context
    if year == 1946:
        st.info("🌍 **1946 Context**: Post-World War II, colonial borders being redrawn")
    elif year == 1990:
        st.info("🌍 **1990 Context**: Pre-Gulf War, major regional shifts upcoming")
    elif year == 2021:
        st.info("🌍 **2021 Context**: Current ethnic distributions with modern borders")
    
    # Regional summary
    if not region_data.empty:
        st.subheader(f"📊 {selected_region} Summary - {year}")
        cols = st.columns(4)
        
        with cols[0]:
            dominant_groups = region_data.loc[region_data.groupby('statename')['percentage'].idxmax()]
            top_group = dominant_groups['group'].value_counts().index[0]
            st.metric("🏆 Dominant Group", top_group)
        
        with cols[1]:
            unique_groups = region_data['group'].nunique()
            st.metric("🎭 Ethnic Groups", unique_groups)
        
        with cols[2]:
            total_countries = region_data['statename'].nunique()
            st.metric("🗺️ Countries", total_countries)
        
        with cols[3]:
            avg_diversity = region_data.groupby('statename')['group'].nunique().mean()
            st.metric("📈 Diversity Score", f"{avg_diversity:.1f}")

with tab2:
    st.subheader("Country Ethnic Profile")
    selected_country = st.selectbox("Select Country", sorted(selected_countries))
    country_data = df[(df['statename'] == selected_country) & (df['to'] >= year)]
    
    if not country_data.empty:
        col1, col2 = st.columns([2, 1])
        with col1:
            # Use bar chart instead of treemap for better performance
            fig_bar = px.bar(country_data.sort_values('percentage', ascending=False),
                           x='group', y='percentage',
                           title=f"Ethnic Composition of {selected_country}",
                           color='group')
            fig_bar.update_traces(texttemplate='%{y:.1f}%', textposition='outside')
            fig_bar.update_layout(xaxis_tickangle=45)
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.metric("Total Groups", len(country_data))
            st.metric("Largest Group", f"{country_data['percentage'].max():.1f}%")
            diversity = 1 - sum((country_data['percentage']/100)**2)
            st.metric("Diversity Index", f"{diversity:.3f}")

with tab3:
    st.subheader("Ethnic Evolution (1946-2021)")
    timeline_country = st.selectbox("Select Country for Timeline", sorted(df['statename'].unique()))
    timeline_data = df[df['statename'] == timeline_country]
    
    if not timeline_data.empty:
        fig_timeline = px.area(timeline_data, x='from', y='percentage', color='group',
                             title=f"Ethnic Composition Evolution in {timeline_country}")
        st.plotly_chart(fig_timeline, use_container_width=True)

with tab4:
    st.subheader("Ethnic Group Spotlight")
    selected_ethnicity = st.selectbox("Select Ethnic Group", sorted(df['group'].unique()))
    ethnic_data = df[(df['group'] == selected_ethnicity) & (df['to'] >= year)]
    
    if not ethnic_data.empty:
        col1, col2 = st.columns(2)
        with col1:
            fig_bar = px.bar(ethnic_data.sort_values('percentage', ascending=False),
                           x='statename', y='percentage',
                           title=f"'{selected_ethnicity}' Population by Country")
            fig_bar.update_layout(xaxis_tickangle=-45)
            st.plotly_chart(fig_bar, use_container_width=True)
        with col2:
            st.metric("Countries Present", ethnic_data['statename'].nunique())
            st.metric("Total Population", f"{ethnic_data['percentage'].sum():.1f}%")
            st.metric("Largest Presence", 
                     f"{ethnic_data.loc[ethnic_data['percentage'].idxmax(), 'statename']} "
                     f"({ethnic_data['percentage'].max():.1f}%)")

# Footer
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates for Yemen, Mauritania, Sudan | **Coverage**: 20 countries, 54 ethnic groups, 1946-2021")
