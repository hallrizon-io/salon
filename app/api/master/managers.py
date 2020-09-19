from django.db import transaction
from api.master.serializers.create_master import CreateMasterSerializer


class MasterViewManager:
    def __init__(self, request):
        self.data = request.data
        self.context = {'new_company': self.data.get('new_company', '')}
        if 'enter_code' in self.data.get('company'):
            self.context['enter_code'] = self.data.get('company').get('enter_code')

    def processing(self):
        master_serializer = CreateMasterSerializer(data=self.data, context=self.context)
        master_serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            master = master_serializer.save()

        return master
