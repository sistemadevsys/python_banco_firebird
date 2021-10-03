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

    cursor_banka.execute("""SELECT ID, FORNECEDOR_ID, CODIGO_BARRAS, NOME, PRECO FROM PRODUTO""")
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

    for id_ref, id_for, c_barras, nome_b, preco in t_banka:
        rf = int(id_ref)
        cd = str(c_barras)
        nom = str(nome_b)
        vl = float(preco)
        prod = [(rf, cd, nom, vl, 0.0, vl),]
        # Incluir ALIQUOTA = T01, ALTERAR = Sim, COMISSAO=Sim, ALIQUOTA_ICM=T00, UNITARIO=UN, CFOP=5405
        # OCTS=500, STATUS=1, COD_AGREGADO=Não, SERVICOS=Não, ALTERADO=Sim, OR_CST=0
        cursor_fire.executemany("insert into EST_PRODUTO (REFERENCIAL, CODIGO, NOME, PRECO_CUSTO, MARGEM, PRECO_VENDA) values (?, ?, ?, ?, ?, ?)", prod)
        con_fire.commit()

    con_banka.close()
    con_fire.close()

except ValueError:
    print('Error database')
else:
    con_banka.close()
    con_fire.close()
