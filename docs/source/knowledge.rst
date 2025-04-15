Knowledge System
===============

This guide provides information about the knowledge system of the exo multi-agent system.

Overview
-------

The knowledge system provides a dual-memory architecture for the exo system:

- **Knowledge Graph**: Long-term memory for storing structured information about entities, relationships, and concepts.
- **Vector Database**: Short-term memory for storing and retrieving unstructured information based on semantic similarity.

This dual-memory approach allows the system to maintain both structured knowledge (like user preferences, task history, and domain-specific information) and unstructured knowledge (like conversation history and document content).

Components
---------

The knowledge system consists of the following components:

VectorStore
~~~~~~~~~~

The VectorStore class provides a vector database for storing and retrieving unstructured information based on semantic similarity. It:

- Stores text and metadata
- Retrieves similar texts based on semantic similarity
- Provides a simple interface for adding and searching texts

.. code-block:: python

    from exo.knowledge.system import VectorStore

    # Create a vector store
    vector_store = VectorStore(collection_name="conversations")

    # Add texts
    texts = ["Hello, world!", "How are you?"]
    metadatas = [{"source": "user"}, {"source": "user"}]
    ids = ["text1", "text2"]
    vector_store.add(texts, metadatas, ids)

    # Search for similar texts
    results = vector_store.search("Hello", n_results=2)
    for result in results:
        print(result["text"], result["metadata"], result["id"], result["distance"])

KnowledgeGraph
~~~~~~~~~~~~

The KnowledgeGraph class provides a graph database for storing structured information about entities, relationships, and concepts. It:

- Stores nodes and relationships
- Retrieves nodes and relationships based on queries
- Provides a simple interface for adding and querying nodes and relationships

.. code-block:: python

    from exo.knowledge.system import KnowledgeGraph

    # Create a knowledge graph
    knowledge_graph = KnowledgeGraph()

    # Run a query
    results = knowledge_graph.run_query(
        "CREATE (u:User {name: 'John'}) RETURN u"
    )
    print(results)

    # Run another query
    results = knowledge_graph.run_query(
        "MATCH (u:User {name: 'John'}) RETURN u"
    )
    print(results)

KnowledgeSystem
~~~~~~~~~~~~~

The KnowledgeSystem class provides a unified interface for the knowledge system. It:

- Initializes the vector store and knowledge graph
- Provides methods for adding and retrieving information
- Manages the dual-memory architecture

.. code-block:: python

    from exo.knowledge.system import KnowledgeSystem

    # Create a knowledge system
    knowledge_system = KnowledgeSystem()

    # Add a conversation
    conversation_id = knowledge_system.add_conversation(
        "Hello, world!",
        {"source": "user"}
    )

    # Search for similar conversations
    results = knowledge_system.search_conversations("Hello", n_results=2)
    for result in results:
        print(result["text"], result["metadata"], result["id"], result["distance"])

    # Create a user
    user_id = knowledge_system.create_user(
        "John",
        {"email": "john@example.com"}
    )

    # Get a user
    user = knowledge_system.get_user(user_id)
    print(user)

Usage
-----

To use the knowledge system, you can either use the KnowledgeSystem class directly or use the individual components.

Using the KnowledgeSystem Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The KnowledgeSystem class provides a high-level interface to the knowledge system:

.. code-block:: python

    from exo.knowledge.system import KnowledgeSystem, get_knowledge_system

    # Create a knowledge system
    knowledge_system = KnowledgeSystem()

    # Or get the singleton instance
    knowledge_system = get_knowledge_system()

    # Add a conversation
    conversation_id = knowledge_system.add_conversation(
        "Hello, world!",
        {"source": "user"}
    )

    # Search for similar conversations
    results = knowledge_system.search_conversations("Hello", n_results=2)
    for result in results:
        print(result["text"], result["metadata"], result["id"], result["distance"])

    # Create a user
    user_id = knowledge_system.create_user(
        "John",
        {"email": "john@example.com"}
    )

    # Get a user
    user = knowledge_system.get_user(user_id)
    print(user)

