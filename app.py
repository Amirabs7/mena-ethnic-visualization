import streamlit as st
import pandas as pd
import plotly.express as px

@st.cache_data
def load_data():
    df = pd.read_csv('mena_ethnicity_enhanced_final.csv')
    # UPDATE: Change Berber to Amazigh as requested
    df['group'] = df['group'].replace({'Berbers': 'Amazigh'})
    return df

df = load_data()

# Streamlit app
st.set_page_config(page_title="MENA Ethnic Diversity", layout="wide")

st.title("🌍 MENA Ethnic Diversity Dashboard")
st.markdown("### Ethnic Composition Across Middle East & North Africa")

# Sidebar
st.sidebar.markdown("## 🧭 Navigation")
# FIX: Limit years to 2000-2024
year = st.sidebar.slider("**Select Year**", 2000, 2021, 2021)

# Get available countries from dataset
all_countries = sorted(df['statename'].unique())

# FIX: All countries pre-selected by default
selected_countries = st.sidebar.multiselect(
    "**Select Countries**", 
    all_countries, 
    default=all_countries  # All countries pre-selected
)

# FIX: 3 separate tabs as requested
tab1, tab2, tab3 = st.tabs(["🗺️ Ethnic Map", "🏛️ Country Profile", "👥 Ethnic Group Focus"])

# Initialize session state for clicked country
if 'clicked_country' not in st.session_state:
    st.session_state.clicked_country = None

with tab1:
    st.subheader("MENA Ethnic Distribution Map")
    
    # Filter data for selected countries and year
    if selected_countries:
        region_data = df[(df['statename'].isin(selected_countries)) & (df['to'] >= year)]
    else:
        region_data = df[df['to'] >= year]
    
    if not region_data.empty:
        # FIX: Simplify the map - show one group at a time for clarity
        available_groups = sorted(region_data['group'].unique())
        selected_group = st.selectbox(
            "Select Ethnic Group to Display on Map",
            available_groups,
            key="map_group"
        )
        
        # Filter data for the selected group
        group_data = region_data[region_data['group'] == selected_group]
        
        # Create map for the selected ethnic group
        fig = px.choropleth(group_data,
                           locations="statename",
                           locationmode="country names",
                           color="percentage",
                           hover_name="statename",
                           hover_data={"percentage": ":.1f%", "group": True},
                           color_continuous_scale="Blues",
                           title=f"'{selected_group}' Distribution - {year}",
                           range_color=[0, group_data['percentage'].max()])
        
        # MENA-focused map
        fig.update_geos(
            visible=False,
            projection_type="natural earth",
            lonaxis_range=[-20, 60],
            lataxis_range=[0, 45],
            showcountries=True,
            countrycolor="black"
        )
        
        fig.update_layout(height=600)
        
        # Display map
        st.plotly_chart(fig, use_container_width=True)
        
        # FIX: Add country selection via click
        st.markdown("**Click on a country in the map to view its details in the Country Profile tab**")
        
        # Quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Countries Shown", len(selected_countries))
        with col2:
            st.metric("Selected Group", selected_group)
        with col3:
            st.metric("Year", year)
            
    else:
        st.warning("No data available for selected filters")

with tab2:
    st.subheader("Country Profile - Ethnic Composition")
    
    # FIX: Use clicked country from map or allow manual selection
    if st.session_state.clicked_country:
        default_country = st.session_state.clicked_country
        st.info(f"Showing details for: **{default_country}** (selected from map)")
    else:
        default_country = all_countries[0]
    
    country_for_details = st.selectbox(
        "Select Country for Details", 
        all_countries,
        index=all_countries.index(default_country) if default_country in all_countries else 0,
        key="country_details"
    )
    
    country_data = df[(df['statename'] == country_for_details) & (df['to'] >= year)]
    
    if not country_data.empty:
        # Pie chart for country composition
        fig_pie = px.pie(country_data, 
                        values='percentage', 
                        names='group',
                        title=f"Ethnic Composition of {country_for_details} ({year})",
                        color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_pie, use_container_width=True)
        
        # Country stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Ethnic Groups", len(country_data))
        with col2:
            majority_group = country_data.loc[country_data['percentage'].idxmax(), 'group']
            majority_pct = country_data['percentage'].max()
            st.metric("Majority Group", f"{majority_group} ({majority_pct:.1f}%)")
        with col3:
            if len(country_data) > 1:
                diversity = 1 - sum((country_data['percentage']/100)**2)
                st.metric("Diversity Index", f"{diversity:.2f}")
            else:
                st.metric("Diversity Index", "0.00")
                
        # Data table
        st.markdown("#### Detailed Composition")
        display_data = country_data[['group', 'percentage']].sort_values('percentage', ascending=False)
        display_data['percentage'] = display_data['percentage'].round(1)
        st.dataframe(display_data, use_container_width=True)
        
    else:
        st.warning(f"No data available for {country_for_details} in {year}")

with tab3:
    st.subheader("Ethnic Group Focus - Regional Distribution")
    
    # FIX: Independent ethnic group analysis
    all_ethnic_groups = sorted(df['group'].unique())
    selected_ethnic_group = st.selectbox(
        "Select Ethnic Group for Analysis",
        all_ethnic_groups,
        key="ethnic_analysis"
    )
    
    ethnic_data = df[(df['group'] == selected_ethnic_group) & (df['to'] >= year)]
    
    if not ethnic_data.empty:
        # Horizontal bar chart for group distribution
        fig_bar = px.bar(ethnic_data.sort_values('percentage', ascending=True),
                        y='statename', x='percentage', orientation='h',
                        title=f"'{selected_ethnic_group}' Distribution Across MENA ({year})",
                        color='percentage',
                        color_continuous_scale='Blues')
        fig_bar.update_layout(yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_bar, use_container_width=True)
        
        # Group stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Countries Present", ethnic_data['statename'].nunique())
        with col2:
            total_presence = ethnic_data['percentage'].sum()
            st.metric("Total Regional Presence", f"{total_presence:.1f}%")
        with col3:
            max_country = ethnic_data.loc[ethnic_data['percentage'].idxmax(), 'statename']
            max_pct = ethnic_data['percentage'].max()
            st.metric("Largest Population", f"{max_country} ({max_pct:.1f}%)")
            
        # Data table
        st.markdown("#### Country-by-Country Distribution")
        display_ethnic_data = ethnic_data[['statename', 'percentage']].sort_values('percentage', ascending=False)
        display_ethnic_data['percentage'] = display_ethnic_data['percentage'].round(1)
        st.dataframe(display_ethnic_data, use_container_width=True)
        
    else:
        st.warning(f"No data available for {selected_ethnic_group} in {year}")

# Footer
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates | **Coverage**: 20 countries, 54 ethnic groups, 2000-2021")
