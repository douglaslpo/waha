import requests
import time
import sys
import os
from rich.console import Console
from rich.panel import Panel
from rich.progress import Progress
from qrcode import QRCode
import json

console = Console()

def check_waha_service():
    """Verifica se o serviço WAHA está rodando"""
    try:
        response = requests.get("http://localhost:3000/api/health")
        return response.status_code == 200
    except:
        return False

def get_qr_code():
    """Obtém o QR code para autenticação"""
    try:
        response = requests.get("http://localhost:3000/api/screenshot")
        if response.status_code == 200:
            return response.json().get("qrcode")
    except:
        return None

def display_qr_code(qr_data):
    """Exibe o QR code no terminal"""
    qr = QRCode()
    qr.add_data(qr_data)
    qr.make()
    qr.print_ascii()

def check_connection_status():
    """Verifica o status da conexão"""
    try:
        response = requests.get("http://localhost:3000/api/status")
        return response.json().get("status") == "CONNECTED"
    except:
        return False

def main():
    console.print(Panel.fit("🚀 Configurando WAHA", title="Setup"))

    # Verifica se o serviço está rodando
    with Progress() as progress:
        task = progress.add_task("Verificando serviço WAHA...", total=100)
        
        while not progress.finished:
            if check_waha_service():
                progress.update(task, completed=100)
                break
            progress.update(task, advance=10)
            time.sleep(1)

    if not check_waha_service():
        console.print("❌ Serviço WAHA não está rodando. Execute docker-compose up primeiro.", style="red")
        sys.exit(1)

    console.print("✅ Serviço WAHA está rodando", style="green")

    # Verifica se já está conectado
    if check_connection_status():
        console.print("✅ WAHA já está autenticado e conectado!", style="green")
        return

    # Aguarda e exibe QR Code
    console.print("\n📱 Aguardando QR Code...", style="yellow")
    
    with Progress() as progress:
        task = progress.add_task("Aguardando autenticação...", total=None)
        
        while not check_connection_status():
            qr_data = get_qr_code()
            if qr_data:
                console.clear()
                console.print("🔍 Escaneie o QR Code abaixo com seu WhatsApp:", style="yellow")
                display_qr_code(qr_data)
            time.sleep(2)
            progress.update(task, advance=1)

    console.print("\n✅ WAHA autenticado com sucesso!", style="green")

    # Salva informações da sessão
    session_info = {
        "setup_date": time.strftime("%Y-%m-%d %H:%M:%S"),
        "status": "configured"
    }
    
    os.makedirs("data", exist_ok=True)
    with open("data/waha_session.json", "w") as f:
        json.dump(session_info, f, indent=2)

    console.print("\n📝 Informações da sessão salvas", style="green")
    console.print("\n🎉 Configuração concluída! O WAHA está pronto para uso.", style="green")

if __name__ == "__main__":
    main() 