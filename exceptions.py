class FileIOException(Exception):
  """
  Raised when there's something goes wrong while writing to/reading from file 
  """

  def __init__(self):
    super().__init__("Error while writing to/reading from file")
