import requests
from datetime import datetime, timedelta

# =============================================================================
# Configuracion
# =============================================================================

BASE_URL = "http://localhost:8000/tasks"

# ID de la nota creada en el test 1, reutilizado en tests posteriores
note_id = None


# =============================================================================
# Helpers
# =============================================================================

def get_future_date() -> str:
    """Devuelve una fecha futura (hoy + 7 dias) en formato YYYY-MM-DD."""
    return (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")


def get_past_date() -> str:
    """Devuelve una fecha pasada (ayer) en formato YYYY-MM-DD."""
    return (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")


def assert_status(response: requests.Response, expected: int):
    """Comprueba que el status code de la respuesta coincide con el esperado."""
    actual = response.status_code
    assert actual == expected, f"Status esperado {expected}, obtenido {actual}. Body: {response.text[:200]}"


# =============================================================================
# Tests
# =============================================================================

def test_cleanup_inicial():
    """Limpieza inicial: eliminar todas las notas para partir de un estado limpio."""
    r = requests.delete(BASE_URL)
    # 204 si habia notas, o 204 igualmente (remove_all devuelve bool pero el endpoint siempre da 204)
    assert_status(r, 204)

    # Verificar que la lista esta vacia
    r = requests.get(BASE_URL)
    assert_status(r, 200)
    notes = r.json()["notes"]
    assert len(notes) == 0, f"Se esperaba lista vacia, hay {len(notes)} notas"


def test_crear_nota_ok():
    """Crear una nota valida y verificar que se persiste correctamente."""
    global note_id

    # POST sin body de respuesta -> 201
    payload = {"title": "Test Note", "content": "Contenido de prueba", "deadline": get_future_date()}
    r = requests.post(BASE_URL, json=payload)
    assert_status(r, 201)

    # Verificar con GET que la nota existe
    r = requests.get(BASE_URL)
    assert_status(r, 200)
    notes = r.json()["notes"]
    assert len(notes) == 1, f"Se esperaba 1 nota, hay {len(notes)}"

    nota = notes[0]
    assert nota["title"] == "Test Note", f"Title incorrecto: {nota['title']}"
    assert nota["content"] == "Contenido de prueba", f"Content incorrecto: {nota['content']}"
    assert nota["completed"] is False, "La nota deberia estar sin completar"
    assert nota["created_date"] is not None, "created_date no deberia ser None"

    # Guardar el ID para tests posteriores
    note_id = nota["id"]


def test_crear_nota_ko_campos_faltantes():
    """POST con campos obligatorios faltantes -> 422."""
    payload = {"title": "Solo titulo"}
    r = requests.post(BASE_URL, json=payload)
    assert_status(r, 422)


def test_crear_nota_ko_deadline_invalido():
    """POST con deadline en formato invalido -> 422."""
    payload = {"title": "Nota", "content": "Contenido", "deadline": "no-es-fecha"}
    r = requests.post(BASE_URL, json=payload)
    assert_status(r, 422)


def test_obtener_todas_ok():
    """GET todas las notas -> 200 con al menos 1 nota y campos esperados."""
    r = requests.get(BASE_URL)
    assert_status(r, 200)

    notes = r.json()["notes"]
    assert len(notes) >= 1, "Deberia haber al menos 1 nota"

    # Verificar que cada nota tiene los campos esperados
    campos = {"id", "title", "content", "deadline_date", "completed", "created_date"}
    for nota in notes:
        campos_faltantes = campos - set(nota.keys())
        assert not campos_faltantes, f"Faltan campos en la respuesta: {campos_faltantes}"


def test_obtener_por_id_ok():
    """GET nota por ID existente -> 200 con datos correctos."""
    r = requests.get(f"{BASE_URL}/{note_id}")
    assert_status(r, 200)

    nota = r.json()
    assert nota["id"] == note_id, f"ID esperado {note_id}, obtenido {nota['id']}"
    assert nota["title"] == "Test Note", f"Title incorrecto: {nota['title']}"


def test_obtener_por_id_ko_no_existe():
    """GET nota con ID inexistente -> 404."""
    r = requests.get(f"{BASE_URL}/99999")
    assert_status(r, 404)

    # Verificar formato de error
    body = r.json()
    assert "status" in body, "La respuesta de error debe tener campo 'status'"
    assert "detail" in body, "La respuesta de error debe tener campo 'detail'"


def test_obtener_por_id_ko_id_invalido():
    """GET nota con ID no numerico -> 422."""
    r = requests.get(f"{BASE_URL}/abc")
    assert_status(r, 422)


def test_modificar_nota_ok():
    """PUT modificar nota existente -> 200 con datos actualizados."""
    payload = {"title": "Nota Modificada", "content": "Contenido nuevo", "deadline": get_future_date()}
    r = requests.put(f"{BASE_URL}/{note_id}", json=payload)
    assert_status(r, 200)

    nota = r.json()
    assert nota["title"] == "Nota Modificada", f"Title no se actualizo: {nota['title']}"
    assert nota["content"] == "Contenido nuevo", f"Content no se actualizo: {nota['content']}"


def test_modificar_nota_ko_no_existe():
    """PUT modificar nota inexistente -> 404."""
    payload = {"title": "X", "content": "Y", "deadline": get_future_date()}
    r = requests.put(f"{BASE_URL}/99999", json=payload)
    assert_status(r, 404)


def test_modificar_nota_ko_title_largo():
    """PUT con title que excede 16 caracteres -> 422 (falla validacion de schema)."""
    payload = {"title": "X" * 17, "content": "Contenido", "deadline": get_future_date()}
    r = requests.put(f"{BASE_URL}/{note_id}", json=payload)
    assert_status(r, 422)


def test_modificar_nota_ko_deadline_pasado():
    """PUT con deadline en el pasado -> 400 (schema valido, pero validacion de negocio rechaza)."""
    payload = {"title": "Nota", "content": "Contenido", "deadline": get_past_date()}
    r = requests.put(f"{BASE_URL}/{note_id}", json=payload)
    assert_status(r, 400)


def test_agregar_contenido_ok():
    """PATCH agregar contenido a una nota -> 200."""
    payload = {"content": "Texto adicional"}
    r = requests.patch(f"{BASE_URL}/{note_id}/content", json=payload)
    assert_status(r, 200)


def test_agregar_contenido_ko_vacio():
    """PATCH con contenido vacio -> 422 (min_length=1)."""
    payload = {"content": ""}
    r = requests.patch(f"{BASE_URL}/{note_id}/content", json=payload)
    assert_status(r, 422)


def test_completar_nota_ok():
    """PATCH marcar nota como completada -> 204, verificar con GET."""
    payload = {"completed": True}
    r = requests.patch(f"{BASE_URL}/{note_id}/completed", json=payload)
    assert_status(r, 204)

    # Verificar que el cambio se refleja al consultar la nota
    r = requests.get(f"{BASE_URL}/{note_id}")
    assert_status(r, 200)
    assert r.json()["completed"] is True, "La nota deberia estar completada"


def test_completar_nota_ko_tipo_invalido():
    """PATCH completed con tipo incorrecto (string en vez de bool) -> 422."""
    payload = {"completed": "yes"}
    r = requests.patch(f"{BASE_URL}/{note_id}/completed", json=payload)
    assert_status(r, 422)


def test_notas_expiradas_ok():
    """Crear nota con fecha pasada y verificar que aparece en notas expiradas."""
    # Crear nota con deadline en el pasado
    payload = {"title": "Nota expirada", "content": "Ya vencio", "deadline": get_past_date()}
    r = requests.post(BASE_URL, json=payload)
    assert_status(r, 201)

    # Consultar notas expiradas
    r = requests.get(f"{BASE_URL}/expirationNotes")
    assert_status(r, 200)

    notes = r.json()["notes"]
    assert len(notes) >= 1, "Deberia haber al menos 1 nota expirada"

    # Verificar que la nota expirada esta en la lista
    titles = [n["title"] for n in notes]
    assert "Nota expirada" in titles, f"La nota expirada no aparece en la lista: {titles}"


def test_eliminar_por_id_ok():
    """DELETE nota por ID -> 200, verificar que ya no existe con GET -> 404."""
    r = requests.delete(f"{BASE_URL}/{note_id}")
    assert_status(r, 200)

    # La respuesta es una lista con los IDs eliminados
    ids_eliminados = r.json()
    assert note_id in ids_eliminados, f"El ID {note_id} no esta en la lista de eliminados: {ids_eliminados}"

    # Verificar que la nota ya no existe
    r = requests.get(f"{BASE_URL}/{note_id}")
    assert_status(r, 404)


def test_eliminar_por_id_ko_invalido():
    """DELETE con ID no numerico -> 422."""
    r = requests.delete(f"{BASE_URL}/abc")
    assert_status(r, 422)


def test_eliminar_todas_ok():
    """Crear 2 notas, DELETE todas -> 204, verificar que la lista queda vacia."""
    # Crear 2 notas
    for i in range(2):
        payload = {"title": f"Nota temp {i}", "content": f"Contenido {i}", "deadline": get_future_date()}
        r = requests.post(BASE_URL, json=payload)
        assert_status(r, 201)

    # Verificar que hay al menos 2
    r = requests.get(BASE_URL)
    assert len(r.json()["notes"]) >= 2, "Deberian existir al menos 2 notas"

    # Eliminar todas
    r = requests.delete(BASE_URL)
    assert_status(r, 204)

    # Verificar lista vacia
    r = requests.get(BASE_URL)
    assert_status(r, 200)
    assert len(r.json()["notes"]) == 0, "La lista deberia estar vacia tras eliminar todas"


# =============================================================================
# Main
# =============================================================================

if __name__ == "__main__":
    try:
        test_cleanup_inicial()
        test_crear_nota_ok()
        test_crear_nota_ko_campos_faltantes()
        test_crear_nota_ko_deadline_invalido()
        test_obtener_todas_ok()
        test_obtener_por_id_ok()
        test_obtener_por_id_ko_no_existe()
        test_obtener_por_id_ko_id_invalido()
        test_modificar_nota_ok()
        test_modificar_nota_ko_no_existe()
        test_modificar_nota_ko_title_largo()
        test_modificar_nota_ko_deadline_pasado()
        test_agregar_contenido_ok()
        test_agregar_contenido_ko_vacio()
        test_completar_nota_ok()
        test_completar_nota_ko_tipo_invalido()
        test_notas_expiradas_ok()
        test_eliminar_por_id_ok()
        test_eliminar_por_id_ko_invalido()
        test_eliminar_todas_ok()
    except AssertionError as assertError:
        print(f"Ha habido errores de validaciones en los tests {assertError}")
    
    else:
        print("Todos los tests se han completado correctamente")
