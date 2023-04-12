from view.view import View, Screen
from model.model import Model


class Controller:
  def __init__(self, view: View, model: Model):
    self._view = view
    self._model = model

  def main_loop(self):
    if not self._model.file_exists():
      user_data = self._view.show_screen(Screen.SIGNUP)
      self._model.signup(user_data["username"], user_data["password"])
    password = self._view.show_screen(Screen.LOGIN).get("password", None)
    login_successful = self._model.login(password)
    while login_successful is not True:
      password = self._view.show_screen(
        Screen.LOGIN, "WRONG PASSWORD").get("password", None)
      login_successful = self._model.login(password)

    self.home_page(self._view.show_screen(
        Screen.HOME, "Logged in successfully")["input"])

  def home_page(self, i: str):
    inp = i
    while inp != 'E':
      message = None
      match inp:
        case 'A':
          # Add new password
          new_password_data = self._view.show_screen(Screen.ADD_ITEM)
          self._model.add_password(
            new_password_data["name"], new_password_data["password"])
          message = "Password saved successfully..."
        case 'G':
          # Get a saved password
          name = self._view.show_screen(Screen.ITEM)["name"]
          if name != "":
            password = self._model.get_password(name)
            # Wait for input ig
            temp = self._view.show_screen(
              Screen.ITEM, data={"name": name, "password": password})
          else:
            passwords = self._model.get_passwords()
            # Wait for input ig
            temp = self._view.show_screen(
              Screen.ITEMS, data=passwords)

      inp = self._view.show_screen(
          Screen.HOME, message)["input"]
