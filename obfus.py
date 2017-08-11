import os
import requests
import re 

data = {
'ObfuscatorForm[source]' : '',
'ObfuscatorForm[code]' : '',
'ObfuscatorForm[save_code]' : '0',
'ObfuscatorForm[save_code]' : '1',
'ObfuscatorForm[code_mixup]': '0',
'ObfuscatorForm[code_mixup]': '1',
'ObfuscatorForm[change_logic]' : '0',
'ObfuscatorForm[change_logic]' : '1',
'ObfuscatorForm[mutation_passes]' : '2',
'ObfuscatorForm[expand_calls]' : '0',
'ObfuscatorForm[expand_calls]' : '1',
'ObfuscatorForm[assume_stdcall]' : '0',
'ObfuscatorForm[assume_stdcall]' : '1',
'ObfuscatorForm[resolve_const]' : '0',
'ObfuscatorForm[resolve_const]' : '1',
'ObfuscatorForm[fake_cmd]' : '0',
'ObfuscatorForm[fake_cmd]' : '1',
'ObfuscatorForm[fake_cmd_32]' : '0',
'ObfuscatorForm[fake_cmd_32]' : '1',
'ObfuscatorForm[fake_cmd_16]' : '0',
'ObfuscatorForm[fake_cmd_16]' : '1',
'ObfuscatorForm[fake_cmd_8]' : '0',
'ObfuscatorForm[fake_cmd_8]' : '1',
'ObfuscatorForm[insert_fake_jumps]' : '0',
'ObfuscatorForm[insert_fake_jumps]' : '1',
'ObfuscatorForm[insert_reg_jumps]' : '0',
'ObfuscatorForm[insert_reg_jumps]' : '1',
'ObfuscatorForm[insert_com_jumps]' : '0',
'ObfuscatorForm[insert_com_jumps]' : '1',
'ObfuscatorForm[com_jumps_min]' : '1',
'ObfuscatorForm[com_jumps_max]' : '5',
'ObfuscatorForm[insert_junks]' : '0',
'ObfuscatorForm[insert_junks]' : '1',
'ObfuscatorForm[junks_min]' : '1',
'ObfuscatorForm[junks_max]' : '5',
'ObfuscatorForm[rep_prefix]' : '0',
'ObfuscatorForm[rep_prefix]' : '1',
'ObfuscatorForm[insert_seh]' : '0',
'ObfuscatorForm[insert_seh]' : '1',
'obfuscate-button' : ''
}

if not os.path.exists("add_obfus_result"):
    os.makedirs("add_obfus_result")

url = "https://www.pelock.com/obfuscator/"
s = requests.Session()
get_csrf = s.get(url)
csrf = re.search('csrf-token" content="(.*?)">', get_csrf.text)
data['_csrf'] = csrf.group(1)

for item in os.listdir("add_obfus"):
    if item == ".DS_Store": continue;
    with open("add_obfus/" + item, "r") as f:
        data['ObfuscatorForm[source]'] = f.read()
    
    html = s.post(url, data=data)
    pattern = re.compile('<h2 class="h3">Obfuscated code</h2>.*?' + 
        '<textarea class="form-control monospaced-font-xs".*?"false">' + 
        '(.*?)</textarea>', re.S)

    output = re.search(pattern, html.text)
    with open("add_obfus_result/" + item, "w") as f:
        f.write(output.group(1))

