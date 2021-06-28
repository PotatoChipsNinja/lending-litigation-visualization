# coding=utf-8

import json
import re
import datetime

with open('data/Task4-private-lending-case-data.json', 'r', encoding='utf8') as f:
    raw = json.load(f)

def extract_defendant_and_plaintiff():
    for item in raw:
        item['defendant'] = re.findall(r'原审被告[)）]?[:：](.+)，(.)，(\d+)年(\d+)月(\d+)日出生', item['content'])
        item['plaintiff'] = re.findall(r'原审原告[)）]?[:：](.+)，(.)，(\d+)年(\d+)月(\d+)日出生', item['content'])

def extract_court_location():
    for item in raw:
        if len(re.findall(r'(.+)第..级人民法院', item['court_name'])) > 0:
            item['court_location'] = re.findall(r'(.+)第..级人民法院', item['court_name'])[0]
        elif len(re.findall(r'(.+).级人民法院', item['court_name'])) > 0:
            item['court_location'] = re.findall(r'(.+).级人民法院', item['court_name'])[0]
        elif len(re.findall(r'(.+)人民法院', item['court_name'])) > 0:
            item['court_location'] = re.findall(r'(.+)人民法院', item['court_name'])[0]
        else:
            item['court_location'] = ''

def extract_decision():
    for item in raw:
        if len(re.findall(r'维持原判', item['content'])) > 0:
            item['decision'] = '维持原判'
        else:
            item['decision'] = '改判'

def extract_province():
    name = ["河北省", "山西省", "辽宁省", "吉林省", "黑龙江省", "江苏省", "浙江省", "安徽省", "福建省", "江西省", "山东省", "河南省", "湖北省", "湖南省", "广东省", "海南省", "四川省", "贵州省", "云南省", "陕西省", "甘肃省", "青海省", "台湾省", "内蒙古自治区", "广西壮族自治区", "西藏自治区", "宁夏回族自治区", "新疆维吾尔自治区", "北京市", "天津市", "上海市", "重庆市", "香港特别行政区", "澳门特别行政区"]
    abbr = ['冀', '晋', '辽', '吉', '黑', '苏', '浙', '皖', '闽', '赣', '鲁', '豫', '鄂', '湘', '粤', '琼', '川', '黔', '云', '陕', '甘', '青', '台', '内', '桂', '藏', '宁', '新', '京', '津', '沪', '渝', '港', '澳']
    for item in raw:
        if item['caseNO'][6] in abbr:
            item['province'] = name[abbr.index(item['caseNO'][6])]

label = [{}, {}, {}]
level = ['level1', 'level2', 'level3']

for item in raw:
    for i in range(3):
        for l in item['label'][level[i]]:
            if l in label[i]:
                label[i][l] += 1
            else:
                label[i][l] = 1

extract_defendant_and_plaintiff()
extract_court_location()
extract_province()
extract_decision()

for item in raw:
    del item['content']
    del item['result']

print('finish preprocess')

def get_label(level):
    return json.dumps(list(label[int(level)].keys()), ensure_ascii=False)

def get_label_stat(level):
    return json.dumps(label[int(level)], ensure_ascii=False)

def select_by_label(labels):
    if len(labels) == 0:
        return raw
    ret = []
    for item in raw:
        all_label = item['label']['level1'] + item['label']['level2'] + item['label']['level3']
        if set(all_label) >= set(labels):
            ret.append(item)
    return ret

def get_court_stat(labels):
    l = select_by_label(labels)
    court_name = {}
    court_location = {}
    province = {}
        
    for item in l:
        if item['court_name'] in court_name:
            court_name[item['court_name']] += 1
        else:
            court_name[item['court_name']] = 1

        if item['court_location'] in court_location:
            court_location[item['court_location']] += 1
        else:
            court_location[item['court_location']] = 1

        if 'province' in item:
            if item['province'] in province:
                province[item['province']] += 1
            else:
                province[item['province']] = 1
    return json.dumps({ 'court_name': court_name, 'court_location': court_location, 'province': province }, ensure_ascii=False)

def get_decision_stat(labels):
    l = select_by_label(labels)
    decision = {'维持原判': 0, '改判': 0}
    for item in l:
        decision[item['decision']] += 1
    return json.dumps(decision, ensure_ascii=False)

def get_person_stat(labels, defendant=True):
    l = select_by_label(labels)
    if defendant:
        key = 'defendant'
    else:
        key = 'plaintiff'
    gender = { 'male': 0, 'female': 0 }
    age = {'小于18': 0, '18-25': 0, '25-40': 0, '40-55': 0, '55-70': 0, '大于70': 0}
    for item in l:
        for person in item[key]:
            # 性别
            if person[1] == '男':
                gender['male'] += 1
            else:
                gender['female'] += 1

            # 年龄
            person_age = datetime.date.today().year - int(person[2])
            if person_age < 18:
                age['小于18'] += 1
            elif person_age < 25:
                age['18-25'] += 1
            elif person_age < 40:
                age['25-40'] += 1
            elif person_age < 55:
                age['40-55'] += 1
            elif person_age < 70:
                age['55-70'] += 1
            else:
                age['大于70'] += 1

    return json.dumps({ 'gender': gender, 'age': age }, ensure_ascii=False)

def get_law_stat(labels):
    l = select_by_label(labels)
    law = {}

    for item in l:
        for case in item['law_case']:
            if case['law_name'] in law:
                law[case['law_name']] += 1
            else:
                law[case['law_name']] = 1

    return json.dumps(law, ensure_ascii=False)

def get_clause_stat(labels, law):
    l = select_by_label(labels)
    clause = {}

    for item in l:
        for case in item['law_case']:
            if case['law_name'] == law:
                if case['law_clause'] in clause:
                    clause[case['law_clause']]['cnt'] += 1
                else:
                    clause[case['law_clause']] = { 'cnt': 1, 'content': case['text'] }

    return json.dumps(clause, ensure_ascii=False)

def get_year_stat(labels):
    l = select_by_label(labels)
    year = {}

    for item in l:
        d = datetime.date.fromisoformat(item['judge_date'])
        if d.year in year:
            year[d.year] += 1
        else:
            year[d.year] = 1
    return json.dumps(year, ensure_ascii=False)
