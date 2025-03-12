from gingerit.gingerit import GingerIt

parser = GingerIt()
text = "Themselfs are going to the store."
result = parser.parse(text)
print(result)
print(result['result']) # print the corrected string.