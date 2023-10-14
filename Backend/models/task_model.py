from Backend.models.connection_pool import MySQLPool

class TaskModel:
    def __init__(self):        
        self.mysql_pool = MySQLPool()


    def get_evaluate(self):
        rv = self.mysql_pool.execute('SELECT * from evaluate')
        data = []
        content = {}
        for result in rv:
            content = {'id': result[0], 'value': result[1], 'fecha': result[2], 'hora': result[3]}
            data.append(content)
            content = {}
        return data

    def get_evaluate_month(self, selectedMonth):
        params = {'selectedMonth' : selectedMonth}      
        rv = self.mysql_pool.execute("SELECT * FROM evaluate WHERE DATE_FORMAT(fecha, '%Y-%m') = %(selectedMonth)s", params)
        data = []
        content = {}
        for result in rv:
            content = {'id': result[0], 'value': result[1], 'fecha': result[2], 'hora': result[3]}
            data.append(content)
            content = {}
        return data

################### Actividad ################################
    # Funcion para obtener una actividad por su ID
    def get_actividad(self, id_act):    
        params = {'id_act' : id_act}      
        rv = self.mysql_pool.execute("SELECT * from actividad where id_act=%(id_act)s", params)                
        data = []
        content = {}
        for result in rv:
            content = {'id_act': result[0], 'nombre': result[1], 'descripcion': result[2], 'fecha': result[3], 'hora_inicio': result[4], 'hora_fin': result[5], 'estado': result[6], 'enlace_reu': result[7]}
            data.append(content)
            content = {}
        return data

    # Funcion para obtener todas las actividades
    def get_actividads(self):
        rv = self.mysql_pool.execute("SELECT * from actividad")  
        data = []
        content = {}
        for result in rv:
            content = {'id_act': result[0], 'nombre': result[1], 'descripcion': result[2], 'fecha': result[3], 'hora_inicio': result[4], 'hora_fin': result[5], 'estado': result[6], 'enlace_reu': result[7]}
            data.append(content)
            content = {}
        return data

    # Funcion para agregar una actividad
    def add_actividad(self, nombre, descripcion, fecha, hora_inicio, hora_fin, estado, enlace_reu):
        params = {
            'nombre' : nombre,
            'descripcion' : descripcion,
            'fecha' : fecha,
            'hora_inicio' : hora_inicio,
            'hora_fin' : hora_fin,
            'estado' : estado,
            'enlace_reu' : enlace_reu
        }  
        query = """insert into actividad (nombre, descripcion, fecha, hora_inicio, hora_fin, estado, enlace_reu)
            values (%(nombre)s, %(descripcion)s, %(fecha)s, %(hora_inicio)s, %(hora_fin)s, %(estado)s, %(enlace_reu)s)"""    
        cursor = self.mysql_pool.execute(query, params, commit=True)   

        data = {'id_act': cursor.lastrowid, 'nombre': nombre, 'descripcion': descripcion, 'fecha': fecha, 'hora_inicio': hora_inicio, 'hora_fin': hora_fin, 'estado': estado, 'enlace_reu': enlace_reu}
        return data

    # Funcion para eliminar una actividad
    def delete_actividad(self, id_act):
        params = {'id_act' : id_act}      
        query = """delete from actividad where id_act = %(id_act)s"""    
        self.mysql_pool.execute(query, params, commit=True)   

        data = {'result': 1}
        return data


################### Administrador ################################

    # Funcion para obtener un administrador por su ID
    def get_administrador(self, id_adm):
        params = {'id_adm' : id_adm}      
        rv = self.mysql_pool.execute("SELECT * from administrador where id_adm=%(id_adm)s", params)                
        data = []
        content = {}
        for result in rv:
            content = {'id_adm': result[0], 'rol': result[1]}
            data.append(content)
            content = {}
        return data
    
    # Funcion para obtener todos los administradores
    def get_administradors(self):
        rv = self.mysql_pool.execute("SELECT * from administrador")  
        data = []
        content = {}
        for result in rv:
            content = {'id_adm': result[0], 'rol': result[1]}
            data.append(content)
            content = {}
        return data
    
    # Funcion para agregar un administrador
    def add_administrador(self, rol):
        params = {
            'rol' : rol
        }  
        query = """insert into administrador (rol)
            values (%(rol)s)"""    
        cursor = self.mysql_pool.execute(query, params, commit=True)   

        data = {'id_adm': cursor.lastrowid, 'rol': rol}
        return data
    
    # Funcion para eliminar un administrador
    def delete_administrador(self, id_adm):
        params = {'id_adm' : id_adm}      
        query = """delete from administrador where id_adm = %(id_adm)s"""    
        self.mysql_pool.execute(query, params, commit=True)   

        data = {'result': 1}
        return data


if __name__ == "__main__":    
    tm = TaskModel()     

    #print(tm.create_actividad('prueba 10', 'desde python'))