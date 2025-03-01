import os
import google.generativeai as genai
from flask import Flask, request, render_template, jsonify
import io
import base64
from PIL import Image

app = Flask(__name__)

# Configure Gemini API (Replace with your actual API Key)
GENAI_API_KEY = "YOUR_GENAI_API_KEY"
genai.configure(api_key=GENAI_API_KEY)

ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
UPLOADED_IMAGE = None  # Store uploaded image globally


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


# Function to analyze landmark image with a user question
def analyze_landmark(image_bytes, user_question):
    try:
        print("Processing image...")

        # Open image and convert to base64
        img = Image.open(io.BytesIO(image_bytes))
        img = img.convert("RGB")
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode()

        print("Image converted to base64 successfully.")

        # Load Gemini Vision Pro model
        model = genai.GenerativeModel("gemini-1.5-pro-latest")

        # Structure the request to Gemini API
        response = model.generate_content([
            {"inline_data": {"mime_type": "image/jpeg", "data": img_str}},
            user_question
        ])

        print("Response received from Gemini API:", response)

        if response and hasattr(response, "text"):
            landmark_info = response.text
        else:
            landmark_info = "No detailed information available."

        return {"answer": landmark_info}

    except Exception as e:
        print("Error in analyze_landmark:", str(e))
        return {"error": str(e)}


# Route for image upload
@app.route("/upload", methods=["POST"])
def upload_image():
    global UPLOADED_IMAGE

    if "image" not in request.files:
        return jsonify({"error": "No image uploaded."})

    file = request.files["image"]
    if file.filename == "":
        return jsonify({"error": "No selected file."})

    if not allowed_file(file.filename):
        return jsonify({"error": "Invalid file type. Please upload a PNG or JPG image."})

    UPLOADED_IMAGE = file.read()  # Store uploaded image in memory
    print("Image successfully uploaded and stored in memory.")
    return jsonify({"message": "Image uploaded successfully."})


# Route for asking a question about the uploaded image
@app.route("/ask", methods=["POST"])
def ask_question():
    global UPLOADED_IMAGE

    if UPLOADED_IMAGE is None:
        return jsonify({"error": "No image uploaded. Please upload an image first."})

    user_question = request.json.get("question")
    if not user_question:
        return jsonify({"error": "No question provided."})

    print("Processing question:", user_question)
    result = analyze_landmark(UPLOADED_IMAGE, user_question)
    return jsonify(result)

@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/aboutus")
def aboutus():
    return render_template("aboutus.html")

@app.route("/hiw")
def hiw():
    return render_template("hiw.html")

@app.route("/reg")
def reg():
    return render_template("reg.html")

@app.route("/contactus")
def contact_us():
    return render_template("contactus.html")

@app.route("/privacy")
def privacy_policy():
    return render_template("privacy.html")

@app.route("/terms")
def terms_conditions():
    return render_template("TandC.html")

if __name__ == "__main__":
    app.run(debug=True)
