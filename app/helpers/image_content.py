import numpy as np
from transformers import CLIPProcessor, CLIPModel
import torch
import faiss
import json
import os
from PIL import Image
from torchvision import transforms
from app.helpers.file_content import generate_with_ollama
from langchain_core.prompts import PromptTemplate
from typing import List, Tuple


clip_model = CLIPModel.from_pretrained("openai/clip-vit-base-patch32")
clip_processor = CLIPProcessor.from_pretrained("openai/clip-vit-base-patch32")


def embed_text(query: str):
    inputs = clip_processor(text=[query], return_tensors="pt", padding=True)
    with torch.no_grad():
        text_features = clip_model.get_text_features(**inputs)
        # text_features = text_features / text_features.norm(p=2, dim=-1, keepdim=True)
    return text_features.cpu().numpy().astype("float32")


def embed_images(images):
    inputs = clip_processor(images=images, return_tensors="pt", padding=True)
    with torch.no_grad():
        outputs = clip_model.get_image_features(**inputs)
    embeddings = outputs.cpu().numpy().astype("float32")
    return np.atleast_2d(embeddings)  # Ensures shape (N, 512)



def load_images_from_folder(folder_path):
    image_list = []
    image_paths = []

    for filename in os.listdir(folder_path):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            path = os.path.join(folder_path, filename)
            image_paths.append(path)
            try:
                img = Image.open(path).convert('RGB')

                image_list.append(img)
            except Exception as e:
                print(f"Failed to load {filename}: {e}")

    return image_list, image_paths


# use this
def build_index(image_paths):
    folder = '/Users/alokchauhan/Downloads/new_Projects/Langchain/1-Langchain/Digital_Marketing.ipynb/data'
    images, image_paths = load_images_from_folder(folder)
    if images:
        image_embeddings = embed_images(images)
        # print(f"Embedded {len(embeddings)} images.")
        # print("Embedding shape:", embeddings.shape)

        image_embeddings = np.array(image_embeddings).astype('float32')
        print(image_embeddings)
        index = faiss.IndexFlatIP(image_embeddings.shape[1])
        faiss.normalize_L2(image_embeddings)
        index.add(image_embeddings)

    return index, image_embeddings, image_paths

def short_query(content):

    template = "Concise the content to keep token count under 70:\n\n{content}"

    prompt_template = PromptTemplate(
        input_variables=["content"],
        template=template,
    )
    # Format the prompt into a string
    formatted_prompt = prompt_template.format(content=content)
    # Then pass that to Ollama
    short_query = generate_with_ollama(formatted_prompt)
    return short_query



def search_by_query(query: str, image_paths, image_embeddings, index):
    query_embedding = embed_text(query)
    # query_embedding = np.array([query_embedding]).astype('float32')
    # faiss.normalize_L2(query_embedding)

    distances, indices = index.search(query_embedding, k=5)

    results = []
    for i, idx in enumerate(indices[0]):
        if idx >= 0:  # FAISS returns -1 for invalid indices
            results.append({
                'image_path': image_paths[idx],
                'score': float(distances[0][i]),
                'embedding': image_embeddings[idx]
            })
    return results
