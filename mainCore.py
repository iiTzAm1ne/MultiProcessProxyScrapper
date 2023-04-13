import threading
from tkinter import *
from tkinter import messagebox
from PIL.ImageTk import PhotoImage
from customtkinter import *
from PIL import ImageTk, Image
import requests

set_appearance_mode('Dark')
proxies_http = []
http = 'https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt'
check_link = 'http://httpbin.org/ip'
user_ip = requests.get(check_link).text.split('"')[3]
def getProxies():
    source = requests.get(http)

    for _ in source.text.split('\n'):
        proxies_http.append(_)


slider_value= 0
def slider_event(value):
    global slider_value
    slider_value= value

class App(CTk):

    def __init__(self):
        super().__init__()
        self.textBox = None
        self.bot_Frame = None
        self.mid_Frame = None
        self.slider = None
        self.top_Frame = None
        #os.chdir('')
        self.title('Multi-Process Proxy_Scrapper v.1-Beta')
        self.eval('tk::PlaceWindow . center')
        self.resizable(False, False)
        self.geometry('420x400')
        self.iconbitmap('assets\\icon.ico')

        self.topFrame()
        self.midFrame()
        self.botFrame()

    def topFrame(self):
        image: PhotoImage = ImageTk.PhotoImage(Image.open('assets\\logo.png').resize((100, 100)))
        self.top_Frame = CTkFrame(self, width=420, height=100, border_color='white')
        self.top_Frame.pack(fill=BOTH)
        # noinspection PyBroadException
        try:
            CTkLabel(self.top_Frame, image=image, text='').grid(row=0, rowspan=2, column=0, sticky='w', pady=(10, 0),
                                                                padx=(10, 0))
        except:
            pass
        CTkLabel(self.top_Frame, text='This script is used to target the premium\n'
                                      'DataBasses to get http / https premium proxies\n'
                                      'but please use it in education Only!!', font=('Arial', 12, 'bold'))\
            .grid(row=0, column=1, columnspan=2, sticky='ne', padx=(20, 0))
        slider = CTkSlider(master=self.top_Frame, from_=0, to=200, button_length=20, command=slider_event, button_color='#cccccc')
        slider.set(0)
        slider.grid(row=1, column=2)
        CTkLabel(self.top_Frame, text='Threads:\n(0 - 200)', font=('Arial', 15, 'bold')).grid(row=1, column=1, padx=(20, 0))

    def midFrame(self):
        self.mid_Frame = CTkFrame(self, width=275, height=250)
        self.mid_Frame.pack(fill=BOTH)
        self.textBox = CTkTextbox(self.mid_Frame, width=375, height=250, corner_radius=20)
        self.textBox.grid(row=0, column=0, padx=(23, 0))

    def botFrame(self):
        self.bot_Frame = CTkFrame(self, width=275, height=250)
        self.bot_Frame.pack(fill=BOTH)
        CTkButton(self.bot_Frame, text='Scrap Proxies', fg_color='#cccccc',
                  text_color='black', hover_color='#999999', font=('arial', 12, 'bold'), command=lambda: self.loadProxies()).grid(row=0, column=0, pady=5)
        CTkButton(self.bot_Frame, text='Check Proxies', fg_color='#cccccc',
                  text_color='black', hover_color='#999999', font=('arial', 12, 'bold'), command=lambda: self.checkTextbox()).grid(row=0, column=1, pady=5)
        CTkButton(self.bot_Frame, text='Exit', command=lambda: self.destroy(),
                  fg_color='#cccccc', text_color='black', hover_color='#999999', font=('arial', 12, 'bold')).grid(row=0, column=2, pady=5)

    def loadProxies(self):
        getProxies()
        if len(proxies_http) == 0:
            self.textBox.insert(END, 'Error')
        else:
            file = open('http.txt', 'a+')
            file.truncate(0)
            for _ in proxies_http:
                file.write(f'{_}\n')
                self.textBox.insert(END, f'{_}\n')

            messagebox.showinfo('Success!', 'Your proxies has been scrapped Successfully!!\n'
                                            'and all the proxies has been saved to http.txt')

    def checkTextbox(self):
        if len(self.textBox.get('1.0', 'end-3c')) == 0:
            messagebox.showerror('Connection Error', 'Unable to establish connection with DataBase!!\n'
                                                     'please try to re-scrap again or wait afew second!!')
        else:
            self.textBox.delete('1.0', END)
            self.multiProcessHandel()

    def multiProcessHandel(self):
        #print(slider_value)
        for _ in proxies_http:
            t = threading.Thread(target=self.checkProxiesFunc, args=(_,))
            t.start()

    # noinspection PyBroadException
    def checkProxiesFunc(self, proxy):
        try:
            r = requests.get(url=check_link, proxies={'http': f'http://{proxy}'}, timeout=0.5)
            if r.text.__contains__(user_ip):
                self.textBox.insert(END, f'Bad Proxy: {proxy}\n')
                #print(f'Bad Proxy: {proxy}')
            else:
                self.textBox.insert(END, f'Good Proxy: {proxy}\n')
                #print(f'Good Proxy: {proxy}')
        except:
            pass

if __name__ == '__main__':
    app = App()
    app.mainloop()