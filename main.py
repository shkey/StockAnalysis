import wx
import getdata as data


class MyFrame(wx.Frame):
    data_all = {}

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"股票分析", pos=wx.DefaultPosition, size=wx.Size(400, 300),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # self.SetSizeHintsSz(wx.Size(400, 300), wx.Size(400, 300))
        self.SetMinSize(wx.Size(400, 300))
        self.SetMaxSize(wx.Size(400, 300))
        self.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_WINDOW))

        bSizer1 = wx.BoxSizer(wx.VERTICAL)

        bSizer2 = wx.BoxSizer(wx.HORIZONTAL)

        self.stxt_stockcode = wx.StaticText(self, wx.ID_ANY, u"股票代码   ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stxt_stockcode.Wrap(-1)
        bSizer2.Add(self.stxt_stockcode, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.txt_stockcode = wx.TextCtrl(self, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0)
        self.txt_stockcode.SetMaxLength(6)
        bSizer2.Add(self.txt_stockcode, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(bSizer2, 1, wx.EXPAND, 5)

        bSizer3 = wx.BoxSizer(wx.HORIZONTAL)

        self.stxt_type = wx.StaticText(self, wx.ID_ANY, u"查询类型   ", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stxt_type.Wrap(-1)
        bSizer3.Add(self.stxt_type, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        choice_typeChoices = [u"1、日K", u"2、周K", u"3、月K"]
        self.choice_type = wx.Choice(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_typeChoices, 0)
        self.choice_type.SetSelection(0)
        bSizer3.Add(self.choice_type, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(bSizer3, 1, wx.EXPAND, 5)

        bSizer4 = wx.BoxSizer(wx.HORIZONTAL)

        self.stxt_count = wx.StaticText(self, wx.ID_ANY, u"查询信息数", wx.DefaultPosition, wx.DefaultSize, 0)
        self.stxt_count.Wrap(-1)
        bSizer4.Add(self.stxt_count, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.spinc_count = wx.SpinCtrl(self, wx.ID_ANY, u"100", wx.DefaultPosition, wx.DefaultSize,
                                       wx.SP_ARROW_KEYS, 0, 999, 100)
        bSizer4.Add(self.spinc_count, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.chkbtn_pic = wx.CheckBox(self, wx.ID_ANY, u"是否保存图片", wx.DefaultPosition, wx.DefaultSize, 0)
        self.chkbtn_pic.SetValue(True)
        bSizer4.Add(self.chkbtn_pic, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(bSizer4, 1, wx.EXPAND, 5)

        bSizer5 = wx.BoxSizer(wx.HORIZONTAL)

        self.btn_linechart = wx.Button(self, wx.ID_ANY, u"查询折线图", wx.DefaultPosition, wx.Size(-1, 40), wx.NO_BORDER)
        self.btn_linechart.SetFont(
            wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑"))
        self.btn_linechart.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        bSizer5.Add(self.btn_linechart, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btn_klinechart = wx.Button(self, wx.ID_ANY, u"查询K线图", wx.DefaultPosition, wx.Size(-1, 40), wx.NO_BORDER)
        self.btn_klinechart.SetFont(
            wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑"))
        self.btn_klinechart.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        bSizer5.Add(self.btn_klinechart, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        self.btn_both = wx.Button(self, wx.ID_ANY, u"联合查询", wx.DefaultPosition, wx.Size(-1, 40), wx.NO_BORDER)
        self.btn_both.SetFont(
            wx.Font(11, wx.FONTFAMILY_SWISS, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, "微软雅黑"))
        self.btn_both.SetBackgroundColour(wx.SystemSettings.GetColour(wx.SYS_COLOUR_3DLIGHT))

        bSizer5.Add(self.btn_both, 1, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 5)

        bSizer1.Add(bSizer5, 1, wx.EXPAND, 5)

        self.SetSizer(bSizer1)
        self.Layout()

        self.Centre(wx.BOTH)

        # Connect Events
        self.choice_type.Bind(wx.EVT_CHOICE, self.m_choice1OnChoice)
        self.chkbtn_pic.Bind(wx.EVT_CHECKBOX, self.m_checkBox1OnCheckBox)
        self.btn_linechart.Bind(wx.EVT_BUTTON, self.btn_linechartOnButtonClick)
        self.btn_klinechart.Bind(wx.EVT_BUTTON, self.btn_klinechartOnButtonClick)
        self.btn_both.Bind(wx.EVT_BUTTON, self.btn_bothOnButtonClick)

    def __del__(self):
        pass

    def m_choice1OnChoice(self, event):
        event.Skip()

    def m_checkBox1OnCheckBox(self, event):
        event.Skip()

    def btn_linechartOnButtonClick(self, event):
        if self.txt_stockcode.GetLineText(0) == "":
            wx.MessageBox("股票代码不能为空！", "错误", wx.OK | wx.ICON_INFORMATION)
        elif len(self.txt_stockcode.GetLineText(0)) < 6:
            wx.MessageBox("输入的股票代码有误！", "错误", wx.OK | wx.ICON_INFORMATION)
        else:
            self.data_all = data.get_data(self.txt_stockcode.GetValue(), self.choice_type.GetSelection(),
                                          self.spinc_count.GetValue())
            if self.data_all is not None:
                data.show_linechart(self.data_all['date_list'], self.data_all['open_list'], self.data_all['high_list'],
                                    self.data_all['low_list'], self.data_all['close_list'],
                                    self.data_all['sh_symbolName'],
                                    self.data_all['sh_code'], self.chkbtn_pic.IsChecked())

    def btn_klinechartOnButtonClick(self, event):
        if self.txt_stockcode.GetLineText(0) == "":
            wx.MessageBox("股票代码不能为空！", "错误", wx.OK | wx.ICON_INFORMATION)
        elif len(self.txt_stockcode.GetLineText(0)) < 6:
            wx.MessageBox("输入的股票代码有误！", "错误", wx.OK | wx.ICON_INFORMATION)
        else:
            self.data_all = data.get_data(self.txt_stockcode.GetValue(), self.choice_type.GetSelection(),
                                          self.spinc_count.GetValue())
            if self.data_all is not None:
                data.show_candlechart(self.data_all['data_list'], self.data_all['sh_symbolName'],
                                      self.data_all['sh_code'], self.chkbtn_pic.IsChecked())

    def btn_bothOnButtonClick(self, event):
        if self.txt_stockcode.GetLineText(0) == "":
            wx.MessageBox("股票代码不能为空！", "错误", wx.OK | wx.ICON_INFORMATION)
        elif len(self.txt_stockcode.GetLineText(0)) < 6:
            wx.MessageBox("输入的股票代码有误！", "错误", wx.OK | wx.ICON_INFORMATION)
        else:
            self.data_all = data.get_data(self.txt_stockcode.GetValue(), self.choice_type.GetSelection(),
                                          self.spinc_count.GetValue())
            if self.data_all is not None:
                data.show_twochart(self.data_all['date_list'], self.data_all['open_list'], self.data_all['high_list'],
                                   self.data_all['low_list'], self.data_all['close_list'], self.data_all['data_list'],
                                   self.data_all['sh_symbolName'], self.data_all['sh_code'],
                                   self.chkbtn_pic.IsChecked())


def run():
    app = wx.App(False)
    frame = MyFrame(None)
    frame.Show(True)
    app.MainLoop()


run()
