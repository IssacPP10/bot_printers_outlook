import win32com.client

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

print("Cuentas detectadas por Outlook:")
for i, folder in enumerate(outlook.Folders):
    print(f"{i+1}. {folder.Name}")
