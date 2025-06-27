from app.main import app
import pytest
from fastapi.testclient import TestClient
from PIL import Image
import io


client = TestClient(app)

def test_post_digital_content_from_text():
    url = "https://www.pfizer.com/products/product-detail/abriladatm"
    form_data = {
        "url": url,
        "channel": "facebook",
        "language": "english",
        "audience": "consumer"
    }

    response = client.post("/app/digital/text", data=form_data)
    assert response.status_code == 200
    assert "output" in response.json()



def test_post_digital_content_from_image():
    # Create an in-memory red image
    image = Image.new("RGB", (100, 100), color="red")
    image_bytes_io = io.BytesIO()
    image.save(image_bytes_io, format="PNG")
    image_bytes_io.seek(0)

    # Form fields
    form_data = {
        "channel": "facebook",
        "language": "english",
        "audience": "consumer"
    }

    # Multipart-form file upload
    files = {
        "image": ("test.png", image_bytes_io, "image/png")
    }

    # Make POST request
    response = client.post("/app/digital/image", data=form_data, files=files)

    # Debug info if needed
    print("RESPONSE:", response.status_code, response.text)

    # Assertions
    assert response.status_code == 200
    assert "output" in response.json()


