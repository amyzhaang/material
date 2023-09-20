
SLASH = "/"

class Directory:

  def __init__(self, name, id_num):
    self.name = name
    self.id = id_num
    self.contents = []


class File:

  def __init__(self, name, contents):
    self.name = name
    self.contents = contents


def get_next_file_name(directory, name):
  count = 1
  new_name = name
  while new_name in directory:
    count += 1
    new_name = name + "_" + str(count)
  return new_name


class FileSystem:

  def __init__(self):
    self.root = {}
    self.current_dir = self.root
    self.current_name = None
    self.id = -1

  def __get_next_id(self):
    self.id += 1
    return self.id


  def __validate_in_current_dir(self, name, message):
    if name not in self.current_dir:
      raise Exception(message)


  def make_directory(self, new_dir):
    self.current_dir[new_dir] = {}
    self.current_dir[new_dir][None] = self.__get_next_id()


  def change_directory(self, dir_name):
    self.__validate_in_current_dir(dir_name, "Cannot open " +  dir_name + ": Not in current directory.")
    self.current_name = dir_name
    self.current_dir = self.current_dir[dir_name]


  def get_working_directory(self):
    if self.current_name == None:
      return SLASH

    queue = list((key, value, "") for key, value in self.root.items())
    while len(queue) > 0:
      name, value, ans = queue.pop(0)
      if type(value) is dict:
        if value[None] == self.current_dir[None]:
          return ans + SLASH + name
        queue.extend(list((k, v, ans + SLASH + name) for k, v in value.items()))


  def get_working_directory_contents(self):
    return list(filter(lambda x: x != None, self.current_dir.keys()))


  def remove(self, name):
    self.__validate_in_current_dir(name, "Cannot delete " +  name + ": Not in current directory.")
    del self.current_dir[name]


  def change_directory_to_parent(self):
    if self.current_name == None:
      return

    queue = queue = list((key, value, None, self.root) for key, value in self.root.items())
    while len(queue) > 0:
      name, value, prev_name, prev_dir = queue.pop(0)
      if type(value) is dict:
        if value[None] == self.current_dir[None]:
          self.current_name = prev_name
          self.current_dir = prev_dir
          return
        queue.extend(list((k, v, name, value) for k, v in value.items()))


  def make_file(self, new_file):
    self.current_dir[new_file] = None


  def write_file_contents(self, file_name, content):
    self.__validate_in_current_dir(file_name, file_name + " not in current directory.")
    self.current_dir[file_name] = content


  def get_file_contents(self, file_name):
    self.__validate_in_current_dir(file_name, file_name + " not in current directory.")
    return self.current_dir[file_name]


  def move_file(self, file_name, new_location):
    self.__validate_in_current_dir(file_name, file_name + " not in current directory.")

    file_contents = self.current_dir[file_name]
    path = list(filter(lambda x: x != "", new_location.split(SLASH)))
    directory = self.root[path[0]]
    for d in path[1:]:
      if d not in directory:
        directory[d] = {}
      directory = directory[d]
    new_dir_name = get_next_file_name(directory, file_name) if file_name in directory else file_name
    directory[new_dir_name] = file_contents
    self.remove(file_name)


  def move_directory(self, dir_name, new_location):
    self.__validate_in_current_dir(dir_name, dir_name + " not in current directory.")

    dir_contents = self.current_dir[dir_name]
    path = list(filter(lambda x: x != "", new_location.split(SLASH)))
    directory = self.root[path[0]]
    for d in path[1:]:
      if d not in directory:
        directory[d] = {}
      directory = directory[d]
    if dir_name in directory:
      directory[dir_name].update(dir_contents)
    else:
      directory[dir_name] = dir_contents
    self.remove(dir_name)