Using the Individual Components
~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can also use the individual components directly:

.. code-block:: python

    from exo.knowledge.system import VectorStore, KnowledgeGraph

    # Create a vector store
    vector_store = VectorStore(collection_name="conversations")

    # Add texts
    texts = ["Hello, world!", "How are you?"]
    metadatas = [{"source": "user"}, {"source": "user"}]
    ids = ["text1", "text2"]
    vector_store.add(texts, metadatas, ids)

    # Search for similar texts
    results = vector_store.search("Hello", n_results=2)
    for result in results:
        print(result["text"], result["metadata"], result["id"], result["distance"])

    # Create a knowledge graph
    knowledge_graph = KnowledgeGraph()

    # Run a query
    results = knowledge_graph.run_query(
        "CREATE (u:User {name: 'John'}) RETURN u"
    )
    print(results)

    # Run another query
    results = knowledge_graph.run_query(
        "MATCH (u:User {name: 'John'}) RETURN u"
    )
    print(results)

Initialization
------------

The knowledge system needs to be initialized before use. The initialization process:

- Creates the vector store collections
- Creates the knowledge graph schema
- Creates the initial data

To initialize the knowledge system, use the init module:

.. code-block:: python

    from exo.knowledge.init import init_knowledge_system

    # Initialize the knowledge system
    init_knowledge_system()

Alternatively, you can use the command-line interface:

.. code-block:: bash

    python -m exo.knowledge.init

Customization
-----------

You can customize the knowledge system by:

- Creating custom vector store collections
- Creating custom knowledge graph schemas
- Extending the KnowledgeSystem class

Creating Custom Vector Store Collections
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create custom vector store collections by using the VectorStore class:

.. code-block:: python

    from exo.knowledge.system import VectorStore

    # Create a custom vector store collection
    vector_store = VectorStore(collection_name="custom_collection")

    # Add texts
    texts = ["Custom text 1", "Custom text 2"]
    metadatas = [{"source": "custom"}, {"source": "custom"}]
    ids = ["custom1", "custom2"]
    vector_store.add(texts, metadatas, ids)

Creating Custom Knowledge Graph Schemas
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can create custom knowledge graph schemas by using the KnowledgeGraph class:

.. code-block:: python

    from exo.knowledge.system import KnowledgeGraph

    # Create a knowledge graph
    knowledge_graph = KnowledgeGraph()

    # Create a custom schema
    knowledge_graph.run_query("""
        CREATE CONSTRAINT unique_user_name IF NOT EXISTS
        FOR (u:User)
        REQUIRE u.name IS UNIQUE
    """)

    # Create custom nodes and relationships
    knowledge_graph.run_query("""
        CREATE (u:User {name: 'John'})
        CREATE (p:Product {name: 'Widget'})
        CREATE (u)-[:PURCHASED {date: '2025-04-15'}]->(p)
    """)

Extending the KnowledgeSystem Class
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can extend the KnowledgeSystem class by subclassing it:

.. code-block:: python

    from exo.knowledge.system import KnowledgeSystem

    class CustomKnowledgeSystem(KnowledgeSystem):
        def __init__(self):
            super().__init__()

        def custom_method(self, param):
            # Custom method implementation
            return f"Custom method: {param}"

API Reference
-----------

VectorStore
~~~~~~~~~~

