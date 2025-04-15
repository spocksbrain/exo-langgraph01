"""
Knowledge system for the exo multi-agent system.

This module provides classes for interacting with the Neo4j knowledge graph
and ChromaDB vector database.
"""
import logging
import time
from typing import Dict, Any, List, Optional, Tuple, Union

import chromadb
from neo4j import GraphDatabase

from exo.config import VECTOR_DB_PATH, NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD


# Configure logging
logger = logging.getLogger(__name__)


class VectorStore:
    """Vector store for short-term memory using ChromaDB."""
    
    def __init__(self, collection_name: str = "conversation_history"):
        """Initialize the vector store.
        
        Args:
            collection_name: Name of the collection to use
        """
        self.client = chromadb.PersistentClient(path=str(VECTOR_DB_PATH))
        
        # Get or create the collection
        try:
            self.collection = self.client.get_collection(collection_name)
            logger.info(f"Using existing collection: {collection_name}")
        except ValueError:
            self.collection = self.client.create_collection(
                name=collection_name,
                metadata={"description": f"Collection for {collection_name}"}
            )
            logger.info(f"Created new collection: {collection_name}")
    
    def add(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None,
    ) -> None:
        """Add texts to the vector store.
        
        Args:
            texts: List of texts to add
            metadatas: List of metadata dictionaries
            ids: List of IDs for the texts
        """
        if not texts:
            return
        
        # Generate IDs if not provided
        if ids is None:
            ids = [f"{int(time.time() * 1000)}_{i}" for i in range(len(texts))]
        
        # Generate empty metadata if not provided
        if metadatas is None:
            metadatas = [{} for _ in range(len(texts))]
        
        # Add to collection
        self.collection.add(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
        )
        
        logger.debug(f"Added {len(texts)} texts to vector store")
    
    def search(
        self,
        query: str,
        n_results: int = 5,
        where: Optional[Dict[str, Any]] = None,
    ) -> List[Dict[str, Any]]:
        """Search for similar texts.
        
        Args:
            query: Query text
            n_results: Number of results to return
            where: Filter for metadata
            
        Returns:
            List of results with text, metadata, and ID
        """
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results,
            where=where,
        )
        
        # Format results
        formatted_results = []
        for i in range(len(results["documents"][0])):
            formatted_results.append({
                "text": results["documents"][0][i],
                "metadata": results["metadatas"][0][i],
                "id": results["ids"][0][i],
                "distance": results["distances"][0][i] if "distances" in results else None,
            })
        
        logger.debug(f"Found {len(formatted_results)} results for query: {query[:50]}...")
        return formatted_results
    
    def get(self, ids: List[str]) -> List[Dict[str, Any]]:
        """Get texts by ID.
        
        Args:
            ids: List of IDs to get
            
        Returns:
            List of results with text, metadata, and ID
        """
        results = self.collection.get(ids=ids)
        
        # Format results
        formatted_results = []
        for i in range(len(results["documents"])):
            formatted_results.append({
                "text": results["documents"][i],
                "metadata": results["metadatas"][i],
                "id": results["ids"][i],
            })
        
        return formatted_results
    
    def delete(self, ids: List[str]) -> None:
        """Delete texts by ID.
        
        Args:
            ids: List of IDs to delete
        """
        self.collection.delete(ids=ids)
        logger.debug(f"Deleted {len(ids)} texts from vector store")
    
    def count(self) -> int:
        """Get the number of texts in the vector store.
        
        Returns:
            Number of texts
        """
        return self.collection.count()


