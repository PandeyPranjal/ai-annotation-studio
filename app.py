import streamlit as st
import pandas as pd

from annotation import create_annotation
from prompt_refiner import refine_prompt
from response_corrector import correct_response
from quality_scorer import calculate_quality_score

#PAGE CONFIG
st.set_page_config(page_title="AI Annotation Studio", layout="wide")

st.title("🧠 AI Data Annotation & Prompt Refinement Studio")
st.markdown("Annotate AI responses, refine prompts, and build high-quality datasets.")

#SESSION STATE
if "data" not in st.session_state:
    st.session_state.data = []

if "annotation_saved" not in st.session_state:
    st.session_state.annotation_saved = False

# INPUT SECTION
st.header("📥 Input Section")

prompt = st.text_area("Enter Prompt", height=120)
response = st.text_area("Enter AI Response", height=200)

if st.button("Start Annotation"):
    if prompt.strip() == "" or response.strip() == "":
        st.warning("⚠️ Please fill both fields.")
    else:
        st.session_state.current_entry = {
            "prompt": prompt,
            "response": response
        }
        st.session_state.annotation_saved = False
        st.success("✅ Ready for annotation!")

#MAIN PIPELINE
if "current_entry" in st.session_state:

    # DISPLAY
    st.subheader("📝 Current Entry")
    st.info(f"Prompt: {st.session_state.current_entry['prompt']}")
    st.info(f"Response: {st.session_state.current_entry['response']}")

    #ANNOTATION
    st.subheader("🏷️ Annotation Section")

    error_type = st.selectbox(
        "Select Error Type",
        ["Factual Error", "Logical Error", "Hallucination", "Bias", "Clarity Issue"]
    )

    severity = st.slider("Severity (1 = Low, 5 = High)", 1, 5, 3)
    notes = st.text_area("Annotation Notes")

    if st.button("Save Annotation"):
        quality_score = calculate_quality_score(error_type, severity)

        annotation = create_annotation(
            st.session_state.current_entry["prompt"],
            st.session_state.current_entry["response"],
            error_type,
            severity,
            notes
        )

        annotation["quality_score"] = quality_score

        st.session_state.data.append(annotation)
        st.session_state.current_index = len(st.session_state.data) - 1
        st.session_state.annotation_saved = True

        st.success(f"✅ Annotation Saved! Quality Score: {quality_score}")

    #PROMPT REFINEMENT
    if st.session_state.annotation_saved:
        st.subheader("✨ Prompt Refinement")

        if st.button("Generate Improved Prompt"):
            refined = refine_prompt(
                st.session_state.current_entry["prompt"],
                error_type
            )
            st.session_state.refined_prompt = refined

        if "refined_prompt" in st.session_state:
            st.success(st.session_state.refined_prompt)

    #RESPONSE CORRECTION
    if st.session_state.annotation_saved:
        st.subheader("🛠️ Response Correction")

        corrected_text = st.text_area("✍️ Write Corrected Response (Manual)")

        if st.button("Generate Correction Suggestion"):
            suggestion = correct_response(
                st.session_state.current_entry["response"],
                error_type
            )
            st.session_state.suggested_response = suggestion

        if "suggested_response" in st.session_state:
            st.info(st.session_state.suggested_response)

        if st.button("Save Corrected Response"):
            final_response = corrected_text if corrected_text else st.session_state.get("suggested_response", "")

            if final_response == "":
                st.warning("⚠️ No corrected response provided.")
            else:
                idx = st.session_state.current_index
                st.session_state.data[idx]["corrected_response"] = final_response
                st.success("✅ Corrected response saved!")

#DISPLAY DATA
if st.session_state.data:
    st.subheader("📊 Annotated Data")

    for i, item in enumerate(st.session_state.data):
        st.write(f"### Entry {i+1}")
        st.write(item)

#EXPORT
if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)

    st.download_button(
        label="⬇️ Download Annotated Dataset (CSV)",
        data=df.to_csv(index=False),
        file_name="annotated_data.csv",
        mime="text/csv"
    )

#ANALYTICS DASHBOARD
st.header("📊 Analytics Dashboard")

if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)

    st.write("### Error Type Distribution")
    st.bar_chart(df["error_type"].value_counts())

    st.write("### Severity Distribution")
    st.bar_chart(df["severity"].value_counts())

    st.write("### Average Severity")
    st.metric("Avg Severity", round(df["severity"].mean(), 2))

#CONSISTENCY CHECKER 
st.header("⚠️ Consistency Checker")

if st.session_state.data:
    df = pd.DataFrame(st.session_state.data)

    duplicates = df[df.duplicated("prompt", keep=False)]

    if not duplicates.empty:
        st.warning("⚠️ Potential inconsistent annotations found")
        st.dataframe(duplicates)
    else:
        st.success("✅ No inconsistency detected")

#BATCH UPLOAD
st.header("📂 Batch Upload")

uploaded_file = st.file_uploader("Upload CSV File", type=["csv"])

if uploaded_file is not None:
    batch_df = pd.read_csv(uploaded_file)

    required_cols = ["prompt", "response"]
    if not all(col in batch_df.columns for col in required_cols):
        st.error("❌ CSV must contain 'prompt' and 'response'")
    else:
        st.dataframe(batch_df)

        if st.button("Load Batch Data"):
            st.session_state.batch_data = batch_df.to_dict(orient="records")
            st.session_state.batch_index = 0

# BATCH FLOW 
if "batch_data" in st.session_state:

    current = st.session_state.batch_data[st.session_state.batch_index]

    st.subheader(f"📌 Batch Entry {st.session_state.batch_index + 1}")
    st.info(f"Prompt: {current.get('prompt', '')}")
    st.info(f"Response: {current.get('response', '')}")

    if st.button("Use This Entry"):
        st.session_state.current_entry = current
        st.session_state.annotation_saved = False

    if st.button("Next Entry"):
        if st.session_state.batch_index < len(st.session_state.batch_data) - 1:
            st.session_state.batch_index += 1
        else:
            st.warning("⚠️ End of dataset")