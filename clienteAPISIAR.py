"""
    Esta primera versión es una prueba de concepto para probar el funcionamiento de la API

    Existen distintas partes del código que necesitan revisión, están marcados con el símbolo !!!

"""
import requests # peticiones html
import datetime # Para trabajar con las fechas u horas
import time # Para trabajar con las fechas u horas
import math 


API_URL_ROOT = "https://ias1.larioja.org/apiSiar/servicios/v2/"

# FUNCIONES AUXILIARES
def extrae_num_maximo_registros():
    api_url = API_URL_ROOT + "numero-maximo-registros"
    res = requests.get(api_url)
    
    if res.ok:
        res = res.json()
        return(res["numero-maximo-registros"])
    else:
        print("Error al comunicar con la API")

# Test
#extrae_num_maximo_registros()

def extrae_funciones_agregacion(extrae_abreviatura = False):
    api_url = API_URL_ROOT + "funciones-agregacion"
    
    res = requests.get(api_url)
    
    if res.ok:
        res = res.json()
        res = res["funciones"]
        if extrae_abreviatura:
            abreviatura = []
            for i in range(0, len(res)):
                abreviatura.append(res[i]["abreviatura"])
            return(abreviatura)
        else:
            return(res)

    else:
        print("Error al comunicar con la API")

#Test
#extrae_funciones_agregacion()
#extrae_funciones_agregacion(True)



def existe_funcion(abreviatura):
    abreviaturas_posibles = extrae_funciones_agregacion(True)
    for i in abreviaturas_posibles:
        if(i == abreviatura): return(True)
    return(False)

#Test
#existe_funcion("Med")
#existe_funcion("Tremp")


def extrae_parametros(extrae_abreviatura = False):
    api_url = API_URL_ROOT + "parametros"
    
    res = requests.get(api_url)
    
    if res.ok:
        res = res.json()
        res = res["parametros"]
        if extrae_abreviatura:
            abreviatura = []
            for i in range(0, len(res)):
                abreviatura.append(res[i]["abreviatura"])
            return(abreviatura)
        else:
            return(res)

    else:
        print("Error al comunicar con la API")

#Test
#extrae_parametros()
#extrae_parametros(True)

def existe_parametro(abreviatura):
    abreviaturas_posibles = extrae_parametros(True)
    for i in abreviaturas_posibles:
        if(i == abreviatura): return(True)
    return(False)

#Test
#existe_parametro("T")
#existe_parametro("Tremp")

def extrae_frecuencias(extrae_abreviatura = False):
    api_url = API_URL_ROOT + "frecuencias"
    
    res = requests.get(api_url)
    
    if res.ok:
        res = res.json()
        res = res["frecuencias"]
        if extrae_abreviatura:
            abreviatura = []
            for i in range(0, len(res)):
                abreviatura.append(res[i]["abreviatura"])
            return(abreviatura)
        else:
            return(res)

    else:
        print("Error al comunicar con la API")

#Test
#extrae_frecuencias()
#extrae_frecuencias(True)


def existe_frecuencia(abreviatura):
    abreviaturas_posibles = extrae_frecuencias(True)
    for i in abreviaturas_posibles:
        if(i == abreviatura): return(True)
    return(False)

#Test
#existe_frecuencia("T")
#existe_frecuencia("Tremp")

def extrae_posiciones(extrae_abreviatura = False):
    api_url = API_URL_ROOT + "posiciones"
    
    res = requests.get(api_url)
    
    if res.ok:
        res = res.json()
        res = res["posiciones"]
        if extrae_abreviatura:
            abreviatura = []
            for i in range(0, len(res)):
                abreviatura.append(res[i]["abreviatura"])
            return(abreviatura)
        else:
            return(res)

    else:
        print("Error al comunicar con la API")

#Test
#extrae_posiciones()
#extrae_posiciones(True)

def existe_posicion(abreviatura):
    abreviaturas_posibles = extrae_posiciones(True)
    for i in abreviaturas_posibles:
        if(i == abreviatura): return(True)
    return(False)

#Test
#existe_posicion("Standard")
#existe_posicion("Tremp")

NUMERO_MAXIMO_REGISTROS = extrae_num_maximo_registros()
FUNCIONES_AGREGACION = extrae_funciones_agregacion()
PARAMETROS = extrae_parametros()
FRECUENCIAS = extrae_frecuencias()
POSICIONES = extrae_posiciones()


def extrae_estaciones(extrae_codigos = False): #, codigo_estacion = None):
    #if(codigo_estacion  == None): #!!! is.none????
    #    api_url = API_URL_ROOT + "estaciones"
    #else:
    api_url = API_URL_ROOT + "estaciones/" #+ codigo_estacion
    
    res = requests.get(api_url)
    
    if res.ok:
        res = res.json()
        res = res["estaciones"]
        if extrae_codigos:
            codigo_estacion = list()  #[]
            for i in range(0, len(res)):
                codigo_estacion.append(res[i]["codigo_estacion"])
            return(codigo_estacion)
        else:
            return(res)

    else:
        print("Error al comunicar con la API")

