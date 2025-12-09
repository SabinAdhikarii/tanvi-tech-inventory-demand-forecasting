# Retail Inventory Demand Forecasting System

## 📋 Project Overview

The **Retail Inventory Demand Forecasting System** is a comprehensive data science and web application project designed to help retail businesses optimize their inventory management. This project combines machine learning models with an interactive web application to predict product demand, monitor inventory levels, and provide actionable insights for store managers and administrators.

### Key Features:
- **Demand Forecasting**: Uses machine learning models (Random Forest, XGBoost) to predict future product demand
- **Inventory Management**: Real-time tracking of inventory levels across multiple stores
- **Interactive Dashboard**: Visualize sales trends, inventory status, and key performance metrics
- **Alert System**: Get notified about low stock levels and high-demand products
- **Product Management**: Comprehensive product catalog with pricing and inventory details
- **Admin Portal**: Configure system settings and manage store operations

---

## 🛠️ Required Libraries & Dependencies

The project uses the following Python libraries:

| Library | Version | Purpose |
|---------|---------|---------|
| **streamlit** | 1.37.1 | Web application framework for building the interactive UI |
| **pandas** | 2.3.3 | Data manipulation and analysis |
| **numpy** | 2.2.6 | Numerical computing and array operations |
| **scikit-learn** | 1.7.2 | Machine learning algorithms and preprocessing |
| **xgboost** | 2.1.3 | Gradient boosting for advanced predictive models |
| **matplotlib** | 3.9.2 | Data visualization and plotting |
| **seaborn** | 0.13.2 | Statistical data visualization |
| **joblib** | 1.4.2 | Model serialization and parallel computing |
| **plotly** | 5.22.0 | Interactive visualizations and charts |

---

## 📥 Installation & Setup

### Prerequisites
- **Python 3.8 or higher** installed on your system
- **pip** (Python package manager)
- **Git** (for cloning the repository)

### Step 1: Clone the Repository

Choose one of the following methods:

#### Method A: Using Git (Recommended)
```bash
git clone https://github.com/SabinAdhikarii/tanvi-tech-inventory-demand-forecasting.git
cd tanvi-inventory-demand-forecasting
```

#### Method B: Download as ZIP
1. Visit the GitHub repository: [Inventory_demand_forecasting](https://github.com/SabinAdhikarii/tanvi-tech-inventory-demand-forecasting/)
2. Click the **Code** button and select **Download ZIP**
3. Extract the ZIP file to your desired location
4. Open terminal/command prompt and navigate to the extracted folder:
   ```bash
   cd tanvi-inventory-demand-forecasting
   ```

### Step 2: Create a Virtual Environment (Optional but Recommended)

Creating a virtual environment isolates your project dependencies from the system Python installation.

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Required Libraries

Navigate to the `web_app` directory and install all dependencies:

```bash
cd web_app
pip install -r requirements.txt
```

Alternatively, you can install libraries individually:
```bash
pip install streamlit==1.37.1 pandas==2.3.3 numpy==2.2.6 scikit-learn==1.7.2 xgboost==2.1.3 matplotlib==3.9.2 seaborn==0.13.2 joblib==1.4.2 plotly==5.22.0
```

---

## 🚀 Running the Project

### Running the Web Application

Once you've installed all dependencies, launch the Streamlit web application:

```bash
# Make sure you're in the web_app directory
cd web_app

# Run the application
streamlit run app.py
```

The application will start and automatically open in your default web browser at `http://localhost:8501`

**Note:** If it doesn't open automatically, manually navigate to the URL shown in the terminal.

### Running the Jupyter Notebook

To explore the machine learning analysis and model training:

```bash
# From the project root directory
jupyter notebook notebooks/Retail_Inventory_Demand_Forecasting.ipynb
```

The notebook will open in your browser and contains:
- Data loading and preprocessing
- Exploratory Data Analysis (EDA)
- Feature engineering
- Model training and evaluation
- Performance metrics and visualizations

---

## 📁 Project Structure

```
tanvi-inventory-demand-forecasting/
├── README.md                          # Project documentation
├── notebooks/
│   ├── Retail_Inventory_Demand_Forecasting.ipynb  # ML analysis notebook
│   └── retail_store_inventory.csv     # Dataset
├── web_app/
│   ├── app.py                         # Main Streamlit application
│   ├── utils.py                       # Utility functions
│   ├── requirements.txt               # Python dependencies
│   └── pages/
│       ├── dashboard.py               # Dashboard page
│       ├── alerts.py                  # Alerts and notifications
│       ├── products.py                # Products management
│       └── admin.py                   # Admin panel
└── __pycache__/                       # Python cache files
```

---

## 📊 Using the Application

### Navigation

The web application has a sidebar menu with the following sections:

1. **Dashboard**: View sales trends, inventory status, and key metrics at a glance
2. **Alerts**: Monitor low stock warnings and high-demand products
3. **Products List**: Browse and search the product catalog with inventory levels
4. **Admin**: Manage settings, store information, and system configuration

### Data

The project uses a retail inventory dataset (`retail_store_inventory.csv`) containing:
- **Date**: Transaction date
- **Store ID**: Unique store identifier
- **Product ID**: Unique product identifier
- **Units Sold**: Number of units sold
- **Units Ordered**: Number of units ordered
- Additional features for demand forecasting

---

## 🔧 Troubleshooting

### Common Issues

**Issue: Module not found error**
```
ModuleNotFoundError: No module named 'streamlit'
```
**Solution:** Ensure all requirements are installed:
```bash
pip install -r web_app/requirements.txt
```

**Issue: Port 8501 already in use**
**Solution:** Run Streamlit on a different port:
```bash
streamlit run app.py --server.port 8502
```

**Issue: Jupyter notebook not found**
**Solution:** Install Jupyter:
```bash
pip install jupyter
```

---

## 📈 Project Workflow

1. **Data Collection**: Raw retail inventory data from multiple stores
2. **Data Exploration**: Analyze patterns and identify trends using the Jupyter notebook
3. **Feature Engineering**: Create lag features, rolling averages, and seasonal indicators
4. **Model Training**: Train machine learning models (Random Forest, XGBoost)
5. **Prediction**: Generate demand forecasts for inventory optimization
6. **Visualization**: Present insights through the interactive web dashboard

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit issues or pull requests to improve the project.

---



## 👤 Author

**SabinAdhikari**  
GitHub: [SabinAdhikarii](https://github.com/SabinAdhikarii)

---

## 📞 Support

For questions or issues, please open an issue on the [GitHub repository](https://github.com/SabinAdhikarii/tanvi-tech-inventory-demand-forecasting).

---

**Last Updated:** December 2025


