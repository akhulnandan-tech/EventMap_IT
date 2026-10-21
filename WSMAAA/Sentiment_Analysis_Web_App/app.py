import streamlit as st
import pandas as pd

from sentiment_analyzer import analyze_sentiment
from visualizations import create_sentiment_chart
from styles import load_styles

st.set_page_config(
    page_title="SentimentScope | Sentiment Analysis",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

load_styles()

st.markdown(
    """
    <div style="
        background: linear-gradient(120deg, #14213d, #2563eb);
        padding: 28px;
        border-radius: 16px;
        margin-bottom: 24px;
        color: white;
    ">
        <h1 style="margin: 0; color: white;">
            📊 SentimentScope
        </h1>
        <p style="margin: 8px 0 0 0; color: #e5edff;">
            Understand opinions and emotions through text analysis.
        </p>
    </div>
    """,
    unsafe_allow_html=True
)

st.sidebar.title("📊 SentimentScope")
st.sidebar.caption("Sentiment Analysis Dashboard")

page = st.sidebar.radio(
    "Navigate",
    [
        "Analyze Text",
        "Batch CSV Analysis",
        "About Project"
    ]
)

st.sidebar.divider()
st.sidebar.info(
    "Powered by Python, Streamlit, TextBlob, Pandas, and Matplotlib."
)


# --------------------------------------------------
# HELPER FUNCTION
# --------------------------------------------------
def show_sentiment_result(result):
    """Display sentiment classification and numerical scores."""

    sentiment = str(result.get("Sentiment", "Neutral"))
    polarity = float(result.get("Polarity", 0))
    subjectivity = float(result.get("Subjectivity", 0))

    if sentiment == "Positive":
        st.success(f"😊 Sentiment: {sentiment}")
    elif sentiment == "Negative":
        st.error(f"😞 Sentiment: {sentiment}")
    else:
        st.info(f"😐 Sentiment: {sentiment}")

    col1, col2 = st.columns(2)

    with col1:
        st.metric("Polarity Score", f"{polarity:.3f}")
        st.caption("Range: -1 (negative) to +1 (positive)")

    with col2:
        st.metric("Subjectivity Score", f"{subjectivity:.3f}")
        st.caption("Range: 0 (objective) to 1 (subjective)")


# --------------------------------------------------
# PAGE 1: ANALYZE INDIVIDUAL TEXT
# --------------------------------------------------
if page == "Analyze Text":

    st.header("🔍 Analyze a Review")
    st.write(
        "Enter a sentence, product review, customer comment, "
        "or social media post to identify its sentiment."
    )

    text_input = st.text_area(
        "Enter your text",
        placeholder=(
            "Example: I really love this product. "
            "The quality is excellent!"
        ),
        height=150,
        key="single_review"
    )

    analyze_button = st.button(
        "✨ Analyze Sentiment",
        type="primary",
        use_container_width=True
    )

    if analyze_button:
        if not text_input.strip():
            st.warning("Please enter some text before analyzing.")
        else:
            try:
                with st.spinner("Analyzing your text..."):
                    result = analyze_sentiment(text_input.strip())

                st.divider()
                st.subheader("Analysis Result")

                show_sentiment_result(result)

                with st.expander("View analyzed text"):
                    st.write(text_input.strip())

            except Exception as error:
                st.error(
                    "Unable to analyze the text. "
                    "Please check sentiment_analyzer.py."
                )
                st.exception(error)


# --------------------------------------------------
# PAGE 2: BATCH CSV ANALYSIS
# --------------------------------------------------
elif page == "Batch CSV Analysis":

    st.header("📁 Batch Sentiment Analysis")
    st.write(
        "Upload a CSV file to analyze multiple reviews at once. "
        "Your CSV must contain a column named `review`."
    )

    uploaded_file = st.file_uploader(
        "Choose a CSV file",
        type=["csv"],
        help="The CSV file must include a column named review."
    )

    if uploaded_file is not None:

        try:
            df = pd.read_csv(uploaded_file)

            # Validate uploaded data
            if df.empty:
                st.warning("The uploaded CSV file is empty.")

            elif "review" not in df.columns:
                st.error(
                    "The required 'review' column was not found. "
                    f"Available columns: {', '.join(map(str, df.columns))}"
                )

            else:
                # Remove empty reviews
                df = df.copy()
                df["review"] = df["review"].fillna("").astype(str)
                df = df[df["review"].str.strip() != ""].reset_index(drop=True)

                if df.empty:
                    st.warning(
                        "No non-empty reviews were found in the CSV file."
                    )

                else:
                    with st.spinner(
                        f"Analyzing {len(df)} reviews..."
                    ):
                        results = [
                            analyze_sentiment(review)
                            for review in df["review"]
                        ]

                    result_df = pd.concat(
                        [
                            df.reset_index(drop=True),
                            pd.DataFrame(results)
                        ],
                        axis=1
                    )

                    # Summary metrics
                    counts = (
                        result_df["Sentiment"]
                        .value_counts()
                        .reindex(
                            ["Positive", "Neutral", "Negative"],
                            fill_value=0
                        )
                    )

                    st.divider()
                    st.subheader("📈 Analysis Overview")

                    col1, col2, col3, col4 = st.columns(4)

                    col1.metric("Total Reviews", len(result_df))
                    col2.metric("😊 Positive", int(counts["Positive"]))
                    col3.metric("😐 Neutral", int(counts["Neutral"]))
                    col4.metric("😞 Negative", int(counts["Negative"]))

                    # Chart
                    st.subheader("Sentiment Distribution")

                    try:
                        chart = create_sentiment_chart(counts)
                        st.pyplot(chart)
                    except Exception as chart_error:
                        st.warning(
                            "The chart could not be displayed. "
                            "Please check visualizations.py."
                        )
                        st.exception(chart_error)

                    # Results table
                    st.subheader("📋 Detailed Results")
                    st.dataframe(
                        result_df,
                        use_container_width=True,
                        hide_index=True
                    )

                    # Download
                    csv_data = result_df.to_csv(
                        index=False
                    ).encode("utf-8-sig")

                    st.download_button(
                        label="⬇️ Download Analysis as CSV",
                        data=csv_data,
                        file_name="sentiment_analysis_results.csv",
                        mime="text/csv",
                        use_container_width=True
                    )

        except pd.errors.EmptyDataError:
            st.error("The uploaded file does not contain readable CSV data.")

        except Exception as error:
            st.error(
                "An error occurred while processing the file. "
                "Please verify the CSV format and analyzer code."
            )
            st.exception(error)


# --------------------------------------------------
# PAGE 3: ABOUT PROJECT
# --------------------------------------------------
elif page == "About Project":

    st.header("ℹ️ About SentimentScope")

    st.markdown(
        """
        **SentimentScope** is a Python-based web application that
        analyzes written text and classifies it as Positive, Neutral,
        or Negative.

        ### Project Objectives

        - Identify sentiment in customer reviews and social media text.
        - Calculate polarity and subjectivity scores.
        - Analyze multiple reviews from CSV files.
        - Present results through summary metrics and visualizations.
        - Export analyzed results for further examination.

        ### Technologies Used

        | Technology | Purpose |
        |---|---|
        | Python | Application logic |
        | Streamlit | Web interface |
        | TextBlob | Sentiment analysis |
        | Pandas | CSV processing and data handling |
        | Matplotlib | Data visualization |

        ### Methodology

        1. The user enters text or uploads a CSV file.
        2. TextBlob calculates polarity and subjectivity.
        3. The application classifies sentiment using the thresholds
           defined in `sentiment_analyzer.py`.
        4. Results are displayed as scores, tables, and charts.
        5. Batch results can be downloaded as a CSV file.

        ### Understanding the Scores

        - **Polarity:** ranges from -1 to +1; negative values indicate
          negative sentiment and positive values indicate positive sentiment.
        - **Subjectivity:** ranges from 0 to 1; higher values generally
          indicate more subjective language.

        ### Important Note

        TextBlob uses a lexicon-based approach. Results are estimates
        and may not correctly interpret sarcasm, context, or every
        language.
        """
    )

    st.info(
        "Project: Sentiment Analysis Web Application"
    )


# --------------------------------------------------
# FOOTER
# --------------------------------------------------
st.divider()

st.markdown(
    """
    <div style="text-align: center; padding: 10px;">
        <p style="color: #64748b;">
            SentimentScope · Python Sentiment Analysis Project
        </p>
    </div>
    """,
    unsafe_allow_html=True
)
