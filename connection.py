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


    def update_project(self, properties : dict):
        with self.driver.session() as session:
            session.write_transaction(self._update_project, properties)

    @staticmethod
    def _update_project(tx, p: dict):
        print(p.get("name"), p.get("new_name"), p.get("new_subject"))
        query = (
           '''MATCH (p: Project {name: $name})
           SET p.name= $new_name
           SET p.subject = $new_subject
           RETURN p'''
        )
        tx.run(query, name=p.get("name"), new_name = p.get("new_name"), new_subject=p.get("new_subject"))


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
            "MATCH (e:Student { firstname: $student_name, lastname: $student_surname }) "
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
        print(name[0], name[1])
        query = (
            """MATCH (s:Student {firstname: $name, lastname: $lastname})
            MATCH (p:Project)
            WHERE (s)-[:IS_MAKING]->(p)
            RETURN properties(p) as prop"""
        )
        result = tx.run(query, name = name[0], lastname = name[1])
        return [row["prop"] for row in result]

    def delete_student(self, name):
        with self.driver.session() as session:
            return session.read_transaction(self._delete_student, name)
    
    @staticmethod
    def _delete_student(tx, name):
        query = (
            """MATCH (e:Student {firstname: $name}) 
            DETACH DELETE e"""
        )
        result = tx.run(query, name = name)
        return [row["prop"] for row in result]

    def delete_project(self, name):
        with self.driver.session() as session:
            return session.write_transaction(self._delete_project, name)
    
    @staticmethod
    def _delete_project(tx, name):
        print(name)
        query = (
            """MATCH (e:Project {name: $name}) 
            DETACH DELETE e
            RETURN e"""
        )
        result = tx.run(query, name = name)

    def delete_student_from_project(self, name, project_name):
        with self.driver.session() as session:
            return session.write_transaction(self._delete_student_from_project, name, project_name)
    
    @staticmethod
    def _delete_student_from_project(tx, name, project_name):
        print(name, project_name)
        query = (
            """OPTIONAL MATCH (s:Student {firstname:$name, lastname: $lastname})-[w:IS_MAKING]->(p:Project {name:$project_name}) 
                DETACH DELETE w"""
        )
        result = tx.run(query, name = name[0], lastname = name[1], project_name = project_name)
