import firebirdsql
from decouple import config


try:
    # devsys
    con_fire = firebirdsql.connect(
        host=config("host_d"),
        database=config("database_d"),
        port=config("port_d"),
        user=config("user_d"),
        password=config("password_d"),
        charset=config("charset_d")
    )
    print("Database devsys Firebird connection made!")
    cursor_fire = con_fire.cursor()

    # ARRUMAR PRIMEIRO IBEXPERT ESTOQUE ATUAL E REFERENCIAL DAS DUAS ENTRADA JA FEITAS

    cursor_fire.execute("""
                        SELECT REFERENCIAL, CODIGO FROM EST_PRODUTO
                        """)

    t_produto = cursor_fire.fetchall()

    # SELECT REFERENCIAL, REF_PRODUTO, REF_EMPRESA, ESTOQUE_ATUAL, ESTOQUE_ENTRADA,
    #                     ESTOQUE_SAIDA, CODIGO, STATUS FROM EST_ESTOQUE
    i = 3
    for ref, codigo in t_produto:
        est_e = [(i, ref, 1, codigo, 1),]
        cursor_fire.executemany("""insert into EST_ESTOQUE (REFERENCIAL, REF_PRODUTO,
                                    REF_EMPRESA, CODIGO, STATUS)
                                    values (?, ?, ?, ?, ?)""", est_e)
        con_fire.commit()
        i += 1

    con_fire.close()

except ValueError:
    print('Error database')
else:
    con_fire.close()
