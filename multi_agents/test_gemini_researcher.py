#!/usr/bin/env python3
"""
Simple test script for the GeminiResearcherAgent and GeminiEditorAgent.
This script tests the basic functionality without requiring API calls.
"""

import sys
import os

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_agents.agents import GeminiResearcherAgent, GeminiEditorAgent

def test_agent_initialization():
    """Test that the Gemini agents can be initialized."""
    print("Testing Gemini agents initialization...")
    
    try:
        # Test GeminiResearcherAgent initialization
        researcher = GeminiResearcherAgent()
        print("✓ GeminiResearcherAgent initialization successful")
        
        # Test GeminiEditorAgent initialization
        editor = GeminiEditorAgent()
        print("✓ GeminiEditorAgent initialization successful")
        
        # Test initialization with parameters
        researcher_with_params = GeminiResearcherAgent(
            websocket=None,
            stream_output=None,
            tone="professional",
            headers={"User-Agent": "test"}
        )
        print("✓ GeminiResearcherAgent with parameters successful")
        
        editor_with_params = GeminiEditorAgent(
            websocket=None,
            stream_output=None,
            tone="professional",
            headers={"User-Agent": "test"}
        )
        print("✓ GeminiEditorAgent with parameters successful")
        
        return True
        
    except Exception as e:
        print(f"✗ Initialization failed: {e}")
        return False

def test_researcher_methods():
    """Test that the GeminiResearcherAgent has the required methods."""
    print("Testing GeminiResearcherAgent methods...")
    
    try:
        agent = GeminiResearcherAgent()
        
        # Test that the agent has the required methods
        required_methods = [
            'research',
            'run_subtopic_research', 
            'run_initial_research',
            'run_depth_research'
        ]
        
        for method in required_methods:
            if hasattr(agent, method):
                print(f"✓ Method '{method}' exists")
            else:
                print(f"✗ Method '{method}' missing")
                return False
        
        print("✓ All required methods present")
        return True
        
    except Exception as e:
        print(f"✗ Method test failed: {e}")
        return False

def test_editor_methods():
    """Test that the GeminiEditorAgent has the required methods."""
    print("Testing GeminiEditorAgent methods...")
    
    try:
        agent = GeminiEditorAgent()
        
        # Test that the agent has the required methods
        required_methods = [
            'plan_research',
            'run_parallel_research'
        ]
        
        for method in required_methods:
            if hasattr(agent, method):
                print(f"✓ Method '{method}' exists")
            else:
                print(f"✗ Method '{method}' missing")
                return False
        
        print("✓ All required methods present")
        return True
        
    except Exception as e:
        print(f"✗ Method test failed: {e}")
        return False

def test_imports():
    """Test that all required imports work."""
    print("Testing imports...")
    
    try:
        # Test basic imports
        from multi_agents.agents import GeminiResearcherAgent, GeminiEditorAgent
        print("✓ Gemini agents import successful")
        
        # Test gemini_agent imports
        from multi_agents.agents.gemini_agent.graph import graph as gemini_graph
        print("✓ Gemini graph import successful")
        
        from multi_agents.agents.gemini_agent.configuration import Configuration
        print("✓ Configuration import successful")
        
        # Test utils imports
        from multi_agents.agents.utils.views import print_agent_output
        print("✓ Utils imports successful")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import failed: {e}")
        return False
    except Exception as e:
        print(f"✗ Unexpected error during import: {e}")
        return False

def test_agent_interface():
    """Test that the agents follow the expected interface."""
    print("Testing agent interface...")
    
    try:
        researcher = GeminiResearcherAgent()
        editor = GeminiEditorAgent()
        
        # Test that the agents have the expected attributes
        expected_attrs = ['websocket', 'stream_output', 'headers', 'tone']
        
        for attr in expected_attrs:
            if hasattr(researcher, attr):
                print(f"✓ Researcher attribute '{attr}' present")
            else:
                print(f"✗ Researcher attribute '{attr}' missing")
                return False
                
            if hasattr(editor, attr):
                print(f"✓ Editor attribute '{attr}' present")
            else:
                print(f"✗ Editor attribute '{attr}' missing")
                return False
        
        # Test that methods are callable
        researcher_methods = [
            researcher.research,
            researcher.run_subtopic_research,
            researcher.run_initial_research,
            researcher.run_depth_research
        ]
        
        editor_methods = [
            editor.plan_research,
            editor.run_parallel_research
        ]
        
        for method in researcher_methods:
            if callable(method):
                print(f"✓ Researcher method '{method.__name__}' is callable")
            else:
                print(f"✗ Researcher method '{method.__name__}' is not callable")
                return False
                
        for method in editor_methods:
            if callable(method):
                print(f"✓ Editor method '{method.__name__}' is callable")
            else:
                print(f"✗ Editor method '{method.__name__}' is not callable")
                return False
        
        print("✓ Interface test passed")
        return True
        
    except Exception as e:
        print(f"✗ Interface test failed: {e}")
        return False

def main():
    """Run all tests."""
    print("Gemini Agents Test Suite")
    print("=" * 40)
    
    tests = [
        ("Import Test", test_imports),
        ("Initialization Test", test_agent_initialization),
        ("Researcher Methods Test", test_researcher_methods),
        ("Editor Methods Test", test_editor_methods),
        ("Interface Test", test_agent_interface)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} failed")
    
    print(f"\n{'='*40}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All tests passed! The Gemini agents are ready to use.")
        return True
    else:
        print("✗ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 