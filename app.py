import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('mena_ethnicity_enhanced_final.csv')
    # FIX: Update Mauritania terminology
    df['group'] = df['group'].replace({
        'Arab-Berber': 'Arab-Amazigh',
        'Berbers': 'Amazigh'
    })
    return df

df = load_data()

# Streamlit app
st.set_page_config(page_title="MENA Ethnic Diversity", layout="wide")

st.title("🌍 MENA Ethnic Diversity Dashboard")
st.markdown("### Ethnic Composition Across Middle East & North Africa")

# Sidebar
st.sidebar.markdown("## 🧭 Navigation")
year = st.sidebar.slider("**Select Year**", 1946, 2021, 2021)

# Simple country selector - NO REGIONS
all_countries = sorted(df['statename'].unique())
selected_countries = st.sidebar.multiselect(
    "**Select Countries**", 
    all_countries, 
    default=['Egypt', 'Saudi Arabia', 'Israel', 'Morocco', 'Iran']
)

# Single tab for simplicity
tab1, tab2, tab3 = st.tabs(["🗺️ Ethnic Map", "📊 Country Analysis", "📈 Group Analysis"])

with tab1:
    st.subheader("MENA Ethnic Distribution Map")
    
    # Filter data for selected countries and year
    if selected_countries:
        region_data = df[(df['statename'].isin(selected_countries)) & (df['to'] >= year)]
    else:
        region_data = df[df['to'] >= year]
    
    if not region_data.empty:
        # SIMPLE WORKING MAP - no complex satellite styling
        fig = px.choropleth(region_data,
                           locations="statename",
                           locationmode="country names",
                           color="group",
                           hover_name="statename",
                           hover_data={"percentage": ":.1f%", "group": True},
                           color_discrete_sequence=px.colors.qualitative.Bold,
                           title=f"Ethnic Groups Distribution - {year}")
        
        # Clean, working map settings
        fig.update_geos(
            visible=False,
            projection_type="natural earth",
            lonaxis_range=[-20, 60],  # MENA focus
            lataxis_range=[0, 45]     # MENA focus
        )
        
        fig.update_layout(height=600)
        st.plotly_chart(fig, use_container_width=True)
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Countries", region_data['statename'].nunique())
        with col2:
            st.metric("Ethnic Groups", region_data['group'].nunique())
        with col3:
            st.metric("Year", year)
    else:
        st.warning("No data available for selected filters")

with tab2:
    st.subheader("Country Ethnic Composition")
    
    if selected_countries:
        for country in selected_countries:
            country_data = df[(df['statename'] == country) & (df['to'] >= year)]
            
            if not country_data.empty:
                st.markdown(f"#### {country}")
                
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    # Horizontal bar chart for better readability
                    fig = px.bar(country_data.sort_values('percentage', ascending=True),
                                y='group', x='percentage', orientation='h',
                                title=f"Ethnic Groups in {country}",
                                color='percentage',
                                color_continuous_scale='Viridis')
                    st.plotly_chart(fig, use_container_width=True)
                
                with col2:
                    st.metric("Groups", len(country_data))
                    st.metric("Largest", f"{country_data['percentage'].max():.1f}%")
                    if len(country_data) > 1:
                        diversity = 1 - sum((country_data['percentage']/100)**2)
                        st.metric("Diversity", f"{diversity:.2f}")
                
                st.markdown("---")

with tab3:
    st.subheader("Ethnic Group Analysis")
    
    # Working timeline for specific country
    st.markdown("#### Ethnic Evolution Over Time")
    timeline_country = st.selectbox("Select Country for Timeline", sorted(df['statename'].unique()))
    
    country_timeline = df[df['statename'] == timeline_country]
    
    if not country_timeline.empty:
        # Group by decade for cleaner timeline
        country_timeline['decade'] = (country_timeline['from'] // 10) * 10
        decade_avg = country_timeline.groupby(['decade', 'group'])['percentage'].mean().reset_index()
        
        fig = px.line(decade_avg, 
                     x='decade', y='percentage', color='group',
                     title=f"Ethnic Composition in {timeline_country} (by decade)",
                     markers=True)
        st.plotly_chart(fig, use_container_width=True)
    
    # Ethnic group distribution
    st.markdown("#### Ethnic Group Distribution")
    selected_ethnicity = st.selectbox("Select Ethnic Group", sorted(df['group'].unique()))
    ethnic_data = df[(df['group'] == selected_ethnicity) & (df['to'] >= year)]
    
    if not ethnic_data.empty:
        fig = px.bar(ethnic_data.sort_values('percentage', ascending=True),
                    y='statename', x='percentage', orientation='h',
                    title=f"'{selected_ethnicity}' Population Distribution",
                    color='percentage',
                    color_continuous_scale='Blues')
        st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates | **Coverage**: 20 countries, 54 ethnic groups, 1946-2021")
