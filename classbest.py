# -*- coding: utf-8 -*-
'''
@time: 2018/8/15 20:28
@author: Jack Luo
@file: classbest.py
'''
import pandas as pd
import requests


class Best(object):
    def __init__(self, hangye, daima, nums=30):
        self.hangye = hangye
        self.daima = daima
        self.nums = nums
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36'}
        self.url = f'https://best.zhaopin.com/api/zhaopin/zpcompanylabsum/page?insId={self.daima}&pageNumber={self.nums}&currentPage=1&type=0&at=7d409fdabf954d23af9db0ca0263db3d&rt=540cff9e9fa74cdeaa3880b42322a86b'

    def get_infos(self):
        paiming = []
        votes = []
        name = []
        resp = requests.get(self.url, headers=self.headers)
        resp = resp.json()

        for i in resp['data']['pp']:
            paiming.append(i['ranking'])
            votes.append(i['labPointCount'])
            name.append(i['companyInfo']['coName'])
        return {'排名': paiming, '数据': {'支持票': votes, f'{self.hangye}': name}}

    def get_dataframe(self):
        get = self.get_infos()
        datas = pd.DataFrame(get['数据'], index=get['排名'])
        datas.index.name = '排名'
        return datas

    def write_excel(self):
        datas = self.get_dataframe()
        datas.to_excel(w, sheet_name=f'{self.hangye}')


if __name__ == '__main__':
    hangyes = ['政府', '农林', '金融']
    daimas = [11100, 11400, 10200]
    with pd.ExcelWriter('votes.xls') as w:
        for h, d in zip(hangyes, daimas):
            datas = Best(h, d)
            datas.write_excel()
        w.save()
