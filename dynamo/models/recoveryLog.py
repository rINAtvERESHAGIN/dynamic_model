from django.db import models


class RecoveryLog(models.Model):
    # 1) Сохраняем record_uuid записи которую хотят восстановить ( что воостановил )
    restored_object = models.UUIDField()
# 2) С какого instance пришел запрос ( кто попросил )
    instance = models.CharField(max_length=100)
# 3) instance token
    token = models.UUIDField()
# 4) Когда пришел запрос на восстановление ( когда попросил )
    request_time = models.DateTimeField()
# 5) Когда отправляется собранный объект ( когда отправил )
    response_time = models.DateTimeField()
# 6) Когда пришел ответ о восстановление ( время восстановления )
    success = models.DateTimeField()

