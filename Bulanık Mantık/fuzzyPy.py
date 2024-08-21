import numpy as np

#üçgen üyelik fonskiyonu
def ucgen(x, abc):
    # a<=b<=c olmalıdır
    assert len(abc) == 3, 'Başlangıc Tepe ve Bitiş Değeri Verilmelidir' 
    a,b,c = np.r_[abc]
    assert a <= b <=c, 'Uyelik FOnksiyon Degerleri Baslangıc <= Tepe <= Bitis'
    y= np.zeros(len(x))


    #sol
    if a != b:
        idx =np.nonzero(np.logical_and(a < x, x < b))[0]
        y[idx] = (x[idx]-a) / float(b-a)
    
    #sağ
    if b != c:
        idx = np.nonzero(np.logical_and(b < x, x < c))
        y[idx] = (c - x[idx]) / float(c-b)
    
    idx =np.nonzero(x==b)
    y[idx] = 1
    return y


def trapez(x, rot, abc):
    y =np.zeros(len(x))
    if(rot == "ORTA"):
        assert len(abc) == 3, 'Baslangic, Tepe ve bitiş Degerleri Verilmelidir!'
        a, b, c = np.r_[abc]
        assert a < b and b < c, 'Uyelik Fonksiyon Degerleri Baslangic <= Tepe <= Bitis'
        idx = np.nonzero(np.logical_and(x >= 0, x < a))[0]
        y[idx] = (x[idx]) /float(a)
        idx = np.nonzero(np.logical_and( x >= a, x < b))[0]
        y[idx]=1
        idx = np.nonzero(np.logical_and(x >= b, x < c))
        y[idx] = (c - x[idx] / float(c - b))
        return y
    else: 
        assert len(abc) == 2, 'Baslangic, Tepe ve Bitis Degerleri Verilmelidir!'
        a, b = np.r_[abc]
        
        if (rot == "SOL"):
            assert a <= b, 'Uyelik Fonksiyonlar Degerleri Baslangic <= Tepe <= Bitis'
            idx = np.nonzero(x < a)[0]
            y[idx] = 1
            idx = np.nonzero(np.logical_and(x >=a, x < b))[0]
            y[idx] = (x[idx] - b) / float(a - b)
            return y
        elif(rot == "SAG"):
            assert a <= b, 'Uyelik Fonksiyon Degerleri Baslangic <= Tepe <= Bitis'
            idx= np.nonzero(x > a)[0]
            y[idx]=1
            idx = np.nonzero(np.logical_and(x > a, x<=b))[0]
            y[idx] = (x[idx]-a) / float(b-a)
            return y 
        
# Gerçek bir degerin bir üyelik fonksiyonuna olan üyelik degerini hesaplayın
def uyelik (x, xmf, xx, zero_outside_x=True):
    if not zero_outside_x:
        kwargs=(None, None)
    else:
        kwargs=(0.0 , 0.0)
        #Numpy ın interpolasyon fonksiyonu
    return np.interp(xx, x, xmf, left=kwargs[0], right=kwargs[1])

def durulastir(x, LFX, model):
    model = model.lower()
    x = x.ravel()
    LFX = LFX.ravel()
    n = len(x)

    if n != len(LFX):
        print("Bulanık Küme Üyeliği ve Değer Sayısı Eşit Olmalıdır.")
        return None
    
    if 'agirlik_merkezi' in model:
        return agirlik_merkezi(x, LFX)
    elif 'maxort' in model:
        return np.mean(x[LFX == LFX.max()])
    elif 'minom' in model:
        return np.min(x[LFX == LFX.max()])
    elif 'maxom' in model:
        return np.max(x[LFX == LFX.max()])
    else:
        print("Geçersiz model ismi:", model)
        return None
    


# Ağırlık merkezi durulaştırma metodu
def agirlik_merkezi(x, LFX):
    sum_moment_area = 0.0
    sum_area = 0.0

    print(f"x: {x}")
    print(f"LFX: {LFX}")

    if len(x) == 1:
        result = x[0] * LFX[0] / np.fmax(LFX[0], np.finfo(float).eps).astype(float)
        print(f"Tek elemanlı durum sonucu: {result}")
        return result
    
    for i in range(1, len(x)):
        x1 = x[i-1]
        x2 = x[i]
        y1 = LFX[i-1]
        y2 = LFX[i]

        print(f"Adım {i}: x1={x1}, x2={x2}, y1={y1}, y2={y2}")

        if not (y1 == y2 == 0.0 or x1 == x2):
            if y1 == y2:
                moment = 0.5 * (x1 + x2)
                area = (x2 - x1) * y1
            elif y2 == 0.0 and y1 != 0.0:
                moment = (2.0/3.0) * (x2 - x1) + x1
                area = 0.5 * (x2 - x1) * y1
            elif y1 == 0.0 and y2 != 0.0:
                moment = (1.0/3.0) * (x2 - x1) + x1
                area = 0.5 * (x2 - x1) * y2
            else:
                moment = (2.0/3.0 * (x2 - x1) * (y2 + 0.5 * y1) / (y1 + y2) + x1)
                area = 0.5 * (x2 - x1) * (y1 + y2)

            print(f"moment: {moment}, area: {area}")

            sum_moment_area += moment * area
            sum_area += area

            print(f"sum_moment_area: {sum_moment_area}, sum_area: {sum_area}")

    if sum_area == 0:
        print("Uyarı: sum_area sıfır, durulaştırma işlemi yapılamadı.")
        return None

    result = sum_moment_area / np.fmax(sum_area, np.finfo(float).eps).astype(float)
    print(f"Nihai sonuç: {result}")
    return result
