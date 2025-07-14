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
```
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

```

## 📝 Notes

- **`name`**: Must match the column name in your CSV.
- **`type`**: Should be one of: `"float"`, `"integer"`, `"string"`, `"boolean"`, etc.
- **`description`**: Briefly explain what the column means.

---

## 4. Start Chatting!

Once your files are uploaded and the description is provided, type any question about your data, such as:

- “What is the average price of the cars?”
- “List all car brands from most to least expensive.”
- “Which car was manufactured most recently?”

The chatbot will reply with text, tables, or even charts based on your question.

---

## 📂 Sample Data

Curious? Try out the chatbot with ready-made examples from the `sample_data` folder!

---

## ❓ FAQ

**Q: Do I have to upload a metadata file?**  
A: Yes! The chatbot relies on column metadata to understand and answer your questions accurately.

**Q: What format should the metadata file be in?**  
A: Use JSON as shown above. Each column is described as a separate JSON object in a list.

**Q: What if I get an “Invalid Question” error?**  
A: Try rephrasing your question. The chatbot may not understand highly complex or ambiguous queries.

---

## 🛠️ How It Works

- **AI Engine:** Uses Google Gemini for natural language understanding
- **Backend:** [pandasai](https://github.com/gventuri/pandas-ai) for data analysis
- **Frontend:** Streamlit for an interactive web interface

---

## 🌟 Try it Now

[chat-with-data-g14f.streamlit.app](https://chat-with-data-g14f.streamlit.app)

---

**Enjoy chatting with your data! 🚀**
