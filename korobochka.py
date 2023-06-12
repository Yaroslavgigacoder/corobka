import matplotlib.pyplot as plt
import math
import openpyxl
book = openpyxl.open("logs.xlsx", read_only=True)
sheet = book.active

R = 6371000
grad_to_rad = math.pi / 180
rad_to_grad = 180 / math.pi
phiklist = [55.9667]
lyambdaklist = [37.4]
listphiTC = []
listlyambdaTC = []

S1 = 5700
S3 = 500
A = 181  * math.pi / 180
CHPM = 6000
r = 1000
PRAVorLEV = 1
def GeodezZadacha(phi, lyambda, S, A):
    phi = phi * grad_to_rad
    lyambda = lyambda * grad_to_rad

    phik = math.sin(phi) * math.cos(S/R) + math.cos(phi) * math.sin(S/R) * math.cos(A)
    phik = math.asin(phik)

    deltalyambda =(math.sin(A) * math.sin(S/R) * math.cos(phi)) / (math.cos(S/R) - math.sin(phi) * math.sin(phik))
    deltalyambda = math.atan(deltalyambda)

    lyambdak = lyambda + deltalyambda

    phik = phik * rad_to_grad
    lyambdak = lyambdak * rad_to_grad

    phiklist.append(phik)
    lyambdaklist.append(lyambdak)
# ЛЕВЫЙ МАРШРУТ
if PRAVorLEV == 1:
    #  точка начала первого разворота ТНР1
    GeodezZadacha(55.9667, 37.4, S1, A)
    # точка цели 1 ТЦ1
    GeodezZadacha(55.9667, 37.4, S1+r, A)
    # точка начала второго разворота ТНР2
    GeodezZadacha(phiklist[2], lyambdaklist[2], CHPM - r, A + math.pi/2)
    # точка цели ТЦ2
    GeodezZadacha(phiklist[2], lyambdaklist[2], CHPM, A + math.pi/2)
    # точка  4 Тц4
    GeodezZadacha(55.9667, 37.4, S1 + S3 + r, A + math.pi)
    # ТОЧНА ЦЕЛИ 4 тнр4
    GeodezZadacha(phiklist[5], lyambdaklist[5], r, A + math.pi/2)
    # Точка цели тц3
    GeodezZadacha(phiklist[5], lyambdaklist[5], CHPM, A + math.pi/2)
    # ТОчка разворота 3 Тнр3
    GeodezZadacha(phiklist[7], lyambdaklist[7], r, A)
#     ПРАВЫЙ МАРШРУТ
else:
    #  точка начала первого разворота ТНР1
    GeodezZadacha(55.9667, 37.4, S1, A)
    # точка цели 1 ТЦ1
    GeodezZadacha(55.9667, 37.4, S1+r, A)
    # точка начала второго разворота ТНР2
    GeodezZadacha(phiklist[2], lyambdaklist[2], CHPM - r, A - math.pi/2)
    # точка цели ТЦ2
    GeodezZadacha(phiklist[2], lyambdaklist[2], CHPM, A - math.pi/2)
    # точка  4 Тц4
    GeodezZadacha(55.9667, 37.4, S1 + S3 + r, A + math.pi)
    # ТОЧНА ЦЕЛИ 4 тнр4
    GeodezZadacha(phiklist[5], lyambdaklist[5], r, A - math.pi/2)
    # Точка цели тц3
    GeodezZadacha(phiklist[5], lyambdaklist[5], CHPM, A - math.pi/2)
    # ТОчка разворота 3 Тнр3
    GeodezZadacha(phiklist[7], lyambdaklist[7], r, A)

# формирование листов с данными о точках цели
listphiTC.append(phiklist[5])
listphiTC.append(phiklist[2])
listphiTC.append(phiklist[4])
listphiTC.append(phiklist[7])
listphiTC.append(phiklist[5])


listlyambdaTC.append(lyambdaklist[5])
listlyambdaTC.append(lyambdaklist[2])
listlyambdaTC.append(lyambdaklist[4])
listlyambdaTC.append(lyambdaklist[7])
listlyambdaTC.append(lyambdaklist[5])
print(listphiTC, listlyambdaTC)

def CalculetedXTEandXTD (phi1, lyambda1, phi2, lyambda2, phila, lyambdala):
    phi1 = grad_to_rad * phi1
    lyambda1 = grad_to_rad * lyambda1
    phi2 = grad_to_rad * phi2
    lyambda2 = grad_to_rad * lyambda2
    phila = grad_to_rad * phila
    lyambdala = grad_to_rad * lyambdala

    d = math.acos(math.sin(phi1) * math.sin(phila) + math.cos(phi1) * math.cos(phila) * math.cos(lyambdala - lyambda1))
    A = math.atan(math.cos(phila) * math.sin(lyambdala - lyambda1)/(math.cos(phi1) * math.sin(phila) - math.sin(phi1) * math.cos(phila) * math.cos(lyambdala - lyambda1)))
    PU = math.atan(math.cos(phi2) * math.sin(lyambda2 - lyambda1) / (math.cos(phi1) * math.sin(phi2) - math.sin(phi1) * math.cos(phi2) * math.cos(lyambda2 - lyambda1)))

    # print(d, A, PU)
    XTE = math.asin(math.sin(d) * math.sin(A - PU))
    XTD = XTE * R * 180 / math.pi
    ATD = math.acos(math.cos(d) / math.cos(XTE))
    # print(ATD, XTD)

#     уСЛОВИЕ ВЫБОРА ЦЕЛЕВОЙ ТОЧКИ ПРИ ЛЕВОМ КРУГЕ
    if PRAVorLEV == 1:
        if XTD > 0 and 0 < ATD < S1 + S3 + 2000:
            print('ТЦ4 - ТЦ1')
        elif XTD > 0 and ATD < CHPM:
            print('ТЦ1 - ТЦ2')
        elif XTD > 0 and 0 < ATD < S1 + S3 + 2000:
            print('ТЦ2 - ТЦ3')
        elif XTD > 0 and ATD < CHPM:
            print('ТЦ3- ТЦ4')
        else:
            print('участок не подходит')
    else:
        if XTD < 0 and 0 < ATD < S1 + S3 + 2000:
            print('ТЦ4 - ТЦ1')
        elif XTD < 0 and ATD < CHPM:
            print('ТЦ1 - ТЦ2')
        elif XTD < 0 and 0 < ATD < S1 + S3 + 2000:
            print('ТЦ2 - ТЦ3')
        elif XTD < 0 and ATD < CHPM:
            print('ТЦ3 - ТЦ4')
        else:
            print('участок неподходит')


for row in range(1, sheet.max_row):
    phiLA = float(sheet[row+1][0].value)
    lyambdaLA = float(sheet[row+1][1].value)
    print('\n')
    # print(phiLA, lyambdaLA)
    for i in range(0, 4):
        CalculetedXTEandXTD(listphiTC[i], listlyambdaTC[i], listphiTC[i+1], listlyambdaTC[i+1], phiLA, lyambdaLA)




plt.plot(phiklist, lyambdaklist, 'ro')
plt.plot(listphiTC, listlyambdaTC, 'go')
# plt.plot(phiklist, lyambdaklist)
plt.show()
