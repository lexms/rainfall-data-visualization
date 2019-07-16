
import matplotlib.pyplot as plt 
import math
import numpy

# NIM : 10116370
# Nama : Alexander M S
# Kelas : MOSI-8


count_global = 28

class simulate_curah_hujan_harian:
    def __init__(self):
        self.a = 2
        self.c = 3
        self.m = 270000
        self.z0 = 10116370

        self.fi_times_xi = 789
        self.fi = 90
        self.beta = self.fi_times_xi/self.fi
        
        self.count = count_global

    def LCG_formula(self,zi_minus_1):
        return (self.a * zi_minus_1 + self.c) % self.m


    def ui_generate(self, zi):
        return zi / self.m

    def curah_hujan_harian_generate(self,ui):
        return -1 * self.beta * math.log(ui)


    def rng_list(self):
        _list=[]
        for i in range(0,self.count):
            if i == 0:
                zi = self.LCG_formula(self.z0)
                ui = self.ui_generate(zi)
                chh = self.curah_hujan_harian_generate(ui)
                _list.append({'Zi-1': self.z0, 'Zi' : zi, 'Ui' : ui, 'CHH': chh})
            elif i>0:
                zi_minus_1 = self.LCG_formula(_list[i-1]['Zi-1'])
                zi = self.LCG_formula(zi_minus_1)
                ui = self.ui_generate(zi)
                chh = self.curah_hujan_harian_generate(ui)
                _list.append({'Zi-1': zi_minus_1, 'Zi' : zi, 'Ui' : ui, 'CHH': chh})

        return _list


    def day_name_generate(self, day_number):
        switcher = {
            1: "Senin",
            2: "Selasa",
            3: "Rabu  ",
            4: "Kamis",
            5: "Jumat",
            6: "Sabtu",
            0: "Minggu"
        }
        return switcher.get(day_number,"invalid number days")

    def print_table(self):
        _list = self.rng_list()
        print('\n===Curah Hujan Harian===\n')
        print('| No.\t |  Hari\t | Zi\t\t | Ui\t\t | Curah Hujan Harian\t |')
        print('--------------------------------------------------------------------------')
        for i in range(0,len(_list)):
            print("| {}\t | {}\t | {:.4f} \t | {:.4f} \t | {:.4f} \t |".format(i+1, self.day_name_generate((i+1)%7), _list[i]['Zi'], _list[i]['Ui'], _list[i]['CHH']))

    def get_mean(self):
        _list = self.rng_list()
        x=0
        for i in range(0,len(_list)):
            x = _list[i]['CHH'] + x
        mean = x/self.count
        print('\n Rata-rata Curah Hujan = {:.4f}'.format(mean),'mm')


class simulate_lama_hujan_harian:
    def __init__(self, max, min):
        self.a = 4
        self.m = 741293
        self.z0 = 10116370

        self.min = 1
        self.max = 19
        
        self.count = count_global

    def multiplicative_formula(self,zi_minus_1):
        return (self.a * zi_minus_1) % self.m

    def ui_generate(self, zi):
        return zi / self.m

    def lama_hujan_harian_generate(self,ui):
        return self.min + ( (self.max-self.min) * ui )


    def multiplicative_list(self):
        _list = []
        for i in range(0,self.count):
            if i == 0:
                zi = self.multiplicative_formula(self.z0)
                ui = self.ui_generate(zi)
                lhh = self.lama_hujan_harian_generate(ui)
                _list.append({'Zi-1': self.z0, 'Zi' : zi, 'Ui' : ui, 'LHH': lhh})
            elif i>0:
                zi_minus_1 = self.multiplicative_formula(_list[i-1]['Zi-1'])   
                zi = self.multiplicative_formula(zi_minus_1)
                ui = self.ui_generate(zi)
                lhh = self.lama_hujan_harian_generate(ui)
                _list.append({'Zi-1': zi_minus_1, 'Zi' : zi, 'Ui' : ui, 'LHH': lhh})

        return _list


    def day_name_generate(self, day_number):
        switcher = {
            1: "Senin",
            2: "Selasa",
            3: "Rabu  ",
            4: "Kamis",
            5: "Jumat",
            6: "Sabtu",
            0: "Minggu"
        }
        return switcher.get(day_number,"invalid number days")

    def print_table(self):
        _list = self.multiplicative_list()
        print('\n===Lama Hujan Harian===\n')
        print('| No. |  Hari\t | Zi\t\t | Ui\t\t | Lama Hujan Harian\t |')
        print('--------------------------------------------------------------------------')
        for i in range(0,len(_list)):
            print("| {} | {}\t | {:.4f} \t | {:.4f} \t | {:.4f} \t |".format(i+1, self.day_name_generate((i+1)%7), _list[i]['Zi'], _list[i]['Ui'], _list[i]['LHH']))

    def get_mean(self):
        _list = self.multiplicative_list()
        x=0
        for i in range(0,len(_list)):
            x = _list[i]['LHH'] + x
        mean = x/self.count
        print('\n Rata-rata Lama Hujan = {:.4f}'.format(mean),'jam')






