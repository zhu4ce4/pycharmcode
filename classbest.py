# -*- coding: utf-8 -*-
'''
@time: 2018/8/15 20:28
@author: Jack Luo
@file: classbest.py
'''
import requests
import pandas as pd


class Best(object):
    def __init__(self, hangye, nums=30):
        self.hangye = hangye
        self.nums = nums

    def get_infos(self):
        paiming = []
        votes = []
        name = []
        url = f'https://best.zhaopin.com/api/zhaopin/zpcompanylabsum/page?insId={self.hangye}&pageNumber={self.nums}&currentPage=1&type=0&at=7d409fdabf954d23af9db0ca0263db3d&rt=540cff9e9fa74cdeaa3880b42322a86b'
        resp = requests.get(url).json()
        for i in resp['data']['pp']:
            paiming.append(i['ranking'])
            votes.append(i['labPointCount'])
            name.append(i['companyInfo']['coName'])
        return {'排名': paiming, '数据': {'支持': votes, '名称': name}}

    def df(self):
        get=self.get_infos()
        datas = pd.DataFrame(get['数据'], index=get['排名'])
        datas.index.name = '排名'
        return datas

    def pr(self):
        datas=self.df()
        print(datas)

jinrong=Best('11100')
jinrong.pr()
