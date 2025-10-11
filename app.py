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
for country in all_countries:
    country_data = df[(df['statename'] == country) & (df['to'] >= year)]
    if not country_data.empty:
        # Use most recent data for each country
        most_recent_year = country_data['to'].max()
        country_data_recent = country_data[country_data['to'] == most_recent_year]
        
        if len(country_data_recent) > 1:
            diversity = 1 - sum((country_data_recent['percentage']/100)**2)
            country_diversity.append({
                'country': country, 
                'diversity': diversity,
                'groups_count': len(country_data_recent)
            })

if country_diversity:
    # Find most and least diverse countries
    most_diverse = max(country_diversity, key=lambda x: x['diversity'])
    least_diverse = min(country_diversity, key=lambda x: x['diversity'])
    
    st.sidebar.metric(
        "Most Diverse Country", 
        f"{most_diverse['country']}", 
        f"{most_diverse['diversity']:.3f}"
    )
    st.sidebar.metric(
        "Least Diverse Country", 
        f"{least_diverse['country']}", 
        f"{least_diverse['diversity']:.3f}"
    )

# Find most widespread ethnic group
group_distribution = []
for group in df['group'].unique():
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

# 3 tabs with diversity ranking
tab1, tab2, tab3 = st.tabs(["🏛️ Country Profile", "👥 Ethnic Group Focus", "📊 Diversity Ranking"])

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
        
        fig_pie = px.pie(country_data, 
                        values='percentage', 
                        names='group',
                        title=f"Ethnic Composition of {country_for_details}",
                        color_discrete_sequence=px.colors.qualitative.Set3)
        st.plotly_chart(fig_pie, use_container_width=True)
        
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
    st.subheader("Country Diversity Ranking")
    st.markdown("### Ethnic Diversity Index Across MENA Countries")
    
    if country_diversity:
        # Create diversity ranking dataframe
        diversity_df = pd.DataFrame(country_diversity)
        diversity_df = diversity_df.sort_values('diversity', ascending=False)
        diversity_df['diversity'] = diversity_df['diversity'].round(3)
        diversity_df['rank'] = range(1, len(diversity_df) + 1)
        
        # Display ranking table
        st.dataframe(
            diversity_df[['rank', 'country', 'diversity', 'groups_count']].rename(columns={
                'rank': 'Rank',
                'country': 'Country', 
                'diversity': 'Diversity Index',
                'groups_count': 'Ethnic Groups'
            }),
            use_container_width=True,
            hide_index=True
        )
        
        # Diversity index explanation
        st.markdown("---")
        st.markdown("**About Diversity Index**:")
        st.markdown("""
        - **Range**: 0 (completely homogeneous) to 1 (maximum diversity)
        - **Calculation**: 1 - Σ(percentage²) 
        - Higher values indicate more ethnic diversity
        - Lower values indicate more ethnic homogeneity
        """)
        
        # Visualize diversity ranking
        fig_diversity = px.bar(
            diversity_df.head(15),  # Show top 15 for clarity
            x='diversity', 
            y='country',
            orientation='h',
            title="Top 15 Most Ethnically Diverse Countries",
            color='diversity',
            color_continuous_scale='Viridis'
        )
        fig_diversity.update_layout(yaxis={'categoryorder': 'total ascending'})
        st.plotly_chart(fig_diversity, use_container_width=True)
        
    else:
        st.warning("No diversity data available for the selected year")

# SIMPLE FOOTER
st.markdown("---")
st.markdown("**Data Sources**: EPR Core 2021 + Estimates")
