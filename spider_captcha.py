import requests
import os
from multiprocessing import Pool

if not os.path.exists('驗證碼'):
    os.makedirs('驗證碼')

def main(i):
    response = requests.get('https://regist.nctu.edu.tw/CheckImageCode.aspx')
    with open('驗證碼/' + str(i) + '.jpg','wb') as f:
        f.write(response.content)
        f.close()

if __name__ == '__main__':
    pool = Pool()
    pool.map(main, [i+1 for i in range(100)])
