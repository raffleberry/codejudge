def status(start_time, end_time, now):
  ret = {
    'status_text' : '',
    'status_code' : '',
    'time' : ''
  }

  if start_time <= now and now <= end_time:
    ret['status_text'] = "Active "
    ret['time'] = str(end_time)
    ret['status_code'] = "A"
  elif now <= start_time:
    ret['status_text'] = "Starts in "
    ret['time'] = str(start_time)
    ret['status_code'] = "S"
  else:
    ret['status_text'] = "Ended : "
    ret['time'] = str(end_time)
    ret['status_code'] = "X"
  return ret