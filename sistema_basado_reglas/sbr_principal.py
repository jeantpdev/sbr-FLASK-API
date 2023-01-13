from sistema_basado_reglas.sistemadereglas import *
from sistema_basado_reglas.reglas import *

def sbr(datos_usuario_temporal):

    engine = sistemadereglas()

    engine.reset()

    lista = datos_usuario_temporal[0]
    Respuesta_abdominal = lista['respuesta_abdominal']
    Respuesta_diarrea = lista['respuesta_diarrea']
    Respuesta_estrenimiento = lista['respuesta_estrenimiento']
    Respuesta_acidez = lista['respuesta_acidez']
    Respuesta_vomitos = lista['respuesta_vomitos']
    engine.declare(reglas(resp_vomitos=Respuesta_vomitos))
    engine.declare(reglas(resp_abdominal=Respuesta_abdominal))
    engine.declare(reglas(resp_diarrea=Respuesta_diarrea))
    engine.declare(reglas(resp_acidez=Respuesta_acidez))
    engine.declare(reglas(resp_estrenimiento=Respuesta_estrenimiento))

    engine.run()

    respuesta_sbr = engine.lista_respuestas[0]
    lista.clear()

    return respuesta_sbr