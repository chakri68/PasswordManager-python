from model.model import Model
from view.view import View
from controller.controller import Controller

app_model = Model()
app_view = View(app_model)
app_controller = Controller(app_view, app_model)

app_controller.main_loop()
