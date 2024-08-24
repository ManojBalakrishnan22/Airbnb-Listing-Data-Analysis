# Airbnb Listing Analysis

## Overview

This project aims to analyze and visualize Airbnb listings using a cleaned dataset. The analysis is built with **Streamlit**, a popular Python library for building interactive web applications. The dataset has been cleaned to ensure accurate insights and smooth functionality.

## Features

- **Interactive Filters**: Filter listings by location, price range, room type, and other criteria.
- **Visualizations**: Generate various charts and graphs to understand trends in the dataset.
- **Detailed Listing View**: Explore detailed information about individual listings.
  
## Dataset

The dataset used for this project contains information about Airbnb listings. It has been cleaned to remove duplicates, handle missing values, and correct inconsistencies. The cleaning process involved:

- **Removing Duplicates**: Duplicate entries were identified and removed.
- **Handling Missing Values**: Missing values were either filled with appropriate estimates or removed based on relevance.
- **Correcting Inconsistencies**: Columns were standardized, and incorrect or outlier data points were addressed.

## Technologies and Skills

- **Python**: Programming language used for data analysis and application development.
- **Streamlit**: Framework for building interactive web applications.
- **Plotly**: Library for creating interactive plots and charts.
- **Pandas**: Data manipulation and analysis library.
- **Postgres**: Database management system used for data storage.
- **Git**: Version control system for managing code changes.

## Getting Started

To run this project locally, follow these steps:

1. **Clone the Repository**:
    ```bash
    git clone https://github.com/ManojBalakrishnan22/Phonepe-Pulse-Data-Visualization-and-Exploration.git
    cd your-directory
    ```

2. **Install Dependencies**:
    Make sure you have Python installed. Then, install the necessary Python packages using pip:
    ```bash
    pip install pandas jsonlib-python3 matplotlib psycopg2-binary streamlit plotly pydeck sqlalchemy
    ```

3. **Set Up the Database**:
    Configure postgres and import the dataset into the database. Update the database connection settings in application code .

4. **Run the Streamlit Application**:
    Start the Streamlit application using the following command:
    ```bash
    python3 app.py
    streamlit run app.py
    ```

5. **Access the Dashboard**:
    Open your web browser and navigate to `http://localhost:8501` to interact with the dashboard.

## Screenshots
**Home**
![airbnb-home](https://github.com/user-attachments/assets/14b683b1-27d5-4d9b-a794-2e4659f36f1b)

**Data Exploration**
![airbnb-de](https://github.com/user-attachments/assets/d9641bf3-77c9-4667-a256-a3b28d065057)

**Advanced Analysis**
![airbnb-AA](https://github.com/user-attachments/assets/40c02faf-5638-4024-a67b-21fec6126dc8)

**Map View**
![airbnb-map](https://github.com/user-attachments/assets/0860bad8-1d01-43e5-bdea-374b1dbcbf9f)

**Search Listing**
![airbnb-search](https://github.com/user-attachments/assets/f0930923-ba19-4357-bb53-78771d7fee69)


## Contributing

Feel free to contribute to this project by submitting issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](https://github.com/ManojBalakrishnan22/Airbnb-Listing-Data-Analysis/blob/main/LICENSE) file for details.

