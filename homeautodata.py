""" 
Created By: Themba Pakula
Description: This module is used to manage connetion to the database\s for data for read and manupulation
"""


import psycopg2 as psycopg2
import bdsconfig

##postgresql connection string

con_postgresql = psycopg2.connect(user= bdsconfig.DB_USER, password= bdsconfig.DB_PASS, host= bdsconfig.DB_HOST, port= bdsconfig.DB_PORT,
                                  database= bdsconfig.DB_DATABASE)


## postgresql Database fuctions and SP's
# Get User Level
def pgsql_get_scalar(schema, fn_name, paramenters):
    value = 0
    fn_parameters = ''
    Sp_QueryStr = ''
    Fn_Values=[]
    ##Get Parameters

    try:
        for par in paramenters:
            if fn_parameters == '':
                fn_parameters = fn_parameters + par + ":= %s"
                Fn_Values.append(paramenters[par])
            else:
                fn_parameters = fn_parameters + ',' + par + ":= %s"
                Fn_Values.append(paramenters[par])

        Sp_QueryStr = 'SELECT {schema}.{function} ({params})'.format(schema='"' + schema + '"', function=fn_name, params=fn_parameters)
        #print(Sp_QueryStr)

        ##Sql Call
        mycursor = con_postgresql.cursor()
        mycursor.execute(Sp_QueryStr,Fn_Values)
        user_record = mycursor.fetchone()
        mycursor.close()
        con_postgresql.commit()
        value = user_record
    except Exception as e:
        mycursor.close()
        con_postgresql.commit()
        print(e)
    return value[0]



#This is void SP, can be used for inserts and updates
def pgsql_call_SP(schema, sp_name, paramenters):
    fn_parameters = ''
    Sp_QueryStr = ''
    Fn_Values=[]
    ##Get Parameters
    try:
        for par in paramenters:
            if fn_parameters == '':
                fn_parameters = fn_parameters + par + ":=  %s"
                Fn_Values.append(paramenters[par])

            else:
                fn_parameters = fn_parameters + ',' + par['name'] + ":=  %s"
                Fn_Values.append(paramenters[par])

        Sp_QueryStr = 'call {schema}.{sp} ({params})'.format(schema='"' + schema + '"', sp=sp_name, params=fn_parameters)
        #print(Sp_QueryStr)
        ##Sql Call
        mycursor = con_postgresql.cursor()
        mycursor.execute(Sp_QueryStr,Fn_Values)
        mycursor.close()
        con_postgresql.commit()
    except Exception as e:
        mycursor.close()
        con_postgresql.commit()
        print(e)


# this table value function takes a schema name as string, function name as string and a dictinary list of parameter name and values [{name: name,value: value}]. returns Dataset
def pgsql_call_Tablefunction_P(schema, fn_name, paramenters):
    fn_parameters = ''
    DataSet = []
    fn_QueryStr = ''
    Fn_Values=[]
    ##Get Parameters
    try:
        for par in paramenters:
            if fn_parameters == '':
                fn_parameters = fn_parameters + par + ":=  %s"
                Fn_Values.append(paramenters[par])
            else:
                fn_parameters = fn_parameters + ',' + par + ":=  %s"
                Fn_Values.append(paramenters[par])

        fn_QueryStr = 'SELECT * FROM {schema}.{function} ({params})'.format(schema='"' + schema + '"', function=fn_name,
                                                                            params=fn_parameters)
        #print(fn_QueryStr)
        ##Sql Call
        mycursor = con_postgresql.cursor()
        mycursor.execute(fn_QueryStr,Fn_Values)
        DataSet = mycursor.fetchall()
        mycursor.close()
        con_postgresql.commit()
    except Exception as e:
        mycursor.close()
        con_postgresql.commit()
        print(e)
    return DataSet

# this table vale function takes a schema name as string and function name as string returns Dataset
def pgsql_call_Tablefunction(schema, fn_name):
    fn_QueryStr = ''
    DataSet = []
    ##Get Parameters

    fn_QueryStr = 'SELECT * FROM {schema}.{function}()'.format(schema='"' + schema + '"', function=fn_name)
    try:
        #print(fn_QueryStr)
        ##Sql Call
        mycursor = con_postgresql.cursor()
        mycursor.execute(fn_QueryStr)
        DataSet = mycursor.fetchall()
        mycursor.close()
        con_postgresql.commit()

    except Exception as e:
        mycursor.close()
        con_postgresql.commit()
        print(e)

    return DataSet



# this table vale function takes a schema name as string and function name as string returns Dataset
def pgsql_call_FromTable(schema, TableName):
    fn_QueryStr = ''
    DataSet = []
    ##Get Parameters

    fn_QueryStr = 'SELECT * FROM {schema}.{function}'.format(schema='' + schema + '', function=TableName)
    try:
        #print(fn_QueryStr)
        ##Sql Call
        mycursor = con_postgresql.cursor()
        mycursor.execute(fn_QueryStr)
        DataSet = mycursor.fetchall()
        mycursor.close()
        con_postgresql.commit()

    except Exception as e:
        mycursor.close()
        con_postgresql.commit()
        print(e)

    return DataSet