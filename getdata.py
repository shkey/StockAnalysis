import urllib.request
import time
import json
import datetime
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
import matplotlib.dates as mdates
import wx


def show_linechart(date, open, high, low, close, sh_symbolName, sh_code, save_pic):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    plt.plot(date, close, "y", linewidth=0.8, label="收盘价")
    plt.plot(date, open, "b", linewidth=0.8, label="开盘价")
    plt.plot(date, high, "r", linewidth=0.8, label="最高价")
    plt.plot(date, low, "g", linewidth=0.8, label="最低价")
    plt.legend()
    # 设置图表标题
    plt.title("%s %s" % (sh_symbolName, sh_code[2:]), fontsize=20)
    # 设置坐标标签
    plt.xlabel("时间")
    plt.ylabel("股价（元）")
    plt.xticks(rotation=45)
    plt.grid(True)
    fig = plt.gcf()
    fig.set_size_inches(19.2, 10.8)
    if save_pic:
        plt.savefig("linechart.png", dpi=100)
    plt.show()


def show_candlechart(data_list, sh_symbolName, sh_code, save_pic):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    # 创建一个子图
    fig, ax = plt.subplots()
    fig.subplots_adjust(bottom=0.2)
    # 设置X轴刻度为日期时间
    ax.xaxis_date()
    plt.xticks(rotation=45)
    plt.yticks()
    plt.title("%s %s" % (sh_symbolName, sh_code[2:]), fontsize=20)
    plt.xlabel("时间")
    plt.ylabel("股价（元）")
    mpf.candlestick_ohlc(ax, data_list, width=2, colorup='r', colordown='g')
    plt.grid(True)
    fig = plt.gcf()
    fig.set_size_inches(19.2, 10.8)
    if save_pic:
        plt.savefig("candlechart.png", dpi=100)
    plt.show()


def show_twochart(date, open, high, low, close, data_list, sh_symbolName, sh_code, save_pic):
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 用来正常显示中文
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
    plt.subplot(211)  # 在画板上画子图1
    plt.plot(date, close, "y", linewidth=0.8, label="收盘价")  # 画出收盘价折线图
    plt.plot(date, open, "b", linewidth=0.8, label="开盘价")  # 画出开盘价折线图
    plt.plot(date, high, "r", linewidth=0.8, label="最高价")  # 画出最高价折线图
    plt.plot(date, low, "g", linewidth=0.8, label="最低价")  # 画出最低价折线图
    plt.legend()  # 设置图示
    # 设置图表标题
    plt.title("%s %s" % (sh_symbolName, sh_code[2:]), fontsize=20)
    # 设置坐标标签
    plt.xlabel("时间")  # 设置x轴标签
    plt.ylabel("股价（元）")  # 设置y轴标签
    plt.xticks(rotation=45)  # 设置x轴标签旋转45度
    plt.grid(True)  # 设置背景的网格
    ax = plt.subplot(212)  # 在画板上画子图2
    # 设置X轴刻度为日期时间
    ax.xaxis_date()
    plt.xticks(rotation=45)  # 设置x轴标签旋转45度
    plt.yticks()
    plt.xlabel("时间")  # 设置x轴标签
    plt.ylabel("股价（元）")  # 设置y轴标签
    mpf.candlestick_ohlc(ax, data_list, width=2, colorup='r', colordown='g')  # 画出K线图
    plt.grid(True)  # 设置背景的网格
    fig = plt.gcf()
    fig.set_size_inches(19.2, 10.8)  # 设置图片大小
    if save_pic:
        plt.savefig("twochart.png", dpi=100)  # 保存生成的图片
    plt.show()  # 显示画出的图片


def get_data(sh_num, sh_type, sh_count):
    try:
        ticks = time.time()
        choice_type = ['stockdaybar', 'stockweekbar', 'stockmonthbar']
        sh_url = "https://gupiao.baidu.com/api/search/stockquery?from=pc&os_ver=1&cuid=xxx&vv=3.2&format=json&asset=0" \
                 "%2C4%2C14&query_content=" + sh_num
        sh_name = urllib.request.urlopen(sh_url).read()
        sh_name = json.loads(sh_name)
        sh_symbolName = sh_name['data']['stock_data'][0]['f_symbolName']
        sh_code = sh_name['data']['stock_data'][0]['f_code']
        url = 'https://gupiao.baidu.com/api/stocks/%s?from=pc&os_ver=1&cuid=xxx&vv=100&format=json&stock_code' \
              '=%s&step=3&start=&count=%s&fq_type=no&timestamp=%s' % (
                  choice_type[sh_type], sh_code, sh_count, round(ticks))
        data = urllib.request.urlopen(url).read()
        data = json.loads(data)
        date_list = []
        open_list = []
        high_list = []
        low_list = []
        close_list = []
        data_list = []
        if data['errorMsg'] == 'SUCCESS':
            for week_data in data['mashData']:
                date1 = datetime.datetime.strptime(str(week_data['date']), '%Y%m%d')
                date_list.append(date1)
                open_list.append(week_data['kline']['open'])
                high_list.append(week_data['kline']['high'])
                low_list.append(week_data['kline']['low'])
                close_list.append(week_data['kline']['close'])
                datas = (mdates.date2num(date1), week_data['kline']['open'], week_data['kline']['high'],
                         week_data['kline']['low'], week_data['kline']['close'])
                data_list.append(datas)
        else:
            wx.MessageBox("获取数据失败！请重试！", "错误", wx.OK | wx.ICON_INFORMATION)
        all_data = {'date_list': date_list, 'open_list': open_list, 'high_list': high_list, 'low_list': low_list,
                    'close_list': close_list, 'data_list': data_list, 'sh_symbolName': sh_symbolName,
                    'sh_code': sh_code}
        return all_data  # 返回获得的所有数据，方便外部调用
    except:
        wx.MessageBox("网络错误！请重试！", "网络错误", wx.OK | wx.ICON_INFORMATION)
