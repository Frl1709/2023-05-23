from database.DB_connect import DBConnect
from model.player import Player


class DAO:

   @staticmethod
   def getYears():
      conn = DBConnect.get_connection()
      result = []
      cursor = conn.cursor(dictionary=True)
      query = """select distinct(`year`) as anno
                from salaries s """

      cursor.execute(query,)
      for row in cursor:
         result.append(row['anno'])

      cursor.close()
      conn.close()
      return result

   @staticmethod
   def getNodes(anno, salario):
     conn = DBConnect.get_connection()
     result = []
     cursor = conn.cursor(dictionary=True)
     query = """select p.playerID, nameFirst, nameLast, ID, year, teamCode, teamID, SUM(s.salary)  as salary
                from people p , salaries s 
                where p.playerID = s.playerID and s.`year` = %s 
                group by p.playerID
                having salary > %s"""

     cursor.execute(query, (anno, salario,))
     for row in cursor:
         result.append(Player(**row))

     cursor.close()
     conn.close()
     return result

   @staticmethod
   def getEdge(anno, salario, idMap):
       conn = DBConnect.get_connection()
       result = []
       cursor = conn.cursor(dictionary=True)
       query = """select distinct(t1.p1), t2.p2
                from (select p.playerID as p1, a.teamID as tm1, SUM(s.salary)  as salary
                        from people p , salaries s, appearances a 
                        where p.playerID = s.playerID and p.playerID = a.playerID and s.`year` = %s and s.`year` = a.`year`
                        group by p.playerID, a.teamID
                        having salary > %s) t1,
                       (select p.playerID as p2, a.teamID as tm2, SUM(s.salary)  as salary
                            from people p , salaries s, appearances a 
                            where p.playerID = s.playerID and p.playerID = a.playerID and s.`year` = %s and s.`year` = a.`year`
                            group by p.playerID, a.teamID
                            having salary > %s) t2
                where p1 < p2 and tm1 = tm2 """

       cursor.execute(query, (anno, salario, anno, salario,))
       for row in cursor:
           result.append((idMap[row['p1']],
                          idMap[row['p2']]))

       cursor.close()
       conn.close()
       return result

   @staticmethod
   def getPlayerTeamsInYear(anno, playerID):
       conn = DBConnect.get_connection()
       result = []
       cursor = conn.cursor(dictionary=True)
       query = """select a.playerID, a.teamID 
                    from appearances a
                    where `year` = %s and playerID = %s """

       cursor.execute(query, (anno, playerID, ))
       for row in cursor:
           result.append(row['teamID'])

       cursor.close()
       conn.close()
       return result

