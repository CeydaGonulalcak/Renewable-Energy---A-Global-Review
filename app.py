import streamlit as st
import pandas as pd
import plotly.express as px
import altair as alt
import matplotlib.pyplot as plt
import plotly.graph_objs as go
import seaborn as sns
st.set_page_config(page_title='Sales Dashboard',page_icon=':bar_chart:',layout='wide')

df = pd.read_csv('C:/Users/Sedat/Desktop/dashboard/energyy.csv')
df.drop('Unnamed: 0', axis=1,inplace=True)
df_solar=pd.read_csv('C:/Users/Sedat/Desktop/dashboard/energy_solar.csv')
df_solar.drop('Unnamed: 0', axis=1,inplace=True)

# Streamlit uygulamasını başlat
st.title('Renewable Energy Data Visualization')

# Sol sidebar oluştur
st.sidebar.header('Please Choose:')
data_type = st.sidebar.radio("Data Type:", ("Region", "Country"))

if data_type == "Region":
    st.sidebar.subheader("Region Options:")
    selected_option = st.sidebar.selectbox("Graph Options:", ("Production of Worldwide Renewable Energy Consumption 2020", "Regional Changes in Geothermal Capacity from 1990 to 2020"))

    if selected_option == "Production of Worldwide Renewable Energy Consumption 2020":
        # Dünya verisini filtrele
        drop_1 = ['Africa', 'Asia Pacific', 'CIS', 'North America', 'Other Europe', 'Other South & Central America',
                  'South & Central America', 'World']
        # final value creating without regions
        df_region = df[df["Country"].isin(drop_1)]
        df_region = df_region[df_region["Country"].isin(drop_1)]

        # Streamlit uygulamasını başlatın
        st.title('Production of Worldwide Renewable Energy Consumption 2020')

        # Kıta ve ülke seçeneklerini ekleyin
        selected_option = st.radio("Select Option:", ["World"])

        if selected_option == "World":
            # Dünya verisini filtreleyin
            world = df_region[(df_region.Year == 2020) & (df_region.Country == 'World')]
            # Gereksiz sütunları düşürün
            world.drop(['Country', 'Year'], axis=1, inplace=True)
            pie_world = world[
                ['Solar Generation - TWh', 'Wind Generation - TWh', 'Hydro Generation - TWh', 'Geo Biomass Other - TWh']]
            plt.style.use("seaborn-pastel")
            plt.figure(figsize=(3, 3))
            plt.title('Production of Worldwide Renewable Energy Consumption 2020')

            plt.pie(pie_world.iloc[0],
                    labels=['Solar Generation - TWh', 'Wind Generation - TWh', 'Hydro Generation - TWh', 'Geo Biomass Other - TWh'],
                    autopct='%1.1f%%', wedgeprops={'edgecolor': 'black'})
            st.pyplot(plt)
        else:
            # Ülke seçeneği için ilgili kodları buraya ekleyebilirsiniz
            st.write("Select a specific country for the chart.")

    elif selected_option == "Regional Changes in Geothermal Capacity from 1990 to 2020":
        st.title('Regional Changes in Geothermal Capacity from 1990, %')

        # Veriyi filtrele ve yüzde değişikliğini hesapla
        drop_1 = ['Africa', 'Asia Pacific', 'CIS', 'North America', 'Other Europe', 'Other South & Central America',
                  'South & Central America', 'World']
        df_region = df[df["Country"].isin(drop_1)]
        consumption = df_region[df_region['Year'] >= 1990]
        consumption["Geothermal Capacity Change (%)"] = (consumption["Geothermal Capacity"] / consumption["Geothermal Capacity"].sum()) * 100

        # Plotly grafiğini oluştur
        fig = px.bar(consumption,
                     x='Country', y='Geothermal Capacity Change (%)',
                     color='Country',
                     animation_frame='Year',
                     animation_group="Country",
                     labels={'Geothermal Capacity Change (%)': 'Geothermal Capacity change, %'},
                     title='Regional Changes in Geothermal Capacity from 1990 to 2020, %')

        fig.update_layout(showlegend=False)
        fig.add_vrect(x0=11.5, x1=10.5)
        fig.update_xaxes(title_text='Country', title_standoff=0)

        # Streamlit üzerinde grafiği görüntüle
        st.plotly_chart(fig, use_container_width=True)

