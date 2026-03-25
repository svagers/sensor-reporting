import json
import os
from abc import ABC, abstractmethod
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class BaseImportCommand(BaseCommand, ABC):
    
    def error(self, message: str) -> None:
        self.stdout.write(self.style.ERROR(message))
    
    def warn(self, message: str) -> None:
        self.stdout.write(self.style.WARNING(message))
    
    def info(self, message: str) -> None:
        self.stdout.write(self.style.SUCCESS(message))
    
    @abstractmethod
    def get_json_file_name(self) -> str:
        pass
    
    @abstractmethod
    def import_data(self, raw_data: dict) -> None:
        pass
    
    def load_json_file(self) -> dict:
        json_path = os.path.join(settings.BASE_DIR, 'data', self.get_json_file_name())
        
        if not os.path.exists(json_path):
            raise CommandError(f'File not found: {json_path}')
        
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def handle(self, *args, **options):
        raw_data = self.load_json_file()
        self.import_data(raw_data)
