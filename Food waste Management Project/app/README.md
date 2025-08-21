# 🥗 Food Waste Management Project

This project is a **Food Donation Management System** built using **Streamlit** and **SQLite**.  
It helps analyze and manage food donations, providers, receivers, and claims.

---

## 🚀 Features
- 📊 **View Data**: Browse tables (Providers, Receivers, Food Listings, Claims).  
- 📈 **Analytics Dashboard**: Answers 13 SQL queries with **interactive charts and tables**.  
- 📝 **CRUD Operations**: Add, update, or delete food listings.  
- 🌐 **Deployed on Streamlit Cloud** for easy access.  

---

## 📂 Project Structure
```
Food-Waste-Management/
│── app.py              # Streamlit frontend app
│── food_wastage.db     # SQLite database
│── requirements.txt    # Project dependencies
│── README.md           # Project documentation
```

---

## 🛠️ Installation & Setup (Local)
1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/food-waste-management.git
   cd food-waste-management
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```
4. Open browser → `http://localhost:8501`

---

## 🌍 Deployment
This app can be deployed for free using **[Streamlit Community Cloud](https://share.streamlit.io/)**:
1. Upload this repo (`app.py`, `food_wastage.db`, `requirements.txt`, `README.md`) to GitHub.  
2. Go to Streamlit Cloud → New App → Connect GitHub repo → Deploy.  
3. Share your app link 🎉  

---

## 📊 Analytics Queries (13 Key Questions)
1. How many food providers and receivers are there in each city?  
2. Which type of food provider contributes the most food?  
3. What is the contact information of food providers in a specific city?  
4. Which receivers have claimed the most food?  
5. What is the total quantity of food available from all providers?  
6. Which city has the highest number of food listings?  
7. What are the most commonly available food types?  
8. How many food claims have been made for each food item?  
9. Which provider has had the highest number of successful food claims?  
10. What percentage of food claims are completed vs pending vs canceled?  
11. What is the average quantity of food claimed per receiver?  
12. Which meal type is claimed the most?  
13. What is the total quantity of food donated by each provider?  

---

## 👩‍💻 Tech Stack
- **Frontend:** Streamlit  
- **Database:** SQLite  
- **Backend Queries:** SQLAlchemy + SQL  

---

## 📸 Demo
*(Add screenshots or Streamlit Cloud link here once deployed)*  

---

## 🙌 Acknowledgements
This project was created as part of an academic assignment on **Database Management & Analytics**.
