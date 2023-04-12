from abc import ABC, abstractmethod
from typing import List, TextIO, Dict
import os


class ModelEventListener(ABC):
  pass


class Model:
  def __init__(self):
    self._listeners: List[ModelEventListener] = []
    self._file: TextIO | None = None
    self._file_path = "./passwords.pwd"
    self._master_password: str | None = None

  def register_listener(self, listener: ModelEventListener):
    self._listeners.append(listener)

  def file_exists(self):
    return os.path.isfile(self._file_path)

  def login(self, password: str):
    # TODO: Add option to login using usernames
    self._file = open(self._file_path, "r+")
    first_line = self._file.readline().rstrip('\n')
    if first_line == Model.encrypt(password, password):
      self._master_password = password
      self._file.seek(0)
      return True
    self._file.close()
    self._file = None
    return False

  def signup(self, username: str, password: str):
    # TODO: Add option to login using usernames
    self._file = open(self._file_path, "w+")
    password_encrypted = Model.encrypt(password, password)
    self._file.write(password_encrypted)
    self._file.close()
    self._file = None

  def add_password(self, name: str, password: str):
    # TODO: Add some error handling
    self._file.read()
    self._file.write("\n")
    self._file.write(
      f"{name.replace(' ', '_')} {Model.encrypt(password, self._master_password)}")
    self._file.seek(0)

  def get_password(self, name: str):
    # TODO: Add some error handling
    password: str | None = None
    lines = self._file.readlines()
    for line in lines:
      line = line.rstrip('\n')
      if line.split(" ")[0] == name:
        password = Model.decrypt(line.split(" ")[1], self._master_password)
        break
    self._file.seek(0)
    return password

  def get_passwords(self):
    # TODO: Add some error handling
    passwords: List[Dict[str, str]] = []
    lines = self._file.readlines()
    for line in lines[1:]:
      line = line.rstrip('\n')
      passwords.append(
        {"name": line.split(' ')[0], "password": Model.decrypt(line.split(" ")[1], self._master_password)})
    self._file.seek(0)
    return passwords

  @staticmethod
  def cipher(key: str, message: str):
    """
    Encrypts/decrypts a message using the Vigenere Cipher.

    :param key: The key to use for the cipher (a string).
    :param message: The message to encrypt/decrypt (a string).
    :return: The encrypted/decrypted message (a string).
    """
    vigenere_square = [[chr((i + j) % 256)
                        for j in range(256)] for i in range(256)]
    key = key * (len(message) // len(key) + 1)
    key = key[:len(message)]

    result = ""
    for i in range(len(message)):
      row = ord(message[i])
      col = ord(key[i])
      result += vigenere_square[row][col]

    return result

  @staticmethod
  def generate_key(message: str, keyword: str):
    key = ""
    index = 0
    for char in message:
        # If the character is not an ASCII character, use it as it is
      if ord(char) < 0 or ord(char) > 127:
        key += char
      # Otherwise, use the keyword character cyclically
      else:
        key += keyword[index % len(keyword)]
        index += 1
    return key

  @staticmethod
  def encrypt(message: str, keyword: str):
    ciphertext = ""
    key = Model.generate_key(message, keyword)
    for i in range(len(message)):
      # If the character is not an ASCII character, use it as it is
      if ord(message[i]) < 0 or ord(message[i]) > 127:
        ciphertext += message[i]
      # Otherwise, use the Vigenère formula to get the ciphertext character
      else:
        ciphertext += chr((ord(message[i]) + ord(key[i])) % 128)
    return ciphertext

  @staticmethod
  def decrypt(ciphertext: str, keyword: str):
    plaintext = ""
    key = Model.generate_key(ciphertext, keyword)
    for i in range(len(ciphertext)):
      # If the character is not an ASCII character, use it as it is
      if ord(ciphertext[i]) < 0 or ord(ciphertext[i]) > 127:
        plaintext += ciphertext[i]
      # Otherwise, use the inverse Vigenère formula to get the plaintext character
      else:
        plaintext += chr((ord(ciphertext[i]) - ord(key[i]) + 128) % 128)
    return plaintext
