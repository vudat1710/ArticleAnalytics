FULL_DATE = "^([Nn]gày|[Tt]háng|[Nn]ăm)?(0?[1-9]|[12][0-9]|3[01])(\/|-|\.)(0?[1-9]|1[012])(\/|-|\.)\d{2,4}$"
DATE_MONTH = "^([Nn]gày|[Tt]háng|[Nn]ăm)?(0?[1-9]|[12][0-9]|3[01])(\/|-|\.)\d{1,2}$"
MONTH_YEAR = "^([Nn]gày|[Tt]háng|[Nn]ăm)?(0?[1-9]|1[012])(\/|-|\.)\d{2,4}$"
URL = "^((http[s]?|ftp):\/\/|www\\.)?(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+$"
ELLIPSIS = "^\.{2,}$"
TIME = "^(\d{1,2})(:|h?)(\d{1,2})(:?|'?|m?)(\d{1,2})?(s?)$"
NUMBER = "[-+]?\d+([\.,]\d+)*"
PUNCTUATION = "!|\?|\.|,|\"|-|:|;|_|'|“|”|\\|\(|\)|\{|\}|\[|\]|…|‘|’"
SPECIAL_CHAR = "\~|\@|\#|\^|\&|\*|\+|\-|<|>|\/|%|–|!|\?|\.|,|\"|-|:|;|_|'|“|”|\\|\(|\)|\{|\}|\[|\]|…|‘|’"
COST_MONEY = "\$\d+([\.,]\d+)*|\d+([\.,]\d+)*"
EMAIL = "^([\w\d_\.-]+)@(([\d\w-]+)\.)*([\d\w-]+)$"
ALL_CAP = "^[A-Z]+(\.?)[A-Z]+$"
# SHORT_NAME = "[A-Z]+[\.\-][A-Z]?([\.\-][A-Z]?)*"
SHORT_NAME = "^[A-Z]+[\.]$"
WORD = "\w+"
NOT_WORD = "[^\w\s]"
PHONE_NUMBER = "^\d+\.?\d+\.?\d+$"
PERCENTAGE = "^\d+%$"
ABBREVIATION = [
    "M.City","PGS.Ts","MRS.","Mrs.","Man.United",
    "Mr.","SHB.ĐN","Gs.Bs","TMN.CSG","Kts.Ts",
    "R.Madrid","Tp.","T.Ư","Gs.Tskh","PGS.KTS",
    "GS.BS","KTS.TS","PGS-TS","Co.","Ths.Bs","T&T.HN",
    "MR.","Ms.","TT.","TP.","ĐH.QGHN","Gs.Kts","Man.Utd",
    "GD-ĐT","Corp.","ĐT.LA","Dr.","T&T","HN.ACB",
    "GS.KTS","MS.","Prof.","GS.TS","PGs.Ts","PGS.BS",
    "Ltd.","ThS.BS","Gs.Ts","SL.NA","Th.S","Gs.Vs",
    "PGs.Bs","PGS.TS","HN.T&T","SG.XT","TS.BS",
    "Yahoo!","Man.City","MISS.","HA.GL","GS.Ts","TBT.",
    "GS.VS","GS.TSKH","Ts.Bs","Gs.TSKH","Miss.",
    "GD.ĐT","PGs.Kts","N.O.V.A","Â.","Đ.","Ô"
]
EXCEPTION = [
    "Wi-fi","17+","km/h","M7","M8","21+","G3","M9",
    "G4","km3","m/s","km2","5g","4G","8K","3g","E9",
    "U21","4K","U23","Z1","Z2","Z3","Z4","Z5","Jong-un",
    "u19","5s","wi-fi","18+","Wi-Fi","m2","16+","m3",
    "V-League","Geun-hye","5G","4g","Z3+","3G","km/s",
    "6+","u21","WI-FI","u23","U19","6s","4s","HN","HP",
    "NĐ"
]

SENTENCES = "(?<!\w\.\w.)(?<![A-Z]\.)(?<=\.|\?|\!)\s"