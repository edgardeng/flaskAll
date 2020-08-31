# import json
# a = 'abc'
# # print(a.startswith('ab' || 'a'))
#
#
#
# with open("/Users/edgar/Downloads/FireShot/list.json", 'r', encoding='UTF-8') as f:
#   load_dict = json.load(f)
#   print("加载文件完成...")
#   list_cities = load_dict["result"][1]
#   print("城市数量", len(list_cities))
#   list_citie_new = []
#   list_p = load_dict["result"][0]
#   print("省数量", len(list_p))
#   for itemp in list_p:
#     if itemp["id"].startswith("500") or itemp["id"].startswith("110") or itemp["id"].startswith("310") or itemp["id"].startswith("120") or itemp["id"].startswith("810") or itemp["id"].startswith("820"):
#       itemp.pop('cidx')
#       list_citie_new.append(itemp)
#   for item in list_cities:
#     if item["id"].startswith("500"):
#       continue
#     if item["id"].startswith("110"):
#       continue
#     if item["id"].startswith("310"):
#       continue
#     if item["id"].startswith("120"):
#       continue
#     if item["id"].startswith("820"):
#       continue
#     if item["id"].startswith("810"):
#       continue
#     list_citie_new.append(item)
#
#
# with open("/Users/edgar/Downloads/FireShot/china_city_5.json", "w") as f:
#   json.dump(list_citie_new, f, ensure_ascii=False)
#   print("写出完成...")

# 回文

# def longestPalindrome(s):
#   if s is None:
#     return ''
#   s_len = len(s)
#   if s_len < 1:
#     return ''
#   max_start = 0
#   max_len = 1
#   for i in range(s_len):
#     left = i - 1
#     right = i + 1
#     row_len = 1
#     # bb开始型
#     if right >= s_len:
#       break
#
#     if s[right] == s[i]:
#       left = i
#       right = i + 1
#     while left >= 0 and right < s_len and s[right] == s[left]:
#       left -= 1
#       right += 1
#     if max_len < right - left - 1:
#       max_len = right - left - 1
#       max_start = left + 1
#       print(left, right, row_len)
#
#     # aaa 型
#     if i - 1 >= 0 and s[i + 1] == s[i - 1] and s[i] == s[i - 1]:
#       left = i - 1
#       right = i + 1
#       while left >= 0 and right < s_len and s[right] == s[left]:
#         left -= 1
#         right += 1
#       if max_len < right - left - 1:
#         max_len = right - left - 1
#         max_start = left + 1
#
#   return s[max_start:max_start + max_len]
#
# a = 'a'
# print(len(a))
# print(a, '回文', longestPalindrome(a))
import math
# def convert( s: str, numRows: int) -> str:
#   s_len = len(s)
#   rows = numRows
#   if rows == 1:
#     return s
#   cols = math.ceil(s_len * (rows - 1) / (rows * 2 - 2))
#   matrix = [[None for i in range(cols)] for j in range(rows)]
#   x = 0
#   y = 0
#   plus = True
#   for i in range(s_len):
#     letter = s[i]
#     matrix[x][y] = letter
#     if plus:
#       x += 1
#     else:
#       x -= 1
#       y += 1
#     if x == rows : # 到低了
#       x = rows - 2
#       y += 1
#       plus = False
#     if not plus and x == -1: # 回去了
#       x = 1
#       y -= 1 # 剪回来
#       plus = True
#
#   result = ''
#   for x in range(rows):
#     for y in range(cols):
#       if matrix[x][y]:
#         result += matrix[x][y]
#   return result
#
# print(convert('LEETCODEISHIRING', 2))

# def reverse(x: int) -> int:
#   if x < 0:
#     return 0 - reverse(0-x)
#   #
#   left = math.floor(x / 10)
#   res = x % 10
#   print(left, res)
#   while left > 0:
#     a = left % 10
#     left = math.floor(left / 10)
#     res = res * 10 + a
#     print(a, left, res, )
#   bound = math.pow(2, 31) - 1
#   if res > bound:
#     return 0
#   return res
#
# # 如果反转后整数溢出那么就返回 0
# import sys
# max = sys.maxsize
# print (max)
# print(reverse(-8463847412))


def myAtoi(s: str):
  s_len = len(s)
  fu = False
  res = 0
  start = False
  right = math.pow(2, 31) -1
  for i in range(s_len):
    letter = s[i]
    if not start:
      if letter == ' ':
        continue
      if letter == '-':
        start = True
        fu = True
        continue
      if letter in '0123456789':
        res = int(letter)
        start = True
        continue
      return 0
    else:
      if letter in '0123456789':
        res = res * 10 + int(letter)
        if res > right:
          return right if not fu else int(0 - math.pow(2, 31))
        continue
      else:
        break

  return res if not fu else int(0 - res)


print(myAtoi(' -91283472332 ddd'))

