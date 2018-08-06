"""
This is a demonstration program for Hydroponic Machine.
If you excution this program, the GUI display and measurments start.
"""
#import libraries
import wx# import wxPython --> Used to create a GUI.
import serial#import pyserial --> Used to Communication with Arduino.
import os
import sys
import time
import threading
import random
import csv
from datetime import datetime
from datetime import timedelta

#In this part, create a GUI.
class Application(wx.App):
    #In this part, create a frame about GUI.
    def frame(self):
        print("Communication started with Arduino.")
        self.main_frame = wx.Frame(None, wx.ID_ANY, u"Control_Panel", size = (1300,630))
        self.panel()
        self.button()
        self.slider()
        self.font()
        self.Display_data_label()
        self.Display_data()
        return self.main_frame

    #In this part, create a panel on frame.
    def panel(self):
        #create upper panel
        self.upper_control_panel = wx.Panel(self.main_frame, wx.ID_ANY, pos=(0,0), size = (1300,315))
        self.upper_control_panel.SetBackgroundColour("#f0f80f")
        #create lower panel
        self.lower_control_panel = wx.Panel(self.main_frame, wx.ID_ANY, pos=(0,300), size = (1300,315))
        self.lower_control_panel.SetBackgroundColour("#f0f8ff")

    #In this part, create a button on panel.
    def button(self):
        #on upper panel
        self.upper_red_button = wx.Button(self.upper_control_panel, wx.ID_ANY, u"RED(U)", pos = (600,250), size = (100,50))
        self.upper_red_button.Bind(wx.EVT_BUTTON, self.click_upper_red_button)
        self.upper_green_button = wx.Button(self.upper_control_panel, wx.ID_ANY, u"GREEN(U)", pos = (700,250), size = (100,50))
        self.upper_green_button.Bind(wx.EVT_BUTTON, self.click_upper_green_button)
        self.upper_blue_button = wx.Button(self.upper_control_panel, wx.ID_ANY, u"BLUE(U)", pos = (800,250), size = (100,50))
        self.upper_blue_button.Bind(wx.EVT_BUTTON, self.click_upper_blue_button)
        self.upper_fan_button = wx.ToggleButton(self.upper_control_panel, wx.ID_ANY, u"FAN(U)", pos = (0,0), size = (100,50))
        self.upper_fan_button.Bind(wx.EVT_TOGGLEBUTTON, self.click_upper_fan_button)
        self.upper_pel_h_button = wx.ToggleButton(self.upper_control_panel, wx.ID_ANY, u"HEATER(U)", pos = (100,0), size = (100,50))
        self.upper_pel_h_button.Bind(wx.EVT_TOGGLEBUTTON, self.click_upper_pel_h_button)
        self.upper_pel_c_button= wx.ToggleButton(self.upper_control_panel, wx.ID_ANY, u"COOLER(U)", pos = (200,0), size = (100,50))
        self.upper_pel_c_button.Bind(wx.EVT_TOGGLEBUTTON, self.click_upper_pel_c_button)
        self.upper_pump_in_button = wx.ToggleButton(self.upper_control_panel, wx.ID_ANY, u"PUMP-IN(U)", pos = (300,0), size = (100,50))
        self.upper_pump_in_button.Bind(wx.EVT_TOGGLEBUTTON, self.click_upper_pump_in_button)
        self.upper_pump_out_button = wx.ToggleButton(self.upper_control_panel, wx.ID_ANY, u"PUMP-OUT(U)", pos = (400,0), size = (100,50))
        self.upper_pump_out_button.Bind(wx.EVT_TOGGLEBUTTON, self.click_upper_pump_out_button)
        self.end_button = wx.ToggleButton(self.upper_control_panel, wx.ID_ANY, u"END", pos = (500,0), size = (100,50))
        self.end_button.Bind(wx.EVT_TOGGLEBUTTON, self.click_end_button)
        #on lower panel
        self.lower_red_button = wx.Button(self.lower_control_panel, wx.ID_ANY, u"RED(L)", pos = (600,250), size = (100,50))
        self.lower_red_button.Bind(wx.EVT_BUTTON, self.click_lower_red_button)
        self.lower_green_button = wx.Button(self.lower_control_panel, wx.ID_ANY, u"GREEN(L)", pos = (700,250), size = (100,50))
        self.lower_green_button.Bind(wx.EVT_BUTTON, self.click_lower_green_button)
        self.lower_blue_button = wx.Button(self.lower_control_panel, wx.ID_ANY, u"BLUE(L)", pos = (800,250), size = (100,50))
        self.lower_blue_button.Bind(wx.EVT_BUTTON, self.click_lower_blue_button)
        self.lower_fan_button = wx.ToggleButton(self.lower_control_panel, wx.ID_ANY, u"FAN(L)", pos = (0,0), size = (100,50))
        self.lower_fan_button.Bind(wx.EVT_TOGGLEBUTTON, self.click_lower_fan_button)
        self.lower_pel_h_button = wx.ToggleButton(self.lower_control_panel, wx.ID_ANY, u"HEATER(L)", pos = (100,0), size = (100,50))
        self.lower_pel_h_button.Bind(wx.EVT_TOGGLEBUTTON, self.click_lower_pel_h_button)
        self.lower_pel_c_button = wx.ToggleButton(self.lower_control_panel, wx.ID_ANY, u"COOLER(L)", pos = (200,0), size = (100,50))
        self.lower_pel_c_button.Bind(wx.EVT_TOGGLEBUTTON, self.click_lower_pel_c_button)
        self.lower_pump_in_button = wx.ToggleButton(self.lower_control_panel, wx.ID_ANY, u"PUMP-IN(L)", pos = (300,0), size = (100,50))
        self.lower_pump_in_button.Bind(wx.EVT_TOGGLEBUTTON, self.click_lower_pump_in_button)

        self.lower_pump_out_button = wx.ToggleButton(self.lower_control_panel, wx.ID_ANY, u"PUMP-OUT(L)", pos = (400,0), size = (100,50))
        self.lower_pump_out_button.Bind(wx.EVT_TOGGLEBUTTON, self.click_lower_pump_out_button)

    #In this part, create a slider on panel.
    def slider(self):
        self.upper_red_slider = wx.Slider(self.upper_control_panel, wx.ID_ANY, value = 0, minValue = 0, maxValue = 255, style = wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_AUTOTICKS , pos = (600,0), size = (100,250))
        self.upper_green_slider = wx.Slider(self.upper_control_panel, wx.ID_ANY, value = 0, minValue = 0, maxValue = 255, style = wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_AUTOTICKS , pos = (700,0), size = (100,250))
        self.upper_blue_slider = wx.Slider(self.upper_control_panel, wx.ID_ANY, value = 0, minValue = 0, maxValue = 255, style = wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_AUTOTICKS , pos = (800,0), size = (100,250))
        self.lower_red_slider = wx.Slider(self.lower_control_panel, wx.ID_ANY, value = 0, minValue = 0, maxValue = 255, style = wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_AUTOTICKS , pos = (600,0), size = (100,250))
        self.lower_green_slider = wx.Slider(self.lower_control_panel, wx.ID_ANY, value = 0, minValue = 0, maxValue = 255, style = wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_AUTOTICKS , pos = (700,0), size = (100,250))
        self.lower_blue_slider = wx.Slider(self.lower_control_panel, wx.ID_ANY, value = 0, minValue = 0, maxValue = 255, style = wx.SL_VERTICAL | wx.SL_LABELS | wx.SL_AUTOTICKS , pos = (800,0), size = (100,250))
    #In this part, specify the font.
    def font(self):
        self.font = wx.Font(30, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)

    #In this part, create a data lable on panel.
    def Display_data_label(self):
        #on upper panel
        self.upper_temp_label = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, u"Temp", pos = (0,150), size = (100,50))
        self.upper_temp_label.SetFont(self.font)
        self.upper_hum_label = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, u"Hum", pos = (0,200), size = (100,50))
        self.upper_hum_label.SetFont(self.font)
        self.upper_atm_label = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, u"Atm", pos = (0,250), size = (100,50))
        self.upper_atm_label.SetFont(self.font)
        self.upper_r_label = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, u"R", pos = (300,150), size = (100,50))
        self.upper_r_label.SetFont(self.font)
        self.upper_r_label.SetForegroundColour("#FF0000")
        self.upper_g_label = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, u"G", pos = (300,200), size = (100,50))
        self.upper_g_label.SetFont(self.font)
        self.upper_g_label.SetForegroundColour("#00FF00")
        self.upper_b_label = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, u"B", pos = (300,250), size = (100,50))
        self.upper_b_label.SetFont(self.font)
        self.upper_b_label.SetForegroundColour("#0000FF")
        #on lower panel
        self.lower_temp_label = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, u"Temp", pos = (0,150), size = (100,50))
        self.lower_temp_label.SetFont(self.font)
        self.lower_hum_label = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, u"Hum", pos = (0,200), size = (100,50))
        self.lower_hum_label.SetFont(self.font)
        self.lower_atm_label = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, u"Atm", pos = (0,250), size = (100,50))
        self.lower_atm_label.SetFont(self.font)
        self.lower_r_label = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, u"R", pos = (300,150), size = (100,50))
        self.lower_r_label.SetFont(self.font)
        self.lower_r_label.SetForegroundColour("#FF0000")
        self.lower_g_label = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, u"G", pos = (300,200), size = (100,50))
        self.lower_g_label.SetFont(self.font)
        self.lower_g_label.SetForegroundColour("#00FF00")
        self.lower_b_label = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, u"B", pos = (300,250), size = (100,50))
        self.lower_b_label.SetFont(self.font)
        self.lower_b_label.SetForegroundColour("#0000FF")

    #In this part, create a data display section on panel.
    def Display_data(self):
        #on upper panel
        self.upper_temp_data = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, temp_data, pos = (100,150), size = (200,50))
        self.upper_temp_data.SetFont(self.font)
        self.upper_hum_data = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, hum_data, pos = (100,200), size = (200,50))
        self.upper_hum_data.SetFont(self.font)
        self.upper_atm_data = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, atm_data, pos = (100,250), size = (200,50))
        self.upper_atm_data.SetFont(self.font)
        self.upper_r_data = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, r_data, pos = (400,150), size = (200,50))
        self.upper_r_data.SetFont(self.font)
        self.upper_g_data = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, g_data, pos = (400,200), size = (200,50))
        self.upper_g_data.SetFont(self.font)
        self.upper_b_data = wx.TextCtrl(self.upper_control_panel, wx.ID_ANY, b_data, pos = (400,250), size = (200,50))
        self.upper_b_data.SetFont(self.font)
        #on lower panel
        self.lower_temp_data = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, temp_data, pos = (100,150), size = (200,50))
        self.lower_temp_data.SetFont(self.font)
        self.lower_hum_data = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, hum_data, pos = (100,200), size = (200,50))
        self.lower_hum_data.SetFont(self.font)
        self.lower_atm_data = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, atm_data, pos = (100,250), size = (200,50))
        self.lower_atm_data.SetFont(self.font)
        self.lower_r_data = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, r_data, pos = (400,150), size = (200,50))
        self.lower_r_data.SetFont(self.font)
        self.lower_g_data = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, g_data, pos = (400,200), size = (200,50))
        self.lower_g_data.SetFont(self.font)
        self.lower_b_data = wx.TextCtrl(self.lower_control_panel, wx.ID_ANY, b_data, pos = (400,250), size = (200,50))
        self.lower_b_data.SetFont(self.font)

    #In this part, called if you click the button.
    def click_upper_red_button(self,event):
        print("upper_red_button -- ")
        time.sleep(2)
        ser.write(b"b")
        time.sleep(2)
        if ser.readline() == b'Control_upper_red\n':
            self.upper_red_value = str(self.upper_red_slider.GetValue())
            self.message_to_guest = self.upper_red_value + ";"
            time.sleep(2)
            ser.write(self.message_to_guest.encode("UTF-8"))
            time.sleep(1)
            self.message_to_host = ser.readline()
            print(self.upper_red_value)
            print(self.message_to_host)
        else:
            print("massage lost")

    def click_upper_green_button(self,event):
        print("upper_green_button -- ")
        time.sleep(2)
        ser.write(b"c")
        time.sleep(2)
        if ser.readline() == b'Control_upper_green\n':
            self.upper_green_value = str(self.upper_green_slider.GetValue())
            self.message_to_guest = self.upper_green_value + ";"
            time.sleep(2)
            ser.write(self.message_to_guest.encode("UTF-8"))
            time.sleep(1)
            self.message_to_host = ser.readline()
            print(self.upper_green_value)
            print(self.message_to_host)
        else:
            print("massage lost")

    def click_upper_blue_button(self,event):
        print("upper_blue_button -- ")
        time.sleep(2)
        ser.write(b"d")
        time.sleep(2)
        if ser.readline() == b'Control_upper_blue\n':
            self.upper_blue_value = str(self.upper_blue_slider.GetValue())
            self.message_to_guest = self.upper_blue_value + ";"
            time.sleep(2)
            ser.write(self.message_to_guest.encode("UTF-8"))
            time.sleep(1)
            self.message_to_host = ser.readline()
            print(self.upper_blue_value)
            print(self.message_to_host)
        else:
            print("massage lost")

    def click_upper_fan_button(self,event):
        print("upper_fan_button -- " + str(self.upper_fan_button.GetValue()))

    def click_upper_pel_h_button(self,event):
        print("upper_pel_h_button -- " + str(self.upper_pel_h_button.GetValue()))

    def click_upper_pel_c_button(self,event):
        print("upper_pel_c_button -- " + str(self.upper_pel_c_button.GetValue()))

    def click_upper_pump_in_button(self,event):
        print("upper_pump_in_button -- " + str(self.upper_pump_in_button.GetValue()))

    def click_upper_pump_out_button(self,event):
        print("upper_pump_out_button -- " + str(self.upper_pump_out_button.GetValue()))

    def click_lower_red_button(self,event):
        print("lower_red_button -- " + str(self.lower_red_button.GetValue()))

    def click_lower_green_button(self,event):
        print("lower_green_button -- " + str(self.lower_green_button.GetValue()))

    def click_lower_blue_button(self,event):
        print("lower_blue_button -- " + str(self.lower_blue_button.GetValue()))

    def click_lower_fan_button(self,event):
        print("lower_fan_button -- " + str(self.lower_fan_button.GetValue()))

    def click_lower_pel_h_button(self,event):
        print("lower_pel_h_button -- " + str(self.lower_pel_h_button.GetValue()))

    def click_lower_pel_c_button(self,event):
        print("lower_pel_c_butto -- " + str(self.lower_pel_c_button.GetValue()))

    def click_lower_pump_in_button(self,event):
        print("lower_pump_in_button -- " + str(self.lower_pump_in_button.GetValue()))

    def click_lower_pump_out_button(self,event):
        print("lower_pump_out_button -- " + str(self.lower_pump_out_button.GetValue()))

    def click_end_button(self,event):
        sys.exit()

