import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pydeck as pdk
from sqlalchemy import create_engine

db_user = 'postgres'
db_password = 'postgres'
db_host = 'localhost'
db_port = '5432'
db_name = 'airbnb'

class StreamlitApp:
    def __init__(self):
        self.df = self.fetch_data()

    def fetch_data(self):
        """Fetch the data from the db"""
        try:
            engine = create_engine(f'postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}')
            query = "SELECT * FROM airbnb;"
            df = pd.read_sql_query(query, engine)
        except Exception as e:
            st.error(f"Error fetching data: {e}")
            df = pd.DataFrame()
        return df

    def plot_room_type_distribution(self, df):
        room_type_counts = df['room_type'].value_counts().reset_index()
        room_type_counts.columns = ['room_type', 'count']
        
        fig = px.sunburst(room_type_counts, path=['room_type'], values='count',
                          title='Room Type Distribution')
        return fig

    def plot_price_vs_reviews(self, df):
        fig = px.scatter(df, x='number_of_reviews', y='price', color='property_type', 
                         size='review_scores_rating', hover_data=['name'],
                         title='Price vs Number of Reviews',
                         labels={'number_of_reviews': 'Number of Reviews', 'price': 'Price'},
                         log_x=True, log_y=True)
        
        fig.update_layout(xaxis_title='Number of Reviews (log scale)', 
                          yaxis_title='Price (log scale)')
        return fig

    def plot_price_heatmap(self, df):
        pivot = df.pivot_table(values='price', index='property_type', columns='room_type', aggfunc='mean')
        fig = px.imshow(pivot, text_auto=True, aspect="auto",
                        title="Average Price Heatmap by Property Type and Room Type")
        fig.update_xaxes(title="Room Type")
        fig.update_yaxes(title="Property Type")
        return fig

    def plot_radar_chart(self, df, hotel_name):
        if hotel_name not in df['name'].values:
            return go.Figure()  # Return empty figure if hotel not found

        hotel = df[df['name'] == hotel_name].iloc[0]
        categories = ['price', 'number_of_reviews', 'review_scores_rating']
        values = [hotel[cat] for cat in categories]
        
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=values + [values[0]],  # Closing the circle
            theta=categories + [categories[0]],  # Closing the circle
            fill='toself'
        ))

        fig.update_layout(polar=dict(
            radialaxis=dict(visible=True)
        ), title=f"Review Metrics for {hotel_name}")
        
        return fig

    def plot_advanced_map(self, df, map_style='light'):
        df = df[['latitude', 'longitude', 'price', 'name', 'number_of_reviews', 'review_scores_rating']]
        
        layer = pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position=['longitude', 'latitude'],
            get_fill_color='[200, 30, 0, 160]',
            get_radius='price / 10',
            radius_min_pixels=1,
            radius_max_pixels=100,
            pickable=True,
            auto_highlight=True
        )
        
        view = pdk.ViewState(
            latitude=df['latitude'].mean(),
            longitude=df['longitude'].mean(),
            zoom=11,
            pitch=0
        )
        
        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view,
            map_style=map_style,
            tooltip={
                'text': '{name}\nPrice: ${price}\nReviews: {number_of_reviews}\nRating: {review_scores_rating}'
            }
        )
        
        return deck

    def plot_price_distribution_by_property(self, df):
        fig = px.histogram(df, x='price', color='property_type', nbins=50,
                           title='Price Distribution by Property Type',
                           labels={'price': 'Price'})
        return fig

    def plot_review_score_distribution(self, df):
        fig = px.histogram(df, x='review_scores_rating', nbins=20,
                           title='Distribution of Review Scores',
                           labels={'review_scores_rating': 'Review Scores Rating'})
        return fig

    def plot_price_vs_review_scores(self, df):
        fig = px.scatter(df, x='review_scores_rating', y='price', color='property_type',
                         size='number_of_reviews', hover_data=['name'],
                         title='Price vs Review Scores',
                         labels={'review_scores_rating': 'Review Scores Rating', 'price': 'Price'})
        return fig

    def plot_cancellation_policy_distribution(self, df):
        # Count the number of hotels for each cancellation policy
        cancellation_policy_counts = df['cancellation_policy'].value_counts().reset_index()
        cancellation_policy_counts.columns = ['cancellation_policy', 'number_of_hotels']

        fig = px.bar(cancellation_policy_counts, x='cancellation_policy', y='number_of_hotels',
                     title='Number of Hotels by Cancellation Policy',
                     labels={'cancellation_policy': 'Cancellation Policy', 'number_of_hotels': 'Number of Hotels'})
        return fig

    def plot_availability_vs_hotels(self, df):
        # Create a new DataFrame to aggregate the number of hotels by availability
        availability_columns = ['availability_30', 'availability_60', 'availability_90', 'availability_365']
        availability_dfs = [df[['country'] + [col]].groupby(col).size().reset_index(name='number_of_hotels') for col in
                            availability_columns]

        fig = go.Figure()

        for availability_df, availability_col in zip(availability_dfs, availability_columns):
            fig.add_trace(go.Scatter(
                x=availability_df[availability_col],
                y=availability_df['number_of_hotels'],
                mode='lines+markers',
                hovertemplate='Availability: %{x}<br>' +
                              'Number of Hotels: %{y}<br>' +
                              '<extra></extra>',
                name=availability_col
            ))

        fig.update_layout(
            title='Availability vs Number of Hotels',
            xaxis_title='Availability (Days)',
            yaxis_title='Number of Hotels'
        )

        return fig

    def apply_filters(df, filters):
        for key, (min_val, max_val) in filters.items():
            if key in df.columns:
                df = df[(df[key] >= min_val) & (df[key] <= max_val)]
        return df

    def home_page(self):
        st.title("Airbnb Overview")

        # Introduction Section
        st.header("Introduction")
        st.write("""
        Airbnb, founded in 2008, is a global online marketplace that connects people seeking accommodations with hosts offering their properties. 
        It revolutionizes the travel and hospitality industry by providing a platform where travelers can find unique, cost-effective, and 
        often personalized lodging options that go beyond traditional hotels.
        """)

        # Key Features Section
        st.header("Key Features")
        st.write("""
        - **Diverse Accommodations:** Airbnb offers a wide range of lodging options including entire homes, private rooms, shared spaces, and even unique stays like treehouses, castles, and boats.
        - **Global Reach:** The platform operates in over 220 countries and regions, listing millions of properties worldwide.
        - **User Reviews:** Guests and hosts can leave reviews, which helps maintain trust and transparency within the community.
        - **Experiences:** In addition to accommodations, Airbnb offers "Experiences," which are activities hosted by locals ranging from cooking classes to guided tours.
        - **Flexible Booking:** Users can book accommodations for short stays, long-term rentals, and everything in between.
        - **Host Tools:** Hosts have access to a suite of tools for managing their listings, including pricing suggestions, booking management, and analytics.
        """)

        # How It Works Section
        st.header("How It Works")
        st.write("""
        - **Searching:** Users can search for accommodations by entering their destination, travel dates, and number of guests. Filters allow users to narrow down their search based on various preferences such as price range, type of property, and amenities.
        - **Booking:** Once a suitable property is found, users can book it directly through the Airbnb platform. Payment is handled securely through the site.
        - **Staying:** Upon arrival, guests follow the instructions provided by the host to check in and enjoy their stay.
        - **Reviewing:** After the stay, guests and hosts can leave reviews to share their experiences and provide feedback.
        """)

        # Impact and Innovation Section
        st.header("Impact and Innovation")
        st.write("""
        - **Economic Impact:** Airbnb has created economic opportunities for millions of hosts around the world, enabling them to earn income by renting out their properties.
        - **Travel Experience:** The platform has contributed to a more personalized travel experience, allowing guests to stay in neighborhoods and properties that offer a more local feel compared to traditional hotels.
        - **Community Building:** Airbnb fosters a sense of community by connecting people from diverse backgrounds and encouraging cultural exchange.
        """)
    def data_exploration_page(self):
        st.title("Data Exploration")

        # Sidebar filters
        st.sidebar.subheader("Filter Options")
        print(self.df)
        countries = self.df['country'].unique()
        selected_country = st.sidebar.selectbox('Select Country:', countries, index=0)
        filtered_df = self.df[self.df['country'] == selected_country]

        if filtered_df.empty:
            st.write("No listings available for the selected country.")
            return

        min_price, max_price = int(filtered_df['price'].min()), int(filtered_df['price'].max())
        selected_min_price = st.sidebar.slider('Select Minimum Price:', min_value=min_price, max_value=max_price, value=min_price)
        selected_max_price = st.sidebar.slider('Select Maximum Price:', min_value=min_price, max_value=max_price, value=max_price)
        filtered_df = filtered_df[(filtered_df['price'] >= selected_min_price) & (filtered_df['price'] <= selected_max_price)]

        if filtered_df.empty:
            st.write("No listings available for the selected price range.")
            return

        st.write(f"Displaying {len(filtered_df)} listings")

        # Display filtered hotels and their prices
        st.subheader("Filtered Hotels and Prices")
        hotel_list = filtered_df[['name', 'price']]
        selected_hotel = st.selectbox("Select a hotel to view details:", hotel_list['name'])

        if selected_hotel:
            st.write(f"Details for {selected_hotel}")
            st.dataframe(filtered_df[filtered_df['name'] == selected_hotel][['name', 'price', 'number_of_reviews', 'review_scores_rating']])
            st.plotly_chart(self.plot_radar_chart(filtered_df, selected_hotel), use_container_width=True)

    def advanced_analysis_page(self):
        st.title("Advanced Analysis")

        # Sidebar filters
        st.sidebar.subheader("Filter Options")

        countries = self.df['country'].unique()
        selected_country = st.sidebar.selectbox('Select Country:', countries, index=0)
        filtered_df = self.df[self.df['country'] == selected_country]

        if filtered_df.empty:
            st.write("No listings available for the selected country.")
            return

        property_types = filtered_df['property_type'].unique()
        selected_property_types = st.sidebar.multiselect('Select Property Type(s):', property_types, default=property_types)
        filtered_df = filtered_df[filtered_df['property_type'].isin(selected_property_types)]

        room_types = filtered_df['room_type'].unique()
        selected_room_types = st.sidebar.multiselect('Select Room Type(s):', room_types, default=room_types)
        filtered_df = filtered_df[filtered_df['room_type'].isin(selected_room_types)]

        # Handle missing or invalid price values
        min_price, max_price = filtered_df['price'].min(), filtered_df['price'].max()
        
        if pd.isna(min_price) or pd.isna(max_price):
            st.write("Price data is missing or invalid.")
            return

        min_price, max_price = int(min_price), int(max_price)
        
        selected_min_price = st.sidebar.slider('Select Minimum Price:', min_value=min_price, max_value=max_price, value=min_price)
        selected_max_price = st.sidebar.slider('Select Maximum Price:', min_value=min_price, max_value=max_price, value=max_price)
        filtered_df = filtered_df[(filtered_df['price'] >= selected_min_price) & (filtered_df['price'] <= selected_max_price)]

        if filtered_df.empty:
            st.write("No listings available for the selected price range.")
            return

        min_reviews, max_reviews = filtered_df['number_of_reviews'].min(), filtered_df['number_of_reviews'].max()
        
        if pd.isna(min_reviews) or pd.isna(max_reviews):
            st.write("Number of reviews data is missing or invalid.")
            return
        
        min_reviews, max_reviews = int(min_reviews), int(max_reviews)
        
        selected_min_reviews = st.sidebar.slider('Select Minimum Number of Reviews:', min_value=min_reviews, max_value=max_reviews, value=min_reviews)
        selected_max_reviews = st.sidebar.slider('Select Maximum Number of Reviews:', min_value=min_reviews, max_value=max_reviews, value=max_reviews)
        filtered_df = filtered_df[(filtered_df['number_of_reviews'] >= selected_min_reviews) & (filtered_df['number_of_reviews'] <= selected_max_reviews)]

        if filtered_df.empty:
            st.write("No listings available for the selected number of reviews.")
            return

        st.write(f"Displaying {len(filtered_df)} listings")

        if len(filtered_df) > 0:

            st.subheader("Room Type Distribution")
            st.plotly_chart(self.plot_room_type_distribution(filtered_df), use_container_width=True)

            st.subheader("Price Heatmap")
            st.plotly_chart(self.plot_price_heatmap(filtered_df), use_container_width=True)

            col3, col4 = st.columns(2)

            with col3:
                st.subheader("Price Distribution by Property Type")
                st.plotly_chart(self.plot_price_distribution_by_property(filtered_df), use_container_width=True)

            with col4:
                st.subheader("Review Score Distribution")
                st.plotly_chart(self.plot_review_score_distribution(filtered_df), use_container_width=True)

            st.subheader("Price vs Review Scores")
            st.plotly_chart(self.plot_price_vs_review_scores(filtered_df), use_container_width=True)

            st.subheader("Cancellation Policy Distribution")
            st.plotly_chart(self.plot_cancellation_policy_distribution(filtered_df), use_container_width=True)

            st.subheader("Availability vs Number of Hotels")
            st.plotly_chart(self.plot_availability_vs_hotels(filtered_df), use_container_width=True)

        else:
            st.write("No data available for the selected filters.")


    def map_page(self):
        st.title("Map Visualization")

        # Sidebar filters
        st.sidebar.subheader("Filter Options")

        countries = self.df['country'].unique()
        selected_country = st.sidebar.selectbox('Select Country:', countries, index=0)
        filtered_df = self.df[self.df['country'] == selected_country]

        if filtered_df.empty:
            st.write("No listings available for the selected country.")
            return

        property_types = filtered_df['property_type'].unique()
        selected_property_type = st.sidebar.selectbox('Select Property Type:', property_types, index=0)
        filtered_df = filtered_df[filtered_df['property_type'] == selected_property_type]

        room_types = filtered_df['room_type'].unique()
        selected_room_types = st.sidebar.multiselect('Select Room Type(s):', room_types, default=room_types)
        filtered_df = filtered_df[filtered_df['room_type'].isin(selected_room_types)]

        min_price, max_price = int(filtered_df['price'].min()), int(filtered_df['price'].max())
        selected_min_price = st.sidebar.slider('Select Minimum Price:', min_value=min_price, max_value=max_price, value=min_price)
        selected_max_price = st.sidebar.slider('Select Maximum Price:', min_value=min_price, max_value=max_price, value=max_price)
        filtered_df = filtered_df[(filtered_df['price'] >= selected_min_price) & (filtered_df['price'] <= selected_max_price)]

        if filtered_df.empty:
            st.write("No listings available for the selected price range.")
            return

        min_reviews, max_reviews = int(filtered_df['number_of_reviews'].min()), int(filtered_df['number_of_reviews'].max())
        selected_min_reviews = st.sidebar.slider('Select Minimum Number of Reviews:', min_value=min_reviews, max_value=max_reviews, value=min_reviews)
        selected_max_reviews = st.sidebar.slider('Select Maximum Number of Reviews:', min_value=min_reviews, max_value=max_reviews, value=max_reviews)
        filtered_df = filtered_df[(filtered_df['number_of_reviews'] >= selected_min_reviews) & (filtered_df['number_of_reviews'] <= selected_max_reviews)]

        if filtered_df.empty:
            st.write("No listings available for the selected number of reviews.")
            return

        selected_map_style = st.sidebar.selectbox('Select Map Style:', ['light', 'dark'], index=0)

        st.write(f"Displaying {len(filtered_df)} listings on the map")

        if len(filtered_df) > 0:
            st.pydeck_chart(self.plot_advanced_map(filtered_df, map_style=selected_map_style))
        else:
            st.write("No data available for the selected filters.")

    def search_page(self):
        st.title("Search Listings")

        search_term = st.text_input("Enter search term (e.g., name, neighborhood, amenities):")

        if search_term:
            search_results = self.df[self.df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
            st.write(f"Displaying {len(search_results)} listings matching '{search_term}'")
            if len(search_results) > 0:
                st.dataframe(search_results)
            else:
                st.write("No listings match the search term.")
        else:
            st.write("No search term entered.")

    def run(self):
        st.set_page_config(layout="wide")
        st.markdown(
            """
            <style>
            .main {
                background-color: #ff8a72;  /* Change to your desired background color */
            }
            .st-emotion-cache-6qob1r {
                background-color: #72c9c9;  /* Change to your desired background color */
            }
            .st-emotion-cache-12fmjuu {
                background-color: #ff8a72;  /* Change to your desired background color */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.sidebar.title("Navigation")
        options = st.sidebar.radio("Choose a page", ["Home", "Data Exploration", "Advanced Analysis", "Map", "Search"])
        
        if options == "Home":
            self.home_page()
        elif options == "Data Exploration":
            self.data_exploration_page()
        elif options == "Advanced Analysis":
            self.advanced_analysis_page()
        elif options == "Map":
            self.map_page()
        elif options == "Search":
            self.search_page()

if __name__ == "__main__":
    app = StreamlitApp()
    app.run()

