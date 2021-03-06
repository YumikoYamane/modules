import time #?
import threading    #?
import pyinterface

class slider_controller(object):    #class・・変数・関数が集まったコードブロック
    pos_sky =   #skyの位置
    pos_sig =   #？
    pos_r =     #rの位置
    
    speed =     #駆動速度
    low_speed =     #最小駆動速度
    acc =        #加速度指定
    dec =       #減速の指定
    
    error = []  #エラーメッセージ用の箱
    
    position = ''
    count = 0   #countの初期値?

    
    shutdown_flag = False   #shutdown_flagはFalseで指定
    
    def __init__(self, move_org=True):  #def 関数名(引数1,引数2)　 
        self.mtr = pyinterface.create_gpg7204(1)
        if move_org: self.move_org()
        self.start_cosmos_server()  #自分の関数の中の関数または、定数は、selfで呼び出し可能
        pass
        
    def print_msg(self, msg):
        print(msg)
        return
        
    def print_error(self, msg):     #エラーの表示
        self.error.append(msg)  #errorにmsgを加える(append)
        self.print_msg('!!!! ERROR !!!! ' + msg) #errorにmsgを入れてエラーメッセージを表示
        return
    
    def get_count(self):
        self.count = self.mtr.get_position()
        return
    
    def move_org(self):

        self.mtr.do_output(3)
        self.mtr.set_org()
        self.position = 'ORG'
        self.get_count()
        return

    def move(self, dist, lock=True):
        pos = self.mtr.get_position()
        if pos == dist: return
        diff = dist - pos       #現在位置と指定した場所の差(差が0になったら停止)
        if lock: self.mtr.move_with_lock(self.speed, diff, self.low_speed,
                                         self.acc, self.dec)
        else: self.mtr.move(self.speed, diff, self.low_speed, self.acc,
                            self.dec)
        
        self.get_count()
        return
    
    def move_r(self, lock=True):
     
        self.move(self.pos_r, lock)
        self.position = 'R'
        return
    
    def move_sky(self, lock=True):
      
        self.move(self.pos_sky, lock)
        self.position = 'SKY'
        return
    
    def move_sig(self, lock=True):
       
        self.move(self.pos_sig, lock)
        self.position = 'SIG'
        return
    
    def unlock_brake(self):
       
        self.mtr.do_output(2, 0)
        msg = '!! Electromagnetic brake is now UNLOCKED !!'
        print('*'*len(msg))
        print(msg)
        print('*'*len(msg))
        return
    
    def lock_brake(self):
     
        self.mtr.do_output(0)
        self.get_count()
        print('')
        print('')
        print('!! CAUTION !!')
        print('-------------')
        print('You must execute s.move_org() method, before executing any "move_**" method.')
        print('')
        return
    
    def clear_alarm(self):
      
        self.mtr.do_output(1)
        return
        
    def clear_interlock(self):
       
        self.mtr.ctrl.off_inter_lock()
        return

def slider():
    client = pyinterface.server_client_wrapper.control_client_wrapper(
        slider_controller, '192.168.40.13', 4004)
    return client

def slider_monitor():
    client = pyinterface.server_client_wrapper.monitor_client_wrapper(
        slider_controller, '192.168.40.13', 4104)
    return client

def start_slider_server():
    slider = slider_controller()
    server = pyinterface.server_client_wrapper.server_wrapper(slider,
                                                              '', 4004, 4104)
    server.start()
    return server


Enter file contents here
