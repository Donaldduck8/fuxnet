import os
import ctypes
import shutil
import subprocess

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def create_self_signed_cert(domain_name, cert_dir):
    if isinstance(domain_name, list) and not isinstance(domain_name, str):
        domain_name_string = ", ".join(['"' + name + '"' for name in domain_name])
    else:
        domain_name_string = '"' + domain_name + '"'


    command = rf"""
    $cert = New-SelfSignedCertificate -DnsName {domain_name_string} -CertStoreLocation "cert:\LocalMachine\My" -NotAfter (Get-Date).AddYears(100)
    $pwd = ConvertTo-SecureString -String "a" -Force -AsPlainText
    Export-PfxCertificate -cert "cert:\LocalMachine\My\$($cert.Thumbprint)" -FilePath "{cert_dir}\cert.pfx" -Password $pwd
    Export-Certificate -Cert "cert:\LocalMachine\My\$($cert.Thumbprint)" -FilePath "{cert_dir}\cert.cer" -Type CERT
    """

    print(command)

    subprocess.run(["powershell", "-Command", command], check=True)


def convert_der_to_pem_and_extract_private_key(cert_dir):
    # Convert DER (.cer) to PEM
    subprocess.run(["openssl", "x509", "-inform", "der", "-in", rf"{cert_dir}\cert.cer", "-out", rf"{cert_dir}\cert.pem"], check=True)
    
    # Extract private key from .pfx and convert to PEM
    subprocess.run(["openssl", "pkcs12", "-in", rf"{cert_dir}\cert.pfx", "-out", rf"{cert_dir}\cert_key.pem", "-nodes", "-password", "pass:a"], check=True)


def import_der_to_trusted_root(cert_dir):
    cert_p = os.path.join(cert_dir, "cert.pem")

    # PowerShell command to add the certificate to the trusted root
    powershell_command = f"""
    $certPath = '{cert_p}'
    $cert = New-Object System.Security.Cryptography.X509Certificates.X509Certificate2($certPath)
    $store = New-Object System.Security.Cryptography.X509Certificates.X509Store('Root', 'LocalMachine')
    $store.Open([System.Security.Cryptography.X509Certificates.OpenFlags]::ReadWrite)
    $store.Add($cert)
    $store.Close()
    """

    # Execute the PowerShell command
    subprocess.run(["powershell", "-Command", powershell_command], check=True)


def main():
    if not is_admin():
        print("Run this script as administrator!")
        return
    
    openssl_p = shutil.which("openssl")

    if openssl_p == None:
        print("Install openssl!")
        return

    certs_folder = os.path.expandvars(r"%USERPROFILE%\Desktop\certs")
    os.makedirs(certs_folder, exist_ok=True)

    while True:
        domain_name = input("Enter the domain you want to impersonate ('exit' to quit): ")

        if domain_name == "exit":
            return

        domain_folder = os.path.join(certs_folder, domain_name)

        if os.path.exists(domain_folder):
            print(f"Certificates have already been generated for {domain_name}!")
            continue

        os.makedirs(domain_folder, exist_ok=True)

        create_self_signed_cert([domain_name], domain_folder)
        convert_der_to_pem_and_extract_private_key(domain_folder)
        import_der_to_trusted_root(domain_folder)

        print(f"Success! Certificates have been written to {domain_folder}")
        print()
    

if __name__ == "__main__":
    main()