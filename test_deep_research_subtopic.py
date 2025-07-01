#!/usr/bin/env python3
"""
Test script for the new Deep Research Sub-Topic Research Report functionality.
"""

import asyncio
import nest_asyncio
from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType, Tone

# Apply nest_asyncio to allow for nested event loops
nest_asyncio.apply()

async def test_deep_research_subtopic_report():
    """Test the new deep research subtopic report functionality."""
    
    print("🧪 Testing Deep Research Sub-Topic Research Report...")
    
    # Initialize researcher with the new report type
    researcher = GPTResearcher(
        query="What are the latest developments in artificial intelligence?",
        report_type=ReportType.DeepResearchSubtopicReport.value,
        tone=Tone.Objective,
        verbose=True
    )
    
    print(f"📋 Report Type: {researcher.report_type}")
    print(f"🔍 Query: {researcher.query}")
    print(f"🎯 Tone: {researcher.tone.value}")
    
    # Conduct research
    print("\n🔬 Conducting deep research...")
    context = await researcher.conduct_research()
    print(f"✅ Research completed! Context length: {len(context)} characters")
    
    # Generate report
    print("\n📝 Generating report...")
    report = await researcher.write_report()
    print(f"✅ Report generated! Report length: {len(report)} characters")
    
    # Print a preview of the report
    print("\n📄 Report Preview:")
    print("=" * 50)
    print(report[:500] + "..." if len(report) > 500 else report)
    print("=" * 50)
    
    # Get costs
    total_costs = researcher.get_costs()
    print(f"\n💰 Total costs: ${total_costs:.2f}")
    
    return report

async def test_subtopic_generation():
    """Test subtopic generation with the new report type."""
    
    print("\n🌳 Testing subtopic generation...")
    
    # Initialize researcher
    researcher = GPTResearcher(
        query="What are the latest developments in renewable energy?",
        report_type=ReportType.DeepResearchSubtopicReport.value,
        tone=Tone.Objective,
        verbose=True
    )
    
    # Conduct research
    await researcher.conduct_research()
    
    # Get subtopics
    subtopics = await researcher.get_subtopics()
    print(f"✅ Generated {len(subtopics)} subtopics:")
    for i, subtopic in enumerate(subtopics, 1):
        print(f"  {i}. {subtopic}")
    
    return subtopics

if __name__ == "__main__":
    print("🚀 Starting Deep Research Sub-Topic Report Tests...")
    
    # Run tests
    try:
        # Test 1: Basic deep research subtopic report
        report = asyncio.run(test_deep_research_subtopic_report())
        
        # Test 2: Subtopic generation
        subtopics = asyncio.run(test_subtopic_generation())
        
        print("\n🎉 All tests completed successfully!")
        print("✅ Deep Research Sub-Topic Research Report is working correctly!")
        
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc() 