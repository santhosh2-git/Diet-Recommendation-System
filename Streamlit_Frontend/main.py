import streamlit as st
from pages import Custom_Food_Recommendation, Diet_Recommendation

def main():
    st.set_page_config(page_title="Diet Recommendation System", page_icon="🥗")

    st.title("Diet Recommendation System")

    # Create a navigation sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ("Home", "Custom Food Recommendation", "Personalized Nutrition"))

    if page == "Home":
        st.write("Welcome to the Diet Recommendation System! Use the sidebar to navigate.")
    
    elif page == "Custom Food Recommendation":
        Custom_Food_Recommendation.main()
    
    elif page == "Personalized Nutrition":
        Diet_Recommendation.main()

if __name__ == "__main__":
    main()
