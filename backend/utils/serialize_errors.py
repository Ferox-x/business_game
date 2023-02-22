class ErrorsSerializer:
    """Класс обработчик ошибок."""

    def get_list_of_validates_errors(self):
        """Метод формирует список ошибок из словаря."""
        errors = []
        for key, value in self.errors.items():
            errors.append(f'{key}: {" ".join(value)}')
        return {"errors": errors}
