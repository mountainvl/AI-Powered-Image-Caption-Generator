from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.image import load_img, img_to_array
from tensorflow.keras.applications.inception_v3 import preprocess_input
from PIL import Image
import io

app = Flask(__name__)

# Load Pre-Trained Captioning Model
model = tf.keras.models.load_model("image_caption_model.h5")  # Pre-trained model file
tokenizer = tf.keras.preprocessing.text.tokenizer_from_json(open("tokenizer.json").read())

# Function to preprocess image
def preprocess_image(image):
    image = image.resize((299, 299))
    image_array = img_to_array(image)
    image_array = np.expand_dims(image_array, axis=0)
    return preprocess_input(image_array)

# Generate caption function
def generate_caption(image):
    processed_image = preprocess_image(image)
    features = model.predict(processed_image)  # Extract image features

    caption = "<start>"
    for _ in range(20):  # Max length of caption
        sequence = tokenizer.texts_to_sequences([caption])[0]
        sequence = tf.keras.preprocessing.sequence.pad_sequences([sequence], maxlen=20)
        prediction = model.predict([features, sequence])
        word_index = np.argmax(prediction)
        word = tokenizer.index_word.get(word_index, "<end>")
        if word == "<end>":
            break
        caption += " " + word

    return caption.replace("<start>", "").replace("<end>", "").strip()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/caption", methods=["POST"])
def caption():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"})

    file = request.files["file"]
    image = Image.open(io.BytesIO(file.read()))
    caption = generate_caption(image)
    
    return jsonify({"caption": caption})

if __name__ == "__main__":
    app.run(debug=True)
