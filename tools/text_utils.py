

def text_encode(text):
    characters = []
    for c in text:
        ascii_value = ord(c)
        
        if 0x30 <= ascii_value <= 0x39:
            characters.append(0xF6 + (ascii_value - 0x30))
        elif 0x41 <= ascii_value <= 0x5A:
            characters.append(0x80 + (ascii_value - 0x41))
        elif 0x61 <= ascii_value <= 0x7A:
            characters.append(0xA0 + (ascii_value - 0x61))
        elif c == " ":
            characters.append(0x7F)
    
    return bytearray(characters)

def text_decode(arr):
    characters = []
    for c in arr:
        if 0xF6 <= c <= 0xFF:
            characters.append(chr(0x30 + (c - 0xF6)))
        elif 0x80 <= c <= 0x99:
            characters.append(chr(0x41 + (c - 0x80)))
        elif 0xA0 <= c <= 0xB9:
            characters.append(chr(0x61 + (c - 0xA0)))
        elif c == 0x7F:
            characters.append(" ")
        else:
            characters.append("@")
    
    return "".join(characters)
    


