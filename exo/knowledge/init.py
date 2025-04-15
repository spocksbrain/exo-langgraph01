"""
Initialization script for the exo knowledge system.

This script initializes the Neo4j knowledge graph and ChromaDB vector database.
"""
import os
import logging
from pathlib import Path

from exo.config import DATA_DIR, VECTOR_DB_PATH, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


def init_vector_db():
    """Initialize the ChromaDB vector database."""
    try:
        import chromadb
        
        # Create the vector database directory if it doesn't exist
        os.makedirs(VECTOR_DB_PATH, exist_ok=True)
        
        # Initialize the client
        client = chromadb.PersistentClient(path=str(VECTOR_DB_PATH))
        
        # Create a collection for conversation history
        collection = client.create_collection(
            name="conversation_history",
            metadata={"description": "Conversation history for the exo system"}
        )
        
        logger.info(f"Initialized ChromaDB vector database at {VECTOR_DB_PATH}")
        return True
    except Exception as e:
        logger.exception(f"Error initializing ChromaDB: {e}")
        return False


def init_knowledge_graph():
    """Initialize the Neo4j knowledge graph."""
    try:
        from neo4j import GraphDatabase
        
        # Connect to Neo4j
        driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
        
        # Create constraints and indexes
        with driver.session() as session:
            # Create constraint on User nodes
            session.run("""
                CREATE CONSTRAINT user_id IF NOT EXISTS
                FOR (u:User)
                REQUIRE u.id IS UNIQUE
            """)
            
            # Create constraint on Agent nodes
            session.run("""
                CREATE CONSTRAINT agent_id IF NOT EXISTS
                FOR (a:Agent)
                REQUIRE a.id IS UNIQUE
            """)
            
            # Create constraint on Task nodes
            session.run("""
                CREATE CONSTRAINT task_id IF NOT EXISTS
                FOR (t:Task)
                REQUIRE t.id IS UNIQUE
            """)
            
            # Create constraint on Entity nodes
            session.run("""
                CREATE CONSTRAINT entity_id IF NOT EXISTS
                FOR (e:Entity)
                REQUIRE e.id IS UNIQUE
            """)
            
            # Create index on Entity nodes
            session.run("""
                CREATE INDEX entity_name IF NOT EXISTS
                FOR (e:Entity)
                ON (e.name)
            """)
        
        # Close the driver
        driver.close()
        
        logger.info(f"Initialized Neo4j knowledge graph at {NEO4J_URI}")
        return True
    except Exception as e:
        logger.exception(f"Error initializing Neo4j: {e}")
        return False


def init_knowledge_system():
    """Initialize the knowledge system."""
    logger.info("Initializing knowledge system...")
    
    # Create data directory if it doesn't exist
    os.makedirs(DATA_DIR, exist_ok=True)
    
    # Initialize vector database
    vector_db_success = init_vector_db()
    
    # Initialize knowledge graph
    knowledge_graph_success = init_knowledge_graph()
    
    if vector_db_success and knowledge_graph_success:
        logger.info("Knowledge system initialization complete")
        return True
    else:
        logger.error("Knowledge system initialization failed")
        return False


if __name__ == "__main__":
    init_knowledge_system()
