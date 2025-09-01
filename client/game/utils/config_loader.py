"""
Carregador de configurações - lê e analisa arquivos de configuração
"""
import yaml
import json
from typing import Dict, Any

class ConfigLoader:
    """
    Utilitário para carregar configurações de arquivos YAML e JSON
    """
    
    @staticmethod
    def load_yaml(file_path: str) -> Dict[str, Any]:
        """
        Carrega configurações de um arquivo YAML
        file_path: Caminho para o arquivo YAML
        Retorna um dicionário com as configurações
        """
        try:
            with open(file_path, 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"Erro ao carregar arquivo YAML {file_path}: {e}")
            return {}
            
    @staticmethod
    def load_json(file_path: str) -> Dict[str, Any]:
        """
        Carrega configurações de um arquivo JSON
        file_path: Caminho para o arquivo JSON
        Retorna um dicionário com as configurações
        """
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except Exception as e:
            print(f"Erro ao carregar arquivo JSON {file_path}: {e}")
            return {}
            
    @staticmethod
    def save_yaml(file_path: str, data: Dict[str, Any]) -> bool:
        """
        Salva dados em um arquivo YAML
        file_path: Caminho para o arquivo YAML
        data: Dicionário com dados a serem salvos
        Retorna True se bem-sucedido, False caso contrário
        """
        try:
            with open(file_path, 'w') as file:
                yaml.dump(data, file, default_flow_style=False)
            return True
        except Exception as e:
            print(f"Erro ao salvar arquivo YAML {file_path}: {e}")
            return False
            
    @staticmethod
    def save_json(file_path: str, data: Dict[str, Any]) -> bool:
        """
        Salva dados em um arquivo JSON
        file_path: Caminho para o arquivo JSON
        data: Dicionário com dados a serem salvos
        Retorna True se bem-sucedido, False caso contrário
        """
        try:
            with open(file_path, 'w') as file:
                json.dump(data, file, indent=4)
            return True
        except Exception as e:
            print(f"Erro ao salvar arquivo JSON {file_path}: {e}")
            return False