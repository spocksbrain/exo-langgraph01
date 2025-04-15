"""
Tests for the knowledge system.
"""
import unittest
from unittest.mock import MagicMock, patch

from exo.knowledge.system import VectorStore, KnowledgeGraph, KnowledgeSystem, get_knowledge_system


class TestVectorStore(unittest.TestCase):
    """Tests for the VectorStore class."""
    
    @patch("exo.knowledge.system.chromadb.PersistentClient")
    def test_init(self, mock_client):
        """Test initialization."""
        # Mock the client and collection
        mock_client_instance = MagicMock()
        mock_collection = MagicMock()
        mock_client_instance.get_collection.return_value = mock_collection
        mock_client.return_value = mock_client_instance
        
        # Create the vector store
        vector_store = VectorStore(collection_name="test_collection")
        
        # Check that the client was created
        mock_client.assert_called_once()
        
        # Check that the collection was retrieved
        mock_client_instance.get_collection.assert_called_once_with("test_collection")
        
        # Check that the collection was set
        self.assertEqual(vector_store.collection, mock_collection)
    
    @patch("exo.knowledge.system.chromadb.PersistentClient")
    def test_add(self, mock_client):
        """Test add method."""
        # Mock the client and collection
        mock_client_instance = MagicMock()
        mock_collection = MagicMock()
        mock_client_instance.get_collection.return_value = mock_collection
        mock_client.return_value = mock_client_instance
        
        # Create the vector store
        vector_store = VectorStore()
        
        # Test the add method
        texts = ["Test text 1", "Test text 2"]
        metadatas = [{"source": "test"}, {"source": "test"}]
        ids = ["test_id_1", "test_id_2"]
        
        vector_store.add(texts, metadatas, ids)
        
        # Check that the collection.add method was called
        mock_collection.add.assert_called_once_with(
            documents=texts,
            metadatas=metadatas,
            ids=ids,
        )
    
    @patch("exo.knowledge.system.chromadb.PersistentClient")
    def test_search(self, mock_client):
        """Test search method."""
        # Mock the client and collection
        mock_client_instance = MagicMock()
        mock_collection = MagicMock()
        mock_client_instance.get_collection.return_value = mock_collection
        mock_client.return_value = mock_client_instance
        
        # Mock the collection.query method
        mock_collection.query.return_value = {
            "documents": [["Test text 1", "Test text 2"]],
            "metadatas": [[{"source": "test"}, {"source": "test"}]],
            "ids": [["test_id_1", "test_id_2"]],
            "distances": [[0.1, 0.2]],
        }
        
        # Create the vector store
        vector_store = VectorStore()
        
        # Test the search method
        results = vector_store.search("Test query", n_results=2)
        
        # Check that the collection.query method was called
        mock_collection.query.assert_called_once_with(
            query_texts=["Test query"],
            n_results=2,
            where=None,
        )
        
        # Check the results
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["text"], "Test text 1")
        self.assertEqual(results[0]["metadata"], {"source": "test"})
        self.assertEqual(results[0]["id"], "test_id_1")
        self.assertEqual(results[0]["distance"], 0.1)


class TestKnowledgeGraph(unittest.TestCase):
    """Tests for the KnowledgeGraph class."""
    
    @patch("exo.knowledge.system.GraphDatabase")
    def test_init(self, mock_graph_db):
        """Test initialization."""
        # Mock the driver
        mock_driver = MagicMock()
        mock_graph_db.driver.return_value = mock_driver
        
        # Create the knowledge graph
        knowledge_graph = KnowledgeGraph()
        
        # Check that the driver was created
        mock_graph_db.driver.assert_called_once_with(
            "bolt://localhost:7687",
            auth=("neo4j", "password"),
        )
        
        # Check that the driver was set
        self.assertEqual(knowledge_graph.driver, mock_driver)
    
    @patch("exo.knowledge.system.GraphDatabase")
    def test_run_query(self, mock_graph_db):
        """Test run_query method."""
        # Mock the driver and session
        mock_driver = MagicMock()
        mock_session = MagicMock()
        mock_result = MagicMock()
        mock_record = MagicMock()
        mock_record.data.return_value = {"key": "value"}
        mock_result.__iter__.return_value = [mock_record]
        mock_session.run.return_value = mock_result
        mock_driver.session.return_value.__enter__.return_value = mock_session
        mock_graph_db.driver.return_value = mock_driver
        
        # Create the knowledge graph
        knowledge_graph = KnowledgeGraph()
        
        # Test the run_query method
        result = knowledge_graph.run_query("MATCH (n) RETURN n", {"param": "value"})
        
        # Check that the session.run method was called
        mock_session.run.assert_called_once_with("MATCH (n) RETURN n", {"param": "value"})
        
        # Check the result
        self.assertEqual(result, [{"key": "value"}])


