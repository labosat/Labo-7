from __future__ import division
import numpy as np
from scipy.odr import Model, RealData, ODR
import scipy.stats as stats

def R_Rq(path, tolerancia):
    """
    Calcula la resistencia de quenching y la temperatura (escrita en funcion de la
    resistencia que mide T) de un conjunto de mediciones, haciendo estadistica sobre los
    datos. 
    Es decir, si mido muchas curvas IV para una dada T, guardo las mediciones en una carpeta
    que contenga: una carpeta '/iv/' que contenga las curvas '/i (iv).txt' y otra carpeta
    '/res/' que contenga las resistencias '/i (res).txt'.
    Esta funcion va a calcular la Rq y la T para cada par (iv, res), y luego va a realizar
    un promedio pesado sobre las Rq y las T, devolviendo dichos parametros con sus errores.
    La funcion se va a encargar de filtrar aquellas mediciones en que la temperatura
    fluctuo mas que la tolerancia deseada, utilizando al funcion pulidor(). La tolerancia
    tipica es de 0.025 para mediciones estacionarias en T.
    El path de la funcion debe ser la carpeta donde se encuentren las carpetas iv y res.

    La funcion asume que la temperatura se midio con una RTD, sourceando corriente y
    midiendo voltaje.
    
    Input:  (path, tolerancia)   [string, float]    
    
    Returns: (R, R_err, Rq, Rq_err, chi2_out, array)  [float, float, float, float, float, list]
    .
    .
    """
    array = f.pulidor(tolerancia, path)
    celdas = 18980
    parameters = 2
    R = []
    R_err = []
    Rq = []
    Rq_err = []
    chi2_out = []
    for i in array:
        data1 = np.loadtxt(path+'/res/%s (res).txt' % i, skiprows=1)
        Res = data1[:, 1]   
        I = data1[:, 2]
        V = I*Res
        V_err = error_V(V, source = False)
        I_err = error_I(I, source = True)
        Res_err_estadistico = f.dispersion(Res) 
        Res_err_sistematico = [np.sqrt((1/I[i]**2) * V_err[i]**2 + ((V[i]/(I[i]**2))**2)*I_err[i]**2) for i in range(len(I))]
        Res_err = [np.sqrt(Res_err_estadistico**2 +  Res_err_sistematico[i]**2) for i in range(len(Res_err_sistematico))]
        R.append(f.weightedMean(Res, Res_err))
        R_err.append(f.weightedError(Res, Res_err))
        data2 = np.loadtxt(path+'/iv/%s (iv).txt' % i)
        V = data2[:, 0]
        I = data2[:, 1]
        dI = error_I(I)
        dV = error_V(V)

        chi2 = []
        Rq_err_temp = []
        m = []
        for j in range(0, len(V) - 2):
            V_temp = V[j:]
            I_temp = I[j:]
            dI_temp = dI[j:]
            dV_temp = dV[j:]

            linear_model = Model(Linear)
            data = RealData(V_temp, I_temp, sx=dV_temp, sy=dI_temp)
            odr = ODR(data, linear_model, beta0=[0., 1.])
            out = odr.run()
            
            m_temp = out.beta[0]
            b_temp = out.beta[1]
            m_err_temp = out.sd_beta[0]
            
            m.append(m_temp)
            chi2.append(out.res_var)
            Rq_err_temp.append((celdas/m_temp**2) * m_err_temp)
        index = f.ClosestToOne(chi2)
        Rq.append(celdas/m[index])
        chi2_out.append(chi2[index])
        Rq_err.append(Rq_err_temp[index])
    return R, R_err, Rq, Rq_err, chi2_out, array