.. code-block:: python

    class VectorStore:
        """Vector store for storing and retrieving unstructured information."""

        def __init__(self, collection_name="conversations", persist_directory=None):
            """Initialize the vector store.

            Args:
                collection_name (str): The name of the collection.
                persist_directory (str): The directory to persist the vector store.
            """
            self.collection_name = collection_name
            self.persist_directory = persist_directory
            self.client = chromadb.PersistentClient(path=persist_directory)
            self.collection = self.client.get_collection(collection_name)

        def add(self, texts, metadatas=None, ids=None):
            """Add texts to the vector store.

            Args:
                texts (List[str]): The texts to add.
                metadatas (List[Dict]): The metadata for each text.
                ids (List[str]): The IDs for each text.
            """
            self.collection.add(
                documents=texts,
                metadatas=metadatas,
                ids=ids,
            )

        def search(self, query, n_results=5, where=None):
            """Search for similar texts.

            Args:
                query (str): The query text.
                n_results (int): The number of results to return.
                where (Dict): The filter to apply.

            Returns:
                List[Dict]: The search results.
            """
            results = self.collection.query(
                query_texts=[query],
                n_results=n_results,
                where=where,
            )
            return [
                {
                    "text": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "id": results["ids"][0][i],
                    "distance": results["distances"][0][i],
                }
                for i in range(len(results["documents"][0]))
            ]

KnowledgeGraph
~~~~~~~~~~~~

.. code-block:: python

    class KnowledgeGraph:
        """Knowledge graph for storing structured information."""

        def __init__(self, uri=None, user=None, password=None):
            """Initialize the knowledge graph.

            Args:
                uri (str): The URI of the Neo4j database.
                user (str): The username for the Neo4j database.
                password (str): The password for the Neo4j database.
            """
            self.uri = uri or "bolt://localhost:7687"
            self.user = user or "neo4j"
            self.password = password or "password"
            self.driver = GraphDatabase.driver(self.uri, auth=(self.user, self.password))

        def run_query(self, query, parameters=None):
            """Run a Cypher query.

            Args:
                query (str): The Cypher query.
                parameters (Dict): The query parameters.

            Returns:
                List[Dict]: The query results.
            """
            with self.driver.session() as session:
                result = session.run(query, parameters or {})
                return [record.data() for record in result]

KnowledgeSystem
~~~~~~~~~~~~~

.. code-block:: python

    class KnowledgeSystem:
        """Knowledge system for the exo system."""

        def __init__(self):
            """Initialize the knowledge system."""
            self.vector_store = VectorStore()
            self.knowledge_graph = KnowledgeGraph()

        def add_conversation(self, text, metadata=None):
            """Add a conversation to the vector store.

            Args:
                text (str): The conversation text.
                metadata (Dict): The metadata for the conversation.

            Returns:
                str: The conversation ID.
            """
            conversation_id = f"conv_{int(time.time() * 1000)}"
            self.vector_store.add(
                texts=[text],
                metadatas=[metadata or {}],
                ids=[conversation_id],
            )
            return conversation_id

        def search_conversations(self, query, n_results=5, where=None):
            """Search for similar conversations.

            Args:
                query (str): The query text.
                n_results (int): The number of results to return.
                where (Dict): The filter to apply.

            Returns:
                List[Dict]: The search results.
            """
            return self.vector_store.search(query, n_results, where)

        def create_user(self, name, metadata=None):
            """Create a user in the knowledge graph.

            Args:
                name (str): The user name.
                metadata (Dict): The metadata for the user.

            Returns:
                str: The user ID.
            """
            result = self.knowledge_graph.run_query(
                "CREATE (u:User {name: $name, metadata: $metadata}) RETURN id(u) AS id",
                {"name": name, "metadata": metadata or {}},
            )
            return str(result[0]["id"])

        def get_user(self, user_id):
            """Get a user from the knowledge graph.

            Args:
                user_id (str): The user ID.

            Returns:
                Dict: The user data.
            """
            result = self.knowledge_graph.run_query(
                "MATCH (u:User) WHERE id(u) = $id RETURN u",
                {"id": int(user_id)},
            )
            return result[0]["u"] if result else None

def get_knowledge_system():
    """Get the singleton instance of the knowledge system.

    Returns:
        KnowledgeSystem: The knowledge system.
    """
    global _knowledge_system_instance
    if _knowledge_system_instance is None:
        _knowledge_system_instance = KnowledgeSystem()
    return _knowledge_system_instance
