from flask import Flask, render_template, request
import google.generativeai as genai
import PIL.Image
import io  # For handling image data

app = Flask(__name__)

# Replace 'YOUR_API_KEY' with your actual API key
genai.configure(api_key="AIzaSyD4oPMJp_QD_GPnvHB51gmZJpXT7U4sotk")

def load_image(image_data):
    """Loads an image from byte data."""
    try:
        img = PIL.Image.open(io.BytesIO(image_data))
        return img
    except Exception as e:
        print(f"Error loading image: {e}")
        return None

def create_prompt(image, user_prompt="Describe this landmark in detail."):
    """Creates a prompt for the Gemini model."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    prompt_parts = [
        user_prompt,
        image,
    ]
    return prompt_parts

def generate_description(prompt_parts):
    """Generates a description using the Gemini API."""
    model = genai.GenerativeModel('gemini-1.5-flash')
    try:
        response = model.generate_content(prompt_parts)
        return response.text
    except Exception as e:
        return f"Error generating description: {e}"

@app.route('/', methods=['GET', 'POST'])
def index():
    description = None
    if request.method == 'POST':
        user_prompt = request.form.get('prompt')
        image_file = request.files.get('image')

        if image_file and user_prompt:
            image_data = image_file.read()
            image = load_image(image_data)

            if image:
                prompt_parts = create_prompt(image, user_prompt)
                description = generate_description(prompt_parts)

    return render_template('index.html', description=description)

if __name__ == '__main__':
    app.run(debug=True)