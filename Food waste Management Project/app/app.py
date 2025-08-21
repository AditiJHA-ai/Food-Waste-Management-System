import streamlit as st
import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt

# -------------------------------
# Database connection
# -------------------------------
engine = create_engine("sqlite:///food_wastage.db")

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Home", "View Data", "Analytics", "Food Listings CRUD"])

# -------------------------------
# Home Page
# -------------------------------
if page == "Home":
    st.title("🥗 Food Donation Management System")
    st.write("""
        Welcome to the Food Donation Management System.  
        This app helps analyze **food donations, providers, receivers, claims, and trends**.  
        
        ### Features:
        - Browse data (Providers, Receivers, Food Listings, Claims)  
        - Run **13 SQL-based analytics queries** with tables + charts  
        - Perform basic **CRUD operations on Food Listings**  
    """)

# -------------------------------
# View Data Page
# -------------------------------
elif page == "View Data":
    st.title("📊 View Data")

    option = st.selectbox("Select a table to view:", ["providers", "receivers", "food_listings", "claims"])
    df = pd.read_sql(f"SELECT * FROM {option}", con=engine)
    st.dataframe(df)

# -------------------------------
# Analytics Page (with visuals)
# -------------------------------
elif page == "Analytics":
    st.title("📈 Analytics Dashboard")
    st.write("Here are the answers to the 13 project queries with charts:")

    # --- Q1 Providers per city
    st.subheader("Q1. Providers per city")
    df = pd.read_sql("SELECT City, COUNT(*) AS provider_count FROM providers GROUP BY City;", con=engine)
    st.dataframe(df.head(10))  # top 10
    st.bar_chart(df.set_index("City").head(10))

    # --- Q1b Receivers per city
    st.subheader("Q1b. Receivers per city")
    df = pd.read_sql("SELECT City, COUNT(*) AS receiver_count FROM receivers GROUP BY City;", con=engine)
    st.dataframe(df.head(10))
    st.bar_chart(df.set_index("City").head(10))

    # --- Q2 Provider type contributing most food
    st.subheader("Q2. Provider type contributing most food")
    df = pd.read_sql("SELECT Provider_Type, COUNT(*) AS total_listings FROM food_listings GROUP BY Provider_Type;", con=engine)
    st.dataframe(df)
    st.bar_chart(df.set_index("Provider_Type"))

    # --- Q3 Provider contact info (example: Delhi)
    st.subheader("Q3. Provider contact info in Delhi")
    df = pd.read_sql("SELECT Name, Contact, Address, City FROM providers WHERE City = 'Delhi';", con=engine)
    st.dataframe(df)

    # --- Q4 Top receivers by claims
    st.subheader("Q4. Top 10 receivers by claims")
    df = pd.read_sql("""
        SELECT r.Name, COUNT(c.Claim_ID) AS total_claims
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        GROUP BY r.Name
        ORDER BY total_claims DESC
        LIMIT 10;
    """, con=engine)
    st.dataframe(df)
    st.bar_chart(df.set_index("Name"))

    # --- Q5 Total quantity available
    st.subheader("Q5. Total quantity of food available")
    df = pd.read_sql("SELECT SUM(Quantity) AS total_food_available FROM food_listings;", con=engine)
    st.metric("Total Food Available", int(df.iloc[0,0]))

    # --- Q6 City with highest listings
    st.subheader("Q6. City with highest number of food listings")
    df = pd.read_sql("""
        SELECT Location AS City, COUNT(*) AS total_listings
        FROM food_listings
        GROUP BY Location
        ORDER BY total_listings DESC
        LIMIT 10;
    """, con=engine)
    st.dataframe(df)
    st.bar_chart(df.set_index("City"))

    # --- Q7 Most common food types
    st.subheader("Q7. Most commonly available food types")
    df = pd.read_sql("SELECT Food_Type, COUNT(*) AS count_food FROM food_listings GROUP BY Food_Type;", con=engine)
    st.dataframe(df)
    st.bar_chart(df.set_index("Food_Type"))

    # --- Q8 Claims per food item
    st.subheader("Q8. Claims made per food item (Top 10)")
    df = pd.read_sql("""
        SELECT f.Food_Name, COUNT(c.Claim_ID) AS claims_count
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Food_Name
        ORDER BY claims_count DESC
        LIMIT 10;
    """, con=engine)
    st.dataframe(df)
    st.bar_chart(df.set_index("Food_Name"))

    # --- Q9 Provider with most successful claims
    st.subheader("Q9. Provider with highest successful claims")
    df = pd.read_sql("""
        SELECT p.Name, COUNT(c.Claim_ID) AS successful_claims
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        WHERE c.Status = 'Completed'
        GROUP BY p.Name
        ORDER BY successful_claims DESC
        LIMIT 10;
    """, con=engine)
    st.dataframe(df)
    st.bar_chart(df.set_index("Name"))

    # --- Q10 Claim status distribution
    st.subheader("Q10. Claim status distribution (%)")
    df = pd.read_sql("""
        SELECT Status, COUNT(*) * 100.0 / (SELECT COUNT(*) FROM claims) AS percentage
        FROM claims GROUP BY Status;
    """, con=engine)
    st.dataframe(df)

    # Pie chart
    fig, ax = plt.subplots()
    ax.pie(df["percentage"], labels=df["Status"], autopct="%1.1f%%", startangle=90)
    ax.axis("equal")
    st.pyplot(fig)

    # --- Q11 Avg food claimed per receiver
    st.subheader("Q11. Average quantity claimed per receiver (Top 10)")
    df = pd.read_sql("""
        SELECT r.Name, AVG(f.Quantity) AS avg_quantity_claimed
        FROM claims c
        JOIN receivers r ON c.Receiver_ID = r.Receiver_ID
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY r.Name
        ORDER BY avg_quantity_claimed DESC
        LIMIT 10;
    """, con=engine)
    st.dataframe(df)
    st.bar_chart(df.set_index("Name"))

    # --- Q12 Most claimed meal type
    st.subheader("Q12. Most claimed meal type")
    df = pd.read_sql("""
        SELECT f.Meal_Type, COUNT(c.Claim_ID) AS total_claims
        FROM claims c
        JOIN food_listings f ON c.Food_ID = f.Food_ID
        GROUP BY f.Meal_Type ORDER BY total_claims DESC;
    """, con=engine)
    st.dataframe(df)
    st.bar_chart(df.set_index("Meal_Type"))

    # --- Q13 Total donated per provider
    st.subheader("Q13. Total quantity donated by each provider (Top 10)")
    df = pd.read_sql("""
        SELECT p.Name, SUM(f.Quantity) AS total_donated
        FROM food_listings f
        JOIN providers p ON f.Provider_ID = p.Provider_ID
        GROUP BY p.Name
        ORDER BY total_donated DESC
        LIMIT 10;
    """, con=engine)
    st.dataframe(df)
    st.bar_chart(df.set_index("Name"))

