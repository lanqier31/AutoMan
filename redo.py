#！ -*-coding:utf-8-*-

import sqlite3
import sys,time 
import subprocess

import requests,json
#from flask import render_template, g, redirect, url_for, request, send_file
from selenium import webdriver
import  config 


all_page_data = {}
page_urls = config.page_urls
timing_js = config.timing_js

#准备数据
env_for_test= 'syf1.1.1'
current_env = config.hosts['164'] + env_for_test
# 统计页面加载时间的6个维度 登录页专用
index_data = {'dns': 0, 'request': 0, 'dom_parser': 0, 'dom_ready': 0, 'load_event': 0, 'whitewait': 0, 'loadall': 0}
# index页面资源的信息 登录页专用
page_index_info = []
# 将统计数据保存到sqlite
connection = sqlite3.connect(config.db_dir)
cursor = connection.cursor()
# 先删除页面资源细分表webDetailLoad所有数据
clear_resource_sql = "delete from PageDetail where project='Clinical' and version='" + env_for_test + "'"
cursor.execute(clear_resource_sql)
# 先清理上次的数据
clear_webload_sql = "delete from WebLoad where project='Clinical' and version='" + env_for_test + "'"
cursor.execute(clear_webload_sql)
connection.commit()
# get到clinical登录页(登录页需要单独收集其页面加载性能指标)
driver = webdriver.Chrome()
login_url = current_env + '/login/index'
driver.get(login_url)
#driver.maximize_window()
time.sleep(5)
time_line = driver.execute_script(config.timing_js)
# 将页面加载时间存入all_page_data
for key in index_data.keys():
    index_data[key] = time_line[key]
# 将index的数据存入all_page_data
all_page_data['Index'] = index_data

# 获得index页面所有的资源实体
entries = driver.execute_script(config.get_entries_js)
# 遍历登录页面所有资源
for items in entries:
    # 以页面名：数组形式保存页面信息
    page_index_resource = {}
    # 资源名称
    page_index_resource['name'] = items['name']
    # 资源类型分类
    resource_type = str(items['name']).split('.')[-1]
    if resource_type in ['jpg', 'png', 'gif', 'jpeg']:
        page_index_resource['resourceType'] = 'img'
    elif resource_type == 'js':
        page_index_resource['resourceType'] = 'js'
    elif resource_type == 'css':
        page_index_resource['resourceType'] = 'css'
    else:
        if items['initiatorType'] == 'xmlhttprequest':
            page_index_resource['resourceType'] = 'xmlhttprequest'
        elif items['initiatorType'] == 'script':
            page_index_resource['resourceType'] = 'js'
        else:
            page_index_resource['resourceType'] = 'other'
    # 资源大小
    page_index_resource['transferSize'] = items['transferSize']
    # 资源耗时
    page_index_resource['duration'] = items['duration']
    # 将登录页资源信息存入列表
    page_index_info.append(page_index_resource)
    # 将登录页资源列表信息存入字典对象 对应key为Index
    save_resource_sql = 'insert into PageDetail ' + "values('Clinical','" + str(env_for_test) + "'," + "'" + str(
        'Index') + "'," + "'" + str(page_index_resource['name']) + "'," + "'" + str(
        page_index_resource['resourceType']) + "'," + "'" \
                        + str(page_index_resource['transferSize']) + "'," + "'" + str(
        page_index_resource['duration']) + "'," + 'CURRENT_TIMESTAMP)'
    cursor.execute(save_resource_sql)
    connection.commit()

    # 登录系统后 对其他所有页面进行遍历以收集其页面加载性能数据
    driver.find_element_by_id('txtUserName').send_keys('30048')
    driver.find_element_by_id('txtPassword').send_keys('5436')
    driver.find_element_by_id('btnConfirm').click()
    time.sleep(3)

    # 循环登录后的所有页面
    for page in page_urls.keys():
        # 将页面加载时间统计出来存入all_page_data
        current_page_timing = {"dns": 0, "request": 0, "dom_parser": 0, "dom_ready": 0, "load_event": 0, "whitewait": 0, "loadall": 0}
        current_page_url = current_env + (str(page_urls[page]))
        driver.get(current_page_url)
        time.sleep(10)
        durations = driver.execute_script(timing_js)
        for item in current_page_timing.keys():
            current_page_timing[item] = durations[item]
        # 将当前页面的name和统计到数据存入到all_page_data
        all_page_data[page] = current_page_timing

        entries = driver.execute_script("return window.performance.getEntries()")
        # 遍历当前页面所有资源
        for items in entries:
            current_resources = {}
            current_resources['name'] = items['name']
            # 根据资源类型进行统计
            resource_type = str(items['name']).split('.')[-1]
            if resource_type in ['jpg', 'png', 'gif', 'jpeg']:
                current_resources['resourceType'] = 'img'
            elif resource_type == 'js':
                current_resources['resourceType'] = 'js'
            elif resource_type == 'css':
                current_resources['resourceType'] = 'css'
            else:
                if items['initiatorType'] == 'xmlhttprequest':
                    current_resources['resourceType'] = 'xmlhttprequest'
                elif items['initiatorType'] == 'script':
                    current_resources['resourceType'] = 'js'
                else:
                    current_resources['resourceType'] = 'other'
            # 资源大小
            current_resources['transferSize'] = items['transferSize']
            # 资源耗时
            current_resources['duration'] = items['duration']
            # 保存资源
            save_resource_sql = 'insert into PageDetail ' + "values('Clinical','" + str(
                env_for_test) + "'," + "'" + str(
                page) + "'," + "'" + str(
                current_resources['name']) + "'," \
                                + "'" + str(current_resources['resourceType']) + "'," + "'" + str(
                current_resources['transferSize']) + "'," + "'" + str(
                current_resources['duration']) + "'," + 'CURRENT_TIMESTAMP)'
            cursor.execute(save_resource_sql)
            connection.commit()
    # 退出chrome driver进程
    driver.quit()
    # 更新WebLoad表中的数据
    for name in all_page_data.keys():
        page_time = all_page_data[name]
        if name == 'Index':
            insert_sql = 'insert into WebLoad ' + "values('Clinical','" + str(env_for_test) + "'," + "'"\
                         + str(name) + "'," + "'" + str(current_env) + "/login/index'," + str(page_time['dns']) \
                         + ',' + str(page_time['request']) + ',' + str(page_time['dom_parser']) + ',' + str(page_time['dom_ready']) \
                         + ',' + str(page_time['load_event']) + ',' + str(page_time['whitewait']) + ',' + str(page_time['loadall']) + ',' + 'CURRENT_TIMESTAMP)'
        else:
            insert_sql = 'insert into WebLoad ' + "values('Clinical','" + str(env_for_test) + "'," + "'" \
                         + str(name) + "'," + "'" + str(current_env) + str(page_urls[name]) + "'," + str(page_time['dns']) \
                         + ',' + str(page_time['request']) + ',' + str(page_time['dom_parser']) + ',' + str(page_time['dom_ready']) \
                         + ',' + str(page_time['load_event']) + ',' + str(page_time['whitewait']) + ',' + str(page_time['loadall']) + ',' + 'CURRENT_TIMESTAMP)'
        cursor.execute(insert_sql)
        connection.commit()
    connection.close()

    print 'success'
