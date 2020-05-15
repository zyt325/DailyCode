class Val():
  only_read_cache=False
  force_update=False
def set_only_read():
  Val.only_read_cache=True
  Val.force_update=False
def set_force_update():
  Val.only_read_cache=False
  Val.force_update=True
def get_hr_cache():
  return Val.only_read_cache,Val.force_update