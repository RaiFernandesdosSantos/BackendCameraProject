import cv2
import PIL.Image
import google.generativeai as genai
from flask import Flask, request


genai.configure(api_key="API_KEY")
model = genai.GenerativeModel("gemini-1.5-flash")

app = Flask(__name__)


@app.route("/")
def index():
    return "Ta funcionando"


@app.route("/catch", methods=["POST"])
def catch_image():
    image = request.files["image"]

    img = cv2.imread(image)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    _, thresh = cv2.threshold(gray, 102, 255, cv2.THRESH_BINARY_INV)

    cv2.imwrite("imagem_processada.png", thresh)

    text = PIL.Image.open("imagem_processada.png")
    response = model.generate_content(
        ["O que está escrito? apenas transcreva o texto sem comentar nada", text]
    )
    return response.text


if __name__ == "__main__":
    app.run(debug=True, port=8080)
