import streamlit as st
import pandas as pd
import openai

# Sidebar for API key
st.sidebar.title("Settings")
api_key = st.sidebar.text_input("Enter your OpenAI API Key", type="password")

if api_key:
    openai.api_key = api_key

    st.title("Thai to Japanese Translator")
    st.markdown("""
    Translate Thai sentences into **Japanese Casual (タメ口)** and **Japanese Polite (敬語)** forms.
    """)

    # User Input
    thai_sentence = st.text_area("Enter a Thai sentence to translate:")

    if st.button("Translate") and thai_sentence.strip():
        with st.spinner("Translating..."):
            try:
                # Use OpenAI API to get translations
                response = openai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a translator. Translate Thai sentences into Japanese. Provide both タメ口 (casual) and 敬語 (polite) forms. Returns タメ口 (casual) in the first line and 敬語 (polite) in the second line. Returns only sentences"
                        },
                        {"role": "user", "content": thai_sentence},
                    ]
                )

                # Process response
                translations = response.choices[0].message.content.split("\n")
                casual_translation = translations[0].replace("Casual:", "").strip()
                polite_translation = translations[1].replace("Polite:", "").strip()

                # Display results
                df = pd.DataFrame({
                    "Form": ["タメ口 (Casual)", "敬語 (Polite)"],
                    "Japanese Translation": [casual_translation, polite_translation]
                })
                st.markdown("### Translation Results")
                st.dataframe(df, use_container_width=True)

                # Download results
                csv = df.to_csv(index=False).encode("utf-8")
                st.download_button(
                    label="Download Results as CSV",
                    data=csv,
                    file_name="translation_results.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"Error: {e}")
else:
    st.warning("Please enter your OpenAI API Key in the sidebar.")
