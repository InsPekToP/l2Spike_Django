class TestDBRouter:
    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'users' and model.__name__ == 'TestUser':
            return 'test'
        return None

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'users' and model.__name__ == 'TestUser':
            return 'test'
        return None
