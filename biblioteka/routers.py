class MasterSlaveRouter:
    def db_for_read(self, model, **hints):
        return 'slave'

    def db_for_write(self, model, **hints):
        return 'default'

    def allow_relation(self, obj1, obj2, **hints):
        # Allow relations if both models are in the same database
        return obj1._state.db == obj2._state.db

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        # Ensure that all models are migrated to both databases
        return True