#Test
extrae_estaciones()
extrae_estaciones(True)


def existe_estacion(codigo_estacion):
    codigos_posibles = extrae_estaciones(True)
    for i in codigos_posibles:
        if(i == str(codigo_estacion)): return(True) #conversion de tipo porque el valor de la API se registra como str
    return(False)

#Test
#existe_estacion("501")
#existe_estacion(501)
#existe_estacion("Tremp")

def extraer_primera_fecha(estacion, frecuencia):
    # !!! pendiente de modificación API
    # por ahora va a devolver la primera fecha disponible
    res = extrae_estaciones(extrae_codigos = False, codigo_estacion = estacion)
    if frecuencia == 'T':
        return res["fecha_primer_semihorario"]
    else:
        return res["fecha_primer_diario"]

    
def extraer_ultima_fecha(estacion, frecuencia):
    # !!! pendiente de modificación API, por ahora va a devolver la última fecha
  
    h = time.time() # Convetirmos la hora actual a EPOCH y restamos media hora 
    fecha_fin = str(h.year) + "-" + str(h.month) + "-" + str(h.day) + " " + str(h.hour) + ":" + str(h.minute) + ":00"

    return(fecha_fin)
    

def genera_url_datos_climaticos(estacion, frecuencia, **filtros):
    """
    Es función auxiliar de extrae_datos_climaticos_API()

    La url a la que se envía la petición descarta los valores de filtros no válidos, no es necesario analizarlos por nuestra parte
    Ej de la variable filtros = {fecha_inicio: "2015-06-02", funcion = "Max"}, ver manual API los filtros aceptados
    """

    api_url = API_URL_ROOT + "datos-climaticos/" + str(estacion) + "/" + frecuencia # Creamos URL según manual API
    
    if len(filtros) > 0: # probar esta función sin esta condición, si len = 0 (la variable filtro no está definida / está vacía funciona?¿?¿?)
        char_union = "?" # Si hay un filtro se usa el caracter "?" para separar la sintaxis de la consulta principal de los filtros
        for key, value in filtros.items():
            api_url = api_url + char_union + key + "=" + value
            char_union = "&" # Después del primer filtro, si hay otros, se encadenan con "&"
    

    return(api_url)

# Test
#genera_url_datos_climaticos(501, "M")
#genera_url_datos_climaticos(501, "M", **{"fecha_inicio": "2015-01-01", "parametro": "T", "funcion": "Med"})

def extrae_datos_climaticos_API(estacion, frecuencia, **filtros):
    """
        Obtiene la respuesta de la apisiar. Si es correcta devuelve los datos (según la descripción del objeto de respuesta descritos en manual)
        Si es incorrecta puede ser por dos razones:
            - La API responde OK pero hay exceso de parámetros en la respuesta !!! PENDIENTE DE AÑADIR RECURSIVIDAD
            - La API responde OK pero hay algún otro error (???PUEDE SUCEDER???)
            - Error de comunicación con la API (!!!Pendiente gestionar excepción)

        Observaciones:

         !!!posible problema si el usuario quiere más de un parámetro y/o más de una función por cómo se usan los diccionarios y la sintaxis de la API
         !!! pendiente añadir alguna funcionalidad para debugging, si DEBUG = TRUE entonces devolver la api_url generada e información sobre la respuesta recibida.
   
    """
    api_url = genera_url_datos_climaticos(estacion, frecuencia,  **filtros)
    res = requests.get(api_url) # conectamos con esa url método GET y guardamos el contenido en la variable res
    
    if res.ok:
        res = res.json() # lo que nos interesa de la respuesta está en el json, contiene variable "count", "success" y "datos"
        if(res["success"]):
            numero_registros = int(res["count"])
            if numero_registros == 0:
                print("Ningun dato disponible. str(res) = " + str(res))
                return(None)
            elif numero_registros < NUMERO_MAXIMO_REGISTROS:
                return(res)["datos"]
            else:
                print("Se supera el número máximo de registros, numero_registros = ", numero_registros)
                return(extrae_datos_climaticos_exceso_registros(numero_registros, estacion, frecuencia, **filtros))
        else:
            print("Error al recibir los datos. str(res) = " + str(res))
            return(None)
    else:
        print("Error al comunicar con la API")
        return(None)

# Test
print("Extraer datos de la url = " + genera_url_datos_climaticos(501, "M", **{"fecha_inicio": "2015-01-01", "parametro": "T", "funcion": "Med"}))
datos_clima = extrae_datos_climaticos_API(501, "M", **{"fecha_inicio": "2015-01-01", "parametro": "T", "funcion": "Med"})
datos_clima = extrae_datos_climaticos_API(501, "T", **{"fecha_inicio": "2015-01-01", "parametro": "T", "funcion": "Med"})

