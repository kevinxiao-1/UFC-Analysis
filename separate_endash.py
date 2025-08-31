def separate_endash(string: str):
  char_list: list[str] = []
  fighter1_stats_list: list[str] = []
  fighter2_stats_list: list[str] = []

  for char in string:
    char_list.append(char)

  def _find_emdash_index(list: list[str]) -> int:
    idx = 0
    for char in list:
      if char == "-":
        return idx
      else:
        idx += 1

  emdash_index = _find_emdash_index(char_list)

  for char in char_list[0:emdash_index]:
    fighter1_stats_list.append(char)

  for char in char_list[emdash_index + 1:len(char_list)]:
    fighter2_stats_list.append(char)

  def _chars_to_int(list: list[str]) -> int: 
    stats = ""
    for idx in range(len(list)): 
      stats = str(stats + list[idx])
    return int(stats)

  fighter1_stats = _chars_to_int(fighter1_stats_list)
  fighter2_stats = _chars_to_int(fighter2_stats_list)
  
  return fighter1_stats, fighter2_stats

# TESTING
# strikes1: str = "37-13" # Dricus v Khamzat
# strikes2: str = "445-133" # Holloway v Kattar
# strikes3: str = "198-109" # Max v Dustin
# strikes4 = '12345-67'
# print(separate_emdash(strikes4)[1]) 

if __name__ == "__main__":
  separate_endash()