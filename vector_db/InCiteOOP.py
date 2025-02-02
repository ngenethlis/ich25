import os
import json
from datetime import date
import intersystems_iris.dbapi._DBAPI as dbapi
import getpass
from dotenv import load_dotenv

from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.embeddings import OpenAIEmbeddings


class InCiteIRISDatabase:
    def __init__(self, config=None):
        # Use the provided config or the default configuration.
        if config is None:
            config = {
                "hostname": "localhost",
                "port": 1972,
                "namespace": "USER",
                "username": "demo",
                "password": "demo",
            }
        self.config = config

        # Connect to IRIS and get a cursor.
        self.conn = dbapi.connect(**config)
        self.cursor = self.conn.cursor()

        # Define table names.
        self.articles_table_name = "InCite.Articles1"
        self.articles_references_table_name = "InCite.ArticleReferences1"
        self.questions_table_name = "InCite.Questions1"

        # Set up the tables.
        # self.setup_tables() 

    def setup_tables(self):

        # --- Article Table ---
        articles_table_definition = """
        (
          id BIGINT PRIMARY KEY,
          name VARCHAR(255), 
          url VARCHAR(255), 
          authors VARCHAR(255), 
          keywords VARCHAR(255), 
          publication_date DATE,
          content TEXT,
          content_vector VECTOR(DOUBLE, 1536),
          summary TEXT,
          method_issues TEXT,
          coi TEXT
        )
        """
        # Drop the table if it exists.
        try:
            self.cursor.execute(f"DROP TABLE {self.articles_table_name}")
        except Exception as e:
            print("Articles table did not exist or could not be dropped, continuing...")
        # Create the Articles table.
        self.cursor.execute(
            f"CREATE TABLE {self.articles_table_name} {articles_table_definition}"
        )
        print("Articles table created successfully.")

        # --- Article References Table ---
        articles_references_table_definition = f"""
        (
          article_id BIGINT,
          name VARCHAR(255),
          PRIMARY KEY (article_id, name),
          FOREIGN KEY (article_id) REFERENCES {self.articles_table_name}(id)
        )
        """
        try:
            self.cursor.execute(f"DROP TABLE {self.articles_references_table_name}")
        except Exception as e:
            print("Article references table did not exist or could not be dropped, continuing...")
        self.cursor.execute(f"CREATE TABLE {self.articles_references_table_name} {articles_references_table_definition}")
        print("Article references table created successfully.")

        # --- Questions Table ---
        questions_table_definition = """
        (
          id BIGINT PRIMARY KEY,
          question VARCHAR(255), 
          priority INTEGER,
          question_vector VECTOR(DOUBLE, 1536)
        )
        """
        try:
            self.cursor.execute(f"DROP TABLE {self.questions_table_name}")
        except Exception as e:
            print(
                "Questions table did not exist or could not be dropped, continuing..."
            )
        self.cursor.execute(
            f"CREATE TABLE {self.questions_table_name} {questions_table_definition}"
        )
        print("Questions table created successfully.")

    def embed_text(self, text):
        """
        Computes an embedding for the given text using LangChain's OpenAIEmbeddings.
        The document is split into chunks and, for simplicity, only the first chunk is used.
        """
        doc = Document(page_content=text)
        splitter = CharacterTextSplitter(chunk_size=4096)
        chunks = splitter.split_documents([doc])
        embeddings = OpenAIEmbeddings()
        embedded_chunks = embeddings.embed_documents(
            [chunk.page_content for chunk in chunks]
        )
        return embedded_chunks[0]

    def insert_article(
        self,
        id,
        name,
        url,
        authors,
        keywords,
        publication_date,
        content,
        summary,
        method_issues,
        coi,
    ):
        """
        Inserts an article into the Articles table.
        The content is embedded using LangChain and stored in the content_vector column.
        """
        try:
            # Compute the embedding for the article content.
            content_vector = self.embed_text(content)
            print("Article embedding:", content_vector)

            # Convert the embedding into a string for SQL.
            vector_literal = ",".join(str(x) for x in content_vector)

            # Insert into the Articles table.
            sql = f"""
            INSERT INTO {self.articles_table_name} 
              (id, name, url, authors, keywords, publication_date, content, content_vector, summary, method_issues, coi)
            VALUES (?, ?, ?, ?, ?, ?, ?, to_vector(?, double), ?, ?, ?)
            """
            self.cursor.execute(
                sql,
                (
                    id,
                    name,
                    url,
                    authors,
                    keywords,
                    publication_date,
                    content,
                    vector_literal,
                    summary,
                    method_issues,
                    coi,
                ),
            )
            self.conn.commit()
            print(f"Article '{name}' inserted successfully.")
        except dbapi.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                print(f"Error: An article with ID {id} already exists.")
            else:
                print(f"An error occurred: {e}")

    def query_articles(self, query_text, top_k=3):
        """
        Queries the Articles table using a text query.
        Computes an embedding for the query text and performs a similarity search
        by comparing the query embedding with the stored content_vector using IRIS's VECTOR_DOT_PRODUCT.
        """
        # Compute the embedding for the query text.
        query_embedding = self.embed_text(query_text)
        # print("Query embedding:", query_embedding)

        # Convert the query embedding into a comma-separated string literal.
        vector_literal = ",".join(str(x) for x in query_embedding)
        # print("Vector literal:", vector_literal)

        # Build the SQL query.
        sql = f"""
        SELECT TOP {top_k} 
               id, name, url, authors, keywords, publication_date, content,
               VECTOR_DOT_PRODUCT(content_vector, to_vector('{vector_literal}', double)) AS similarity_score 
        FROM {self.articles_table_name}
        ORDER BY similarity_score DESC
        """
        print("Executing SQL:", sql)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def lookup_article(self, article_id):
        """
        Looks up an article by ID and retrieves its details along with referenced articles.
        """
        # Retrieve the article details.
        self.cursor.execute(
            f"SELECT * FROM {self.articles_table_name} WHERE id = ?", (article_id,)
        )
        article = self.cursor.fetchone()

        # Retrieve references.
        self.cursor.execute(
            f"""
            SELECT referenced_article_id FROM {self.articles_references_table_name} WHERE article_id = ?
        """,
            (article_id,),
        )
        references = [row[0] for row in self.cursor.fetchall()]

        return article, references

    def insert_article_references(self, article_id, reference_names):
        """
        Inserts multiple article references into the ArticleReferences table.
        Takes a list of reference names as strings.
        """
        try:
            for ref_name in reference_names:
                sql = f"""
                INSERT INTO {self.articles_references_table_name} (article_id, name)
                VALUES (?, ?)
                """
                self.cursor.execute(sql, (article_id, ref_name))
            self.conn.commit()
            print(f"References for article {article_id} inserted successfully.")
        except dbapi.IntegrityError as e:
            print(f"An error occurred while inserting references: {e}")

    def insert_question(self, id, question, priority):
        """
        Inserts a question into the Questions table.
        The question is embedded using LangChain and stored in the question_vector column.
        """
        try:
            # Compute the embedding for the question.
            question_vector = self.embed_text(question)
            # print("Question embedding:", question_vector)

            # Convert the embedding into a comma-separated string.
            vector_literal = ",".join(str(x) for x in question_vector)

            # Build the INSERT SQL statement.
            sql = f"""
            INSERT INTO {self.questions_table_name} 
              (id, question, priority, question_vector)
            VALUES (?, ?, ?, to_vector('{vector_literal}', double))
            """
            self.cursor.execute(sql, (id, question, priority))
            self.conn.commit()
            print(f"Question '{question}' inserted successfully.")
        except dbapi.IntegrityError as e:
            if "duplicate key value violates unique constraint" in str(e):
                print(f"Error: A question with ID {id} already exists.")
            else:
                print(f"An error occurred: {e}")

    def query_questions(self, query_text, top_k=3):
        """
        Queries the Questions table using a text query.
        Computes an embedding for the query text and performs a similarity search
        by comparing the query embedding with the stored question_vector using IRIS's VECTOR_DOT_PRODUCT.
        """
        query_embedding = self.embed_text(query_text)
        # print("Query embedding:", query_embedding)
        vector_literal = ",".join(str(x) for x in query_embedding)
        # print("Vector literal:", vector_literal)
        sql = f"""
        SELECT TOP {top_k} 
               id, question, priority,
               VECTOR_DOT_PRODUCT(question_vector, to_vector('{vector_literal}', double)) AS similarity_score 
        FROM {self.questions_table_name}
        ORDER BY similarity_score DESC
        """
        print("Executing SQL:", sql)
        self.cursor.execute(sql)
        results = self.cursor.fetchall()
        return results

    def lookup_question(self, question_id):
        """
        Looks up a question by ID and returns its row.
        """
        self.cursor.execute(
            f"SELECT * FROM {self.questions_table_name} WHERE id = ?", (question_id,)
        )
        return self.cursor.fetchone()

    def insert_article_json(self, article_json):
        """
        Inserts an article into the Articles table using a JSON/dict object, then returns the
        article in the specified JSON format.
        """
        # Check if the db already has an article with the same name.
        self.cursor.execute(f"SELECT * FROM {self.articles_table_name} WHERE name = ?", (article_json.get("name"),))
        if self.cursor.fetchone():
            return None
        # Generate a new id by selecting the current maximum and adding 1.
        self.cursor.execute(f"SELECT MAX(id) FROM {self.articles_table_name}")
        max_id_row = self.cursor.fetchone()
        new_id = 1 if (max_id_row[0] is None) else int(max_id_row[0]) + 1

        # Extract fields from the JSON object.
        name = article_json.get("name")
        url = article_json.get("url")
        authors = article_json.get("authors")
        content = article_json.get("content")
        publication_date = article_json.get("publication_date")
        summary = article_json.get("summary")
        method_issues = article_json.get("method_issues")
        coi = article_json.get("coi")
        future_research = article_json.get("future_research", "")
        out_references = article_json.get("out_references", [])

        # Compute the embedding for the article content.
        content_vector = self.embed_text(content)
        vector_literal = ",".join(str(x) for x in content_vector)

        # Insert into the Articles table.
        sql = f"""
        INSERT INTO {self.articles_table_name} 
          (id, name, url, authors, keywords, publication_date, content, content_vector, summary, method_issues, coi)
        VALUES (?, ?, ?, ?, ?, ?, ?, to_vector(?, double), ?, ?, ?)
        """
        self.cursor.execute(
            sql,
            (
                new_id,
                name,
                url,
                authors,
                "",
                publication_date,
                content,
                vector_literal,
                summary,
                method_issues,
                coi,
            ),
        )
        self.conn.commit()

        # If there are outgoing references provided, insert them.
        if out_references:
            self.insert_article_references(new_id, out_references)

        # Build and return the JSON object.
        return {
            "name": name,
            "url": url,
            "authors": authors,
            "content": content,
            "publication_date": publication_date,
            "out_references": out_references,
            "num_out": len(out_references),
            "summary": summary,
            "method_issues": method_issues,
            "coi": coi,
            "future_research": future_research,
        }

    def lookup_article_json(self, article_id):
        """
        Looks up an article by its id and returns its details in JSON format.
        """
        self.cursor.execute(
            f"SELECT * FROM {self.articles_table_name} WHERE id = ?", (article_id,)
        )
        row = self.cursor.fetchone()
        if not row:
            return None

        # Retrieve outgoing references.
        self.cursor.execute(
            f"SELECT referenced_article_id FROM {self.articles_references_table_name} WHERE article_id = ?",
            (article_id,),
        )
        refs = [str(r[0]) for r in self.cursor.fetchall()]

        return {
            "name": row[1],
            "url": row[2],
            "authors": row[3],
            "content": row[6],
            "publication_date": row[5],
            "out_references": refs,
            "num_out": len(refs),
            "summary": row[8],
            "method_issues": row[9],
            "coi": row[10],
            "future_research": "",
        }

    def query_articles_json(self, query_text, top_k=3):
        """
        Queries the Articles table by performing a similarity search and returns a list of articles in JSON format.
        """
        query_embedding = self.embed_text(query_text)
        vector_literal = ",".join(str(x) for x in query_embedding)
        sql = f"""
        SELECT TOP {top_k} 
               id, name, url, authors, keywords, publication_date, content,
               VECTOR_DOT_PRODUCT(content_vector, to_vector('{vector_literal}', double)) AS similarity_score,
               summary, method_issues, coi
        FROM {self.articles_table_name}
        ORDER BY similarity_score DESC
        """
        self.cursor.execute(sql)
        rows = self.cursor.fetchall()

        articles = []
        for row in rows:
            article_id = row[0]
            self.cursor.execute(
                f"SELECT name FROM {self.articles_references_table_name} WHERE article_id = ?",
                (article_id,),
            )
            refs = [str(r[0]) for r in self.cursor.fetchall()]

            article_obj = {
                "name": row[1],
                "url": row[2],
                "authors": row[3],
                "content": row[6],
                "publication_date": row[5],
                "out_references": refs,
                "num_out": len(refs),
                "summary": row[8],
                "method_issues": row[9],
                "coi": row[10],
                "future_research": "",
            }
            articles.append(article_obj)
        return articles
