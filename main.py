import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Si cambias los permisos en la consola, borra el archivo token.json.
SCOPES = ['https://www.googleapis.com/auth/tasks']

def main():
    try:
        creds = None
        # El archivo token.json almacena los tokens de acceso del usuario.
        if os.path.exists('token.json'):
            try:
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            except ValueError:
                print('token.json no es valido, se generara uno nuevo.')
                creds = None

        # Si no hay credenciales válidas, deja que el usuario inicie sesión.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', SCOPES)
                creds = flow.run_local_server(port=0)
            # Guarda las credenciales para la próxima ejecución
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

        service = build('tasks', 'v1', credentials=creds)

        # Llamada a la API para obtener las listas de tareas
        results = service.tasklists().list(maxResults=10).execute()
        items = results.get('items', [])

        if not items:
            print('No se encontraron listas de tareas.')
            return

        print('Tus listas de tareas:')
        all_tasks = []
        for item in items:
            tasklist_id = item.get('id', 'sin-id')
            tasklist_title = item.get('title', 'Sin titulo')
            print(f"Listado: {tasklist_title} (ID: {tasklist_id})")

            # Ahora leemos las tareas de esta lista específica
            tasks_results = service.tasks().list(tasklist=tasklist_id).execute()
            tasks = tasks_results.get('items', [])

            if not tasks:
                print('  -> No hay tareas en esta lista.')
            else:
                for task in tasks:
                    status = "✅" if task.get('status') == 'completed' else "⭕"
                    title = task.get('title', 'Tarea sin titulo')
                    task_id = task.get('id', 'sin-id')
                    print(f"  {status} {title} (ID: {task_id})")
                    if task.get('status') != 'completed' and task_id != 'sin-id':
                        all_tasks.append({
                            'list_id': tasklist_id,
                            'task_id': task_id,
                            'title': title,
                            'list_title': tasklist_title,
                        })

        if all_tasks:
            print('\nTareas pendientes:')
            for idx, task in enumerate(all_tasks, start=1):
                print(f"{idx}. [{task['list_title']}] {task['title']}")

            choice = input('\nEscribe el numero de tarea para marcarla como completada (Enter para salir): ').strip()
            if choice:
                if choice.isdigit() and 1 <= int(choice) <= len(all_tasks):
                    selected = all_tasks[int(choice) - 1]
                    body = {'status': 'completed'}
                    service.tasks().patch(
                        tasklist=selected['list_id'],
                        task=selected['task_id'],
                        body=body,
                    ).execute()
                    print(f"Tarea marcada como completada: {selected['title']}")
                else:
                    print('Seleccion no valida. No se actualizo ninguna tarea.')
        else:
            print('\nNo hay tareas pendientes para marcar como completadas.')
    except FileNotFoundError:
        print('No se encontro credentials.json. Descargalo desde Google Cloud Console.')
    except HttpError as error:
        print(f'Error al llamar a Google Tasks API: {error}')

if __name__ == '__main__':
    main()
