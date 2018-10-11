from django.core.files.storage import FileSystemStorage



class OverwriteStorage(FileSystemStorage):
    def get_available_name(self, name):
        # This make the file being saved overwrite, rather than rename.
        self.delete(name)
        
        return name


