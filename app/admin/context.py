from app.admin import admin
from app.models import GlobalSetting

@admin.app_context_processor
def inject_settings():
    return {
        'enableRegistration': GlobalSetting.get('enableRegistration')
    }