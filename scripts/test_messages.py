import requests
import json
import time
from rich.console import Console
from rich.table import Table
import traceback

console = Console()

def load_contacts():
    """Carrega os contatos do arquivo JSON"""
    try:
        with open("../data/contacts.json", "r") as f:
            return json.load(f)
    except Exception as e:
        console.print(f"[red]Erro ao carregar contatos: {str(e)}")
        return None

def test_send_message(number: str, name: str):
    """Testa o envio de mensagem para um contato"""
    url = "http://localhost:8000/tool/send_message"
    message = f"Olá {name}, esta é uma mensagem de teste automatizado! Hora: {time.strftime('%H:%M:%S')}"
    
    try:
        # Remove o + do número se existir
        formatted_number = number.replace("+", "")
        
        payload = {
            "number": formatted_number,
            "message": message
        }
        
        console.print(f"\n[yellow]Enviando mensagem para {name}[/yellow]")
        console.print(f"[cyan]URL: {url}[/cyan]")
        console.print(f"[cyan]Payload: {json.dumps(payload, indent=2)}[/cyan]")
        
        response = requests.post(url, json=payload, timeout=10)
        
        console.print(f"[cyan]Status Code: {response.status_code}[/cyan]")
        console.print(f"[cyan]Response Headers: {dict(response.headers)}[/cyan]")
        console.print(f"[cyan]Response Body: {response.text}[/cyan]")
        
        if response.status_code == 200:
            result = response.json()
            console.print(f"[green]✓ Mensagem enviada com sucesso![/green]")
            return True, result.get("id", "N/A")
        else:
            error_msg = f"Status code: {response.status_code} - {response.text}"
            console.print(f"[red]❌ Erro ao enviar mensagem: {error_msg}[/red]")
            return False, error_msg
            
    except Exception as e:
        console.print(f"[red]❌ Erro detalhado: {str(e)}[/red]")
        console.print(f"[red]Traceback: {traceback.format_exc()}[/red]")
        return False, str(e)

def check_waha_status():
    """Verifica se o WAHA está conectado"""
    try:
        # Verifica o status do servidor
        console.print("[yellow]Verificando status do servidor WAHA...[/yellow]")
        response = requests.get("http://localhost:3000/api/server/status")
        console.print(f"[cyan]Server Status Response: {response.text}[/cyan]")
        
        # Verifica as sessões
        console.print("[yellow]Verificando sessões do WAHA...[/yellow]")
        sessions = requests.get("http://localhost:3000/api/sessions?all=true")
        sessions_data = sessions.json()
        console.print(f"[cyan]Sessions Response: {json.dumps(sessions_data, indent=2)}[/cyan]")
        
        # Procura a sessão default
        default_session = next((s for s in sessions_data if s.get("name") == "default"), None)
        
        if not default_session:
            console.print("[red]❌ Sessão 'default' não encontrada[/red]")
            return False
            
        status = default_session.get("status", "UNKNOWN")
        console.print(f"[yellow]Status da sessão default: {status}[/yellow]")
        
        # Considera WORKING como um estado válido também
        if status in ["CONNECTED", "WORKING"]:
            console.print("[green]✓ WAHA está operacional![/green]")
            return True
            
        console.print(f"[red]❌ WAHA não está pronto. Status atual: {status}[/red]")
        console.print("[yellow]Por favor, verifique http://localhost:3000[/yellow]")
        return False
        
    except Exception as e:
        console.print(f"[red]❌ Erro ao verificar status do WAHA: {str(e)}[/red]")
        console.print(f"[red]Detalhes do erro: {traceback.format_exc()}[/red]")
        return False

def main():
    console.print("\n[yellow]🚀 Iniciando testes de envio de mensagens...[/yellow]\n")

    # Verifica se a API está online
    try:
        requests.get("http://localhost:8000/docs")
    except:
        console.print("[red]❌ API não está respondendo. Verifique se o servidor está rodando.[/red]")
        return

    # Verifica status do WAHA
    if not check_waha_status():
        return

    # Carrega os contatos
    contacts = load_contacts()
    if not contacts:
        return

    # Cria tabela de resultados
    table = Table(title="Resultados dos Testes")
    table.add_column("Nome", style="cyan")
    table.add_column("Número", style="magenta")
    table.add_column("Status", style="green")
    table.add_column("Message ID", style="yellow")

    # Testa cada contato
    for name, number in contacts.items():
        console.print(f"[cyan]Testando envio para {name} ({number})...[/cyan]")
        success, result = test_send_message(number, name)
        
        status = "✅ Enviado" if success else "❌ Falhou"
        status_style = "green" if success else "red"
        
        table.add_row(
            name,
            number,
            f"[{status_style}]{status}[/{status_style}]",
            str(result)
        )
        
        # Aguarda um pouco entre os envios
        time.sleep(2)

    console.print("\n")
    console.print(table)
    console.print("\n[green]✨ Testes concluídos![/green]")

if __name__ == "__main__":
    main() 