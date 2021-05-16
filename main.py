from binascii import crc32 as _crc32
from words import words

prtl_seed = input("Enter known seed words: ").split()
missing_po = int(input("At which position is the word missing? (First word being 1)\n"))-1


def mn_checksum(wlist):
    """Given a mnemonic seed word list, return a string of the seed checksum."""
    if len(wlist) > 13:
        wlist = wlist[:24]
    else:
        wlist = wlist[:12]
    wstr = "".join(word[:3] for word in wlist)
    z = ((_crc32(wstr.encode()) & 0xffffffff) ^ 0xffffffff) >> 0
    z2 = ((z ^ 0xffffffff) >> 0) % len(wlist)
    return wlist[z2]


def mn_validate_checksum(wlist):
    """Given a mnemonic seed word list, check if checksum word is valid.
    Returns boolean value.
    """
    return True if mn_checksum(wlist) == wlist[-1] else False


possibles = []  # List of possible missing words
for word in words:
    test_seed = prtl_seed[0:missing_po] + [word] + prtl_seed[missing_po:]  # Seed to have checksum tested
    if mn_validate_checksum(test_seed):
        possibles += [word]
        continue
    else:
        continue
print(f"There are {len(possibles)} possibilities for the missing word. These are saved to a text file and printed:\n")
for word in possibles:
    print(word)
with open("possible_seeds.txt", "w+") as text_file:
    for word in possibles:
        text_file.write(" ".join(prtl_seed[0:missing_po] + [word] + prtl_seed[missing_po:]) + "\n\n")
