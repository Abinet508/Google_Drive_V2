import os
from oauth2client.service_account import ServiceAccountCredentials
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive


class GoogleDriveManager:
    """
    A class to manage Google Drive.
    """

    def __init__(self, path=None):
        self.file_dict_by_title = None
        self.file_dict_by_id = None
        self.drive = None
        self.file_list = None
        self.path = path
        if path:
            self.create_path(self.path)
        self.service_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials',
                                              'Service_credentials.json')
        os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'credentials'), exist_ok=True)
        self.drive = self.get_drive()
        self.list_files()

    def get_drive(self):
        """
        Get the Google Drive service.
        """
        if self.drive is None:
            self.drive = self.get_service()
        return self.drive

    def get_service(self):
        """
        Get the Google Drive service.
        """
        gauth = GoogleAuth()
        scopes = ['https://www.googleapis.com/auth/drive']
        credentials = ServiceAccountCredentials.from_json_keyfile_name(self.service_file_path, scopes)
        gauth.credentials = credentials
        drive = GoogleDrive(gauth)
        return drive

    @staticmethod
    def create_path(path):
        """
        Create a directory at the given path if it doesn't already exist.
        """
        os.makedirs(path, exist_ok=True)
        os.chmod(path, 0o777)

    def list_files(self, display=False):
        """
        List all files in the Google Drive.
        """
        self.file_list = self.drive.ListFile({'q': "'root' in parents and trashed=false"}).GetList()
        self.file_dict_by_title = {}
        self.file_dict_by_id = {}
        for file in self.file_list:
            self.file_dict_by_title[file['title']] = file['id']
            self.file_dict_by_id[file['id']] = file['title']
            if display:
                print('title: %s, id: %s' % (file['title'], file['id']))

    def upload_file(self, file_path, title):
        """
        Upload a file to Google Drive.
        """
        if not os.path.exists(file_path):
            raise FileNotFoundError('File not found at {}'.format(file_path))
        else:
            file = self.drive.CreateFile({'title': title})
            file.SetContentFile(file_path)
            file.Upload()
            print('Uploaded file with ID {}'.format(file.get('id')))

    def download_file(self, file_id, output_path):
        """
        Download a file from Google Drive.
        """
        file = self.drive.CreateFile({'id': file_id})
        file.GetContentFile(output_path)
        print('Downloaded file to {}'.format(output_path))

    def delete_file(self, file_id):
        """
        Delete a file from Google Drive.
        """
        file = self.drive.CreateFile({'id': file_id})
        file.Trash()  # Move file to trash.
        file.UnTrash()  # Move file out of trash.
        file.Delete()  # Permanently delete the file.
        print('Deleted file with ID {}'.format(file_id))

    def get_file_id(self, title):
        """
        Get the ID of a file in Google Drive.
        """
        for file in self.file_list:
            if file['title'] == title:
                return file['id']
        return None

    def get_file_title(self, file_id):
        """
        Get the title of a file in Google Drive.
        """
        for file in self.file_list:
            if file['id'] == file_id:
                return file['title']
        return None

    def set_drive(self, drive):
        """
        Set the Google Drive service.
        """
        self.drive = drive

    def update_file(self, file_id, new_title, new_content):
        """
        Update a file in Google Drive.
        """
        file = self.drive.CreateFile({'id': file_id})
        file['title'] = new_title  # Change title of the file.
        file.SetContentString(new_content)  # Change content of the file.
        file.Upload()  # Upload the file.
        print('Updated file with ID {}'.format(file_id))

    def create_folder(self, title):
        """
        Create a folder in Google Drive.
        """
        folder_metadata = {'title': title, 'mimeType': 'application/vnd.google-apps.folder'}
        folder = self.drive.CreateFile(folder_metadata)
        folder.Upload()
        print('Created folder with ID {}'.format(folder.get('id')))

    def upload_file_to_folder(self, folder_id, file_path, title):
        """
        Upload a file to a specific folder in Google Drive.
        """
        file = self.drive.CreateFile({'title': title, 'parents': [{'id': folder_id}]})
        file.SetContentFile(file_path)
        file.Upload()
        print('Uploaded file with ID {} to folder with ID {}'.format(file.get('id'), folder_id))

    def list_files_in_folder(self, folder_id):
        """
        List all files in a specific folder in Google Drive.
        """
        query = "'{}' in parents and trashed=false".format(folder_id)
        file_list = self.drive.ListFile({'q': query}).GetList()
        for file in file_list:
            print('title: %s, id: %s' % (file['title'], file['id']))

    def get_folder_by_file(self, file_id=None, file_title=None):
        """
        Get the folder of a file in Google Drive.
        """
        if file_id:
            file = self.drive.CreateFile({'id': file_id})
        elif file_title:
            if not self.file_dict_by_title:
                self.list_files()
            file_id = self.file_dict_by_title.get(file_title, None)
            if file_id:
                file = self.drive.CreateFile({'id': file_id})
            else:
                return None
        else:
            return None
        return file['parents'][0]

    def download_file_from_folder(self, folder_id, file_id, output_path):
        """
        Download a file from a specific folder in Google Drive.
        """
        file = self.drive.CreateFile({'id': file_id, 'parents': [{'id': folder_id}]})
        file.GetContentFile(output_path)
        print('Downloaded file to {}'.format(output_path))

    def get_file_id_in_folder(self, folder_id, title):
        """
        Get the ID of a file in a specific folder in Google Drive.
        """
        query = "'{}' in parents and trashed=false".format(folder_id)
        file_list = self.drive.ListFile({'q': query}).GetList()
        for file in file_list:
            if file['title'] == title:
                return file['id']
        return None

    def get_file_title_in_folder(self, folder_id, file_id):
        """
        Get the title of a file in a specific folder in Google Drive.
        """
        query = "'{}' in parents and trashed=false".format(folder_id)
        file_list = self.drive.ListFile({'q': query}).GetList()
        for file in file_list:
            if file['id'] == file_id:
                return file['title']
        return None

    def delete_file_in_folder(self, folder_id, file_id):
        """
        Delete a file from a specific folder in Google Drive.
        """
        file = self.drive.CreateFile({'id': file_id, 'parents': [{'id': folder_id}]})
        file.Trash()

    def update_file_in_folder(self, folder_id, file_id, new_title, new_content):
        """
        Update a file in a specific folder in Google Drive.
        """
        file = self.drive.CreateFile({'id': file_id, 'parents': [{'id': folder_id}]})
        file['title'] = new_title
        file.SetContentString(new_content)
        file.Upload()

    def get_folder_id(self, title):
        """
        Get the ID of a folder in Google Drive.
        """
        for file in self.file_list:
            if file['title'] == title and file['mimeType'] == 'application/vnd.google-apps.folder':
                return file['id']
        return None

    def get_folder_title(self, folder_id):
        """
        Get the title of a folder in Google Drive.
        """
        for file in self.file_list:
            if file['id'] == folder_id and file['mimeType'] == 'application/vnd.google-apps.folder':
                return file['title']
        return None

    def share_file(self, file_id, email, role='reader'):
        """
        Share a file in Google Drive.
        """
        file = self.drive.CreateFile({'id': file_id})
        permission = {
            'type': 'user',
            'role': role,
            'value': email
        }
        file.InsertPermission(permission)

    def remove_file_permission(self, file_id, email):
        """
        Remove file permission in Google Drive.
        """
        file = self.drive.CreateFile({'id': file_id})
        permissions = file.GetPermissions()
        for permission in permissions:
            if permission['type'] == 'user' and permission['value'] == email:
                file.DeletePermission(permission['id'])
    def main(self):
        path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'DOCUMENTS')
        print(self.get_folder_by_file(file_title='file-sample_100kB.doc'))


if __name__ == '__main__':
    google_drive_manager = GoogleDriveManager()
    google_drive_manager.main()