def error_I(y, source = False):
    """
    Esta funcion esta diseniada para crear un array con los errores de la corriente 
    medida o sourceada por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene la corriente, y un boolean que indica si la 
    corriente fue medida o sourceada.
    
    Input: (I, source = False)
    
    Si no se especifica el source, entonces la corriente fue medida. Si source = True,
    entonces se sourceo con corriente.
    
    Returns:  I_err  (list)
    .
    .
    """
    I_temp= y
    temp = []
    percentage = 0
    offset = 0
    if source == True:
        for i in range(0, len(I_temp)):
            if I_temp[i] < 100*pow(10, -9):
                percentage = 0.0006
                offset = 100*pow(10, -12)
            elif 100*pow(10, -9) < I_temp[i] and I_temp[i] < 1*pow(10, -6):
                percentage = 0.0003
                offset = 800*pow(10, -12)    
            elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<10*pow(10, -6): 
                percentage = 0.0003
                offset = 5*pow(10, -9)
            elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<100*pow(10, -6): 
                percentage = 0.0003
                offset = 60*pow(10, -9)
            elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<1*pow(10, -3): 
                percentage = 0.0003
                offset = 300*pow(10, -9)
            elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<10*pow(10, -3): 
                percentage = 0.0003
                offset = 6*pow(10, -6)
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<100*pow(10, -3): 
                percentage = 0.0003
                offset = 30*pow(10, -6)                
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<1: 
                percentage = 0.0005
                offset = 1.8*pow(10, -3)
            elif 1<I_temp[i] and I_temp[i] < 1.5: 
                percentage = 0.0006
                offset = 4*pow(10, -3)
            else:
                percentage = 0.005
                offset = 40*pow(10, -3)
            temp.append(I_temp[i]*percentage + offset)
            
    elif source==False:
        for i in range(0, len(I_temp)):
            if I_temp[i] < 100*pow(10, -9):
                percentage = 0.0006
                offset = 100*pow(10, -12)
            elif 100*pow(10, -9) < I_temp[i] and I_temp[i] < 1*pow(10, -6):
                percentage = 0.00025
                offset = 500*pow(10, -12)    
            elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<10*pow(10, -6): 
                percentage = 0.00025
                offset = 1.5*pow(10, -9)
            elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<100*pow(10, -6): 
                percentage = 0.0002
                offset = 25*pow(10, -9)
            elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<1*pow(10, -3): 
                percentage = 0.0002
                offset = 200*pow(10, -9)
            elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<10*pow(10, -3): 
                percentage = 0.0002
                offset = 2.5*pow(10, -6)
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<100*pow(10, -3): 
                percentage = 0.0002
                offset = 20*pow(10, -6)                
            elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<1: 
                percentage = 0.0003
                offset = 1.5*pow(10, -3)
            elif 1<I_temp[i] and I_temp[i] < 1.5: 
                percentage = 0.0005
                offset = 3.5*pow(10, -3)
            else:
                percentage = 0.004
                offset = 25*pow(10, -3)
            temp.append(I_temp[i]*percentage + offset)
    else:
        print('Boolean values True or False.')
    return temp


def error_V(x, source = True):
    """
    Esta funcion esta diseniada para crear un array con los errores del voltaje 
    medido o sourceado por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene el voltaje, y un boolean que indica si el 
    mismo fue medido o sourceado.
    
    Input: (V, source = True)
    
    Si no se especifica el source, entonces el voltaje fue sourceado. Si source = False,
    entonces se midio voltaje.
    
    Returns:  V_err  (list)
    .
    .
    """
    V_temp = x
    temp = []
    percentage = 0
    offset = 0
    if source == True:
        for i in range(0, len(V_temp)):
            if V_temp[i] < 200*pow(10, -3):
                percentage = 0.0002
                offset = 375*pow(10, -6)
            elif 200*pow(10, -3) < V_temp[i] and V_temp[i] < 2:
                percentage = 0.0002
                offset = 600*pow(10, -6)    
            elif 2<V_temp[i] and V_temp[i]<20: 
                percentage = 0.0002
                offset = 5*pow(10, -3)
            else:
                percentage = 0.0002
                offset = 50*pow(10, -3)
            temp.append(V_temp[i]*percentage + offset)
            
    elif source==False:
        for i in range(0, len(V_temp)):
            if V_temp[i] < 200*pow(10, -3):
                percentage = 0.00015
                offset = 225*pow(10, -6)
            elif 200*pow(10, -3) < V_temp[i] and V_temp[i] < 2:
                percentage = 0.0002
                offset = 350*pow(10, -6)    
            elif 2<V_temp[i] and V_temp[i]<20: 
                percentage = 0.00015
                offset = 5*pow(10, -3)
            else:
                percentage = 0.00015
                offset = 50*pow(10, -3)
            temp.append(V_temp[i]*percentage + offset)
    else:
        print('Boolean values True or False.')
    return temp    


