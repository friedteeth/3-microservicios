# Arquitecturas - Microservicios

## Microservicio de Administración de Contenido (MAC)

En la siguiente figura se muestra el diseño del microservicio actual:
![Vista de contenedores del SMAM](docs/diagrama.png)

## Prerrequisitos
- Clonar el repositorio:
   ```shell
   $ git clone https://github.com/friedteeth/3-microservicios.git
   $ cd 3-microservicios
   ```

- Contar con python 3.6 o superior (las pruebas fueron realizadas con la versión 3.6.10). Se recomienda utilizar [pyenv](https://github.com/pyenv/pyenv) como manejador de versiones de python; una vez instalado se pueden seguir los siguientes comandos para instalar la versión deseada de python, esto hay que realizarlo en la raíz del repositorio:
   ```shell
   $ pyenv install 3.6.10
   $ pyenv local 3.6.10
   ```

- Crear un ambiente virtual para manejar las dependencias ejecutando:
   ```shell
   $ python3 -m venv venv
   ```

   o en Windows:
   ```shell
   $ py -3 -m venv venv
   ```

   Esto creará una carpeta llamada "venv" que representa nuestro ambiente virtual y donde instalaremos todas las dependencias.

- Activamos el ambiente virtual:
   ```shell
   $ source venv/bin/activate
   ```

   o en Windows:
   ```shell
   $ venv\Scripts\activate
   ```

- Instalamos las dependencias del sistema ejecutando:
   ```shell
   (venv)$ pip3 install -r requirements.txt 
   ```

   Los paquetes que se instalarán son los siguientes:

   Paquete | Versión | Descripción
   --------|---------|------------
   Flask   | 1.1.1   | Micro framework de desarrollo

   *__Nota__: También puedes instalar estos prerrequisitos manualmente ejecutando los siguientes comandos:*   
   > pip3 install Flask==1.1.1

## Ejecución

Una vez instalados los prerrequisitos es momento de ejecutar el sistema siguiendo los siguientes pasos:
1. Definimos el ambiente de Flask como desarrollo:
   ```shell
   (venv)$ export FLASK_ENV=development
   ```

1. Ejecutamos los microservicios. Cada uno de los microservicios deben correrse en una nueva pestaña de la consola:
   ```shell
   (venv)$ python3 mac/__init__.py
   ```
   ```shell
   (venv)$ python3 mac/ms_create/__init__.py
   ```
   ```shell
   (venv)$ python3 mac/ms_list_and_filter/__init__.py
   ```
   ```shell
   (venv)$ python3 mac/ms_read_and_update/__init__.py
   ```
   
   Si la ejecución fue correcta debe de aparecer lo siguiente en cada pestaña de la consola:
   ```shell
   * Serving Flask app "__init__" (lazy loading)
   * Environment: development
   * Debug mode: on
   * Running on http://0.0.0.0:8084/ (Press CTRL+C to quit)
   * Restarting with stat
   * Debugger is active!
   * Debugger PIN: 285-092-272
   ```

## Pruebas
Para probar los endpoints se pueden realizar a través de un navegador web, una terminal o algún software como [Postman](https://www.postman.com/).

1. Probando con una terminal:
   Obtener los datos de todo el contenido original de Netflix.
   ```shell
   $ curl -X GET localhost:8084/netflix/original-content
   ```

   Respuesta:
   ```shell
   [{"id": 1, "name": "house of cards", "type": "series", "genre": "drama", "imdb_rating": null}, {"id": 2, "name": "stranger things", "type": "series", "genre": "drama", "imdb_rating": null}]
   ```

   Obtener los datos de un contenido original de Netflix.
   ```shell
   $ curl -X GET localhost:8084/netflix/original-content/1
   ```

   Respuesta:
   ```shell
   [{"id": 2, "name": "stranger things", "type": "series", "genre": "drama", "imdb_rating": null}]
   ```

   Filtrar el contenido original de Netflix para únicamente obtener contenido de tipo series y de genero drama.
   ```shell
   $ curl -X GET localhost:8084/netflix/original-content?type=series&genre=drama
   ```

   Respuesta:
   ```shell
   [{"id": 1, "name": "house of cards", "type": "series", "genre": "drama", "imdb_rating": null}, {"id": 2, "name": "stranger things", "type": "series", "genre": "drama", "imdb_rating": null}]
   ```

   Agregar contenido original a Netflix indicando el nombre de la serie o película (Se hace uso del API http://www.omdbapi.com/ para obtener los datos necesarios).
   ```shell
   $ curl -H "Content-Type: application/json" -d "{\"name\":\"Interstellar\"}" -X POST http://localhost:8084/netflix/original-content
   ```

   Respuesta:
   ```shell
   {"success": "Movie added"}
   ```

   Consultamos el contenido original recién agregado.
   ```shell
   $ curl -X GET localhost:8084/netflix/original-content/3
   ```

   Respuesta:
   ```shell
   [{"id": 3, "name": "Interstellar", "type": "movie", "genre": "Adventure, Drama, Sci-Fi, Thriller", "imdb_rating": 8.6}]
   ```

   Se actualiza los datos de un contenido original existente.
   ```shell
   $ curl -H "Content-Type: application/json" -d "{\"genre\":\"Thriller\"}" -X PATCH http://localhost:8084/netflix/original-content/3
   ```

   Respuesta:
   ```shell
   {"success": "Patch successful"}
   ```

   Consultamos nuevamente el contenido original recién actualizado.
   ```shell
   $ curl -X GET localhost:8084/netflix/original-content/3
   ```

   Respuesta:
   ```shell
   [{"id": 3, "name": "Interstellar", "type": "movie", "genre": "Thriller", "imdb_rating": 8.6}]
   ```

## Versión

3.0.0 - Mayo 2020

## Autores

* **Perla Velasco**
* **Yonathan Martínez**
* **Sergio Salazar**
* **Salvador Loera**
* **Francisco Varela**
* **Bryan Villa**
* **Manuel Herrera**