#This part shows Arduino send data to this machine.
def get_data():
    data = measurmant_data(send_data)
    re_data = data[-1]
    get_data_list.append(re_data)
    temp_data = get_data_list[-1][1]
    hum_data = get_data_list[-1][2]
    atm_data = get_data_list[-1][3]
    r_data = get_data_list[-1][4]
    g_data = get_data_list[-1][5]
    b_data = get_data_list[-1][6]
    application.upper_temp_data.SetValue(temp_data)
    application.upper_hum_data.SetValue(hum_data)
    application.upper_atm_data.SetValue(atm_data)
    application.upper_r_data.SetValue(r_data)
    application.upper_g_data.SetValue(g_data)
    application.upper_b_data.SetValue(b_data)
    application.lower_temp_data.SetValue(temp_data)
    application.lower_hum_data.SetValue(hum_data)
    application.lower_atm_data.SetValue(atm_data)
    application.lower_r_data.SetValue(r_data)
    application.lower_g_data.SetValue(g_data)
    application.lower_b_data.SetValue(b_data)
    #print(get_data_list[0][0])
    if len(data) == 10:
        filename = str(get_data_list[0][0]) +"----"+ str(get_data_list[-1][0]) + ".csv"
        os.chdir("measurment_data")
        with open(filename,"w") as csvfile:
            writer = csv.writer(csvfile, lineterminator='\n')
            writer.writerow(["Time","Temperature","Humidity","Atmospheric","R","G","B"])
            for x in range(len(data)):
                writer.writerow(data[x])
                print(data[x])
        os.chdir("../")
        data.clear()

    time_get_data = threading.Timer(600, get_data)
    time_get_data.start()