class TestKnowledgeSystem(unittest.TestCase):
    """Tests for the KnowledgeSystem class."""
    
    @patch("exo.knowledge.system.VectorStore")
    @patch("exo.knowledge.system.KnowledgeGraph")
    def test_init(self, mock_knowledge_graph, mock_vector_store):
        """Test initialization."""
        # Mock the vector store and knowledge graph
        mock_vector_store_instance = MagicMock()
        mock_knowledge_graph_instance = MagicMock()
        mock_vector_store.return_value = mock_vector_store_instance
        mock_knowledge_graph.return_value = mock_knowledge_graph_instance
        
        # Create the knowledge system
        knowledge_system = KnowledgeSystem()
        
        # Check that the vector store and knowledge graph were created
        mock_vector_store.assert_called_once()
        mock_knowledge_graph.assert_called_once()
        
        # Check that the vector store and knowledge graph were set
        self.assertEqual(knowledge_system.vector_store, mock_vector_store_instance)
        self.assertEqual(knowledge_system.knowledge_graph, mock_knowledge_graph_instance)
    
    @patch("exo.knowledge.system.VectorStore")
    @patch("exo.knowledge.system.KnowledgeGraph")
    def test_add_conversation(self, mock_knowledge_graph, mock_vector_store):
        """Test add_conversation method."""
        # Mock the vector store and knowledge graph
        mock_vector_store_instance = MagicMock()
        mock_knowledge_graph_instance = MagicMock()
        mock_vector_store.return_value = mock_vector_store_instance
        mock_knowledge_graph.return_value = mock_knowledge_graph_instance
        
        # Create the knowledge system
        knowledge_system = KnowledgeSystem()
        
        # Test the add_conversation method
        with patch("exo.knowledge.system.time.time", return_value=1000):
            conversation_id = knowledge_system.add_conversation("Test conversation", {"source": "test"})
        
        # Check that the vector_store.add method was called
        mock_vector_store_instance.add.assert_called_once()
        
        # Check the conversation ID
        self.assertEqual(conversation_id, "conv_1000000")


class TestGetKnowledgeSystem(unittest.TestCase):
    """Tests for the get_knowledge_system function."""
    
    @patch("exo.knowledge.system.KnowledgeSystem")
    def test_get_knowledge_system(self, mock_knowledge_system):
        """Test get_knowledge_system function."""
        # Mock the knowledge system
        mock_knowledge_system_instance = MagicMock()
        mock_knowledge_system.return_value = mock_knowledge_system_instance
        
        # Reset the singleton instance
        import exo.knowledge.system
        exo.knowledge.system._knowledge_system_instance = None
        
        # Get the knowledge system
        knowledge_system = get_knowledge_system()
        
        # Check that the knowledge system was created
        mock_knowledge_system.assert_called_once()
        
        # Check that the knowledge system was returned
        self.assertEqual(knowledge_system, mock_knowledge_system_instance)
        
        # Get the knowledge system again
        knowledge_system2 = get_knowledge_system()
        
        # Check that the knowledge system was not created again
        mock_knowledge_system.assert_called_once()
        
        # Check that the same knowledge system was returned
        self.assertEqual(knowledge_system2, mock_knowledge_system_instance)


if __name__ == "__main__":
    unittest.main()
