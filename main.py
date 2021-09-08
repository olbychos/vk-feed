import vk_api
import time
import pandas as pd
import telebot
import re
#from ml import predict 

theme ={
    0:"#Мусор",
    1:"#Математика",
    2:"#Техническое",
    3:"#Программирование",
    4:"#Общее"
}
def calc_label(item):
    if re.search(r' матем| математический| матан|анализ|анализ данных| ml | интеграл| диффур| дифур| тау | умф | урмат|матфиз|ур.матфиз|уравнения|численные методы|численными мет|числюки|числак| твимс| теорвер| тервер| теория| теор |теории вероятности| вероятност|статистика|матстат|мат стат| тфкп | математическ|линал| алгебр| геометр|дифур|оптимиз| тоичм | вектор| вычислител|выч мат| урчп |урматфиз|комплан|комплексные числа| числ |матим| тв | мс | мор |оптимальных решений| оту| исчисление|вариационк|вариационное исчисление ',str(item).lower()):
        return 1
    elif re.search(r' физик| механик| теормех| мех| теор| электротех| тоэ | отц | сопр| сопромат| строймех| теоретически| техмех| оптик| электрич| магнет| атомн| атомк| ядер| детмаш| дмм| тмм | кинемат| динамик| статик| электроник| сапр| электродвиг| элтех',str(item).lower()):
        return 2
    elif re.search(r'js|pascal|python|matlab|scilab|maple|mathcad|css|jav|javascript|oop|html|mathlab| си |паскал|питон|пайтон|программир|информат| бд |excel|sql|access|блок|блок-сх|r | r-studio| r studio',str(item).lower()):
        return 3
    elif re.search(r' курсач| курсовой|зачет|зачёт|подготовк|экзам| ргр | кр |контр|онлайн помощь| онлайн поможет|онлайн сможет| нужна онлайн| контрош| домашк| лаб| диплом| сдат| задач| задани| выполнить | решить | решает |do|anyone|number|тест|дистан| курсов| рассчит|посчитат|срочно нужно| пример |написат| написан|нужна помощь|нужно помочь|кто может помочь|сможет сделат| лабораторн| пересдач| вступител|шарит|кто сделает|кто сделать|кто может сделать',str(item).lower()):
        return 4
    else:
        return 0

def ml_check_message(item):
    item_text=item['text']
    id_sign = None
    if 'signer_id' in item.keys():
        id_sign = item['signer_id']
        link_id = 'https://vk.com/id'+str(id_sign)
    flag = predict(str(item_text).lower())
    if flag !=0:
        item_source_id=item['source_id']
        item_post_id=item['post_id']
        item_link='https://vk.com/wall-{}_{}'.format(str(item_source_id).replace('-',''),str(item_post_id))
        if id_sign != None:
            msg="""{}\nСсылка: {}\nАвтор: {}\nТематика: {}""".format(item_text,item_link,link_id,theme[flag])
        else:
           msg="""{}\nСсылка: {}\nТематика: {}""".format(item_text,item_link,theme[flag])
    else:
        msg = ""
    return msg

def check_message(item):
    item_text=item['text']
    id_sign = None
    if 'signer_id' in item.keys():
        id_sign = item['signer_id']
        link_id = 'https://vk.com/id'+str(id_sign)
    flag = calc_label(item_text)
    if flag !=0:
        item_source_id=item['source_id']
        item_post_id=item['post_id']
        item_link='https://vk.com/wall-{}_{}'.format(str(item_source_id).replace('-',''),str(item_post_id))
        if id_sign != None:
            msg="""{}\nСсылка: {}\nАвтор: {}\nТематика: {}""".format(item_text,item_link,link_id,theme[flag])
        else:
           msg="""{}\nСсылка: {}\nТематика: {}""".format(item_text,item_link,theme[flag])
    else:
        msg = ""
    return msg,flag

    






LOGIN='+601128056097'
PASSWORD='VkFake2019'
TOKEN='e4a88285941fddd97f12dafcff2f0a4667955f54dfd479cfa7eaaa5b54412797ec86b4a6881d04f5405d4'
ID=560165536
TOKEN_TG = '1613239751:AAExF0gCfR5eWU2PFrfu1Lj2NFRukfjm2nU'
CHANNEL_MATH = '-1001360468946'
CHANNEL_ALL = '-1001537714475'

login, password, token = LOGIN, PASSWORD, TOKEN
vk_session = vk_api.VkApi(login,password,token)
vk = vk_session.get_api()
print('vk connected')

bot = telebot.TeleBot(TOKEN_TG)
while True:
    news = vk.newsfeed.get(filters = 'post',count = 10,start_time = time.time()-10)
    items = news['items']
    for item in items:
        msg,flag = check_message(item)
        if len(msg) > 0:
            if flag == 1:
                try:
                    bot.send_message(CHANNEL_MATH,msg)
                except Exception as e:
                    print(e)
            elif flag in [2,3,4]:
                try:
                    bot.send_message(CHANNEL_ALL,msg)
                except Exception as e:
                    print(e)
    time.sleep(10)
