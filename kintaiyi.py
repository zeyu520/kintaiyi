# -*- coding: utf-8 -*-
"""
Created on Sat Aug 27 18:11:44 2022
@author: kentang
"""
import re
import time
import itertools
from itertools import cycle
from ephem import Date
import numpy as np
from cn2an import an2cn
from taiyidict import tengan_shiji, su_dist
import config
import jieqi
from jieqi import jieqi_name
from config import *
import chart
from kinliuren import kinliuren
from taiyi_life_dict import *

class Taiyi():
    """太乙起盤主要函數"""
    def __init__(self, year, month, day, hour, minute):
        self.year = year
        self.month = month
        self.day = day
        self.hour = hour
        self.minute = minute
        #間辰
        self.door = list("開休生傷杜景死驚")

    def jigod(self, ji_style):
        """ji_style 年計、月計、日計、時計或分計"""
        return dict(zip(di_zhi, config.new_list(list(reversed(di_zhi)), "寅"))).get(self.taishui(ji_style))

    def taishui(self, ji_style):
        """太歲"""
        gang_zhi =  config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)
        return {0: gang_zhi[0][1], 1: gang_zhi[1][1], 2: gang_zhi[2][1], 3:gang_zhi[3][1], 4:gang_zhi[4][1], 5: gang_zhi[0][1],}.get(ji_style)

    def skyeyes_des(self, ji_style, taiyi_acumyear):
        """文昌始擊處境 年計、月計、日計、時計或分計；"""
        kook_text = self.kook(ji_style, taiyi_acumyear).get("文")[0]
        kook_num = self.kook(ji_style, taiyi_acumyear).get("數")
        return dict(zip(range(1,73), config.skyeyes_summary.get(kook_text))).get(kook_num)

    def skyeyes(self, ji_style, taiyi_acumyear):
        """文昌(天目)"""
        return dict(zip(range(1,73),skyeyes_dict.get(self.kook(ji_style, taiyi_acumyear).get("文")[0]))).get(int(self.kook(ji_style, taiyi_acumyear).get("數")))

    def hegod(self, ji_style):
        """合神 年計、月計、日計、時計或分計"""
        he_god = dict(zip(di_zhi, config.new_list(list(reversed(di_zhi)), "丑"))).get(self.taishui(ji_style))
        return he_god