def dispersion(x):
    """
    Esta funcion calcula la standard deviation de una muestra 'x'.
    
    Input: x  (list or array)
    
    Returns: int
    .
    .
    """
    return np.sqrt(np.sum(((x - np.mean(x))**2)/(len(x)-1)))



def pulidor(tolerancia, path):
    """
    Esta funcion itera sobre todos los sets de datos que se encuentren en la carpeta 
    del path, y filtra las N mediciones para quedarme solo con las que tienen
    dispersion <= tolerancia. Me devuelve un array sobre el cual tengo analizar los datos,
    asegurandome de que la dispersion en temperatura fue menor a la deseada.
    No hay que poner el numero de mediciones, python las cuenta solo. 
    Solo hay que poner el path!
    Los archivos a iterar deben estar en una location terminada en '/res/i (res).txt', 
    donde i es el numero de set de datos (de 1 a N).
    Tolerancia tipica para mediciones en temperatura en el estacionario ==> 0.03
    
    Input: (tolerancia, path)
    
    Returns: list
    .
    .
    """
    filtro = []
    i = 0
    while True:
        try:
            i = i+1
            data = np.loadtxt(path + '/res/%s (res).txt' % i, skiprows=1)
            Res = data[:, 1]
            if dispersion(Res) <= tolerancia:
                filtro.append(i)
        except IOError:
            break
    return filtro
        
def ClosestToOne(v):
    """
    Esta funcion toma una lista, y devuelve el indice del elemento mas cercano a 1 de 
    la lista.
    
    Input: list
    
    Returns: int  (index)
    .
    .
    """
    compliance = []
    for j in range(0, len(v)):
        compliance.append(abs(v[j] - 1))
    return compliance.index(np.min(compliance))

def promediar_puntos(eje_x, eje_y, p):
    """
    Promediador de puntos para un grafico. Toma un eje X y un eje Y, y promedia cada p
    puntos. Sirve para smoothear mediciones muy ruidosas y densas.
    
    Input: (X, Y, p)  [list, list, int]

    Returns: (X_promediado, Y_promediado)   [list, list]
    .
    .
    """
    array_promediado = []
    array_tiempo_promediado = []
    array1 = eje_y
    array2 = eje_x
    for j in range(int(len(array1)/p)):
        total = 0   
        total_tiempo = 0
        for i in range(p):
            total += array1[j * p + i] / float(p)
            total_tiempo += array2[j * p + i] / float(p)
        array_promediado.append(total)
        array_tiempo_promediado.append(total_tiempo)
    return array_promediado, array_tiempo_promediado


def DerivateData(V, V_err, I, I_err):
    """
    Derivador numerico de datos.
    
    Input: (X, X_err, Y, Y_err)  lists
    
    Returns: (dX, dX_err, dY, dY_err)  lists
    """
    V_temp = []
    I_temp = []
    V_err_temp = []
    I_err_temp = []
    step = V[2] - V[1]
    for i in range(len(I)-1):
        I_temp.append((I[i + 1] - I[i - 1])/(2*step))
        V_temp.append(V[i])
        I_err_temp.append(((I_err[i + 1] - I_err[i - 1])/(2*step))**2)
        V_err_temp.append(V_err[i])
    return V_temp, V_err_temp, I_temp, I_err_temp


def Smooth(V, V_err, I, I_err, degree):
    V_temp = []
    I_temp = []
    V_err_temp = []
    I_err_temp = []
    threshold = 0
    for i in range(len(I)-1):
        if abs(I[i+1]-I[i])> threshold:
            threshold = I[i]            
    for i in range(len(I)-1):
        if not abs(I[i + 1] - I[i]) > (threshold/2) or abs(I[i] - I[i - 1]) > (threshold / 2):
            V_temp.append(V[i])
            I_temp.append(I[i])
            V_err_temp.append(V_err[i])
            I_err_temp.append(I_err[i])
    return V, V_err, I, I_err

