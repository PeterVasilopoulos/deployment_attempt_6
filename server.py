from python_exam_app import app

# IMPORT ALL CONTROLLERS
from python_exam_app.controllers import users_controller, bands_controller

if __name__ == "__main__":
    app.run(debug = True)