def extrae_datos_climaticos_exceso_registros(numero_registros, estacion, frecuencia, **filtros):
    
    # chequear si existen filtros de fecha_inicio y/o fecha_fin
    fecha_inicio = None
    fecha_fin = None
    for key, value in filtros.items():
        if key == fecha_inicio: fecha_inicio = value
        if key == fecha_fin: fecha_fin = value
    
    # si no existen añadir fecha_inicio y fin para usarlos como filtros 
    if(fecha_inicio == None): fecha_inicio = extraer_primera_fecha(estacion, frecuencia)
    if(fecha_fin == None): fecha_fin = extraer_ultima_fecha(estacion, frecuencia)

    #calcular el número de peticiones necesarias y otros parámetros útiles:
    numero_peticiones = math.ceil(numero_registros/NUMERO_MAXIMO_REGISTROS)
    
    diferencia = datetime.strptime(fecha_inicio, '%Y-%m-%d') - datetime.strptime(fecha_fin, '%Y-%m-%d %H:%M:%S')

    amplitud_intervalo_fechas = round(diferencia.total_seconds() / numero_peticiones) 
    amplitud_intervalo_en_dias = math.floor(amplitud_intervalo_fechas / (3600 * 24))

    # rehacemos la variable filtros para eliminar fecha_inicio y fecha_fin
    exclude_keys = ['fecha_inicio', 'fecha_fin'] # https://stackoverflow.com/questions/8717395/retain-all-entries-except-for-one-key-python
    filtros_nuevo = {k: filtros[k] for k in set(list(filtros.keys())) - set(exclude_keys)}
    
    f_ini = fecha_inicio
    datos = []
    for i in range(0, numero_peticiones):
        f_fin = datetime.strptime(f_ini, '%Y-%m-%d') + amplitud_intervalo_en_dias * 3600 * 24
        f_fin = datetime.strptime(f_fin, '%Y-%m-%d')
        filtros_nuevo['fecha_inicio'] = f_ini
        filtros_nuevo['fecha_fin'] = f_fin
        datos.append(extrae_datos_climaticos_API(estacion, frecuencia, filtros_nuevo))
        f_ini = f_fin
    
    return(datos)

def filtra_datos_validos(response, incluir_datos_Sospechosos = False, valor_por_defecto_si_no_valido = ""):
    """
    Este es un primer borrador de esta función, modifica la salida para simplificarla, 
    la modificación está adaptada a los usos comunes de los datos extraidos
    desde la API
    !!! Probablemente lo que se debería hacer es un filtro que devolviera sólo los casos válidos, 
        pero con la misma estructura que lo que ofrece la API (estudiar pandas y los dfs por si se puede hacer en modo R, sin bucle for)
        Si la salida simplificada es útil se puede hacer depender la salida de una variable simplify = True/False
    """
    datos_validados = []
    #!!! si solo tiene un valor, da fallos, usar otra forma para gestionar el json
    if  isinstance(response, dict): # si solo tiene un registro, es un diccionario
        dato_valido = response["dato_valido"]
        
        if dato_valido == "V":
            valor = response["valor"]
        elif (incluir_datos_Sospechosos and dato_valido == "S"):
            valor = response["valor"]
        #elif (valor_por_defecto_si_no_valido != ""):
        #    valor = valor_por_defecto_si_no_valido
        else:
            valor = valor_por_defecto_si_no_valido
            
        datos_validados.append({"parametro": response["parametro"],
                                "funcion_agregacion": response["funcion_agregacion"],
                                "fecha": response["fecha"],
                                "valor": valor})
    else:
        for i in range(0, len(response)):
            dato_valido = response[i]["dato_valido"]
        
            if dato_valido == "V":
                valor = response[i]["valor"]
            elif (incluir_datos_Sospechosos and dato_valido == "S"):
                valor = response[i]["valor"]
            #elif (valor_por_defecto_si_no_valido != ""):
            #    valor = valor_por_defecto_si_no_valido
            else:
                valor = valor_por_defecto_si_no_valido
            
            datos_validados.append({"parametro": response[i]["parametro"],
                                "funcion_agregacion": response[i]["funcion_agregacion"],
                                "fecha": response[i]["fecha"],
                                "valor": valor})
    
    return(datos_validados)


# Test
#print("Extraer datos de la url = " + genera_url_datos_climaticos(501, "M", **{"fecha_inicio": "2015-01-01", "parametro": "P", "funcion": "Ac"}))
#datos_brutos_lluvia = extrae_datos_climaticos_API(501, "M", **{"fecha_inicio": "2015-01-01", "parametro": "P", "funcion": "Ac"})
#datos_lluvia = filtra_datos_validos(datos_brutos_lluvia, incluir_datos_Sospechosos = False, valor_por_defecto_si_no_valido = "") 

             
def extrae_datos_parametro(datos_brutos, parametro):
    """
        Dada un objeto de salida con el formato de la apisiar o el formato simplificado tras función filtra_datos
        extrae del objeto aquellos registros cuyo parámetro sea el solicitado
    """
    datos_filtrados = []
    for i in range(0, len(datos_brutos)):
        if datos_brutos[i]["parametro"] == parametro:
            datos_filtrados.append(datos_brutos[i])
    
    return(datos_filtrados)

