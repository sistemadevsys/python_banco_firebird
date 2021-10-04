import firebirdsql
from decouple import config


try:
    # banka
    con_banka = firebirdsql.connect(
        host=config("host_b"),
        database=config("database_b"),
        port=config("port_b"),
        user=config("user_b"),
        password=config("password_b"),
        charset=config("charset_b")
    )
    print("Database banka Firebird connection made!")
    cursor_banka = con_banka.cursor()

    cursor_banka.execute("""SELECT ID, NOME, UF, IE FROM FORNECEDOR""")
    t_banka = cursor_banka.fetchall()

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

    t_devsys = cursor_fire.fetchall()

    for id_ref, nome_b, uf, ie in t_banka:
        
        forn = [(id_ref, nome_b, nome_b, uf, ie),]

        cursor_fire.executemany("""insert into EST_FORNECEDOR (REFERENCIAL, NOME, RAZAO_SOCIAL, ESTADO, IE)
                                    values (?, ?, ?, ?, ?)""", forn)
        con_fire.commit()

    con_banka.close()
    con_fire.close()

except ValueError:
    print('Error database')
else:
    con_banka.close()
    con_fire.close()
