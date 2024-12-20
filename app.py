import os
import streamlit as st
from openai import OpenAI
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager

# Load environment variables
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# Cookie Manager for Persistent User Tracking
cookies = EncryptedCookieManager(
    prefix="recipe_app_",  # Prefix to differentiate cookies
    password="4qg0DvktqED9q;cbB@q/KS7GH;p9jG",  # Replace with a secure password
)

if not cookies.ready():
    st.stop()

# Retrieve or initialize recipe count from cookies
recipe_count = cookies.get("recipe_count", "0")
recipe_count = int(recipe_count) if recipe_count else 0  # Ensure it's an integer

# UI Enhancements with gradient background and white block for content
st.markdown(
    """
    """,
    unsafe_allow_html=True,
)

st.title("Random Recipe Generator 🍲")
st.write("Welcome! Enter your ingredients to create a unique recipe. Limited to **3 recipes per session**.")

# Input field for ingredients
ingredients = st.text_area("🌿 Ingredients (separate by commas):", placeholder="e.g., carrots, potatoes, chicken")

st.markdown("### Instructions:")
st.markdown("""
- Enter a list of ingredients separated by commas.
- Click **Generate Recipe** to create a recipe.
- You can create up to 3 recipes per session!
""")

# Check if the input is valid
if ingredients.strip() and not any(char.isdigit() for char in ingredients):
    is_valid_input = True
else:
    is_valid_input = False
    if ingredients:
        st.warning("Please enter valid ingredients without numbers!")

# Limit user to 3 recipes
if recipe_count < 3:
    if st.button("Generate Recipe"):
        if is_valid_input:
            try:
                # Call OpenAI API with extended instructions
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",  # Specify the model
                    messages=[
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "system", "content": "You generate unique and creative recipes based on the given ingredients. If ingridients not food, you will tell this to user and write a joke about it"},
                        {"role": "system", "content": "Ensure the recipes are easy to follow and include all necessary steps."},
                        {"role": "user", "content": f"Create a recipe using these ingredients: {ingredients}."}
                    ],
                    max_tokens=350,  # Increased tokens
                )
                recipe = response.choices[0].message.content.strip()
                st.success("Recipe Generated!")
                st.write(recipe)

                # Save recipe in session state for download
                st.session_state["last_recipe"] = recipe

                # Increment recipe count and update cookies
                recipe_count += 1
                cookies["recipe_count"] = str(recipe_count)
                cookies.save()
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
        else:
            st.warning("Please enter some ingredients!")
else:
    st.warning("You have reached the limit of 3 recipes for this session.")


# Add a download button for the recipe
if st.session_state.get("last_recipe"):
    recipe_text = st.session_state["last_recipe"]
    st.download_button(
        label="Download Recipe",
        data=recipe_text,
        file_name="recipe.txt",
        mime="text/plain",
    )

# Add a Reset Button for Testing and Deployment
#if st.button("Reset Usage"):
#   cookies["recipe_count"] = "0"
#   cookies.save()
#   st.success("Usage has been reset. Refresh the page to start over.")
