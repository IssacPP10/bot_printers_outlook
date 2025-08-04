import win32com.client
from config.config_outlook import OUTLOOK_ACCOUNT_NAME, TARGET_FOLDER_NAME

class OutlookClient:
    def __init__(self):
        self.outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        self.account = self._get_account_by_name(OUTLOOK_ACCOUNT_NAME)
        self.folder = self._get_target_folder(self.account, TARGET_FOLDER_NAME)

    def _get_account_by_name(self, name):
        for account in self.outlook.Folders:
            if account.Name == name:
                return account
        raise Exception(f"No se encontró la cuenta: {name}")

    def _get_target_folder(self, account, folder_name):
        try:
            return account.Folders[folder_name]
        except:
            raise Exception(f"No se encontró la carpeta '{folder_name}' en la cuenta '{account.Name}'")

    def get_emails(self):
        return self.folder.Items