class KnowledgeGraph:
    """Knowledge graph for long-term memory using Neo4j."""
    
    def __init__(self):
        """Initialize the knowledge graph."""
        self.driver = GraphDatabase.driver(
            NEO4J_URI,
            auth=(NEO4J_USER, NEO4J_PASSWORD),
        )
    
    def close(self):
        """Close the driver."""
        self.driver.close()
    
    def run_query(self, query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Run a Cypher query.
        
        Args:
            query: Cypher query
            parameters: Query parameters
            
        Returns:
            List of results
        """
        parameters = parameters or {}
        
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]
    
    def create_user(self, user_id: str, name: Optional[str] = None, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a user node.
        
        Args:
            user_id: User ID
            name: User name
            properties: Additional properties
            
        Returns:
            Created user node
        """
        properties = properties or {}
        if name:
            properties["name"] = name
        
        query = """
        MERGE (u:User {id: $user_id})
        SET u += $properties
        RETURN u
        """
        
        result = self.run_query(query, {"user_id": user_id, "properties": properties})
        logger.debug(f"Created user: {user_id}")
        return result[0]["u"] if result else None
    
    def create_agent(self, agent_id: str, name: str, description: Optional[str] = None, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create an agent node.
        
        Args:
            agent_id: Agent ID
            name: Agent name
            description: Agent description
            properties: Additional properties
            
        Returns:
            Created agent node
        """
        properties = properties or {}
        properties["name"] = name
        if description:
            properties["description"] = description
        
        query = """
        MERGE (a:Agent {id: $agent_id})
        SET a += $properties
        RETURN a
        """
        
        result = self.run_query(query, {"agent_id": agent_id, "properties": properties})
        logger.debug(f"Created agent: {agent_id}")
        return result[0]["a"] if result else None
    
    def create_task(self, task_id: str, description: str, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a task node.
        
        Args:
            task_id: Task ID
            description: Task description
            properties: Additional properties
            
        Returns:
            Created task node
        """
        properties = properties or {}
        properties["description"] = description
        properties["created_at"] = int(time.time())
        
        query = """
        MERGE (t:Task {id: $task_id})
        SET t += $properties
        RETURN t
        """
        
        result = self.run_query(query, {"task_id": task_id, "properties": properties})
        logger.debug(f"Created task: {task_id}")
        return result[0]["t"] if result else None
    
    def create_entity(self, entity_id: str, name: str, entity_type: str, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create an entity node.
        
        Args:
            entity_id: Entity ID
            name: Entity name
            entity_type: Entity type
            properties: Additional properties
            
        Returns:
            Created entity node
        """
        properties = properties or {}
        properties["name"] = name
        properties["type"] = entity_type
        
        query = """
        MERGE (e:Entity {id: $entity_id})
        SET e += $properties
        RETURN e
        """
        
        result = self.run_query(query, {"entity_id": entity_id, "properties": properties})
        logger.debug(f"Created entity: {entity_id}")
        return result[0]["e"] if result else None
    
    def create_relationship(self, from_id: str, to_id: str, relationship_type: str, properties: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Create a relationship between nodes.
        
        Args:
            from_id: ID of the source node
            to_id: ID of the target node
            relationship_type: Type of relationship
            properties: Relationship properties
            
        Returns:
            Created relationship
        """
        properties = properties or {}
        
        query = f"""
        MATCH (a), (b)
        WHERE a.id = $from_id AND b.id = $to_id
        MERGE (a)-[r:{relationship_type}]->(b)
        SET r += $properties
        RETURN a, r, b
        """
        
        result = self.run_query(query, {"from_id": from_id, "to_id": to_id, "properties": properties})
        logger.debug(f"Created relationship: ({from_id})-[{relationship_type}]->({to_id})")
        return result[0] if result else None
    
    def get_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Get a node by ID.
        
        Args:
            node_id: Node ID
            
        Returns:
            Node data or None if not found
        """
        query = """
        MATCH (n {id: $node_id})
        RETURN n
        """
        
        result = self.run_query(query, {"node_id": node_id})
        return result[0]["n"] if result else None
    
    def get_relationships(self, node_id: str, relationship_type: Optional[str] = None, direction: str = "outgoing") -> List[Dict[str, Any]]:
        """Get relationships for a node.
        
        Args:
            node_id: Node ID
            relationship_type: Type of relationship to filter by
            direction: Direction of relationship ("outgoing", "incoming", or "both")
            
        Returns:
            List of relationships
        """
        if direction == "outgoing":
            if relationship_type:
                query = f"""
                MATCH (n {{id: $node_id}})-[r:{relationship_type}]->(m)
                RETURN n, r, m
                """
            else:
                query = """
                MATCH (n {id: $node_id})-[r]->(m)
                RETURN n, r, m
                """
        elif direction == "incoming":
            if relationship_type:
                query = f"""
                MATCH (n {{id: $node_id}})<-[r:{relationship_type}]-(m)
                RETURN n, r, m
                """
            else:
                query = """
                MATCH (n {id: $node_id})<-[r]-(m)
                RETURN n, r, m
                """
        else:  # both
            if relationship_type:
                query = f"""
                MATCH (n {{id: $node_id}})-[r:{relationship_type}]-(m)
                RETURN n, r, m
                """
            else:
                query = """
                MATCH (n {id: $node_id})-[r]-(m)
                RETURN n, r, m
                """
        
        return self.run_query(query, {"node_id": node_id})


class KnowledgeSystem:
    """Knowledge system combining vector store and knowledge graph."""
    
    def __init__(self):
        """Initialize the knowledge system."""
        self.vector_store = VectorStore()
        self.knowledge_graph = KnowledgeGraph()
        logger.info("Initialized knowledge system")
    
    def close(self):
        """Close the knowledge system."""
        self.knowledge_graph.close()
        logger.info("Closed knowledge system")
    
    def add_conversation(self, text: str, metadata: Optional[Dict[str, Any]] = None) -> str:
        """Add a conversation to the vector store.
        
        Args:
            text: Conversation text
            metadata: Metadata for the conversation
            
        Returns:
            ID of the added conversation
        """
        metadata = metadata or {}
        conversation_id = f"conv_{int(time.time() * 1000)}"
        metadata["id"] = conversation_id
        metadata["timestamp"] = int(time.time())
        
        self.vector_store.add([text], [metadata], [conversation_id])
        return conversation_id
    
    def search_conversations(self, query: str, n_results: int = 5) -> List[Dict[str, Any]]:
        """Search for similar conversations.
        
        Args:
            query: Query text
            n_results: Number of results to return
            
        Returns:
            List of results
        """
        return self.vector_store.search(query, n_results)
    
    def create_user_task(self, user_id: str, task_description: str, task_id: Optional[str] = None) -> Dict[str, Any]:
        """Create a task for a user.
        
        Args:
            user_id: User ID
            task_description: Task description
            task_id: Task ID (optional)
            
        Returns:
            Created task
        """
        # Create or get user
        self.knowledge_graph.create_user(user_id)
        
        # Create task
        task_id = task_id or f"task_{int(time.time() * 1000)}"
        task = self.knowledge_graph.create_task(task_id, task_description)
        
        # Create relationship
        self.knowledge_graph.create_relationship(
            user_id,
            task_id,
            "REQUESTED",
            {"timestamp": int(time.time())}
        )
        
        return task
    
    def assign_task_to_agent(self, task_id: str, agent_id: str) -> Dict[str, Any]:
        """Assign a task to an agent.
        
        Args:
            task_id: Task ID
            agent_id: Agent ID
            
        Returns:
            Created relationship
        """
        return self.knowledge_graph.create_relationship(
            agent_id,
            task_id,
            "ASSIGNED",
            {"timestamp": int(time.time())}
        )
    
    def complete_task(self, task_id: str, result: str) -> Dict[str, Any]:
        """Mark a task as completed.
        
        Args:
            task_id: Task ID
            result: Task result
            
        Returns:
            Updated task
        """
        query = """
        MATCH (t:Task {id: $task_id})
        SET t.completed = true,
            t.completed_at = $completed_at,
            t.result = $result
        RETURN t
        """
        
        result = self.knowledge_graph.run_query(
            query,
            {
                "task_id": task_id,
                "completed_at": int(time.time()),
                "result": result,
            }
        )
        
        return result[0]["t"] if result else None
    
    def get_user_tasks(self, user_id: str, include_completed: bool = False) -> List[Dict[str, Any]]:
        """Get tasks for a user.
        
        Args:
            user_id: User ID
            include_completed: Whether to include completed tasks
            
        Returns:
            List of tasks
        """
        if include_completed:
            query = """
            MATCH (u:User {id: $user_id})-[:REQUESTED]->(t:Task)
            RETURN t
            ORDER BY t.created_at DESC
            """
        else:
            query = """
            MATCH (u:User {id: $user_id})-[:REQUESTED]->(t:Task)
            WHERE t.completed IS NULL OR t.completed = false
            RETURN t
            ORDER BY t.created_at DESC
            """
        
        result = self.knowledge_graph.run_query(query, {"user_id": user_id})
        return [record["t"] for record in result]
    
    def get_agent_tasks(self, agent_id: str, include_completed: bool = False) -> List[Dict[str, Any]]:
        """Get tasks for an agent.
        
        Args:
            agent_id: Agent ID
            include_completed: Whether to include completed tasks
            
        Returns:
            List of tasks
        """
        if include_completed:
            query = """
            MATCH (a:Agent {id: $agent_id})-[:ASSIGNED]->(t:Task)
            RETURN t
            ORDER BY t.created_at DESC
            """
        else:
            query = """
            MATCH (a:Agent {id: $agent_id})-[:ASSIGNED]->(t:Task)
            WHERE t.completed IS NULL OR t.completed = false
            RETURN t
            ORDER BY t.created_at DESC
            """
        
        result = self.knowledge_graph.run_query(query, {"agent_id": agent_id})
        return [record["t"] for record in result]


# Singleton instance
_knowledge_system_instance: Optional[KnowledgeSystem] = None


def get_knowledge_system() -> KnowledgeSystem:
    """Get the singleton instance of the knowledge system.
    
    Returns:
        KnowledgeSystem instance
    """
    global _knowledge_system_instance
    if _knowledge_system_instance is None:
        _knowledge_system_instance = KnowledgeSystem()
    return _knowledge_system_instance
