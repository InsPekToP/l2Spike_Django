# class TestDBRouter:
#     def db_for_write(self, model, **hints):
#         if model._meta.app_label == 'users' and model.__name__ == 'Accounts':
#             return 'test'
#         return None

#     def db_for_read(self, model, **hints):
#         if model._meta.app_label == 'users' and model.__name__ == 'Accounts':
#             return 'test'
#         return None


# L2spike_Django_180502/db_routers.py

class TestDBRouter:
    """
    Роутер для управления направлением запросов к модели Accounts в test базу данных.
    """

    def db_for_read(self, model, **hints):
        if model._meta.app_label == 'users':
            return 'test'
        return None

    def db_for_write(self, model, **hints):
        if model._meta.app_label == 'users':
            return 'test'
        return None

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label == 'users' or obj2._meta.app_label == 'users':
            return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # models from 'users' app НЕ МИГРИРУЕМ никуда
        if app_label == 'users':
            return False
        return db == 'default'
