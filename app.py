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
year = st.sidebar.slider("**Select Year**", 1946, 2021, 2021)

# Get available countries from dataset
all_countries = sorted(df['statename'].unique())

# FIX: Include Palestine in default selection
selected_countries = st.sidebar.multiselect(
    "**Select Countries**", 
    all_countries, 
    default=['Egypt', 'Saudi Arabia', 'Israel', 'Morocco', 'Palestine']  # Palestine added
)

# Only 2 clear tabs
tab1, tab2 = st.tabs(["🗺️ Ethnic Map", "📊 Country & Group Analysis"])

with tab1:
    st.subheader("MENA Ethnic Distribution Map")
    
    # Filter data for selected countries and year
    if selected_countries:
        region_data = df[(df['statename'].isin(selected_countries)) & (df['to'] >= year)]
    else:
        region_data = df[df['to'] >= year]
    
    if not region_data.empty:
        # Clean, working map
        fig = px.choropleth(region_data,
                           locations="statename",
                           locationmode="country names",
                           color="group",
                           hover_name="statename",
                           hover_data={"percentage": ":.1f%", "group": True},
                           color_discrete_sequence=px.colors.qualitative.Bold,
                           title=f"Ethnic Groups Distribution - {year}")
        
        # MENA-focused map
        fig.update_geos(
            visible=False,
            projection_type="natural earth",
            lonaxis_range=[-20, 60],
            lataxis_range=[0, 45]
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
    st.subheader("Detailed Analysis")
    
    # Two columns for clear separation
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 🏛️ Country Profile")
        
        if selected_countries:
            country = st.selectbox("Select Country for Details", selected_countries)
            country_data = df[(df['statename'] == country) & (df['to'] >= year)]
            
            if not country_data.empty:
                # Pie chart for country composition
                fig_pie = px.pie(country_data, 
                                values='percentage', 
                                names='group',
                                title=f"Ethnic Composition of {country}",
                                color_discrete_sequence=px.colors.qualitative.Set3)
                st.plotly_chart(fig_pie, use_container_width=True)
                
                # Country stats
                st.metric("Total Ethnic Groups", len(country_data))
                st.metric("Majority Group", f"{country_data['percentage'].max():.1f}%")
                if len(country_data) > 1:
                    diversity = 1 - sum((country_data['percentage']/100)**2)
                    st.metric("Diversity Index", f"{diversity:.2f}")
    
    with col2:
        st.markdown("#### 👥 Ethnic Group Focus")
        
        ethnic_group = st.selectbox("Select Ethnic Group", sorted(df['group'].unique()))
        ethnic_data = df[(df['group'] == ethnic_group) & (df['to'] >= year)]
        
        if not ethnic_data.empty:
            # Horizontal bar chart for group distribution
            fig_bar = px.bar(ethnic_data.sort_values('percentage', ascending=True),
                            y='statename', x='percentage', orientation='h',
                            title=f"'{ethnic_group}' Distribution",
                            color='percentage',
                            color_continuous_scale='Blues')
            st.plotly_chart(fig_bar, use_container_width=True)
            
            # Group stats
            st.metric("Countries Present", ethnic_data['statename'].nunique())
            st.metric("Total Population", f"{ethnic_data['percentage'].sum():.1f}%")
            max_country = ethnic_data.loc[ethnic_data['percentage'].idxmax(), 'statename']
            max_pct = ethnic_data['percentage'].max()
            st.metric("Largest Presence", f"{max_country} ({max_pct:.1f}%)")

# Footer
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates | **Coverage**: 20 countries, 54 ethnic groups, 1946-2021")