elif data_type == "Country":
    st.sidebar.subheader("Country Options:")
    selected_option = st.sidebar.selectbox("Graph Options:", ("Energy Source", "Income_group", "Consumption Profiles per Countries", "World Map with Slider"))

    if selected_option == "Energy Source":
        st.title('Energy Source Analysis')

        # Veriyi filtrele
        year_range = df_solar["Year"].isin(range(1990, 2021))
        df_filtered = df_solar[year_range]

        # Altair için veriyi hazırlayın
        renewable_consumption = ["Solar Generation - TWh", "Wind Generation - TWh",
                                 "Hydro Generation - TWh", "Biofuels Production - TWh - Total"]

        # Veriyi uzun formata dönüştürün
        df_long = df_filtered.melt(id_vars=['Year'], value_vars=renewable_consumption, var_name='Energy Source', value_name='Terrawatt Hour')

        # Altair grafiğini oluşturun
        bar_chart = alt.Chart(df_long).mark_bar().encode(
            x=alt.X('Year:N', title='Year'),
            y=alt.Y('sum(Terrawatt Hour):Q', title='Terrawatt Hour'),
            color=alt.Color('Energy Source:N', scale=alt.Scale(scheme='category20'), legend=alt.Legend(title='Energy Source'))
        ).properties(
            width=alt.Step(30),
        )

        # Streamlit üzerinde grafiği görüntüleyin
        st.altair_chart(bar_chart, use_container_width=True)

    elif selected_option == "Income_group":
        st.title('Income Group Analysis')

        # Eksik verileri doldur (Solar (% electricity) sütunu için)
        df_solar['Solar (% electricity)'] = df_solar['Solar (% electricity)'].fillna(0)

        # Ekonomi sınıflarını tanımla
        economies = ['High income',
                     'Upper middle income',
                     'Lower middle income',
                     'Low income']

        # Belirtilen ekonomi sınıflarına ait verileri filtrele
        df_economy = df_solar[df_solar['Income_group'].isin(economies)]
        df_economy = df_economy[df_economy['Year'] > 1990]

        # Hedef değişkenlerin listesini tanımla
        targets = ['Wind (% electricity)', 'Renewables (% electricity)', 'Hydro (% electricity)', 'Solar (% electricity)']

        # Zaman serisi grafiğini oluştur
        def plot_timeseries(df):
            fig, axes = plt.subplots(2, 2, figsize=(18, 10))

            sns.lineplot(ax=axes[0, 0], data=df, x="Year", y=targets[0], hue="Income_group").set(title=targets[0])

            sns.lineplot(ax=axes[0, 1], data=df, x="Year", y=targets[1], hue="Income_group").set(title=targets[1])

            sns.lineplot(ax=axes[1, 0], data=df, x="Year", y=targets[2], hue="Income_group").set(title=targets[2])

            sns.lineplot(ax=axes[1, 1], data=df, x="Year", y=targets[3], hue="Income_group").set(title=targets[3])

            st.pyplot(fig)

        # Zaman serisi grafiğini görüntüle
        st.subheader('Time Series Analysis')
        plot_timeseries(df_economy)

    elif selected_option == "Consumption Profiles per Countries":
        st.title('Consumption Profiles per Countries')

        # Veriyi işleyin
        consumptionpersource = df_solar[df_solar['Year'] >= 2000]
        consumptionpersource['year'] = pd.to_datetime(consumptionpersource['Year'], format='%Y')
        consumptionpersource['year'] = consumptionpersource['year'].dt.year

        # Plotly grafiğini oluşturun
        fig = px.bar(consumptionpersource,
                     x="Country",
                     y=["Solar Generation - TWh",
                        "Wind Generation - TWh",
                        "Hydro Generation - TWh",
                        "Biofuels Production - TWh - Total"],
                     title="Consumption Profiles per Countries",
                     color_discrete_map={
                         'Solar Generation - TWh': 'black',
                         'Wind Generation - TWh': '#eeee00',
                         'Hydro Generation - TWh': "#B8860B",
                         'Biofuels Production - TWh - Total': "#0000FF",
                     },
                     animation_frame="year",
                     animation_group="Country")

        # X ekseni altındaki metni özelleştirme
        fig.update_xaxes(title_text='Country', title_standoff=0)

        # Streamlit üzerinde grafiği görüntüle
        st.plotly_chart(fig, use_container_width=True)

    elif selected_option == "World Map with Slider":
        st.title('World Map with Slider')

        # Seçilebilecek sütun adları
        column_names = ['Renewables (% electricity)', 'Solar Generation - TWh', 'Wind Generation - TWh',
                        'Hydro Generation - TWh', 'Biofuels Production - TWh - Total']

        # Kullanıcıdan sütun seçimini alın
        selected_column = st.selectbox('Select a Column:', column_names)

        # Function to plot features on world map
        def plot_world_map(column_name):
            fig = go.Figure()
            for year in range(2000, 2021):
                # Filter the data for the current year
                filtered_df = df_solar[df_solar['Year'] == year]

                # Create a choropleth trace for the current year
                trace = go.Choropleth(
                    locations=filtered_df['Country'],
                    z=filtered_df[column_name],
                    locationmode='country names',
                    colorscale='Jet',
                    colorbar=dict(title=column_name),
                    zmin=df_solar[column_name].min(),
                    zmax=df_solar[column_name].max(),
                    visible=False
                )

                # Add the trace to the figure
                fig.add_trace(trace)

            # Set the first trace to visible
            fig.data[0].visible = True

            # Create animation steps
            steps = []
            for i in range(len(fig.data)):
                step = dict(
                    method='update',
                    args=[{'visible': [False] * len(fig.data)},
                          {'title_text': f'{column_name} Map - {2000 + i}', 'frame': {'duration': 1000, 'redraw': True}}],
                    label=str(2000 + i)
                )
                step['args'][0]['visible'][i] = True
                steps.append(step)

            # Create the slider
            sliders = [dict(
                active=0,
                steps=steps,
                currentvalue={"prefix": "Year: ", "font": {"size": 14}},  # Increase font size for slider label
            )]

            fig.update_layout(
                title_text=f'{column_name} Map with Slider',
                title_font_size=24,
                title_x=0.5,
                geo=dict(
                    showframe=True,
                    showcoastlines=True,
                    projection_type='robinson'
                ),
                sliders=sliders,
                height=500,
                width=1000,
                font=dict(family='Arial', size=12),
                margin=dict(t=80, l=50, r=50, b=50),
                template='plotly_dark',
            )

            # Show the figure
            st.plotly_chart(fig, use_container_width=True)

        # Seçilen sütuna göre haritayı çiz
        plot_world_map(selected_column)

