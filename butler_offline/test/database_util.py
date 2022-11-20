
def untaint_database(database):
    database.einzelbuchungen.tainted = 0
    database.dauerauftraege.tainted = 0
    database.gemeinsamebuchungen.tainted = 0
    database.depotauszuege.tainted = 0
    database.depotwerte.tainted = 0
    database.sparkontos.tainted = 0
    database.order.tainted = 0
    database.orderdauerauftrag.tainted = 0
    database.sparbuchungen.tainted = 0