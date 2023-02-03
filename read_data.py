import os

cat_path = os.getcwd() + '/data/'

for car in os.listdir(cat_path):
    cur_dir = cat_path + car + '/'
    for txt in os.listdir(cur_dir):
        f = open(cur_dir + txt, 'r', encoding='utf-8')
        for line in f.readlines():
            line = line.strip('\n')
            s_list = line.split(';')
            if len(s_list) < 5:
                continue
            print(s_list)
        f.close()
