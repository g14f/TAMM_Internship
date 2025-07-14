# Chat With Data 🤖📊

**Chat With Data** is an AI-powered chatbot that lets you analyze your own data using natural language!  
Upload your CSV, describe your data, and provide a column metadata file—then ask questions, visualize, and explore your dataset conversationally.

[**Live Demo**](https://chat-with-data-g14f.streamlit.app)

---

## 🚀 Getting Started

### 1. Prepare Your Files

You will need:

- **CSV file:** Your dataset (e.g., `mydata.csv`)
- **Description:** A short text explaining what your data is about
- **Metadata JSON:** A JSON file that describes the columns of your CSV (see format below)

> ❓ **Don’t have data?**  
> No problem! Try out the chatbot using example files in the `sample_data` folder.

---

### 2. File Upload Steps

When you open the app, follow these steps:

1. **Upload your CSV file**  
   Click the upload button and select your data in CSV format.

2. **Describe your data**  
   Enter a brief description, e.g.:  
   `"This data contains information about car brands, manufacturing year, and prices."`

3. **Upload your columns metadata (JSON)**  
   Upload a JSON file describing each column in your CSV.

---

### 3. Example: CSV & Metadata

Suppose your CSV file looks like this:

```csv
Car,Year,Price
Toyota,2015,5000
Honda,2017,7000
Ford,2018,8000

Your **metadata JSON** should look like this:
```json
[
  {
    "name": "Car",
    "type": "string",
    "description": "Brand or make of the car"
  },
  {
    "name": "Year",
    "type": "integer",
    "description": "Year the car was manufactured"
  },
  {
    "name": "Price",
    "type": "integer",
    "description": "Listing price of the car in USD"
  }
]