#%% 積年
    def accnum(self, ji_style, taiyi_acumyear):
        """taiyi_acumyear積年數截法 0太乙統宗, 1太乙金鏡, 2太乙淘金歌", 3太乙局"""
        tndict = {0:10153917, 1:1936557, 2:10154193, 3:10153917 }
        tn_num = tndict.get(taiyi_acumyear)
        lunar_year = config.lunar_date_d(self.year, self.month, self.day).get("年")
        lunar_month = config.lunar_date_d(self.year, self.month, self.day).get("月")
        lunar_day = config.lunar_date_d(self.year, self.month, self.day).get("日")
        if ji_style == 0: #年計
            if lunar_year >= 0:
                return tn_num + lunar_year
            if lunar_year < 0:
                return tn_num + lunar_year + 1
        if ji_style ==1: #月計
            if lunar_year >= 0:
                accyear = tn_num + lunar_year - 1
            if lunar_year < 0:
                accyear = tn_num + lunar_year + 1
            return accyear * 12 + 2 + lunar_month
        if ji_style ==2:#日計
            diff_val = int(Date(f"{str(self.year).zfill(4)}/{str(self.month).zfill(2)}/{str(self.day).zfill(2)} {str(self.hour).zfill(2)}:00:00.00") - Date("1900/06/19 00:00:00.00"))
            if taiyi_acumyear ==0:
                ty_num = 708011105
                return ty_num + diff_val
            if taiyi_acumyear ==2:
                ty_num = 708011105 - 10153917 + tn_num
                return ty_num + diff_val
            if taiyi_acumyear ==1:
                ty_num = 708011105 - 185
                return ty_num + diff_val
            if taiyi_acumyear ==3:
                number_1 = round((lunar_year - 423 )  * (235 / 19) ,0)
                number_2 = round(number_1 * 29.5306, 0)
                number_3 = number_2 + lunar_day
                return int(number_3)
        if ji_style ==3: #時計
            diff_val_two = int(Date(f"{str(self.year).zfill(4)}/{str(self.month).zfill(2)}/{str(self.day).zfill(2)} {str(self.hour).zfill(2)}:00:00.00") - Date("1900/12/21 00:00:00.00"))
            if taiyi_acumyear ==0:
                ty_num = 708011105
                accday = ty_num + diff_val_two
                acchr = ((accday -1) * 12) + (self.hour+1)//2 +1
            if taiyi_acumyear ==2:
                ty_num = 708011105 - 10153917 + tn_num
                accday = ty_num + diff_val_two
                acchr = ((accday -1) * 12) + (self.hour+1)//2 +1
            if taiyi_acumyear ==1:
                ty_num = 708011105 - 10153917 + tn_num
                accday = ty_num + diff_val_two
                acchr = ((accday -1) * 12) + (self.hour+1)//2 -11
            if taiyi_acumyear == 3:
                tiangan = dict(zip([tuple(jiazi()[jiazi().index(i):jiazi().index(i)+6]) for i in jiazi()[0::6]], jiazi()[0::6]))
                getfut = dict(zip(jiazi()[0::6], [1,7,13,19,25,31,37,43,49,55])).get(multi_key_dict_get(tiangan, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2]))
                dgz_num = dict(zip(jiazi(), range(1,61))).get( config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2])
                zhi_num = dict(zip(config.di_zhi, range(1,13))).get(config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1])
                if tiangan != dgz_num:
                    acchr  =  ((dgz_num- getfut) * 12) + zhi_num
                if tiangan == dgz_num:
                    acchr = zhi_num
            return acchr
        if ji_style == 4: #分計
            #diff_val_two = int(Date(f"{str(self.year).zfill(4)}/{str(self.month).zfill(2)}/{str(self.day).zfill(2)} {str(self.hour).zfill(2)}:00:00.00") - Date("-1197/02/02 00:00:00.00"))
            #return int(diff_val_two - 1) * 23 + (self.minute + 1 ) // 23 -48
            diff_val_two = int(Date(f"{str(self.year).zfill(4)}/{str(self.month).zfill(2)}/{str(self.day).zfill(2)} {str(self.hour).zfill(2)}:{str(self.minute).zfill(2)}:00.00") - Date("1900/12/21 00:00:00.00"))
            if taiyi_acumyear ==0 or taiyi_acumyear ==3:
                ty_num = 708011105
                accday = ty_num + diff_val_two
                acchr = ((accday -1) * 23) + (self.hour * 10500) + (self.minute +1)
            if taiyi_acumyear ==2:
                ty_num = 708011105 - 10153917 + tn_num
                accday = ty_num + diff_val_two
                acchr = ((accday -1) * 23) + (self.hour * 10500) + (self.minute +1)
            if taiyi_acumyear ==1:
                ty_num = 708011105 - 10153917 + tn_num
                accday = ty_num + diff_val_two
                acchr = ((accday -1) * 23) + (self.hour * 10500) + (self.minute +1)
            return acchr
        return None

    #太乙命數積日數
    def taiyi_life_accum(self):
        y = calculate_value_for_year(self.year)
        gz = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)
        jie_qi = jieqi.jq(self.year, self.month, self.day, self.hour, self.minute)
        return  (jiazi_accum(gz[0]) + y + jq_accum(jie_qi) + (jieqi.jq_count_days(self.year, self.month, self.day, self.hour, self.minute) *10000)) // 10000

    def three_cai_num(self):
        accum_num = self.taiyi_life_accum()
        sky = accum_num % 720
        earth = sky % 72
        ppl = earth % 72
        return sky, earth, ppl
    
    def yeargua(self, taiyi_acumyear):
        """值年卦"""
        tynum = self.accnum(0, taiyi_acumyear) % 64
        if tynum == 0:
            tynum = 64
        return gua.get(tynum)

    def daygua(self, taiyi_acumyear):
        """值日卦"""
        tynum = self.accnum(1, taiyi_acumyear) % 646464 % 20
        if tynum == 0:
            tynum = 64
        return gua.get(tynum)

    def hourgua(self, taiyi_acumyear):
        """值時卦"""
        tynum = self.accnum(3, taiyi_acumyear) % 64 
        if tynum == 0:
            tynum = 64
        return gua.get(tynum)

    def kook(self, ji_style, taiyi_acumyear):
        """太乙局數"""
        alljq = jieqi_name
        j_q = jieqi.jq(self.year, self.month, self.day, self.hour, self.minute)
        dz = new_list(alljq, "冬至")[0:12]
        dz_num = dict(zip(new_list(alljq, "冬至")[0:12],list(range(1,13))))
        hz = new_list(alljq, "夏至")[0:12]
        hz_num = dict(zip(new_list(alljq, "夏至")[0:12],list(range(1,13))))
        jqmap = {tuple(config.new_list(alljq, "冬至")[0:12]):"冬至", tuple(config.new_list(alljq, "夏至")[0:12]):"夏至"}
        k = self.accnum(ji_style, taiyi_acumyear)%72
        if k == 0:
            k = 72
        three_year = {0:"理天", 1:"理地", 2:"理人"}.get(dict(zip(list(range(1,73)), [0,1,2] * 24)).get(k))
        if ji_style in (0, 1, 5, 2):
            dun = "陽遁"
            return {"文":f"{dun}{an2cn(k)}局", "數":k, "年":three_year, "積"+config.taiyi_name(ji_style)[0]+"數":self.accnum(ji_style, taiyi_acumyear) }
        if ji_style ==3:
            dun = {"夏至":"陰遁", "冬至":"陽遁"}.get(multi_key_dict_get(jqmap, j_q))
            return {"文":f"{dun}{an2cn(k)}局", "數":k, "年":three_year, "積"+config.taiyi_name(ji_style)[0]+"數":self.accnum(ji_style, taiyi_acumyear) }
        if ji_style == 4:
            dun = multi_key_dict_get(jqmap, j_q)
            #dund = dundict.get(dun)
            #dundict = {"夏至":{tuple(list("辰巳午未申酉")):"陽遁", tuple(list("戌亥子丑寅卯")):"陰遁"}, "冬至":{tuple(list("辰巳午未申酉")):"陰遁", tuple(list("戌亥子丑寅卯")):"陽遁"}
            #dunk = multi_key_dict_get(dund, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1])
            #if dun == "冬至":
            #    if dz_num.get(j_q) % 2 == 0:
            #            a = multi_key_dict_get({tuple(list("戌亥子丑寅卯")):"陰遁", tuple(list("辰巳午未申酉")):"陽遁"}, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1])
            #    if dz_num.get(j_q) % 2 != 0:
            #            a =multi_key_dict_get({tuple(list("申酉戌亥子丑")):"陰遁", tuple(list("寅卯辰巳午未")):"陽遁"}, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1])
            #if test == 0
            #if dun == "夏至":
            #    if hz_num.get(j_q) % 2 == 0:
            #        a = multi_key_dict_get({tuple(list("辰巳午未申酉")):"陰遁", tuple(list("戌亥子丑寅卯")):"陽遁"}, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1])
            #    if hz_num.get(j_q) % 2 != 0:
            #        a =multi_key_dict_get({tuple(list("辰巳午未申酉")):"陽遁", tuple(list("戌亥子丑寅卯")):"陰遁"}, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1])
            #return  {"文":f"{a}{an2cn(k)}局", "數":k, "年":three_year, "積"+config.taiyi_name(ji_style)[0]+"數":self.accnum(ji_style, taiyi_acumyear) }
            #dund = dundict.get(dun)
            #dunk = multi_key_dict_get(dund, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1])
            #if dun == "冬至":
            #    if config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][0] in list("甲丙戊庚壬"):
            #        a = "陽遁"
            #    else:
            #        a  = "陰遁"
            #if dun == "夏至":
            #    if config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][0] in list("甲丙戊庚壬"):
            #        a = "陰遁"
            #    else:
            #        a  = "陽遁"
            #return  {"文":f"{a}{an2cn(k)}局", "數":k, "年":three_year, "積"+config.taiyi_name(ji_style)[0]+"數":self.accnum(ji_style, taiyi_acumyear) }
            if dun == "冬至":
                if config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2][0] in list("甲丙戊庚壬"):
                    a = multi_key_dict_get( {tuple(list("申酉戌亥子丑")):"陽遁", tuple(list("寅卯辰巳午未")):"陰遁"}, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1] )
                else:
                    a = multi_key_dict_get( {tuple(list("申酉戌亥子丑")):"陰遁", tuple(list("寅卯辰巳午未")):"陽遁"}, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1] )
            if dun == "夏至":
                if config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2][0] in list("甲丙戊庚壬"):
                    a = multi_key_dict_get( {tuple(list("申酉戌亥子丑")):"陰遁", tuple(list("寅卯辰巳午未")):"陽遁"}, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1] )
                else:
                    a = multi_key_dict_get( {tuple(list("申酉戌亥子丑")):"陽遁", tuple(list("寅卯辰巳午未")):"陰遁"}, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3][1] )
            return  {"文":f"{a}{an2cn(k)}局", "數":k, "年":three_year, "積"+config.taiyi_name(ji_style)[0]+"數":self.accnum(ji_style, taiyi_acumyear) }

    
    def get_five_yuan_kook(self, ji_style, taiyi_acumyear):
        """太乙五子元局"""
        gz = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)
        try:
            return self.kook(ji_style, taiyi_acumyear).get("文")[0:2] + config.five_zi_yuan(self.kook(ji_style, taiyi_acumyear).get("數"), gz[ji_style])
        except ValueError:
            return ""

    def getepoch(self, ji_style, taiyi_acumyear):
        """求太乙的紀"""
        accnum = self.accnum(ji_style, taiyi_acumyear)
        if ji_style in (0, 1, 2):
            if accnum % 360 == 1:
                find_ji_num = 1
            else:
                find_ji_num = int((accnum % 360) // 60 + 1)
            if find_ji_num == 0:
                find_ji_num = 1
            find_ji_num2 = int(accnum % 360 % 72 % 24 / 3)
            if find_ji_num2 == 0:
                find_ji_num2 = 1
            if find_ji_num2 > 6:
                find_ji_num2 = find_ji_num2  - 6
            if find_ji_num > 6:
                find_ji_num = find_ji_num - 6
            return {"元":dict(zip(range(1,7), config.cnum[0:6])).get(find_ji_num2), "紀":dict(zip(range(1,7), config.cnum[0:6])).get(find_ji_num)}
        if ji_style == 3:
            return f"第{multi_key_dict_get(config.epochdict, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2])}紀"
        if ji_style == 4:
            return f"第{multi_key_dict_get(config.epochdict, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3])}紀"

    def getyuan(self, ji_style, taiyi_acumyear):
        """求太乙的元"""
        accnum = self.accnum(ji_style, taiyi_acumyear)
        if round(accnum % 360) == 1:
            find_ji_num = 1
        else:
            find_ji_num = int(round((accnum % 360) / 72, 0))
        fiveyuen_d = dict(zip(range(1,6), jiazi()[0::12]))
        if find_ji_num == 0:
            find_ji_num = 1
        jiyuan = fiveyuen_d.get(find_ji_num)
        return jiyuan

    def jiyuan(self, ji_style, taiyi_acumyear):
        """太乙紀元"""
        gang_zhi = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)
        if ji_style == 3:
            if taiyi_acumyear!=1:
                return f"{self.getepoch(ji_style, taiyi_acumyear)}{multi_key_dict_get(config.jiyuan_dict, gang_zhi[3])}元"
            return f"{self.getepoch(ji_style, taiyi_acumyear)}{multi_key_dict_get(config.jiyuan_dict, gang_zhi[2])}元"
        if ji_style == 4:
            return f"{self.getepoch(ji_style, taiyi_acumyear)}{multi_key_dict_get(config.jiyuan_dict, gang_zhi[3])}元"
        return f"第{self.getepoch(ji_style, taiyi_acumyear).get('紀')}紀第{self.getepoch(ji_style, taiyi_acumyear).get('元')}{self.getyuan(ji_style, taiyi_acumyear)}元"

    def ty(self, ji_style, taiyi_acumyear):
        """求太乙所在"""
        arr = np.arange(10)
        repetitions = 3
        arrangement = np.repeat(arr, repetitions)
        arrangement_r = list(reversed(arrangement))
        yy_dict = {"陽": dict(zip(range(1,73), list(itertools.chain.from_iterable([list(arrangement)[3:15]+ list(arrangement)[18:]] * 3)))),  "陰": dict(zip(range(1,73), (list(arrangement_r)[:12] + list(arrangement_r)[15:][:-3]) * 3))}
        return yy_dict.get(self.kook(ji_style, taiyi_acumyear).get("文")[0]).get(self.kook(ji_style, taiyi_acumyear).get("數"))

    def ty_gong(self, ji_style, taiyi_acumyear):
        """太乙落宮"""
        return dict(zip(range(1,73), config.taiyi_pai)).get(self.kook(ji_style, taiyi_acumyear).get("數"))

    def twenty_eightstar(self, ji_style, taiyi_acumyear):
        s_f = self.sf_num(ji_style, taiyi_acumyear)
        sf = self.sf(ji_style, taiyi_acumyear)
        c = dict(zip(new_list(sixteen, sf), new_list(su, s_f)))
        suu = dict(zip(range(1,29), su))
        snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") + 2 
        if sf == "坤":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") - 2
        if sf == "酉":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") - 3
        if sf == "亥":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") - 5
        if sf == "巳":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") + 1
        if sf == "寅":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") +4
        if sf == "卯":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") +3
        if sf == "子":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") +6
        if sf == "未":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") -1
        if sf == "申":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") -2
        if sf == "戌":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") -4
        if sf == "艮":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") +4
        if sf == "巽":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") +1
        if sf == "丑":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") +5
        if sf == "午":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") 
        if sf == "乾":
           snum = su.index(s_f)-sixteen.index(sf)+sixteen.index("巳") -5
        if snum > 28:
           snum = snum -28
        if snum < 0:
           snum = snum +28
        return new_list(su, suu.get(snum))

    def sf(self, ji_style, taiyi_acumyear):
        """始擊落宮"""
        return dict(zip(range(1,73),config.sf_list)).get(int(self.kook(ji_style, taiyi_acumyear).get("數")))

    def sf_num(self, ji_style, taiyi_acumyear):
        """始擊值"""
        sf = self.sf(ji_style, taiyi_acumyear)
        sf_z = dict(zip(gong, list(range(1,17)))).get(sf)
        sf_su = config.su_gong.get(sf)
        yc_num = dict(zip(su,list(range(1,29)))).get(self.year_chin())
        total = yc_num + sf_z
        if total > 28:
            a = dict(zip(list(range(1,29)),config.new_list(su, sf_su))).get(28)
            return config.new_list(su, a)[total - 28 -1]
        else:
            return dict(zip(list(range(1,29)),config.new_list(su, sf_su))).get(total)

    def se(self, ji_style, taiyi_acumyear):
        """定目"""
        wc,hg,ts = self.skyeyes(ji_style, taiyi_acumyear),self.hegod(ji_style),self.taishui(ji_style)
        start = config.new_list(gong1, hg)
        start1 = len(start[:start.index(ts)+1])
        start2 = config.new_list(gong1, wc)[start1-1]
        return  start2

    def home_cal(self, ji_style, taiyi_acumyear):
        """主算"""
        lnum = [8,8,3,3,4,4,9,9,2,2,7,7,6,6,1,1]
        wancheong = self.skyeyes(ji_style, taiyi_acumyear)
        wc_num = dict(zip(config.new_list(config.sixteen, "亥"), lnum)).get(wancheong)
        taiyi = self.ty(ji_style, taiyi_acumyear)
        wc_jc = list(map(lambda x: x == wancheong, jc)).count(True)
        ty_jc = list(map(lambda x: x == taiyi, tyjc)).count(True)
        wc_jc1  = list(map(lambda x: x == wancheong, jc1)).count(True)
        wc_order = config.new_list(num, wc_num)
        if wc_jc == 1 and ty_jc != 1 and wc_jc1 !=1 :
            return sum(wc_order[: wc_order.index(taiyi)]) +1
        if wc_jc !=1 and ty_jc != 1 and wc_jc1 ==1:
            return sum(wc_order[: wc_order.index(taiyi)])
        if wc_jc != 1 and ty_jc ==1 and wc_jc1 !=1:
            return sum(wc_order[: wc_order.index(taiyi)])
        if wc_jc ==1 and ty_jc ==1 and wc_jc1 !=1 and wc_jc == ty_jc and wc_jc1 == wc_jc:
            return sum(wc_order[wc_order.index(taiyi):])+1
        if wc_jc ==1 and ty_jc ==1 and wc_jc1 !=1 and wc_jc == ty_jc and wc_jc1 != wc_jc:
            return sum(wc_order[:wc_order.index(taiyi)])+1
        if wc_jc ==1 and ty_jc ==1 and wc_jc1 !=1 and wc_jc != ty_jc:
            return sum(wc_order[wc_order.index(ty_jc):])+1
        if wc_jc !=1 and ty_jc ==1 and wc_jc1 ==1 and taiyi != wc_order[wc_jc] and wc_jc1 != wc_jc:
            return sum(wc_order[: wc_order.index(taiyi)])
        if wc_jc !=1 and ty_jc ==1 and wc_jc1 ==1 and taiyi == wc_order[wc_jc] and wc_jc1 == wc_jc:
            return taiyi
        if wc_jc !=1 and ty_jc !=1 and wc_jc1 !=1 and taiyi != wc_num:
            return sum(wc_order[: wc_order.index(taiyi)])
        if wc_jc !=1 and ty_jc !=1 and wc_jc1 !=1 and taiyi == wc_num:
            return taiyi
        else:
            return taiyi

    def home_general(self, ji_style, taiyi_acumyear):
        """主大將"""
        num = self.kook(ji_style, taiyi_acumyear).get("數")
        yy = self.kook(ji_style, taiyi_acumyear).get("文")[0]
        home_cal = config.find_cal(yy, num)[0]
        if home_cal == 1:
            return self.ty(ji_style, taiyi_acumyear)
        if home_cal < 10:
            return self.home_cal(ji_style, taiyi_acumyear)
        if home_cal % 10 == 0:
            return 1
        if home_cal > 10 and home_cal < 20 :
            return home_cal - 10
        if home_cal > 20 and home_cal < 30 :
            return home_cal - 20
        if home_cal > 30 and home_cal < 40 :
            return home_cal - 30

    def home_vgen(self, ji_style, taiyi_acumyear):
        """主參將"""
        home_vg = self.home_general(ji_style, taiyi_acumyear) *3 % 10
        if home_vg ==0:
            home_vg = 5
        return home_vg

    def away_cal(self, ji_style, taiyi_acumyear):
        """主算"""
        lnum = [8,8,3,3,4,4,9,9,2,2,7,7,6,6,1,1]
        shiji = self.sf(ji_style, taiyi_acumyear)
        sf_num = dict(zip(config.new_list(config.sixteen, "亥"), lnum)).get(shiji)
        taiyi = self.ty(ji_style, taiyi_acumyear)
        sf_jc = list(map(lambda x: x == shiji, jc)).count(True)
        ty_jc = list(map(lambda x: x == taiyi, tyjc)).count(True)
        sf_jc1 = list(map(lambda x: x == shiji, jc1)).count(True)
        sf_order = config.new_list(num, sf_num)
        if sf_jc == 1 and ty_jc != 1 and sf_jc1 !=1 and sf_jc == ty_jc:
            return sum(sf_order[: sf_order.index(taiyi)])+1
        if sf_jc == 1 and ty_jc != 1 and sf_jc1 !=1 and sf_jc != ty_jc:
            return sum(sf_order[: sf_jc+1])+1
        
        if sf_jc !=1 and ty_jc != 1 and sf_jc1 ==1 and sf_jc != ty_jc:
            return sum(sf_order[: sf_order.index(taiyi)])
        if sf_jc !=1 and ty_jc != 1 and sf_jc1 ==1 and sf_jc == ty_jc and taiyi >5 and taiyi <7:
            return sum(sf_order[taiyi-2:]) 
        if sf_jc !=1 and ty_jc != 1 and sf_jc1 ==1 and sf_jc == ty_jc and taiyi >5:
            return sum(sf_order[: sf_order.index(taiyi)])
        if sf_jc !=1 and ty_jc != 1 and sf_jc1 ==1 and sf_jc == ty_jc and taiyi <5:
            return sum(sf_order[:taiyi+1])
        if sf_jc != 1 and ty_jc ==1 and sf_jc1 !=1 and ty_jc == sf_jc:
            return sum(sf_order[sf_order.index(taiyi): ])
        if sf_jc != 1 and ty_jc ==1 and sf_jc1 !=1 and ty_jc != sf_jc and sf_jc1 != sf_jc:
            return sum(sf_order[: sf_order.index(ty_jc)])
        if sf_jc != 1 and ty_jc ==1 and sf_jc1 !=1 and ty_jc != sf_jc and sf_jc1 == sf_jc:
            return sum(sf_order[: sf_order.index(taiyi)])
        if sf_jc ==1 and ty_jc ==1 and sf_jc1 !=1 and sf_jc == ty_jc:
            return sum(sf_order[: sf_order.index(taiyi)])+1
        if sf_jc ==1 and ty_jc ==1 and sf_jc1 !=1 and sf_jc != ty_jc:
            return sum(sf_order[:taiyi ])
        if sf_jc !=1 and ty_jc ==1 and sf_jc1 ==1 and sf_jc != ty_jc:
            return sum(sf_order[:sf_order.index(taiyi)])
        if sf_jc !=1 and ty_jc ==1 and sf_jc1 ==1 and sf_jc == ty_jc:
            return sum(sf_order[: sf_order.index(taiyi)])
        if sf_jc !=1 and ty_jc !=1 and sf_jc1 !=1 and sf_num != taiyi:
            return sum(sf_order[: sf_order.index(taiyi)])
        if sf_jc !=1 and ty_jc !=1 and sf_jc1 !=1 and sf_num == taiyi:
            return taiyi

    def away_general(self, ji_style, taiyi_acumyear):
        """客大將"""
        num = self.kook(ji_style, taiyi_acumyear).get("數")
        yy = self.kook(ji_style, taiyi_acumyear).get("文")[0]
        away_cal = config.find_cal(yy, num)[1]
        if away_cal == 1:
            return 1
        if away_cal < 10:
            return away_cal
        if away_cal % 10 == 0:
            return 5
        if away_cal > 10 and away_cal < 20 :
            return away_cal - 10
        if away_cal > 20 and away_cal < 30 :
            return away_cal - 20
        if away_cal > 30 and away_cal < 40 :
            return away_cal - 30

    def away_vgen(self, ji_style, taiyi_acumyear):
        """客參將"""
        away_vg = self.away_general(ji_style, taiyi_acumyear) *3 % 10
        if away_vg == 0:
            away_vg = 5
        return away_vg

    def shensha(self, ji_style, taiyi_acumyear):
        """推太乙當時法"""
        if ji_style ==3 or ji_style ==4:
            general = "貴人,螣蛇,朱雀,六合,勾陳,青龍,天空,白虎,太常,玄武,太陰,天后".split(",")
            #tiany = self.skyyi(ji_style, taiyi_acumyear).replace("兌", "酉").replace("坎", "子").replace("震","卯").replace("離","午").replace("艮", "丑")
            tiany = self.ty_gong(ji_style, taiyi_acumyear).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥")
            kook = self.kook(ji_style, taiyi_acumyear).get("文")[0]
            if kook == "陽":
                return dict(zip(config.new_list(di_zhi, tiany) , general))
            return dict(zip(config.new_list(list(reversed(di_zhi)), tiany), general))
        return "太乙時計才顯示"
        
    def set_cal(self, ji_style, taiyi_acumyear):
        """定算"""
        lnum = [8, 8, 3, 3, 4,4, 9, 9, 2, 2, 7, 7, 6, 6, 1, 1]
        setcal = self.se(ji_style, taiyi_acumyear)
        se_num = dict(zip(config.new_list(config.sixteen, "亥"), lnum)).get(setcal)
        taiyi = self.ty(ji_style, taiyi_acumyear)
        se_jc = list(map(lambda x: x == setcal, jc)).count(True)
        ty_jc = list(map(lambda x: x == taiyi, tyjc)).count(True)
        se_jc1 = list(map(lambda x: x == setcal, jc1)).count(True)
        se_order = config.new_list(num, se_num)
        if se_jc == 1 and ty_jc != 1 and se_jc1 !=1 :
            if sum(se_order[: se_order.index(taiyi)]) == 0:
                return 1
            return sum(se_order[: se_order.index(taiyi)])+1
        if se_jc !=1 and ty_jc != 1 and se_jc1 ==1:
            return sum(se_order[: se_order.index(taiyi)])
        if se_jc != 1 and ty_jc ==1 and se_jc1 !=1:
            return sum(se_order[: se_order.index(taiyi)])
        if se_jc ==1 and ty_jc ==1 and se_jc1 !=1 :
            return sum(se_order[: se_order.index(taiyi)])+1
        if se_jc !=1 and ty_jc ==1 and se_jc1 ==1 :
            if sum(se_order[: se_order.index(taiyi)]) == 0:
                return 1
            return sum(se_order[: se_order.index(taiyi)])
        if se_jc !=1 and ty_jc !=1 and se_jc1 !=1 :
            return sum(se_order[: se_order.index(taiyi)])
        if se_jc !=1 and ty_jc !=1 and se_jc1 !=1 and se_num != taiyi:
            return sum(se_order[: se_order.index(taiyi)])
        if se_jc !=1 and ty_jc !=1 and se_jc1 !=1 and se_num == taiyi:
            return taiyi

    def set_general(self, ji_style, taiyi_acumyear):
        """定大將"""
        set_g = self.set_cal(ji_style, taiyi_acumyear)  % 10
        if set_g == 0:
            set_g = 5
        return set_g

    def set_vgen(self, ji_style, taiyi_acumyear):
        """定參將"""
        set_vg =  self.set_general(ji_style, taiyi_acumyear) *3 % 10
        if set_vg == 0:
            set_vg = 5
        return set_vg

    def sixteen_gong(self, ji_style, taiyi_acumyear):
        """十六宮各星將與十精分佈"""
        if ji_style != 4:
            dict1 = [{self.skyeyes(ji_style, taiyi_acumyear):"文昌"},
                     {self.taishui(ji_style):"太歲"},
                     {self.hegod(ji_style):"合神"},
                     {self.jigod(ji_style):"計神"},
                     {self.sf(ji_style, taiyi_acumyear):"始擊"},
                     {self.se(ji_style, taiyi_acumyear):"定計"}, 
                     {self.kingbase(ji_style, taiyi_acumyear):"君基"}, 
                     {self.officerbase(ji_style, taiyi_acumyear):"臣基"}, 
                     {self.pplbase(ji_style, taiyi_acumyear):"民基"},
                     {self.fgd(ji_style, taiyi_acumyear):"四神"},
                     {self.skyyi(ji_style, taiyi_acumyear):"天乙"},
                     {self.earthyi(ji_style, taiyi_acumyear):"地乙"},
                     {self.zhifu(ji_style, taiyi_acumyear):"直符"},
                     {self.flyfu(ji_style, taiyi_acumyear):"飛符"},
                     {config.tian_wang(self.accnum(ji_style,taiyi_acumyear)):"天皇"},
                     {config.tian_shi(self.accnum(ji_style,taiyi_acumyear)):"天時"},
                     {config.wuxing(self.accnum(ji_style,taiyi_acumyear)):"五行"},
                     {config.kingfu(self.accnum(ji_style,taiyi_acumyear)):"帝符"},
                     {config.taijun(self.accnum(ji_style,taiyi_acumyear)):"太尊"},
                     {config.num2gong(config.wufu(self.accnum(ji_style,taiyi_acumyear))):"五福"},
                     #{self.ty_gong(ji_style, taiyi_acumyear):"太乙"},
                     {config.num2gong(self.home_general(ji_style, taiyi_acumyear)):"主大"},  
                     {config.num2gong(self.home_vgen(ji_style, taiyi_acumyear)):"主參"},
                     {config.num2gong(self.away_general(ji_style, taiyi_acumyear)):"客大"},  
                     {config.num2gong(self.away_vgen(ji_style, taiyi_acumyear)):"客參"},
                     {config.num2gong(config.threewind(self.accnum(ji_style,taiyi_acumyear))):"三風"},  
                     {config.num2gong(config.fivewind(self.accnum(ji_style,taiyi_acumyear))):"五風"},
                     {config.num2gong(config.eightwind(self.accnum(ji_style,taiyi_acumyear))):"八風"},  
                     {config.num2gong(config.flybird(self.accnum(ji_style,taiyi_acumyear))):"飛鳥"},
                     {config.num2gong(config.bigyo(self.accnum(ji_style,taiyi_acumyear))):"大游"},
                     {config.num2gong(config.smyo(self.accnum(ji_style,taiyi_acumyear))):"小游"},  
                     #{config.leigong(self.ty(ji_style, taiyi_acumyear)):"雷公"},  
                     {config.yangjiu(self.year, self.month, self.day):"陽九"}, 
                     {config.baliu(self.year, self.month, self.day):"百六"},
                     #{config.lijin(self.year, self.month, self.day, self.hour, self.minute):"臨津"}, 
                     #{config.lion(self.year, self.month, self.day, self.hour, self.minute):"獅子"}, 
                     #{config.cloud(self.home_general(ji_style, taiyi_acumyear)):"白雲"},
                     #{config.tiger(self.ty(ji_style, taiyi_acumyear)):"猛虎"}, 
                     #{config.returnarmy(self.away_general(ji_style, taiyi_acumyear)):"回軍"}, 
                     {config.num2gong(self.ty(ji_style, taiyi_acumyear)):"太乙"}, 
                     ]
        if ji_style == 4:
            dict1 = [{self.skyeyes(ji_style, taiyi_acumyear):"文昌"},
                     {self.hegod(ji_style):"合神"},
                     {self.jigod(ji_style):"計神"},
                     {self.sf(ji_style, taiyi_acumyear):"始擊"},
                     {self.kingbase(ji_style, taiyi_acumyear):"君基"}, 
                     {self.officerbase(ji_style, taiyi_acumyear):"臣基"}, 
                     {self.pplbase(ji_style, taiyi_acumyear):"民基"},
                     {self.fgd(ji_style, taiyi_acumyear):"四神"},
                     {self.skyyi(ji_style, taiyi_acumyear):"天乙"},
                     {self.earthyi(ji_style, taiyi_acumyear):"地乙"},
                     {self.zhifu(ji_style, taiyi_acumyear):"直符"},
                     {self.flyfu(ji_style, taiyi_acumyear):"飛符"},
                     {config.tian_wang(self.accnum(ji_style,taiyi_acumyear)):"天皇"},
                     {config.wuxing(self.accnum(ji_style,taiyi_acumyear)):"五行"},
                     {config.kingfu(self.accnum(ji_style,taiyi_acumyear)):"帝符"},
                     {config.taijun(self.accnum(ji_style,taiyi_acumyear)):"太尊"},
                     {config.num2gong(config.wufu(self.accnum(ji_style,taiyi_acumyear))):"五福"},
                     {config.num2gong(self.home_general(ji_style, taiyi_acumyear)):"主大"},  
                     {config.num2gong(self.home_vgen(ji_style, taiyi_acumyear)):"主參"},
                     {config.num2gong(self.away_general(ji_style, taiyi_acumyear)):"客大"},  
                     {config.num2gong(self.away_vgen(ji_style, taiyi_acumyear)):"客參"},
                     {config.num2gong(config.threewind(self.accnum(ji_style,taiyi_acumyear))):"三風"},  
                     {config.num2gong(config.fivewind(self.accnum(ji_style,taiyi_acumyear))):"五風"},
                     {config.num2gong(config.eightwind(self.accnum(ji_style,taiyi_acumyear))):"八風"},  
                     {config.num2gong(config.flybird(self.accnum(ji_style,taiyi_acumyear))):"飛鳥"},
                     {config.num2gong(self.ty(ji_style, taiyi_acumyear)):"太乙"}, 
                     ]
        res = {"巳":"", "午":"", "未":"", "坤":"", "申":"", "酉":"", "戌":"", "乾":"", "亥":"", "子":"", "丑":"", "艮":"","寅":"", "卯":"", "辰":"", "巽":"","中":""}
        for dict in dict1:
            for list in dict:
                if list in res:
                    try:
                        res[list] += (dict[list])
                    except TypeError:
                        pass
                else:
                    try:
                        res[list] = dict[list]
                    except TypeError:
                        pass
        rres = str(res.values())[11:].replace("([","").replace("'","").replace("])","").replace(" ", "").split(",")
        rrres = [re.findall("..", i) for i in rres]
        overall = str(res.keys())[11:].replace("([","").replace("'","").replace("])","").replace(" ", "").split(",")
        return {overall[i]:rrres[i] for i in range(0,17)}

    def sixteen_gong1(self, ji_style, taiyi_acumyear):
        """十六星分佈"""
        dict1 = [{self.skyeyes(ji_style, taiyi_acumyear).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥").replace("中", "辰"):"文昌"},
                 {self.jigod(ji_style).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥").replace("中", "辰"):"計神"},
                 {self.sf(ji_style, taiyi_acumyear).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥").replace("中", "辰"):"始擊"},
                 {self.kingbase(ji_style, taiyi_acumyear).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥"):"君基"}, 
                 {self.officerbase(ji_style, taiyi_acumyear).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥").replace("中", "辰"):"臣基"}, 
                 {self.pplbase(ji_style, taiyi_acumyear).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥").replace("中", "辰"):"民基"},
                 {self.fgd(ji_style, taiyi_acumyear).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥").replace("中", "辰"):"四神"},
                 {self.skyyi(ji_style, taiyi_acumyear).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥").replace("中", "辰"):"天乙"},
                 {self.earthyi(ji_style, taiyi_acumyear).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥").replace("中", "辰"):"地乙"},
                 {self.flyfu1(ji_style, taiyi_acumyear).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥").replace("中", "辰"):"飛符"},
                 {config.num2gong_life(config.wufu(self.accnum(ji_style,taiyi_acumyear))).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥"):"五福"},
                 {config.num2gong_life(self.home_general(ji_style, taiyi_acumyear)).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥"):"主大"},  
                 {config.num2gong_life(self.home_vgen(ji_style, taiyi_acumyear)).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥"):"主參"},
                 {config.num2gong_life(self.away_general(ji_style, taiyi_acumyear)).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥"):"客大"},  
                 {config.num2gong_life(self.away_vgen(ji_style, taiyi_acumyear)).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥"):"客參"},
                 {config.num2gong_life(config.smyo(self.accnum(ji_style,taiyi_acumyear))).replace("巽","辰").replace("坤","申").replace("艮","丑").replace("乾","亥"):"小游"},  
                 ]
        res = {"巳":"", "午":"", "未":"", "申":"", "酉":"", "戌":"", "亥":"", "子":"", "丑":"", "寅":"", "卯":"", "辰":"","中":""}
        for dict in dict1:
            for list in dict:
                if list in res:
                    try:
                        res[list] += (dict[list])
                    except TypeError:
                        pass
                else:
                    try:
                        res[list] = dict[list]
                    except TypeError:
                        pass
        rres = str(res.values())[11:].replace("([","").replace("'","").replace("])","").replace(" ", "").split(",")
        rrres = [re.findall("..", i) for i in rres]
        overall = str(res.keys())[11:].replace("([","").replace("'","").replace("])","").replace(" ", "").split(",")
        return {overall[i]:rrres[i] for i in range(0,13)}
           
    def gen_gong(self, ji_style, taiyi_acumyear):
        if ji_style in [0,1,2]:
            return chart.gen_chart( list(self.sixteen_gong( ji_style, taiyi_acumyear).values())[-1], self.geteightdoors_text2(ji_style, taiyi_acumyear), list(self.sixteen_gong( ji_style, taiyi_acumyear).values())[:-1])
        if ji_style in [3,4]:
            #j_q = jieqi.jq(self.year, self.month, self.day, self.hour, self.minute)
            #d = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2]
            #h = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[2]
            #m = config.lunar_date_d(self.year, self.month, self.day).get("月")
            #sg = [ kinliuren.Liuren(j_q, m, d, h).result(0).get("地轉天將").get(i) for i in list("巳午未申酉戌亥子丑寅卯辰")]
            dict1 = self.shensha(ji_style, taiyi_acumyear)
            res = {"巳":" ", "午":" ", "未":" ", "坤":" ", "申":" ", "酉":" ", "戌":" ", "乾":" ", "亥":" ", "子":" ", "丑":" ", "艮":" ","寅":" ", "卯":" ", "辰":" ", "巽":" "}
            res.update(dict1)
            sg = list(res.values())
            return chart.gen_chart_hour( list(self.sixteen_gong( ji_style, taiyi_acumyear).values())[-1], self.geteightdoors_text2(ji_style, taiyi_acumyear), sg, list(self.sixteen_gong( ji_style, taiyi_acumyear).values())[:-1], self.twenty_eightstar(ji_style, taiyi_acumyear))

    def gen_life_gong(self, sex):
        res = {"巳":" ", "午":" ", "未":" ", "申":" ", "酉":" ", "戌":" ", "亥":" ", "子":" ", "丑":" ","寅":" ", "卯":" ", "辰":" "}
        dict1 = self.taiyi_life(sex).get("十二命宮排列")
        res.update(dict1)
        sg = list(res.values())
        return chart.gen_chart_life( list(self.sixteen_gong1(3,0).values())[-1], sg, list(self.sixteen_gong1(3,0).values())[:-1])

    def gen_life_gong_list(self, sex):
        res = {"巳":" ", "午":" ", "未":" ", "申":" ", "酉":" ", "戌":" ", "亥":" ", "子":" ", "丑":" ","寅":" ", "卯":" ", "辰":" "}
        dict1 = self.taiyi_life(sex).get("十二命宮排列")
        res.update(dict1)
        sg = list(res.values())
        return  list(self.sixteen_gong1(3,0).values())[-1], sg, list(self.sixteen_gong1(3,0).values())[:-1]

    def convert_gongs_text(self, a, b):
        c = {}
        for key in set(a.keys()).union(b.keys()):
            value_a = a.get(key, [])
            value_b = b.get(key, [])
            if isinstance(value_a, list) and isinstance(value_b, list):
                c[key] = value_a + [value_b]
            else:
                c[key] = value_a if value_a else value_b
        text_output = ""
        for key, value in c.items():
            if isinstance(value, list):
                value_str = ', '.join(map(str, value))
                text_output += f"【{key}】\n{value_str}\n\n"
            else:
                text_output += f"【{key}】\n{value}\n\n"
        return text_output.replace('[', '').replace(']', '').replace(',', '').replace("'","")

    def gongs_discription_text(self, sex):
        alld = self.gongs_discription_list(sex)
        combined_dict = {}
        for category, subcategories in alld.items():
            combined_dict[category] = []
            for subcategory in subcategories:
                if subcategory in twelve_gong_stars[category]:
                    combined_dict[category].append(twelve_gong_stars[category][subcategory])
        formatted_text = ""
        for key, value in combined_dict.items():
            formatted_text += f"{key}:\n"
            if value:
                formatted_text += "\n".join([f"{line}\n" for line in value])
            formatted_text += "\n"
        return formatted_text
        
    def twostar_disc(self, sex):
        a = twostars
        b = self.gongs_discription_list(sex)
        b = {key: [''.join(value)] for key, value in b.items()}
        c = {}
        for key, values in b.items():
            c[key] = []
            for val in values:
                sub_dict = [ k+"同宮。" + a[k] for k in a if k in val]
                c[key].append(sub_dict)
        for key, values in c.items():
            c[key] = [item for item in values[0] if item]  # Remove empty lists
        return c
    
    def gongs_discription_list(self, sex):
        sixteengongs = self.sixteen_gong1(3,0)
        t = self.gen_life_gong_list(sex)[1]
        stars = self.gen_life_gong_list(sex)[2]
        alld =  dict(zip(t, stars))
        for key, value in alld.items():
            if not value:
                alld[key] = ["空格"]
        return alld

    def gongs_discription(self, sex):
        alld = self.gongs_discription_list(sex)
        combined_dict = {}
        for category, subcategories in alld.items():
            combined_dict[category] = []
            for subcategory in subcategories:
                if subcategory in twelve_gong_stars[category]:
                    combined_dict[category].append(twelve_gong_stars[category][subcategory])
        return combined_dict

    def sixteen_gong2(self, ji_style, taiyi_acumyear):
        original_dict = self.sixteen_gong1(ji_style, taiyi_acumyear)
        c = "五福,君基,臣基,民基,文昌,計神,小游,主大,客大,主參,客參,始擊,飛符,四神,天乙,地乙".split(",")
        a = {star: key for key, values in original_dict.items() for star in values if star in c}
        d = dict(zip(di_zhi, range(0,13)))
        for star, gong_value in a.items():
            a[star] = d[gong_value]
        return  a
    
    def stars_descriptions(self, ji_style, taiyi_acumyear):
        starszhi = self.sixteen_gong2(ji_style, taiyi_acumyear)
        c = "五福,君基,臣基,民基,文昌,計神,小游,主大,客大,主參,客參,始擊,飛符,四神,天乙,地乙".split(",")
        allstar = {}
        for i in c:
            a = {i:stars_twelve.get(i)[starszhi.get(i)]}
            allstar.update(a)
        return allstar

    def stars_descriptions_text(self, ji_style, taiyi_acumyear):
        alld = self.stars_descriptions(ji_style, taiyi_acumyear)
        text = ""
        for key, value in alld.items():
            text += f"【{key}】\n{value}\n\n"
        return text
    
    def year_chin(self):
        """太歲禽星"""
        chin_28_stars_code = dict(zip(range(1,29), su))
        year = config.lunar_date_d(self.year, self.month, self.day).get("年")
        if config.lunar_date_d(self.year, self.month, self.day).get("月") == "十二月" or config.lunar_date_d(self.year, self.month, self.day).get("月") == "十一月":
            if jieqi.jq(self.year, self.month, self.day, self.hour, self.minute) == "立春":
                get_year_chin_number = (int(year)+15) % 28 #求年禽之公式為西元年加15除28之餘數
                if get_year_chin_number == int(0):
                    get_year_chin_number = int(28)
                year_chin = chin_28_stars_code.get(get_year_chin_number) #年禽
            else:
                get_year_chin_number = (int(year-1)+15) % 28 #求年禽之公式為西元年加15除28之餘數
                if get_year_chin_number == int(0):
                    get_year_chin_number = int(28)
                    year_chin = chin_28_stars_code.get(get_year_chin_number) #年禽
        if config.lunar_date_d(self.year, self.month, self.day).get("月") != "十二月" or config.lunar_date_d(self.year, self.month, self.day).get("月") == "十一月":
            get_year_chin_number = (int(year)+15) % 28 #求年禽之公式為西元年加15除28之餘數
            if get_year_chin_number == int(0):
                get_year_chin_number = int(28)
            year_chin = chin_28_stars_code.get(get_year_chin_number) #年禽
        return year_chin

    def kingbase(self, ji_style, taiyi_acumyear):
        """君基"""
        king_base = (self.accnum(ji_style, taiyi_acumyear) +250) % 360 // 30
        if king_base == 0:
            king_base = 1
        return  dict(zip(range(1,13), config.new_list(di_zhi, "午"))).get(int(king_base))
        
    def officerbase(self, ji_style, taiyi_acumyear):
        """臣基"""
        return dict(zip(range(1,73), cycle(config.officer_base))).get(self.kook(ji_style, taiyi_acumyear).get("數"))

    def pplbase(self, ji_style, taiyi_acumyear):
        """民基"""
        return dict(zip(range(1,73), cycle(config.new_list(di_zhi,"申")))).get(self.kook(ji_style, taiyi_acumyear).get("數"))

    def fgd(self, ji_style, taiyi_acumyear):
        """四神"""
        return dict(zip(range(1,73), cycle(list(config.four_god)))).get(self.kook(ji_style, taiyi_acumyear).get("數"))

    def skyyi(self, ji_style, taiyi_acumyear):
        """天乙"""
        return dict(zip(range(1,73), cycle(list(config.sky_yi)))).get(self.kook(ji_style, taiyi_acumyear).get("數"))

    def earthyi(self, ji_style, taiyi_acumyear):
        """地乙"""
        return dict(zip(range(1,73), cycle(list(config.earth_yi)))).get(self.kook(ji_style, taiyi_acumyear).get("數"))

    def zhifu(self, ji_style, taiyi_acumyear):
        """直符"""
        return dict(zip(range(1,73), cycle(list(config.zhi_fu)))).get(self.kook(ji_style, taiyi_acumyear).get("數"))

    def flyfu(self, ji_style, taiyi_acumyear):
        """飛符"""
        fly = self.accnum(ji_style, taiyi_acumyear) % 360 % 36 / 3
        fly_fu = dict(zip(range(1,13), config.new_list(di_zhi, "辰"))).get(int(fly))
        if fly_fu == 0 or fly_fu is None:
            fly_fu = "中"
        return fly_fu

    def flyfu1(self, ji_style, taiyi_acumyear):
        """飛符"""
        fly = self.accnum(ji_style, taiyi_acumyear) % 360 % 36 / 3
        fly_fu = dict(zip(range(1,13), config.new_list(di_zhi, "辰"))).get(int(fly))
        if fly_fu == 0 or fly_fu is None:
            fly_fu = "辰"
        return fly_fu

    def gudan(self, ji_style, taiyi_acumyear):
        """推孤單以占成敗"""
        ty_num = self.ty( ji_style, taiyi_acumyear)
        ying_yang = {tuple(1,3,7,9):"單陽",  tuple(2,4,6,8):"單陰"}
        #def_ty = multi_key_dict_get({tuple(1,3,7,9):"單陽",  tuple(2,4,6,8):"單陰"}, ty_num)
        #《經》曰：算孤單，以占主客成敗。一、三、七、九為單陽；二、四、六、八為單陰，一十、三十為孤陽；單陽並孤陽為重陽，單陰並孤陰為重陰。單陰算，並不利下，不利客；單陽算，不利上，不利主人也。
        homecal = str(self.home_cal( ji_style, taiyi_acumyear))
        awaycal = str(self.away_cal( ji_style, taiyi_acumyear) )
        description = {"單陰":"單陰算，並不利下，不利客。", "單陽":"單陽算，不利上，不利主人也。"}
        if len(homecal) == 1:
            one_digit = multi_key_dict_get(ying_yang, int(homecal))
            if one_digit == "單陽":
                h_result = "主筭得單陽，不利上，不利主人也。"
            if one_digit == "單陰":
                h_result = "主筭得單陰，沒不利也。"
        if len(awaycal) == 1:
            one_digit = multi_key_dict_get(ying_yang, int(awaycal))
            if one_digit == "單陽":
                a_result = "客筭得單陽，沒不利也。"
            if one_digit == "單陰":
                a_result = "客筭得單陰，不利上，不利客人也。"
        if len(homecal) == 2:
            if int(homecal[1]) == 1 or int(homecal[1]) == 3:
               two_digit = "孤陽"
            if int(homecal[1]) != 1 and int(homecal[1]) != 3:
               two_digit = "孤陰"
            first_digit = multi_key_dict_get(ying_yang, int(homecal[0]))
            if two_digit == "孤陰" and first_digit == "單陰":
                return "主算為單陰並孤陰，為重陰。"
            if two_digit == "孤陽" and first_digit == "單陰":
                return "主算為單陰並孤陽，沒不利。"
            if two_digit == "孤陰" and first_digit == "單陽":
                return "主算為單陽並孤陰，沒不利。"
            if two_digit == "孤陽" and first_digit == "單陽":
                return "主算為單陽並孤陽，為重陽。"
        if len(awaycal) == 2:
            if int(awaycal[1]) == 1 or int(awaycal[1]) == 3:
               two_digit = "孤陽"
            if int(awaycal[1]) != 1 and int(awaycal[1]) != 3:
               two_digit = "孤陰"
            first_digit = multi_key_dict_get(ying_yang, int(awaycal[0]))
            if two_digit == "孤陰" and first_digit == "單陰":
                return "客算為單陰並孤陰，為重陰。"
            if two_digit == "孤陽" and first_digit == "單陰":
                return "客算為單陰並孤陽，沒不利。"
            if two_digit == "孤陰" and first_digit == "單陽":
                return "客算為單陽並孤陰，沒不利。"
            if two_digit == "孤陽" and first_digit == "單陽":
                return "客算為單陽並孤陽，為重陽。"

    def tui_harmony(self, ji_style, taiyi_acumyear):
        """推陰遁和不和"""
        ty_num = self.ty( ji_style, taiyi_acumyear)
        homecal = self.home_cal( ji_style, taiyi_acumyear)
        awaycal = self.away_cal( ji_style, taiyi_acumyear) 

        return 

    def tui_danger(self, ji_style, taiyi_acumyear):
        """推陰陽以占厄會"""
        tai_yi = self.ty(ji_style, taiyi_acumyear)
        tyg = num2gong(self.ty(ji_style, taiyi_acumyear))
        homecal = self.home_cal( ji_style, taiyi_acumyear) 
        awaycal = self.away_cal( ji_style, taiyi_acumyear) 
        tyd = multi_key_dict_get({tuple([8,3,4,9]): "太乙在陽宮。", tuple([1,2,6,7]): "太乙在陰宮。"}, tai_yi)
        if homecal % 2 != 0 and tyd == "太乙在陽宮。":
            hr = "太乙在陽宮，主筭得奇，為重陽，厄在火，主厄。"
        if homecal % 2 != 0 and tyd != "太乙在陽宮。":
            hr = "太乙在陰宮，主筭得奇，主沒厄。"
        if homecal % 2 == 0 and tyd != "太乙在陰宮。":
            hr = "太乙在陽宮，主筭得偶，主沒厄。"
        if homecal % 2 == 0 and tyd == "太乙在陰宮。":
            hr = "太乙在陰宮，主筭得偶，為重陰，厄在水，主厄。"
        if awaycal % 2 != 0 and tyd == "太乙在陽宮。":
            ar = "太乙在陽宮，客筭得奇，為重陽，厄在火，客厄。"
        if awaycal % 2 != 0 and tyd != "太乙在陽宮。":
            ar = "太乙在陰宮，客筭得奇，客沒厄。"
        if awaycal % 2 == 0 and tyd != "太乙在陰宮。":
            ar = "太乙在陽宮，客筭得偶，客沒厄。"
        if awaycal % 2 == 0 and tyd == "太乙在陰宮。":
            ar = "太乙在陰宮，客筭得偶，為重陰，厄在水，客厄。"
        return hr + ar
    
    def ty_gong_dist(self, ji_style, taiyi_acumyear):
        """太乙在天外地內法"""
        tai_yi = self.ty(ji_style, taiyi_acumyear)
        tyg = num2gong(self.ty(ji_style, taiyi_acumyear))
        return multi_key_dict_get({tuple([1,8,3,4]): "太乙在"+tyg+"，助主。", tuple([9,2,6,7]): "太乙在"+tyg+"，助客。"}, tai_yi)

    def threedoors(self, ji_style, taiyi_acumyear):
        """推三門具不具"""
        taiyi = self.ty(ji_style, taiyi_acumyear)
        eightd = self.geteightdoors(ji_style, taiyi_acumyear)
        door = eightd.get(taiyi)
        if door in list("休生開"):
            return "三門不具。"
        return "三門具。"

    def fivegenerals(self, ji_style, taiyi_acumyear):
        """推五將發不發"""
        home_general = self.home_general(ji_style, taiyi_acumyear)
        away_general = self.away_general(ji_style, taiyi_acumyear)
        if self.skyeyes_des(ji_style, taiyi_acumyear) == "" and home_general != 5 and away_general != 5:
            return "五將發。"
        if home_general == 5:
            return "主將主參不出中門，杜塞無門。"
        if away_general == 5:
            return "客將客參不出中門，杜塞無門。"
        return self.skyeyes_des(ji_style, taiyi_acumyear)+"。五將不發。"

    def wc_n_sj(self, ji_style, taiyi_acumyear):
        """推主客相闗法"""
        wan_c = self.skyeyes(ji_style, taiyi_acumyear)
        shi_ji = self.sf(ji_style, taiyi_acumyear)
        wc_f = Ganzhiwuxing(wan_c)
        sj_f = Ganzhiwuxing(shi_ji)
        home_g = self.home_general(ji_style, taiyi_acumyear)
        tai_yi = self.ty(ji_style, taiyi_acumyear)
        hguan = multi_key_dict_get(nayin_wuxing, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[3])
        if hguan == wc_f:
            guan = "主關"
        if hguan == sj_f:
            guan = "客關"
        else:
            guan = "關"
        relation = multi_key_dict_get(wuxing_relation_2, wc_f+sj_f)
        if relation == "我尅" and tai_yi == home_g:
            return "主將囚，不利主"
        if relation == "我尅" and tai_yi != home_g:
            return  "主尅客，主勝"
        if relation == "尅我":
            return guan + "得主人，客勝"
        if relation in ["比和","生我","我生"]:
            return guan + relation + "，和"

    
    def geteightdoors(self, ji_style, taiyi_acumyear):
        """推八門分佈"""
        tai_yi = self.ty(ji_style, taiyi_acumyear)
        new_ty_order = config.new_list([8,3,4,9,2,7,6,1], tai_yi)
        doors  = config.new_list(self.door, config.eight_door(self.accnum(ji_style, taiyi_acumyear)))
        if ji_style != 3:
            return dict(zip(new_ty_order, doors))
        if ji_style == 3:
            alljq = jieqi_name
            j_q = jieqi.jq(self.year, self.month, self.day, self.hour, self.minute)
            jqmap = {tuple(config.new_list(alljq, "冬至")[0:12]):"冬至", tuple(config.new_list(alljq, "夏至")[0:12]):"夏至"}
            accu_num = self.accnum(ji_style, taiyi_acumyear)
            dun = multi_key_dict_get(jqmap, j_q)
            if dun == "夏至":    
                num = accu_num % 120 % 30
                if num > 8:
                    num = num %8
                if num ==0:
                    num =8
                new_num = dict(zip(range(1,9), new_ty_order)).get(num)
                return dict(zip(config.new_list(new_ty_order, new_num), doors)) 
            if dun == "冬至":
                num = accu_num % 240 % 30
                if num > 8:
                    num = num %8
                if num ==0:
                    num =8
                new_num = dict(zip(range(1,9), new_ty_order)).get(num)
                return dict(zip(config.new_list(new_ty_order, new_num), doors)) 

    def geteightdoors_text(self, ji_style, taiyi_acumyear):
        k = [an2cn(i) for i in list(self.geteightdoors(ji_style, taiyi_acumyear).keys())]
        v = list(self.geteightdoors(ji_style, taiyi_acumyear).values())
        eightdoors = dict(zip(k,v))
        return str(eightdoors)[1:-1].replace("'", "").replace(",", " |")

    def geteightdoors_text2(self, ji_style, taiyi_acumyear):
        k = [an2cn(i) for i in list(self.geteightdoors(ji_style, taiyi_acumyear).keys())]
        v = list(self.geteightdoors(ji_style, taiyi_acumyear).values())
        eightdoors = dict(zip(k,v))
        eightddors_status = dict(zip(k, list(jieqi.gong_wangzhuai().values())))
        return [[i,eightdoors.get(i)+"門", eightddors_status.get(i)] for i in new_list(list(eightdoors.keys()), "二")]

    def taiyi_life(self, sex):
        twelve_gongs = "命宮,兄弟,妻妾,子孫,財帛,田宅,官祿,奴僕,疾厄,福德,相貌,父母".split(",")
        gz = config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)
        yz = gz[0][1]
        mz = gz[1][1]
        num = di_zhi.index(yz)
        yy = multi_key_dict_get({tuple(di_zhi[0::2]):"陽", tuple(di_zhi[1::2]):"陰"}, yz)
        direction =  multi_key_dict_get({("男陽","女陰"):"順", ("男陰", "女陽"):"逆"}, sex+yy)
        arrangelist = {"順":new_list(new_list(di_zhi,yz), mz), "逆":new_list(list(reversed(new_list(di_zhi,yz))), mz)}.get(direction)
        pan = {
                "性別":"{}{}".format(yy,sex),
                "出生日期":config.gendatetime(self.year, self.month, self.day, self.hour, self.minute),
                "出生干支":gangzhi(self.year, self.month, self.day, self.hour, self.minute),
                "農曆":config.lunar_date_d(self.year, self.month, self.day),
                "紀元":self.jiyuan(0,0),
                "太歲":self.taishui(0),
                "命局":self.kook(0,0),
                "十二命宮排列":dict(zip(arrangelist, twelve_gongs)),
                "陽九":config.yangjiu(self.year, self.month, self.day),
                "百六":config.baliu(self.year, self.month, self.day),
                "太乙落宮":self.ty(0,0),
                "太乙":self.ty_gong(0,0),
                "天乙":self.skyyi(0,0),
                "地乙":self.earthyi(0,0),
                "四神":self.fgd(0,0),
                "直符":self.zhifu(0,0),
                "文昌":[self.skyeyes(0,0), self.skyeyes_des(0,0)],
                "始擊":self.sf(0,0),
                "主算":[self.home_cal(0,0), config.cal_des(self.home_cal(0,0))],
                "主將":self.home_general(0,0),
                "主參":self.home_vgen(0,0),
                "客算":[self.away_cal(0,0), config.cal_des(self.away_cal(0,0))],
                "客將":self.away_general(0,0),
                "客參":self.away_vgen(0,0),
                "定算":[self.set_cal(0,0), config.cal_des(self.set_cal(0,0))],
                "合神":self.hegod(0),
                "計神":self.jigod(0),
                "定目":self.se(0,0),
                "君基":self.kingbase(0,0),
                "臣基":self.officerbase(0,0),
                "民基":self.pplbase(0,0),
                "五福":config.wufu(self.accnum(0,0)),
                "帝符":config.kingfu(self.accnum(0,0)),
                "太尊":config.taijun(self.accnum(0,0)),
                "飛鳥":config.flybird(self.accnum(0,0)),
                "三風":config.threewind(self.accnum(0,0)),
                "五風":config.fivewind(self.accnum(0,0)),
                "八風":config.eightwind(self.accnum(0,0)),
                "大游":config.bigyo(self.accnum(0,0)),
                "小游":config.smyo(self.accnum(0,0))}
        return pan
    
    def pan(self, ji_style, taiyi_acumyear):
        """起盤詳細內容"""
        return {
                "太乙計":config.taiyi_name(ji_style),
                "太乙公式類別":config.ty_method(taiyi_acumyear),
                "公元日期":config.gendatetime(self.year, self.month, self.day, self.hour, self.minute),
                "干支":gangzhi(self.year, self.month, self.day, self.hour, self.minute),
                "農曆":config.lunar_date_d(self.year, self.month, self.day),
                "年號":kingyear(config.lunar_date_d(self.year, self.month, self.day).get("年")),
                "紀元":self.jiyuan(ji_style, taiyi_acumyear),
                "太歲":self.taishui(ji_style),
                "局式":self.kook(ji_style, taiyi_acumyear),
                "五子元局":self.get_five_yuan_kook(ji_style, taiyi_acumyear),
                "陽九":config.yangjiu(self.year, self.month, self.day),
                "百六":config.baliu(self.year, self.month, self.day),
                "太乙落宮":self.ty(ji_style, taiyi_acumyear),
                "太乙":self.ty_gong(ji_style, taiyi_acumyear),
                "天乙":self.skyyi(ji_style, taiyi_acumyear),
                "地乙":self.earthyi(ji_style, taiyi_acumyear),
                "四神":self.fgd(ji_style, taiyi_acumyear),
                "直符":self.zhifu(ji_style, taiyi_acumyear),
                "文昌":[self.skyeyes(ji_style, taiyi_acumyear), self.skyeyes_des(ji_style, taiyi_acumyear)],
                "始擊":self.sf(ji_style, taiyi_acumyear),
                "主算":[self.home_cal(ji_style, taiyi_acumyear), config.cal_des(self.home_cal(ji_style, taiyi_acumyear))],
                "主將":self.home_general(ji_style, taiyi_acumyear),
                "主參":self.home_vgen(ji_style, taiyi_acumyear),
                "客算":[self.away_cal(ji_style, taiyi_acumyear), config.cal_des(self.away_cal(ji_style, taiyi_acumyear))],
                "客將":self.away_general(ji_style, taiyi_acumyear),
                "客參":self.away_vgen(ji_style, taiyi_acumyear),
                "定算":[self.set_cal(ji_style, taiyi_acumyear), config.cal_des(self.set_cal(ji_style, taiyi_acumyear))],
                "合神":self.hegod(ji_style),
                "計神":self.jigod(ji_style),
                "定目":self.se(ji_style, taiyi_acumyear),
                "君基":self.kingbase(ji_style, taiyi_acumyear),
                "臣基":self.officerbase(ji_style, taiyi_acumyear),
                "民基":self.pplbase(ji_style, taiyi_acumyear),
                "五福":config.wufu(self.accnum(ji_style, taiyi_acumyear)),
                "帝符":config.kingfu(self.accnum(ji_style, taiyi_acumyear)),
                "太尊":config.taijun(self.accnum(ji_style, taiyi_acumyear)),
                "飛鳥":config.flybird(self.accnum(ji_style, taiyi_acumyear)),
                "三風":config.threewind(self.accnum(ji_style, taiyi_acumyear)),
                "五風":config.fivewind(self.accnum(ji_style, taiyi_acumyear)),
                "八風":config.eightwind(self.accnum(ji_style, taiyi_acumyear)),
                "大游":config.bigyo(self.accnum(ji_style, taiyi_acumyear)),
                "小游":config.smyo(self.accnum(ji_style, taiyi_acumyear)),
                "二十八宿值日":config.starhouse(self.year, self.month, self.day, self.hour, self.minute),
                "太歲二十八宿":self.year_chin(),
                "太歲值宿斷事": su_dist.get(self.year_chin()),
                "始擊二十八宿":self.sf_num(ji_style, taiyi_acumyear),
                "始擊值宿斷事":su_dist.get(self.sf_num(ji_style, taiyi_acumyear)),
                "十天干歲始擊落宮預測": multi_key_dict_get (tengan_shiji, config.gangzhi(self.year, self.month, self.day, self.hour, self.minute)[0][0]).get(Ganzhiwuxing(self.sf(ji_style, taiyi_acumyear))),
                "八門值事":config.eight_door(self.accnum(ji_style, taiyi_acumyear)),
                "八門分佈":self.geteightdoors(ji_style, taiyi_acumyear),
                "八宮旺衰":jieqi.gong_wangzhuai(),
                "推太乙當時法": self.shensha(ji_style, taiyi_acumyear),
                "推三門具不具":self.threedoors(ji_style, taiyi_acumyear),
                "推五將發不發":self.fivegenerals(ji_style, taiyi_acumyear),
                "推主客相闗法":self.wc_n_sj(ji_style, taiyi_acumyear),
                "推陰陽以占厄會":self.tui_danger(ji_style, taiyi_acumyear),
                "推多少以占勝負":config.suenwl(self.home_cal(ji_style, taiyi_acumyear),
                                        self.away_cal(ji_style, taiyi_acumyear),
                                        self.home_general(ji_style, taiyi_acumyear),
                                        self.away_general(ji_style, taiyi_acumyear)),
                "推太乙風雲飛鳥助戰法":config.flybird_wl(self.accnum(ji_style, taiyi_acumyear),
                                      config.flybird(self.accnum(ji_style, taiyi_acumyear)),
                                      self.home_general(ji_style, taiyi_acumyear),
                                      self.away_general(ji_style, taiyi_acumyear),
                                      self.home_vgen(ji_style, taiyi_acumyear),
                                      self.away_vgen(ji_style, taiyi_acumyear),
                                      self.ty(ji_style, taiyi_acumyear),
                                      gong2.get(self.skyeyes(ji_style, taiyi_acumyear)),
                                      gong2.get(self.sf(ji_style, taiyi_acumyear)) ),
                "推雷公入水":config.leigong(self.ty(ji_style, taiyi_acumyear)),
                "推臨津問道":config.lijin(self.year, self.month, self.day, self.hour, self.minute),
                "推獅子反擲":config.lion(self.year, self.month, self.day, self.hour, self.minute),
                "推白雲捲空":config.cloud(self.home_general(ji_style, taiyi_acumyear)),
                "推猛虎相拒":config.tiger(self.ty(ji_style, taiyi_acumyear)),
                "推白龍得雲":config.dragon(self.ty(ji_style, taiyi_acumyear)),
                "推回軍無言":config.returnarmy(self.away_general(ji_style, taiyi_acumyear)),
                }

if __name__ == '__main__':
    tic = time.perf_counter()
    year = 1552
    month = 9
    day = 24
    hour = 0
    minute = 0
    print(Taiyi(year, month, day, hour, minute).kook(2, 1))
    print(config.gangzhi(year, month, day, hour, minute))
    print(Taiyi(year, month, day, hour, minute).pan(0, 1))
    #print(config.gangzhi(-1197, 2, 2, 0, 0))
    #
    #print(Taiyi(year, month, day, hour, minute).kook(0, 0))
    #print(Taiyi(year, month, day, hour, minute).kook(1, 0))
    #print(Taiyi(year, month, day, hour, minute).kook(2, 0))
    #print(Taiyi(year, month, day, hour, minute).kook(3, 0))
    #print(Taiyi(year, month, day, hour, minute).kook(4, 0))

    toc = time.perf_counter()
    print(f"{toc - tic:0.4f} seconds")
