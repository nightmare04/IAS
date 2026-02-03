
from data.models import *

db = SqliteDatabase('./data/database.db')

query = (OtkazAgregateBase
         .select()
         .join(AgregateBase)
         .join(PlaneSystemBase)
         .join(GroupBase)
         .where(GroupBase.name == 'ЭО и ЭА'))

print(query[0].plane)