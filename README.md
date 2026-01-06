# Malawi Outbreak Predictor

A Streamlit-based application to predict disease outbreaks (Malaria, Cholera, Monkeypox) in Malawi using LSTM and Prophet models, with visualizations, PDF reports, and email alerts and advisory reports.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Usage](#usage)
- [Security](#security)
- [Development](#development)
- [License](#license)
- [Acknowledgments](#acknowledgments)

## Overview
The Malawi Outbreak Predictor is a comprehensive disease surveillance system that leverages machine learning to forecast potential disease outbreaks in Malawi. The application combines historical health data with climate metrics to generate accurate predictions, enabling proactive public health responses.

## Features
- **User Authentication System**: Secure login and account creation with credential management
- **Interactive Dashboard**: Real-time visualization of historical disease cases and climate data with overlay image
- **Geospatial Mapping**: Interactive choropleth maps displaying predicted outbreak risk by district
- **Advanced Predictions**: 4-week forecasts using both LSTM and Prophet models with configurable risk levels
- **Export Functionality**: Generate and download detailed PDF reports of predictions
- **Email Alert System**: Automated notifications for high-risk predictions
- **Feedback Integration**: User feedback logging for continuous improvement
- **Responsive Design**: Mobile-friendly interface optimized for field use

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/noriegaking08-creator/malawi-outbreak-predictor.git
   cd malawi-outbreak-predictor
   ```

2. **Create Virtual Environment**:
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies** (ensure requirements.txt exists or create one):
   ```bash
   pip install streamlit pandas numpy scikit-learn tensorflow prophet folium plotly geopandas pillow
   ```

4. **Set up Environment Variables**:
   Create a `.env` file in the root directory with the following variables:
   ```
   SENDER_EMAIL=your_email@gmail.com
   GMAIL_APP_PASSWORD=your_app_password
   ```

## Project Structure
```
malawi_outbreak_predictor/
├── main.py                 # Main Streamlit application entry point
├── README.md               # Project documentation
├── .gitignore             # Files and directories to ignore in version control
├── .env                   # Environment variables (not committed to repo)
├── .streamlit/            # Streamlit configuration
├── data/                  # Data storage directory
│   ├── images/            # Application images (doctor image, etc.)
│   ├── logs/              # Application logs
│   ├── models/            # Trained ML models
│   └── users.json         # User authentication data (not committed)
├── src/                   # Source code modules
│   ├── auth/              # Authentication functionality
│   ├── data/              # Data loading and processing
│   ├── models/            # Machine learning model implementations
│   │   ├── istm_model.py  # LSTM model implementation
│   │   └── prophet_model.py # Prophet model implementation
│   ├── utils/             # Utility functions
│   └── visualization/     # UI components and visualizations
│       ├── dashboard.py   # Dashboard view
│       ├── map_view.py    # Mapping functionality
│       ├── predictions.py # Prediction interface
│       └── feedback.py    # Feedback system
└── env/                # TensorFlow environment (virtual environment)
```

## Dependencies
The application relies on the following key packages:
- **Streamlit**: Web application framework
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning algorithms
- **TensorFlow/Keras**: Deep learning framework for LSTM models
- **Prophet**: Time series forecasting by Meta
- **Folium**: Interactive mapping
- **Plotly**: Interactive visualizations
- **Geopandas**: Geographic data manipulation
- **Pillow**: Image processing
- **Python-dotenv**: Environment variable management

## Configuration
1. **Environment Variables**:
   - `SENDER_EMAIL`: Email address for sending alert notifications
   - `GMAIL_APP_PASSWORD`: App password for Gmail SMTP authentication

2. **Data Sources**:
   - Historical health data (malawi_health_data.csv)
   - Climate metrics data
   - District boundaries (GeoJSON format)

3. **Model Configuration**:
   - Forecast horizon: 4 weeks
   - Disease types: Malaria, Cholera, Monkeypox
   - Risk level thresholds

## Usage
1. Activate your virtual environment
2. Ensure all required environment variables are set
3. Run the application with:
   ```bash
   streamlit run main.py
   ```
4. Access the application through your browser at the provided local address
5. Register a new account or log in with existing credentials
6. Navigate through the tabs to access different features:
   - Dashboard: Overview of historical data and current status
   - Map View: Geographic visualization of outbreak risks
   - Predictions: Detailed forecasts and risk assessments
   - Feedback: Submit feedback for system improvements

## Security
This application implements several security measures:
- **Authentication**: User login system with password protection
- **Environment Variables**: Sensitive information stored separately from code
- **Input Validation**: Sanitized inputs for all user interactions
- **Secure Storage**: User credentials stored securely (though ideally should use hashing in production)
- **Data Privacy**: Historical health data anonymized for privacy compliance

**Important**: This application is intended for demonstration purposes. In a production environment, implement stronger security measures including:
- Password hashing (bcrypt/scrypt)
- HTTPS encryption
- Regular security audits
- Access logging and monitoring

## Development
### Setting Up for Development
1. Clone the repository
2. Create a virtual environment
3. Install dependencies
4. Set up environment variables
5. Create appropriate directory structure for data files

### Contributing
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests if applicable
5. Commit your changes with clear commit messages (`git commit -m 'Add feature X for Y reason'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request with a detailed description of your changes

### Testing
Currently, the application would benefit from automated tests. Consider adding unit tests for:
- Data loading and preprocessing
- Model prediction functions
- Authentication logic
- Visualization components

## License
This project is open source and available under the MIT License. See the [LICENSE](LICENSE) file for more information.

## Acknowledgments
- The Prophet forecasting model by Meta for robust time series analysis
- Streamlit for providing an intuitive web application framework
- Folium and Plotly for interactive mapping and visualization capabilities
- The health and climate datasets used for demonstration purposes
- Public health researchers and organizations working to prevent disease outbreaks in Malawi