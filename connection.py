from neo4j import GraphDatabase

uri = "neo4j+s://aa4a42da.databases.neo4j.io"
user = "neo4j"
password = "5rfEbDtofGxvMqb9qcps5MondX8LnssabMA6EG3vLnI"

class Connection:
    def __init__(self, uri=uri, user=user, password=password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()
    
    def __del__(self):
        self.driver.close()

    def add_project(self, properties : dict):
        with self.driver.session() as session:
            session.write_transaction(self._add_project, properties)

    @staticmethod
    def _add_project(tx, p: dict):
        print("dodany projekt", p.get("name"))
        query = (
            "CREATE (n:Project { "
            "name:$name, "
            "subject:$subject "
            "})"
        )
        tx.run(query, name=p.get("name"), 
                      subject=p.get("subject"))

    def list_all(self):
        with self.driver.session() as session:
            return session.read_transaction(self._return_all_projects)
    
    @staticmethod
    def _return_all_projects(tx):
        query = (
            "MATCH (e:Project) "
            "RETURN properties(e) AS prop "
            "ORDER BY e.name, e.subject"
        )
        result = tx.run(query)
        return [row["prop"] for row in result]


    def list_students(self, name):
        with self.driver.session() as session:
            return session.read_transaction(self._return_students, name)
    
    @staticmethod
    def _return_students(tx, name):
        print("name", name)
        query = (
            "MATCH (s:Student)-[:IS_MAKING *1..1]->(e: Project { name: $name}) RETURN properties(s) as prop"
        )
        result = tx.run(query, name = name)
        return [row["prop"] for row in result]


    def list_all_students(self):
        with self.driver.session() as session:
            return session.read_transaction(self._return_all_students)
    
    @staticmethod
    def _return_all_students(tx):
        query = (
            "MATCH (s:Student) RETURN properties(s) as prop"
        )
        result = tx.run(query)
        return [row["prop"] for row in result]


    def add_relation(self, proj_name, student_name, student_surname):
        with self.driver.session() as session:
            session.write_transaction(self._create_relation, proj_name, student_name, student_surname)

    @staticmethod
    def _create_relation(tx, proj_name, student_name, student_surname):
        print("create relation", proj_name, student_name)
        query = (
            "MATCH (b:Project { name: $proj_name }) "
            "MATCH (e:Student { firstname: $student_name }) "
            "CREATE (e)-[:IS_MAKING]->(b) "
        )
        tx.run(query, proj_name=proj_name, student_name=student_name, student_surname = student_surname)


    def add_student(self, properties : dict):
        with self.driver.session() as session:
            session.write_transaction(self._add_student, properties)

    @staticmethod
    def _add_student(tx, p: dict):
        query = (
            "CREATE (n:Student { "
            "firstname:$first, "
            "lastname:$lastname, "
            "department:$department "
            "})"
        )
        tx.run(query, first=p.get("first"), 
                      lastname=p.get("last"), 
                      department = p.get("department"))


    def list_projects(self, name):
        with self.driver.session() as session:
            return session.read_transaction(self._list_projects, name)
    
    @staticmethod
    def _list_projects(tx, name):
        query = (
            """MATCH (s:Student {firstname: $name})
            MATCH (p:Project)
            WHERE (s)-[:IS_MAKING]->(p)
            RETURN properties(p) as prop"""
        )
        result = tx.run(query, name = name)
        return [row["prop"] for row in result]