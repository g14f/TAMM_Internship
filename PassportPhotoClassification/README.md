# 🛂 Passport Photo Compliance Classifier

This project is a deep learning solution for **classifying passport photos as "compliant" or "non-compliant"** using a fine-tuned ResNet50 model.  
It supports both **training from scratch** and **inference with a saved model**, with all necessary data already provided.

---

## 📂 Project Structure
app.ipynb # Main notebook for the project (the code)
requirements.txt # List of required Python packages
data/
train/ # Training images
val/ # Validation images
test/ # Test images
train.csv # Training image paths and labels (0: non-compliant, 1: compliant)
val.csv # Validation image paths and labels
test.csv # Test image paths (no labels)
solutions_PRIVATE.csv # True labels for test images (not used for training)
predictions.csv # Model's predictions for the test set
passport.keras # Saved model (ResNet50, fine-tuned, overfitted)
... # Optionally, you can upload your model here if you wish


---

## 🚀 Features

- Loads and preprocesses passport photo data via CSV files (**all data is included**)
- **Image augmentation** to improve model generalization
- Handles **imbalanced classes** (95.5% non-compliant, 4.5% compliant; labels: 0/1)
- Builds a **deep learning classifier** (ResNet50, transfer learning)
- Compiled with Adam optimizer, binary cross-entropy loss, and precision/recall/F1-score metrics
- **Model checkpointing:** Save/load model weights
- Can use your own models for inference or further training

---

## ⚠️ Limitations

- **Severe class imbalance** in data (mostly non-compliant samples)
- **The saved model currently overfits:** High training accuracy, low precision/recall/F1 on validation and test sets  
- More data, rebalancing, and hyperparameter tuning are required for reliable generalization

---

## ⏩ Quick Start

- **No data preparation needed!**  
  All required image folders, CSVs, and a trained model are included in the `data/` directory.
- Specify your `data/` directory if prompted in the code.
- Use the provided model (`passport.keras`) or upload your own for inference or further training.

---

## 🛠️ How It Works

1. **Data Loading & Preprocessing:**  
   - Reads CSVs for image paths and labels, loads images from `train/`, `val/`, and `test/`, applies augmentation, handles imbalanced labels (`0` for non-compliant, `1` for compliant)
2. **Model Construction:**  
   - Fine-tunes a ResNet50 base
3. **Compilation:**  
   - Optimizer: Adam  
   - Loss: Binary Cross-Entropy  
   - Metrics: Precision, Recall, F1-score
4. **Training & Prediction:**  
   - Trains on `train/`, validates on `val/`
   - Predicts on `test/` images (paths from `test.csv`)
   - Predictions saved to `predictions.csv`
   - Ground-truth labels for test set are in `solutions_PRIVATE.csv`
   - Accuracy, precision, and recall are computed by comparing `predictions.csv` to `solutions_PRIVATE.csv`  
     *(Results were poor due to overfitting)*

---

## 📝 Next Steps / Improvements

- Further **hyperparameter tuning**
- Improved class balancing (e.g. oversampling, focal loss)
- Gather more compliant images
- Explore alternative architectures

---
**Automate passport photo compliance—powered by deep learning!**