#Measurement data generator
def measurmant_data(res_data):
    #This data send to this machine from Arduino. But,now can't connect for Arduino. So, using random.
    temp_data = str(round(random.uniform(23,25),2))
    hum_data = str(round(random.uniform(80,85),2))
    atm_data = str(round(random.uniform(1010,1015),2))
    r_data = str(round(random.uniform(252,255),2))
    g_data = str(round(random.uniform(252,255),2))
    b_data = str(round(random.uniform(252,255),2))
    data = ([str(datetime.now().strftime('%Y-%m-%d--%H-%M-%S')),str(temp_data),str(hum_data),str(atm_data),str(r_data),str(g_data),str(b_data)])
    send_data.append(data)
    return send_data

#Start the thread
def boot_thread():
    time_get_data = threading.Thread(target = get_data)
    time_get_data.setDaemon(True)
    time_get_data.start()

#Perform initial setting.
if __name__ == "__main__":
    data = []
    send_data = []
    get_data_list = []
    temp_data = ""
    hum_data = ""
    atm_data = ""
    r_data = ""
    g_data = ""
    b_data = ""
    data_Flag = True
    ser = serial.Serial("COM3",9600)
    time.sleep(3)
    ser.write("z".encode("UTF-8"))
    time.sleep(1)
    message_to_host = ser.readline()
    print(message_to_host)
    starttime = time.time()
    application  =  Application()  #call class
    frame = application.frame()
    frame.Show() #Start GUI
    boot_thread() #call boot_thread
    application.MainLoop() #Maintains the state of the application.
