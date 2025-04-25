import streamlit as st
import sys
import traceback

def run_code(code: str):
    """Run the Python code and capture errors if any."""
    try:
        # Capture output of code execution
        exec(code)
    except Exception as e:
        # If an error occurs, return the exception traceback
        return f"⚠️ Error: {str(e)}\n{traceback.format_exc()}"

def code_debugger_interface():
    """Debugger interface to run and debug the code."""
    st.title("Python Code Debugger Tool")

    st.markdown("""
    This tool allows you to:
    - Enter Python code in the text area.
    - Run the code to see if there are any errors.
    - View the output or error traceback.
    """)

    # Text area for inputting Python code
    code = st.text_area("Enter Python Code to Debug", height=300)

    if code:
        if st.button("Run Code"):
            result = run_code(code)
            if "Error" in result:
                st.error(result)  # Show the error traceback
            else:
                st.success("Code ran successfully!")  # Show success
                st.text(result)  # Display the output

def main():
    """Main function to run the app."""
    # Use the code_debugger_interface here
    code_debugger_interface()

if __name__ == "__main__":
    main()
