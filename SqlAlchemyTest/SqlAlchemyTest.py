#!/usr/bin/python
# -*- coding: utf-8 *-*
"""
Este codigo es para aprender a usar SqlAlchemy ORM
Es un codigo muy simple que lo unico que hace es crear un tabla, agregar
registros, listarlos de diferentes maneras y borrar
"""
__prj__ = 'sqlAlchemyTest'
__version__ = ''
__license__ = 'GNU General Public License v3'
__author__ = 'marcelo'
__email__ = 'marcelo.martinovic@gmail.com'
__url__ = ''
__date__ = '2012/05/21'

from sqlalchemy import *
from sqlalchemy.sql import select

# Esto crea la tabla
engine = create_engine('sqlite:///tutorial.db', echo=True)

metadata = MetaData()

# Esto define la tabla y sus campos
users_table = Table('users', metadata,
    Column('user_id', Integer, primary_key=True),
    Column('name', String(40)),
    Column('age', Integer),
    Column('password', String),
    )

# Esto ejecuta y crea la tabla
metadata.create_all(engine)

# conecta a la base de datos
conn = engine.connect()

# Metodo para insertar
# - Creo un objeto para insrtar en la tabla
ins = users_table.insert()
# - Asigno los valores al objeto
nuevo_usuario = ins.values(name='marcelo', age='42', password='secreta')
# - Ejecuta el insert, esto hace el commit
conn.execute(nuevo_usuario)
# - Otra forma mas simplificada de hacer el insert
usuario = users_table.insert().values(name='sebastian', age='4',
                                        password='secreta')
conn.execute(usuario)


# Hacer un select de la tabla
# - Esto crea un objeto de consulta de la tabla
qryObj = select([users_table])
# - Ejecuta la consulta y guarda el resultado en un objeto
resultado = conn.execute(qryObj)
# - Recorro el resultado
for row in resultado:
    (id, nombre, edad, clave) = row
    print id, nombre, edad, clave


# Traer columnas en particular
qryObj = select([users_table.c.name, users_table.c.age])
# - Ejecuta la consulta y guarda el resultado en un objeto
resultado = conn.execute(qryObj)
# - Recorro el resultado
for row in resultado:
    (nombre, edad) = row
    print nombre, edad

# Traer columnas en particular y recupera segun un valor
qryObj = select([users_table.c.name, users_table.c.age],
        users_table.c.age > 10)
# - Ejecuta la consulta y guarda el resultado en un objeto
resultado = conn.execute(qryObj)
# - Recorro el resultado
for row in resultado:
    (nombre, edad) = row
    print nombre, edad

# Borrado de datos
# - Primero se genera el objeto a ser borrado y luego se ejecuta el commit
objetoDelete = users_table.delete().where(users_table.c.age > 4)
resultado = conn.execute(objetoDelete)

# Traer columnas en particular y recupera segun un valor
qryObj = select([users_table])
# - Ejecuta la consulta y guarda el resultado en un objeto
resultado = conn.execute(qryObj)
# - Recorro el resultado
for row in resultado:
    print row
