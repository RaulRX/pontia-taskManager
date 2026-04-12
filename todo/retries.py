# Leak de variables secretas en GitHub:
# 1 - Artículo interesante sobre problemas en que puedes caer:
# https://dev.to/sky98/10-rookie-mistakes-that-leak-your-api-keys-and-how-to-secure-them-13e8
# 2 - Post de LinkedIn donde también se habla del tema, con referencias y links interesantes:
# https://www.linkedin.com/posts/kalyani-pawar5_im-genuinely-surprised-how-many-openai-api-activity-7345526544842293248-2ubW/






# Sobre el GIL en Python (Global Interpreter Lock) y la concurrencia:
# https://wiki.python.org/moin/GlobalInterpreterLock#:~:text=In%20CPython%2C%20the%20global%20interpreter,areas%20can%20be%20found%20here.
# Artículo más divulgativo:
# https://codigofacilito.com/articulos/gil-python
# En Python 3.14 (bastante reciente) se ha abordado este tema:
# https://towardsdatascience.com/python-3-14-and-the-end-of-the-gil/





# Reintentos en requests con Python

# Para simplemente timeout, lo podemos hacer con requests:
import requests
my_url = "..."
requests.get(my_url, timeout=5)  # Timeout de 5 segundos

# La librería `requests` no tiene reintentos automáticos por defecto,
# pero internamente usa `urllib3`, que SÍ tiene un mecanismo de reintentos
# muy potente. Podemos aprovecharlo mediante "adapters" y "sessions".
#
# Conceptos clave:
#   - Session: objeto que persiste configuración entre peticiones (headers,
#     cookies, auth, adapters...). Más eficiente que llamadas sueltas porque
#     reutiliza la conexión TCP subyacente (keep-alive).
#   - Adapter (HTTPAdapter): intermediario entre la Session y urllib3.
#     Aquí es donde inyectamos la estrategia de reintentos.
#   - Retry (de urllib3): define CUÁNDO y CÓMO reintentar.
# =============================================================================

import requests
from requests.adapters import HTTPAdapter

# urllib3 viene incluido con requests, no hace falta instalar nada extra
from urllib3.util.retry import Retry


# -----------------------------------------------------------------------------
# 1. Configurar la estrategia de reintentos
# -----------------------------------------------------------------------------

estrategia_reintentos = Retry(
    # Número total de reintentos (sin contar el intento original)
    total=3,

    # Códigos de estado HTTP que disparan reintento automático.
    # Típicamente se reintenta en errores de servidor (5xx).
    status_forcelist=[429, 500, 502, 503, 504],
    # 429 = Too Many Requests (rate limiting)
    # 500 = Internal Server Error
    # 502 = Bad Gateway
    # 503 = Service Unavailable
    # 504 = Gateway Timeout

    # Métodos HTTP que se permiten reintentar.
    # Por defecto solo reintenta métodos idempotentes (GET, HEAD, OPTIONS...),
    # NO reintenta POST porque podría duplicar la acción.
    # Si queremos reintentar POST también, lo añadimos explícitamente:
    allowed_methods=["GET", "POST", "PUT", "DELETE", "HEAD", "OPTIONS"],

    # Backoff: tiempo de espera entre reintentos, va aumentando.
    # Fórmula: {backoff_factor} * (2 ** (intento - 1))
    #   intento 1 → 1 * 1 = 1 segundo
    #   intento 2 → 1 * 2 = 2 segundos
    #   intento 3 → 1 * 4 = 4 segundos
    # Esto evita saturar un servidor que ya está con problemas.
    backoff_factor=1,

    # Límite máximo del backoff (por si total es alto y crece demasiado)
    backoff_max=30,

    # ¿Reintentar si la conexión se resetea (broken pipe, etc.)?
    # Útil para conexiones inestables.
    raise_on_status=False,
)


# -----------------------------------------------------------------------------
# 2. Crear una Session con el adapter configurado
# -----------------------------------------------------------------------------

session = requests.Session()

# Montamos el adapter con reintentos para URLs http:// y https://
adapter = HTTPAdapter(max_retries=estrategia_reintentos)
session.mount("https://", adapter)
session.mount("http://", adapter)

# También podemos configurar headers por defecto en la session.
# Todas las peticiones hechas con esta session los incluirán.
session.headers.update({
    "Accept": "application/json",
})


# -----------------------------------------------------------------------------
# 3. Ejemplo: petición con timeout
# -----------------------------------------------------------------------------
# El timeout es INDEPENDIENTE de los reintentos.
# Se puede pasar como:
#   - Un solo número: aplica tanto a conexión como a lectura.
#   - Una tupla (connect_timeout, read_timeout):
#       * connect_timeout: tiempo máximo para establecer la conexión TCP.
#       * read_timeout: tiempo máximo esperando a que el servidor responda.
#
# SIN timeout, una petición puede quedarse colgada INDEFINIDAMENTE.
# SIEMPRE es buena práctica poner timeout.

def hacer_peticion_con_reintentos(url: str) -> dict | None:
    """
    Hace una petición GET con reintentos automáticos y timeout.
    Devuelve el JSON de respuesta o None si falla.
    """
    try:
        respuesta = session.get(
            url,
            timeout=(5, 15),  # 5s para conectar, 15s para leer
        )

        # raise_for_status() lanza una excepción si el código HTTP es 4xx/5xx
        # (después de agotar los reintentos, si aplica)
        respuesta.raise_for_status()

        return respuesta.json()

    except requests.exceptions.ConnectionError:
        # No se pudo conectar al servidor (DNS fallido, servidor caído, etc.)
        print("[ERROR] No se pudo conectar al servidor.")

    except requests.exceptions.Timeout:
        # Se superó el timeout (connect o read)
        print("[ERROR] La petición superó el tiempo de espera (timeout).")

    except requests.exceptions.HTTPError as e:
        # Error HTTP (4xx o 5xx) que no se resolvió con reintentos
        print(f"[ERROR] Error HTTP: {e.response.status_code} - {e.response.reason}")

    except requests.exceptions.RequestException as e:
        # Cualquier otro error de requests (captura genérica, siempre al final)
        print(f"[ERROR] Error inesperado: {e}")

    return None