def Linear(M, x):
    """
    Funcion lineal para ajustar con el ODR:
        
    >>> linear_model = Model(Linear)
    >>> data = RealData(X, Y, sx=X_err, sy=Y_err)
    >>> odr = ODR(data, linear_model, beta0=[0., 1.])
    >>> out = odr.run()
    
    >>> m = out.beta[0]
    >>> b = out.beta[1]
    >>> m_err = out.sd_beta[0]
    >>> b_err = out.sd_beta[1]        
    >>> chi2 = out.res_var
    .
    .
    """
    m, b = M
    return m*x + b

def weightedMean(measurements, weights):
    """
    Devuelve el promedio pesado de una muestra con sus respectivos errores.
    
    Input: (X, X_err)  lists
    
    Returns: float
    .
    .
    """
    wTotal = np.mean([1/i**2 for i in weights])
    mwTotal = 0
    mean = 0 
#    for i in range(0, len(weights)):
#        wTotal += (1 / weights[i]**2)
    for i in range(0, len(measurements)):
        mwTotal += measurements[i]*(1/weights[i]**2)
    mean = mwTotal / wTotal 
    return mean

def weightedError(measurements, weights):
    """
    A chequear
    """
    wTotal = 0
    weights = np.asarray(weights)
    for i in range(0, len(weights)):
        wTotal += 1 / weights[i]**2
    return (1/wTotal)

def weightedErrorR(measurements, weights):
    """
    A chequear
    """
    wTotal = 0
    for i in range(0, len(weights)):
        wTotal += 1 / weights[i]**2
    Rmean = weightedMean(measurements, weights)
    I = 0.0001
    V = I*Rmean
    V_err = V*0.00015 + 0.000225
    I_err = I*0.0003 + 0.00000006
    return np.sqrt(1/wTotal**2 + ((1/I)**2 * V_err**2 + (V/(I**2))**2 * I_err**2))


def ks_iterative(x, y, x_err, y_err, Foward = True):
    """
    Esta funcion agarra un eje X (k), un eje Y (k_nn) y busca los parametros para
    ajustar la mejor recta, buscando el regimen lineal de la curva. Esto lo hace
    sacando puntos de la curva, ajustando la curva resultante, y luego comparando 
    los parametros de los distintos ajustes con el metodo de Kolmogorov Smirnoff.
    
    Si Foward=True entonces la funcion va a ir sacando puntos del final para
    encontrar kmax. Si Foward=False, la funcion va a sacar puntos del principio para
    calcular kmin. El punto va a estar dado por k[index].
    
    Returns: m, b, ks_stat, index
    
    m: pendiente de la recta resultante
    b: ordenada de la recta resultante
    ks_stat: estadistico de KS de la recta resultante
    index: indice del elemento donde empieza/termina el regimen lineal.
    .
    .
    """
    KS_list = []
    pvalue_list = []
    m_list = []
    b_list = []
    m_err_list = []
    b_err_list = []
    if Foward==True:
        for j in range(0, len(x)-3):
            y_temp = y[:len(y)-j]
            x_temp = x[:len(x)-j]
            x_err_temp = x_err[:len(x_err)-j]
            y_err_temp = y_err[:len(y_err)-j]
            linear_model = Model(Linear)
            data = RealData(x_temp, y_temp, sx=x_err_temp, sy=y_err_temp)
            odr = ODR(data, linear_model, beta0=[0., 1.])
            out = odr.run()
            modelo = [j*out.beta[0]+out.beta[1] for j in x_temp]
            KS_list.append(stats.ks_2samp(y_temp, modelo)[0])
            pvalue_list.append(stats.ks_2samp(y_temp, modelo)[1])
            m_list.append(out.beta[0])
            b_list.append(out.beta[1])
            m_err_list.append(out.sd_beta[0])
            b_err_list.append(out.sd_beta[1])
    else:
        for j in range(0, len(x)-3):
            y_temp = y[:len(y)-j]
            x_temp = x[:len(x)-j]
            x_err_temp = x_err[:len(x_err)-j]
            y_err_temp = y_err[:len(y_err)-j]
            linear_model = Model(Linear)
            data = RealData(x_temp, y_temp, sx=x_err_temp, sy=y_err_temp)
            odr = ODR(data, linear_model, beta0=[0., 1.])
            out = odr.run()
            modelo = [j*out.beta[0]+out.beta[1] for j in x_temp]
            KS_list.append(stats.ks_2samp(y_temp, modelo)[0])
            pvalue_list.append(stats.ks_2samp(y_temp, modelo)[1])
            m_list.append(out.beta[0])
            b_list.append(out.beta[1])
            m_err_list.append(out.sd_beta[0])
            b_err_list.append(out.sd_beta[1])
    index = KS_list.index(min(KS_list))
    m = m_list[index]
    b = b_list[index]
    m_err = m_err_list[index]
    b_err = b_err_list[index]
    ks_stat = KS_list[index]
    
    return m, b, m_err, b_err, ks_stat, index