class1 = simulate_curah_hujan_harian()


class2 = simulate_lama_hujan_harian(max,min)

class global_function:
    def __init__(self):        
        self.count = count_global
        self.count_hsr = 0
        self.count_hr = 0
        self.count_hs = 0
        self.count_hl = 0
        self.count_hsl = 0
   

    def rainfall_intensity_list(self):
        _list_chh = class1.rng_list()
        _list_lhh = class2.multiplicative_list()
        _list_rainfall_intensity = []
        for i in range(0, len(_list_chh)):
            rainfall_intensity = _list_chh[i]['CHH'] / _list_lhh[i]['LHH']

            if rainfall_intensity < 1:
                status = 'Hujan Sangat Ringan'
            elif 1 <= rainfall_intensity < 5:
                status = 'Hujan Ringan       ' 
            elif 5 <= rainfall_intensity < 10:
                status = 'Hujan Sedang       '
            elif 10 <= rainfall_intensity < 20:
                status = 'Hujan Lebat        ' 
            elif rainfall_intensity >= 20:
                status = 'Hujan Sangat Lebat'  
            
            _list_rainfall_intensity.append({'R_I': rainfall_intensity, 'STATUS': status}) 
            #R_I = rainfall intensity
        return _list_rainfall_intensity

    def day_name_generate(self, day_number):
        switcher = {
            1: "Senin  ",
            2: "Selasa ",
            3: "Rabu   ",
            4: "Kamis  ",
            5: "Jumat  ",
            6: "Sabtu  ",
            0: "Minggu"
        }
        return switcher.get(day_number,"invalid number days")
        
    def printall(self):
        _list_chh = class1.rng_list()
        _list_lhh = class2.multiplicative_list()
        _list_rainfall_intensity = self.rainfall_intensity_list()
        
        #declaring seperated array
        _list_all_data = []
        _list_rainfall_intensity_only = []
        _list_day_only = []
        _list_chh_only = []
        _list_lhh_only = []
        

        print('\n================================================================Data Hujan Harian=========================================================================\n')
        print('| No.\t |  Hari\t | Ui (LCG)\t | Ui (Multipli) | Curah Hujan(mm) \t  | Lama Hujan(jam) \t  | Intensitas (mm/jam)\t | Status\t\t |')
        print('----------------------------------------------------------------------------------------------------------------------------------------------------------')
        for i in range(0,len(_list_chh)):

            day = self.day_name_generate((i+1) % 7)
            ui_chh = _list_chh[i]['Ui']
            ui_lhh = _list_lhh[i]['Ui']
            chh = _list_chh[i]['CHH']
            lhh = _list_lhh[i]['LHH']
            rainfall_intensity = _list_rainfall_intensity[i]['R_I']
            status = _list_rainfall_intensity[i]['STATUS']

    
            print('| {}\t | {}\t | {:.4f} \t | {:.4f} \t | {:.4f} \t\t  | {:.4f} \t\t  | {:.4f} \t\t | {}\t |'.format(i+1, day, 
                ui_chh, 
                ui_lhh, 
                chh, 
                lhh,
                rainfall_intensity,
                status))

            _list_all_data.append({'NO':i, 'HARI':day, 'UI_CHH': ui_chh, 'UI_LHH': ui_lhh, 'CHH':chh, 'LHH':lhh, 'R_I': rainfall_intensity, 'STATUS': status})
            
            _list_chh_only.append(chh)
            _list_lhh_only.append(lhh)
            _list_rainfall_intensity_only.append(rainfall_intensity)


            _custom_day = str(i+1) + '. ' + day
            _list_day_only.append(_custom_day)

            if status == 'Hujan Sangat Ringan':
                self.count_hsr += 1
            elif status == 'Hujan Ringan       ':
                self.count_hr += 1
            elif status == 'Hujan Sedang       ':
                self.count_hs += 1
            elif status == 'Hujan Lebat        ':
                self.count_hl += 1
            elif status == 'Hujan Sangat Lebat':  
                self.count_hsl += 1

                
 
            #END FOR
        
        
        print('============================================================================================================================================================')


        #PLOTTING GRAPH


        #FIGURE 1
        plt.figure(1)
        grid_1_plotlib_x = 1
        grid_1_1plotlib_y = 1

        #GRAPH 1.1
        data_status = { 'Hujan\nSangat\nRingan': self.count_hsr, 
                        'Hujan\nRingan': self.count_hr, 
                        'Hujan\nSedang': self.count_hs, 
                        'Hujan\nLebat': self.count_hl,
                        'Hujan\nSangat\nLebat': self.count_hsl}

        names_status = list(data_status.keys())
        values_status = list(data_status.values())

        plt.subplot(grid_1_plotlib_x,grid_1_1plotlib_y,1)
        plt.bar(names_status, values_status)
        plt.xlabel('')
        plt.ylabel('Jumlah Kejadian')

 
        #FIGURE 2
        plt.figure(2)
        grid_2_plotlib_x = 1
        grid_2_plotlib_y = 3
        
        #GRAPH 2.1
        plt.subplot(grid_2_plotlib_y,grid_2_plotlib_x,1)
        plt.plot(_list_day_only,_list_chh_only)
        plt.xticks(rotation=90)
        plt.xlabel('')
        plt.ylabel('Curah Hujan (mm)')

        #GRAPH 2.2
        plt.subplot(grid_2_plotlib_y,grid_2_plotlib_x,2)
        plt.plot(_list_day_only,_list_lhh_only)
        plt.xticks(rotation=90)
        plt.xlabel('')
        plt.ylabel('Lama Hujan (jam)')

        #GRAPH 2.3
        plt.subplot(grid_2_plotlib_y,grid_2_plotlib_x,3)
        plt.plot(_list_day_only,_list_rainfall_intensity_only)
        plt.xticks(rotation=90)
        plt.xlabel('')
        plt.ylabel('Intentsitas Hujan (mm/jam)')
  
        #FIGURE 3

    def get_mean(self):
        _list = self.rainfall_intensity_list()
        x=0
        for i in range(0,len(_list)):
            x = _list[i]['R_I'] + x
        mean = x/self.count
        print('\n Rata-rata Intensitas Hujan = {:.4f}'.format(mean),'mm/jam')

    def get_max_min(self):
        _list = self.rainfall_intensity_list()
        rainfall_intensity_only = []

        # converting array style
        for i in range(0,len(_list)):
            rainfall_intensity_list = _list[i]['R_I']
            rainfall_intensity_only.append(rainfall_intensity_list)

        maxR_I = numpy.amax(rainfall_intensity_only)
        minR_I = numpy.amin(rainfall_intensity_only)
        print('\n Max Intensitas Hujan = {:.4f}'.format(maxR_I),'mm/jam')
        print('\n Min Intensitas Hujan = {:.4f}'.format(minR_I),'mm/jam')
        




#FUNCTION CALLING

class3 = global_function()

class3.printall()
class1.get_mean()
class2.get_mean()
class3.get_mean()
class3.get_max_min()


plt.show()