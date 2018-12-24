import numpy as np

def dispersion(x):
    return np.sqrt(np.sum(((x - np.mean(x))**2)/(len(x)-1)))

def tolerance(tolerance, path):
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
    meas_filter = []
    i = 1
    while True:
        try:
            data = np.loadtxt(path + '/res/%s (res).txt' % i, skiprows=1)
            Res = data[:, 1]
            if dispersion(Res) <= tolerance:
                meas_filter.append(i)
            
            i += 1
        except IOError:
            break
        
    return meas_filter

def weightedMean(measurements, weights):
    """
    Devuelve el promedio pesado de una muestra con sus respectivos errores.
    
    Input: (X, X_err)  lists
    
    Returns: float
    .
    .
    """
    wTotal = 0
    mwTotal = 0
    mean = 0
    for i in range(0, len(weights)):
        wTotal += 1 / weights[i]**2
    for i in range(0, len(measurements)):
        mwTotal += measurements[i]*(1/weights[i]**2)
    mean = mwTotal / wTotal 
    return mean

def error_I(y, SMU, source = False):
    """
    Esta funcion esta diseniada para crear un array con los errores de la corriente 
    medida o sourceada por un Kiethley 2611B, 2612B, 2614B.
    La funcion toma una lista que tiene la corriente, y un boolean que indica si la 
    corriente fue medida o sourceada.
    
    Input: (I, source = False)
    
    Si no se especifica el source, entonc
    I_led_temp_1 = I_led[1:int(len(I_led)/2)]es la corriente fue medida. Si source = True,
    entonces se sourceo con corriente.
    
    Returns:  I_err  (list)
    .
    .
    """
    if SMU == '2612':
        I_temp= y
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 100*pow(10, -9):
                    percentage = 0.0006
                    offset = 100*pow(10, -12)
                elif 100*pow(10, -9) < I_temp[i] and I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.0003
                    offset = 800*pow(10, -12)    
                elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<=10*pow(10, -6): 
                    percentage = 0.0003
                    offset = 5*pow(10, -9)
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.0003
                    offset = 60*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.0003
                    offset = 300*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.0003
                    offset = 6*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.0003
                    offset = 30*pow(10, -6)                
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0005
                    offset = 1.8*pow(10, -3)
                elif 1<I_temp[i] and I_temp[i] <= 1.5: 
                    percentage = 0.0006
                    offset = 4*pow(10, -3)
                else:
                    percentage = 0.005
                    offset = 40*pow(10, -3)
                temp.append(I_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 100*pow(10, -9):
                    percentage = 0.0006
                    offset = 100*pow(10, -12)
                elif 100*pow(10, -9) < I_temp[i] and I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00025
                    offset = 500*pow(10, -12)    
                elif 1*pow(10, -6)<I_temp[i] and I_temp[i]<=10*pow(10, -6): 
                    percentage = 0.00025
                    offset = 1.5*pow(10, -9)
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.0002
                    offset = 25*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.0002
                    offset = 200*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.0002
                    offset = 2.5*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.0002
                    offset = 20*pow(10, -6)                
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0003
                    offset = 1.5*pow(10, -3)
                elif 1<I_temp[i] and I_temp[i] <=1.5: 
                    percentage = 0.0005
                    offset = 3.5*pow(10, -3)
                else:
                    percentage = 0.004
                    offset = 25*pow(10, -3)
                temp.append(I_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
    
    elif SMU == '2400':
        I_temp= y
        temp = []
        percentage = 0
        offset = 0
        if source == False:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00029
                    offset = 300*pow(10, -12)
                elif 1*pow(10, -6) < I_temp[i] and I_temp[i] <= 10*pow(10, -6):
                    percentage = 0.00027
                    offset = 700*pow(10, -12)    
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.00025
                    offset = 6*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.00027
                    offset = 60*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.00035
                    offset = 600*pow(10, -9)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.00055
                    offset = 6*pow(10, -6)
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0022
                    offset = 570*pow(10, -6)                
                temp.append(I_temp[i]*percentage + offset)
                
        elif source==True:
            for i in range(0, len(I_temp)):
                if I_temp[i] <= 1*pow(10, -6):
                    percentage = 0.00035
                    offset = 600*pow(10, -12)
                elif 1*pow(10, -6) < I_temp[i] and I_temp[i] <= 10*pow(10, -6):
                    percentage = 0.00033
                    offset = 2*pow(10, -9)    
                elif 10*pow(10, -6)<I_temp[i] and I_temp[i]<=100*pow(10, -6): 
                    percentage = 0.00031
                    offset = 20*pow(10, -9)
                elif 100*pow(10, -6)<I_temp[i] and I_temp[i]<=1*pow(10, -3): 
                    percentage = 0.00034
                    offset = 200*pow(10, -9)
                elif 1*pow(10, -3)<I_temp[i] and I_temp[i]<=10*pow(10, -3): 
                    percentage = 0.00045
                    offset = 2*pow(10, -6)
                elif 10*pow(10, -3)<I_temp[i] and I_temp[i]<=100*pow(10, -3): 
                    percentage = 0.00066
                    offset = 20*pow(10, -6)
                elif 100*pow(10, -3)<I_temp[i] and I_temp[i]<=1: 
                    percentage = 0.0027
                    offset = 900*pow(10, -6)                
                temp.append(I_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')        
    
    return np.asanyarray(temp)


def error_V(x, SMU, source = True):
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
    if SMU == '2612':
        V_temp = x
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.0002
                    offset = 375*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 600*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.0002
                    offset = 5*pow(10, -3)
                else:
                    percentage = 0.0002
                    offset = 50*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.00015
                    offset = 225*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 350*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.00015
                    offset = 5*pow(10, -3)
                else:
                    percentage = 0.00015
                    offset = 50*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
    
    elif SMU == '2400':
        V_temp = x
        temp = []
        percentage = 0
        offset = 0
        if source == True:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.0002
                    offset = 600*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.0002
                    offset = 600*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.0002
                    offset = 2.4*pow(10, -3)
                else:
                    percentage = 0.0002
                    offset = 24*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
                
        elif source==False:
            for i in range(0, len(V_temp)):
                if V_temp[i] <= 200*pow(10, -3):
                    percentage = 0.00012
                    offset = 300*pow(10, -6)
                elif 200*pow(10, -3) < V_temp[i] and V_temp[i] <= 2:
                    percentage = 0.00012
                    offset = 300*pow(10, -6)    
                elif 2<V_temp[i] and V_temp[i]<=20: 
                    percentage = 0.00015
                    offset = 1.5*pow(10, -3)
                else:
                    percentage = 0.00015
                    offset = 10*pow(10, -3)
                temp.append(V_temp[i]*percentage + offset)
        else:
            print('Boolean values True or False.')
        
    return np.asanyarray(temp)

def error_R(x):
	temp = []
	for i in range(len(x)):
		temp.append(x[i]*0.0007 + 0.3)

	return np.asanyarray(temp)