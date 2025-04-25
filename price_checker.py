import streamlit as st
from googlesearch import search

def price_comparison_interface():
    st.title("🛍️ Free Price Comparison Tool & Book PDF Finder")
    st.markdown("""
    Enter a product or book name and we'll fetch top shopping links or book PDFs for free.
    """)
    
    # Input for product or book
    query = st.text_input("Enter Product Name or Book Title")

    search_type = st.selectbox("Choose Search Type", ["Find Best Prices", "Find Book PDFs"])

    if query and st.button("Search"):
        st.info(f"Searching Google for: {query}...")

        if search_type == "Find Best Prices":
            # For finding product prices
            try:
                results = list(search(f"buy {query} best price", num_results=10))
                if results:
                    st.success("Top results:")
                    for i, link in enumerate(results, 1):
                        st.markdown(f"{i}. [🔗 {link}]({link})")
                else:
                    st.warning("No results found for prices.")
            except Exception as e:
                st.error(f"⚠️ Something went wrong: {e}")
        
        elif search_type == "Find Book PDFs":
            # For searching book PDFs
            try:
                # Searching for free PDFs of books
                results = list(search(f"{query} free pdf download", num_results=10))
                if results:
                    st.success("Top Book PDF Links:")
                    for i, link in enumerate(results, 1):
                        st.markdown(f"{i}. [🔗 {link}]({link})")
                else:
                    st.warning("No PDF links found for this book.")
            except Exception as e:
                st.error(f"⚠️ Something went wrong: {e}")
