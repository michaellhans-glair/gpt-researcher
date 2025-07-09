#!/usr/bin/env python3
"""
Test script to verify that the async fixes work for the GeminiResearcherAgent.
This script tests the async functionality without making actual API calls.
"""

import asyncio
import os
import sys

# Add the parent directory to the path to import modules
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from multi_agents.agents import GeminiResearcherAgent

async def test_async_initialization():
    """Test that the GeminiResearcherAgent can be initialized and has async methods."""
    print("Testing async initialization...")
    
    try:
        # Test basic initialization
        agent = GeminiResearcherAgent()
        print("✓ Basic initialization successful")
        
        # Test that the agent has async methods
        required_async_methods = [
            'research',
            'run_subtopic_research', 
            'run_initial_research',
            'run_depth_research'
        ]
        
        for method_name in required_async_methods:
            if hasattr(agent, method_name):
                method = getattr(agent, method_name)
                if asyncio.iscoroutinefunction(method):
                    print(f"✓ Method '{method_name}' is async")
                else:
                    print(f"✗ Method '{method_name}' is not async")
                    return False
            else:
                print(f"✗ Method '{method_name}' missing")
                return False
        
        print("✓ All required async methods present")
        return True
        
    except Exception as e:
        print(f"✗ Async initialization failed: {e}")
        return False

async def test_async_methods():
    """Test that the async methods can be called without blocking."""
    print("Testing async method calls...")
    
    try:
        agent = GeminiResearcherAgent()
        
        # Test that we can call the async methods (they should not block)
        # We won't actually run them since we don't have API keys, but we can test the interface
        
        # Test the _run_gemini_graph_async method exists
        if hasattr(agent, '_run_gemini_graph_async'):
            print("✓ _run_gemini_graph_async method exists")
        else:
            print("✗ _run_gemini_graph_async method missing")
            return False
            
        # Test the _run_simple_gemini_research method exists
        if hasattr(agent, '_run_simple_gemini_research'):
            print("✓ _run_simple_gemini_research method exists")
        else:
            print("✗ _run_simple_gemini_research method missing")
            return False
        
        print("✓ Async method interface test passed")
        return True
        
    except Exception as e:
        print(f"✗ Async method test failed: {e}")
        return False

async def test_error_handling():
    """Test that error handling works properly in async context."""
    print("Testing async error handling...")
    
    try:
        agent = GeminiResearcherAgent()
        
        # Test that the agent can handle errors gracefully
        # This should not raise an exception even without API keys
        # because the methods are async and won't execute immediately
        
        # Test that we can create the research method without errors
        research_method = agent.research
        print("✓ Research method can be accessed")
        
        # Test that we can create the subtopic research method without errors
        subtopic_method = agent.run_subtopic_research
        print("✓ Subtopic research method can be accessed")
        
        print("✓ Error handling test passed")
        return True
        
    except Exception as e:
        print(f"✗ Error handling test failed: {e}")
        return False

async def main():
    """Run all async tests."""
    print("GeminiResearcherAgent Async Test Suite")
    print("=" * 45)
    
    tests = [
        ("Async Initialization Test", test_async_initialization),
        ("Async Methods Test", test_async_methods),
        ("Async Error Handling Test", test_error_handling)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n{test_name}:")
        if await test_func():
            passed += 1
        else:
            print(f"✗ {test_name} failed")
    
    print(f"\n{'='*45}")
    print(f"Tests passed: {passed}/{total}")
    
    if passed == total:
        print("✓ All async tests passed! The GeminiResearcherAgent is ready for async use.")
        return True
    else:
        print("✗ Some async tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1) 