def promediador_grupos(path, tolerancia, punto_a_punto = True):
    """
    Esta funcion toma una carpeta con mediciones de curvas IV a una dada temperatura,
    y promedia punto a punto las curvas.
    Por otro lado, esta la opcion de promediar punto a punto las resistencias medidas
    o promediar la resistencia promedio de todas las curvas.
    La funcion se va a encargar de filtrar aquellas mediciones en que la temperatura
    fluctuo mas que la tolerancia deseada, utilizando al funcion pulidor(). La tolerancia
    tipica es de 0.025 para mediciones estacionarias en T.
    El path de la funcion debe ser la carpeta donde se encuentren las carpetas iv y res.

    La funcion asume que la temperatura se midio con una RTD, sourceando corriente y
    midiendo voltaje.
    
    Input:  (path, tolerancia)   [string, float]    
    
    Returns: (V_promedio, I_promedio, R_promedio, R_err_promedio)  lists
    .
    .
    """
    array = f.pulidor(tolerancia, path)
    R = []
    R_err = []
    I = []
    V = []
    if punto_a_punto == True:
        for h in array:
            data = np.loadtxt(path+'/res/%s (res).txt' % h, skiprows=1)        
            Res = data[:, 1]   
            I = data[:, 2]
            V = I*Res
            V_err = f.error_V(V, source = False)
            I_err = f.error_I(I, source = True)
            Res_err_estadistico = f.dispersion(Res) 
            Res_err_sistematico = np.sqrt((1/I**2) * V_err**2 + ((V/(I**2))**2)*I_err**2)
            Res_err = np.sqrt(Res_err_estadistico**2 +  Res_err_sistematico**2)   
            R.append(list(Res))
            R_err.append(list(Res_err))
        R_promedio = []
        for i in range(len(R[1])):
            c = 0
            for j in range(len(R)):
                c += R[j][i] 
            R_promedio.append(c/len(R))
        R_err_promedio = []
        for i in range(len(R_err[1])):
            c = 0
            for j in range(len(R_err)):
                c += R_err[j][i] 
            R_err_promedio.append(c/len(R_err))
    else:
        for h in array:
            data = np.loadtxt(path+'/res/%s (res).txt' % h, skiprows=1)
            Res = data[:, 1]   
            I = data[:, 2]
            V = I*Res
            V_err = f.error_V(V, source = False)
            I_err = f.error_I(I, source = True)
            Res_err_estadistico = f.dispersion(Res) 
            Res_err_sistematico = np.sqrt((1/I**2) * V_err**2 + ((V/(I**2))**2)*I_err**2)
            Res_err = np.sqrt(Res_err_estadistico**2 +  Res_err_sistematico**2)
            R.append(f.weightedMean(Res, Res_err))
            R_err.append(f.weightedError(Res, Res_err))
            data2 = np.loadtxt(path+'/iv/%s (iv).txt' % h, skiprows=1)
            V.append(list(data2[:, 0]))
            I.append(list(data2[:, 1]))
        R_promedio = f.weightedMean(R, R_err)
        R_err_promedio = f.weightedError(R, R_err)
        
    I_promedio = []
    for i in range(len(I[1])):
        c = 0
        for j in range(len(I)):
            c += I[j][i] 
        I_promedio.append(c/len(I))
        
    V_promedio = []  
    for i in range(len(V[1])):
        c = 0
        for j in range(len(V)):
            c += V[j][i]
        V_promedio.append(c/len(V))
        
    return V_promedio, I_promedio, R_promedio, R_err_promedio