import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from model_utils import analyze_text

st.set_page_config(page_title="Sentiment Analyzer", page_icon="💬", layout="centered")

# ---------- HEADER ----------
st.markdown("""
<h1 style='text-align: center; color: #00C9A7;'>🔥 AI Sentiment Analyzer</h1>
<p style='text-align: center;'>Single Text + Bulk CSV Analysis</p>
""", unsafe_allow_html=True)

st.markdown("---")

# ---------- TABS ----------
tab1, tab2 = st.tabs(["📝 Single Text", "📁 Bulk CSV"])

# =========================
# 🔹 TAB 1: SINGLE TEXT
# =========================
with tab1:
    text = st.text_area("Enter text")

    if st.button("Analyze Text"):
        if text.strip() == "":
            st.warning("Enter some text")
        else:
            result = analyze_text(text)

            st.success(f"Sentiment: {result['sentiment']}")

            values = [result['positive'], result['neutral'], result['negative']]
            labels = ['Positive', 'Neutral', 'Negative']

            fig, ax = plt.subplots()
            ax.pie(values, labels=labels, autopct='%1.1f%%')
            ax.axis('equal')

            st.pyplot(fig)

# =========================
# 🔹 TAB 2: CSV UPLOAD
# =========================
with tab2:
    uploaded_file = st.file_uploader("Upload CSV file", type=["csv"])

    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.write("Preview:", df.head())

        text_column = st.selectbox("Select text column", df.columns)

        if st.button("Analyze CSV"):
            results = []

            for text in df[text_column]:
                res = analyze_text(str(text))
                results.append(res["sentiment"])

            df["Sentiment"] = results

            st.success("Analysis Complete")
            st.write(df.head())

            # ✅ FIX: define values & labels properly
            sentiment_counts = df["Sentiment"].value_counts()

            values = sentiment_counts.values
            labels = sentiment_counts.index

            fig, ax = plt.subplots()

            wedges, texts, autotexts = ax.pie(
                values,
                autopct='%1.1f%%',
                startangle=90
            )

            # Donut hole
            centre_circle = plt.Circle((0, 0), 0.70)
            fig.gca().add_artist(centre_circle)

            # Legend
            ax.legend(wedges, labels, title="Sentiment",
                      loc="center left", bbox_to_anchor=(1, 0.5))

            ax.axis('equal')

            st.pyplot(fig)

            # Download
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button("📥 Download Results", csv, "sentiment_results.csv")

# ---------- FOOTER ----------
st.markdown("---")
st.caption("🚀 Built with Streamlit | NLTK | Data Visualization")