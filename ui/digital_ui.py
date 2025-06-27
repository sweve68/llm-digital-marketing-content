# streamlit
import streamlit as st
from PIL import Image
import base64
from transformers import CLIPProcessor, CLIPModel

from app.helpers.bert import calculate_bert_score, candidate_text
from app.helpers.file_content import generate_content_from_text, generate_content_from_image
from app.files.files import consumer_files, Physician_files
from app.urls.urls import consumer_url_list, Physician_url_list
from app.helpers.image_content import build_index, search_by_query, short_query

# ------------------ Cache Models ------------------ #
@st.cache_resource
def load_clip_model():
    clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
    clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")
    return clip_model, clip_processor

@st.cache_resource
def load_index(folder):
    return build_index(folder)

# ------------------ App UI ------------------ #
# Header
st.markdown("""
    <div style="
        display: flex; 
        align-items: center; 
        border: 2px solid #0072CE;  
        padding: 15px 20px; 
        border-radius: 8px;
        max-width: 700px;
        margin-bottom: 20px;
        position: relative;">
        <img src='https://upload.wikimedia.org/wikipedia/commons/5/57/Pfizer_%282021%29.svg' width='120' style='margin-right: 20px; z-index: 2; position: relative;'>
        <h1 style="margin: 0; font-weight: 700; font-size: 2rem;">Product Marketing Generator</h1>
    </div>
""", unsafe_allow_html=True)

# ------------------ Sidebar Inputs ------------------ #
st.sidebar.markdown("## ⚙️ Configuration")
input_type = st.sidebar.radio("Choose input type:", ["Text", "Image"])

user_type = st.sidebar.radio("Select user type:", ["Consumer", "Professional"])
if st.sidebar.button("Confirm selection"):
    st.session_state.user_type = user_type
    st.sidebar.success(f"You selected: **{input_type}** ({user_type})")
    #         st.markdown("<hr>", unsafe_allow_html=True)
    # st.sidebar.success(f"User type confirmed: **{user_type}**")

if input_type == "Text":
    recommend_images = st.sidebar.radio("Recommend Images?", ["Yes", "No"])
    if st.sidebar.button("Confirm Image Recommendation"):
        st.session_state.recommend_images = recommend_images
        st.sidebar.success(f"Image recommendation: **{recommend_images}**")

# ------------------ Main Panel ------------------ #
if input_type == "Text":

    if 'user_type' not in st.session_state:
        st.warning("Please confirm user type from the sidebar.")
        st.stop()

    user_type = st.session_state.user_type

    st.markdown("### 📄 Select Source File")
    if user_type == "Consumer":
        selected_file = st.selectbox("Choose a files:", consumer_files)
        file_index = consumer_files.index(selected_file)
        url = consumer_url_list[file_index]
    else:
        selected_file = st.selectbox("Choose a files:", Physician_files)
        file_index = Physician_files.index(selected_file)
        url = Physician_url_list[file_index]

    st.markdown("### 📝 Choose Marketing Platform")
    selected_option = st.selectbox("Select platform type:", ["Facebook", "Email", "Banner"])
    selected_sections = selected_option.lower()

    if st.button("Generate Content"):
        marketing_response, content = generate_content_from_text(url, selected_sections, user_type)
        st.session_state['content'] = content

        st.markdown("### 📢 Generated Marketing Content")
        st.json(marketing_response)

        if marketing_response:
            score = calculate_bert_score(marketing_response, url, selected_sections)
            st.markdown("### 📊 BERT Similarity Score")
            st.info(f"**Score:** {score}")

        if marketing_response and st.session_state.get("recommend_images") == "Yes":
            st.markdown("### 🖼️ Recommended Images")
            clip_model, clip_processor = load_clip_model()
            folder = 'app/configs/data'
            index, image_embeddings, image_paths = load_index(folder)

            total_response = candidate_text(marketing_response, selected_sections)
            query = short_query(total_response[:200])

            results = search_by_query(query, image_paths, image_embeddings, index)
            cols = st.columns(2)
            for idx, result in enumerate(results):
                with cols[idx % 2]:
                    st.image(result['image_path'], caption=f"{result['score']:.2f}", width=300)
            # for result in results:
        #         st.image(result['image_path'], caption=f"Score: {result['score']:.3f}", width=300)

# ------------------ Image Input ------------------ #
else:
    if 'user_type' not in st.session_state:
        st.warning("Please confirm user type from the sidebar.")
        st.stop()

    user_type = st.session_state.user_type

    st.markdown("### 📤 Upload an Image")
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png", "webp"])

    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=400)

        img_str = base64.b64encode(uploaded_file.read()).decode()

        st.markdown("### 📝 Choose Marketing Platform")
        selected_option = st.selectbox("Select platform type:", ["Facebook", "Email", "Banner"])
        selected_section = selected_option.lower()

        if st.button("Generate Content"):
            marketing_response = generate_content_from_image(img_str, selected_section, user_type)
            st.markdown("### 📢 Generated Marketing Content")
            st.json(marketing_response)
    else:
        st.warning("Please upload an image to generate marketing content.")




