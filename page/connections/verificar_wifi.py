import subprocess
import platform

def get_wifi_network():
    try:
        if platform.system() == "Windows":
            # Comando para Windows
            result = subprocess.check_output("netsh wlan show interfaces", shell=True, encoding='latin1')
            for line in result.split('\n'):
                if "SSID" in line and "BSSID" not in line:
                    ssid = line.split(":")[1].strip()
                    break
            else:
                ssid = "No conectado a una red WiFi"
        elif platform.system() == "Linux":
            # Comando para Linux
            result = subprocess.check_output("iwgetid -r", shell=True, encoding='utf-8').strip()
            ssid = result if result else "No conectado a una red WiFi"
        else:
            ssid = "Sistema operativo no soportado"
    except Exception as e:
        ssid = f"Error al obtener SSID: {e}"

    return ssid

def get_network_ssid():
    return get_wifi_network()