# -------------------------------
# Food Listings CRUD Page
# -------------------------------
elif page == "Food Listings CRUD":
    st.title("📝 Manage Food Listings")

    choice = st.radio("Choose operation", ["Add", "Update", "Delete"])

    if choice == "Add":
        st.subheader("Add a new food listing")
        provider_id = st.text_input("Provider ID")
        food_name = st.text_input("Food Name")
        food_type = st.text_input("Food Type")
        meal_type = st.text_input("Meal Type")
        quantity = st.number_input("Quantity", min_value=1)
        location = st.text_input("Location")

        if st.button("Add Listing"):
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO food_listings (Provider_ID, Food_Name, Food_Type, Meal_Type, Quantity, Location)
                    VALUES (:pid, :fname, :ftype, :mtype, :qty, :loc)
                """), {"pid": provider_id, "fname": food_name, "ftype": food_type,
                       "mtype": meal_type, "qty": quantity, "loc": location})
            st.success("✅ Food listing added!")

    elif choice == "Update":
        st.subheader("Update a food listing")
        food_id = st.text_input("Food ID to update")
        new_qty = st.number_input("New Quantity", min_value=1)

        if st.button("Update Listing"):
            with engine.begin() as conn:
                conn.execute(text("UPDATE food_listings SET Quantity = :qty WHERE Food_ID = :fid"),
                             {"qty": new_qty, "fid": food_id})
            st.success("✅ Food listing updated!")

    elif choice == "Delete":
        st.subheader("Delete a food listing")
        food_id = st.text_input("Food ID to delete")

        if st.button("Delete Listing"):
            with engine.begin() as conn:
                conn.execute(text("DELETE FROM food_listings WHERE Food_ID = :fid"),
                             {"fid": food_id})
            st.success("🗑️ Food listing deleted!")
