import re
def correct_space(text):
    list_missing = [0]
    for index, letter in enumerate(text): # Ký tự in hoa đầu tiên không phải đứng vị trí thứ 1
        condition = letter.isupper() or letter.isdigit()
        if index > 1 and condition and text[index-1] != ' ':
            list_missing.append(index)
    parts = [text[i:j] + ' ' for i,j in zip(list_missing, list_missing[1:]+[None])]
    return ''.join(parts).re.sub(r'[^\w,]', ' ', s).replace('ˆ',' ').strip().replace('  ',' ')

s = "Lập Trí, Minh Trí, Sóc Sơn\n= ” HàNội.. . ˆ"
print(correct_space(s))