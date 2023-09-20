
SLASH = "/"

def get_moved_file_name(directory, name):
  """
  Handles duplicate file names by appending a number to the duplicate file name.
  """
  if name not in directory:
    return name
  count = 1
  new_name = name
  while new_name in directory:
    count += 1
    new_name = name + "_" + str(count)
  return new_name


class Directory:

  def __init__(self, name, id_num):
    self.name = name
    self.id_num = id_num
    self.contents = {} # Maps name -> File or Directory.


class File:

  def __init__(self, name, id_num, file_contents=None):
    self.name = name
    self.id_num = id_num
    self.file_contents = file_contents


  def set_content(self, content):
    self.file_contents = content


  def get_content(self):
    return self.file_contents


class FileSystem:

  def __init__(self):
    self.root = Directory(SLASH, 0)
    self.current = self.root
    self.id_count = 0


  def _get_next_id(self):
    self.id_count += 1
    return self.id_count


  def _validate_in_current_dir(self, name, message):
    if name not in self.current.contents:
      raise Exception(message)


  def _validate_is_dir(self, dir_name):
    if not isinstance(self.current.contents[dir_name], Directory):
      raise Exception(dir_name + " is not a directory.")


  def _validate_is_file(self, file_name):
    if not isinstance(self.current.contents[file_name], File):
      raise Exception(file_name + " is not a file.")


  def make_directory(self, dir_name):
    if dir_name in self.current.contents:
      raise ValueError(dir_name + " already exists in current directory.")

    self.current.contents[dir_name] = Directory(dir_name, self._get_next_id())


  def change_directory(self, dir_name):
    self._validate_in_current_dir(dir_name, "Cannot open " +  dir_name + ": Not in current directory.")
    self._validate_is_dir(dir_name)
    self.current = self.current.contents[dir_name]


  def get_working_directory(self):
    if self.current.id_num == self.root.id_num:
      return SLASH

    queue = list((key, value, "") for key, value in self.root.contents.items())
    while len(queue) > 0:
      name, value, ans = queue.pop(0)
      if isinstance(value, Directory):
        if value.id_num == self.current.id_num:
          return ans + SLASH + name
        queue.extend(list((k, v, ans + SLASH + name) for k, v in value.contents.items()))


  def get_working_directory_contents(self):
    return list(self.current.contents.keys())


  def remove(self, name):
    self._validate_in_current_dir(name, "Cannot delete " +  name + ": Not in current directory.")
    del self.current.contents[name]


  def change_directory_to_parent(self):
    if self.current.id_num == self.root.id_num:
      return

    queue = queue = list((value, self.root) for value in self.root.contents.values())
    while len(queue) > 0:
      value, prev_dir = queue.pop(0)
      if isinstance(value, Directory):
        if value.id_num == self.current.id_num:
          self.current = prev_dir
          return
        queue.extend(list((v, value) for v in value.contents.values()))


  def make_file(self, file_name):
    if file_name in self.current.contents:
      raise ValueError(file_name + " already exists in current directory.")

    self.current.contents[file_name] = File(file_name, self._get_next_id())


  def write_file_contents(self, file_name, content):
    self._validate_in_current_dir(file_name, file_name + " not in current directory.")
    self._validate_is_file(file_name)
    self.current.contents[file_name].set_content(content)


  def get_file_contents(self, file_name):
    self._validate_in_current_dir(file_name, file_name + " not in current directory.")
    self._validate_is_file(file_name)
    return self.current.contents[file_name].get_content()


  def move_file(self, file_name, new_location):
    self._validate_in_current_dir(file_name, file_name + " not in current directory.")
    self._validate_is_file(file_name)

    file_contents = self.current.contents[file_name].get_content()
    path = list(filter(lambda x: x != "", new_location.split(SLASH)))
    directory = self.root
    for d in path:
      if d not in directory.contents:
        directory.contents[d] = Directory(d, self._get_next_id())
      directory = directory.contents[d]
    new_dir_name = get_moved_file_name(directory.contents, file_name)
    directory.contents[new_dir_name] = file_contents
    self.remove(file_name)


  def move_directory(self, dir_name, new_location):
    self._validate_in_current_dir(dir_name, dir_name + " not in current directory.")
    self._validate_is_dir(dir_name)

    dir_to_copy = self.current.contents[dir_name]
    path = list(filter(lambda x: x != "", new_location.split(SLASH)))

    # Find directory to copy into.
    directory = self.root
    for d in path:
      if d not in directory.contents:
        directory.contents[d] = Directory(d, self._get_next_id())
      directory = directory.contents[d]

    # Copy into directory.
    if dir_name in directory.contents:
      for name, item in dir_to_copy.contents.items():
        final_dir = directory.contents[dir_name].contents
        final_dir[get_moved_file_name(final_dir, name)] = item
    else:
      directory.contents[dir_name] = dir_to_copy

    self.remove(dir_name)

