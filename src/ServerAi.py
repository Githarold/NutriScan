#!/bin/python3
# -*- coding: utf-8 -*-

import os
import sys
import yaml
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template
from ultralytics import YOLO


class AiServer:
    def __init__(self):
        # Initialize Flask application, paths, model, and configurations
        self.app = Flask(__name__)
        self.setup_paths()
        self.model = self.load_model()
        self.korean_food_dict = self.load_food_dict()
        self.setup_config()
        self.user_food_dic = {}
        self.setup_routes()

    def setup_paths(self):
        # Define and add current directory to system path
        self.current_path = os.path.dirname(os.path.realpath(__file__))
        sys.path.append(self.current_path)

    def load_model(self):
        # Load trained model from the file
        train_best = os.path.normpath(os.path.join(self.current_path, "./best.pt"))
        return YOLO(train_best)

    def load_food_dict(self):
        # Load food dictionary from YAML file
        with open(
            os.path.join(self.current_path, "food.yaml"), "r", encoding="utf-8"
        ) as file:
            return yaml.safe_load(file)["korean_food"]

    def setup_config(self):
        # Configure upload folder and allowed file extensions
        upload_folder = "/home/seongbin/workspace/uploads"
        self.allowed_extensions = {"png", "jpg", "jpeg", "gif"}
        self.app.config["UPLOAD_FOLDER"] = upload_folder

    def allowed_file(self, filename):
        # Check if file has an allowed extension
        return (
            "." in filename
            and filename.rsplit(".", 1)[1].lower() in self.allowed_extensions
        )

    def process_image(self, file_path, user_ip):
        # Process the uploaded image using the model to predict the food content.
        # Store the prediction results in a user-specific dictionary.
        results = self.model.predict(source=file_path, save=False)
        output = ""
        for r in results:
            boxes = r.boxes
            for box in boxes:
                c = box.cls
                food = self.korean_food_dict.get(str(self.model.names[int(c)]), "")
                output += food + " "

        # Store the output in user-specific dictionary
        self.user_food_dic[user_ip] = output

    def setup_routes(self):
        # Define the routes for handling web requests.

        @self.app.route("/")
        def index():
            # Render main upload page
            return render_template("upload.html")

        @self.app.route("/upload", methods=["POST"])
        def upload_file():
            # Handle file upload and prediction
            user_ip = request.remote_addr
            self.user_food_dic[user_ip] = ""

            file = request.files.get("file")
            if not file or file.filename == "":
                return "No file part or selected file"
            if self.allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file_path = os.path.join(self.app.config["UPLOAD_FOLDER"], filename)
                file.save(file_path)

                # Process the image and update the user_food_dic
                self.process_image(file_path, user_ip)

                return render_template(
                    "result.html", food_output=self.user_food_dic[user_ip]
                )
            else:
                return "Invalid file type"

        @self.app.route("/check")
        def food_return():
            # Retrieve and return user-specific prediction result
            user_ip = request.remote_addr
            return self.user_food_dic.get(user_ip, "")

    def run(self):
        # Run the Flask application
        self.app.run(host="0.0.0.0", debug=False)


if __name__ == "__main__":
    server = AiServer()
    server.run()
