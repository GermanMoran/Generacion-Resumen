import psycopg2



class conectPostgres():
    
  def __init__(self):
    self.connected=0
    self.error=""
  
  def ConnectDatabase(self):
        try:
              self.connection=psycopg2.connect(host="localhost",
                                                        database="root",
                                                        user="root",
                                                        password="root")
              self.cursor = self.connection.cursor()
              self.connected=1
              return [True, self.cursor, self.connection]
        except:
               self.error="Error desconocido"
        
        return False
  

  def insetSummary(self, expediente, resumen, cursor, conection):
         insert_query = f"INSERT INTO Resumen (EXPEDIENTE, SUMMARY) VALUES ('{expediente}','{resumen}')"
         cursor.execute(insert_query)
         conection.commit()

         



'''        
expediente = "zzzzzzzzzaaaa"
resumen = "Cenicienta es una joven de bondad y dulzura que es maltratada por su madrastra y hermanastras. Su madrina, un hada, la ayuda a prepararse para el baile del rey donde el hijo del rey se enamora de ella. Cenicienta huye antes de la medianoche y deja caer una de sus zapatillas de cristal. El hijo del rey la busca y al encontrarla, se casan. Al final, Cenicienta y sus hermanastras se casan con grandes señores de la corte. La moraleja de la historia es que la bondad y la gentileza son más valiosas que la belleza."


coneccion, cursor, conection = conectPostgres().ConnectDatabase()
print("Estado de la conexion: ", coneccion)
nuevo_registro= conectPostgres().insetSummary(expediente, resumen, cursor, conection)

'''

