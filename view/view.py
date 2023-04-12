from model.model import Model, ModelEventListener
from enum import Enum
import os
from typing import Dict


class Screen(Enum):
  HOME = 1
  ITEM = 2
  ITEMS = 3
  ADD_ITEM = 4
  LOGIN = 5
  SIGNUP = 6


class View(ModelEventListener):
  def __init__(self, model: Model):
    self._model = model
    self._model.register_listener(self)

  def _clear_screen(self):
    os.system('cls')
    # pass

  def show_screen(self, screen: Screen, message: str | None = None, **kwargs) -> Dict[str, str]:
    self._clear_screen()
    print("======= PASSWORD MANAGER =======")
    if message is not None:
      print(message)
    match screen:
      case Screen.LOGIN:
        print("LOGIN")
        pwd = input("Enter the master password you entered during setup: ")
        return {"password": pwd}
      case Screen.HOME:
        print("A: Add new password")
        print("G: Get stored password")
        print("E: Exit")
        inp = input("> ")
        return {"input": inp}
      case Screen.SIGNUP:
        print("Please signup before you use the password manager")
        username = input("Enter new username: ")
        first_password = input("Enter new master password: ")
        second_password = input("Enter the master password again: ")
        if first_password != second_password:
          return self.show_screen(Screen.SIGNUP, "The 2 passwords don't match. Try again...")
        return {"username": username, "password": first_password}
      case Screen.ADD_ITEM:
        print("Add new password")
        name = input("Name: ")
        password = input("Password: ")
        return {"name": name, "password": password}
      case Screen.ITEM:
        if kwargs.get("data", None) is not None:
          print(
            f'PASSWORD FOR {kwargs["data"]["name"]} is {kwargs["data"]["password"]}')
          inp = input("Press ENTER key to go back")
          return {"input": inp}
        print("Get saved passwords")
        name = input(
          "Enter login name (leave blank to get all saved passwords): ")
        return {"name": name}
      case Screen.ITEMS:
        if kwargs.get("data", None) is not None:
          print(f'SAVED PASSWORDS: ')
          print("NAME    PASSWORD")
          for password in kwargs["data"]:
            print(f'{password["name"]}    {password["password"]}')
          inp = input("Press ENTER key to go back")
          return {"input": inp}
        print("Get saved passwords")
        name = input("Enter login name: ")
        return {"name": name}
    return {}
