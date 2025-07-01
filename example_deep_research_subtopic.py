#!/usr/bin/env python3
"""
Example script demonstrating the new Deep Research Sub-Topic Research Report functionality.

This example shows how to use the new report type that combines deep research methodology
with subtopic structure for comprehensive research reports.
"""

import asyncio
import nest_asyncio
from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType, Tone

# Apply nest_asyncio to allow for nested event loops
nest_asyncio.apply()

async def main():
    """Main function demonstrating the deep research subtopic report."""
    
    print("🔬 Deep Research Sub-Topic Research Report Example")
    print("=" * 60)
    
    # Example 1: Basic usage
    print("\n📋 Example 1: Basic Deep Research Sub-Topic Report")
    print("-" * 50)
    
    researcher = GPTResearcher(
        query="What are the latest developments in quantum computing?",
        report_type=ReportType.DeepResearchSubtopicReport.value,
        tone=Tone.Analytical,
        verbose=True
    )
    
    print(f"🔍 Research Query: {researcher.query}")
    print(f"📊 Report Type: {researcher.report_type}")
    print(f"🎯 Tone: {researcher.tone.value}")
    
    # Conduct research
    print("\n🔬 Conducting deep research...")
    context = await researcher.conduct_research()
    print(f"✅ Research completed! Context length: {len(context)} characters")
    
    # Generate report
    print("\n📝 Generating comprehensive report...")
    report = await researcher.write_report()
    print(f"✅ Report generated! Length: {len(report)} characters")
    
    # Display report preview
    print("\n📄 Report Preview:")
    print("=" * 40)
    lines = report.split('\n')[:20]  # Show first 20 lines
    for line in lines:
        print(line)
    if len(report.split('\n')) > 20:
        print("...")
    print("=" * 40)
    
    # Show costs
    total_costs = researcher.get_costs()
    print(f"\n💰 Total Research Costs: ${total_costs:.2f}")
    
    # Example 2: With custom configuration
    print("\n\n📋 Example 2: Custom Configuration")
    print("-" * 50)
    
    # You can also configure deep research parameters
    researcher2 = GPTResearcher(
        query="What are the environmental impacts of electric vehicles?",
        report_type=ReportType.DeepResearchSubtopicReport.value,
        tone=Tone.Informative,
        verbose=True,
        # Deep research configuration (optional)
        deep_research_breadth=3,  # Number of parallel research paths
        deep_research_depth=2,    # How many levels deep to explore
        total_words=1500,         # Target word count
    )
    
    print(f"🔍 Research Query: {researcher2.query}")
    print(f"🎯 Tone: {researcher2.tone.value}")
    print(f"📊 Deep Research Breadth: {researcher2.deep_researcher.breadth}")
    print(f"📊 Deep Research Depth: {researcher2.deep_researcher.depth}")
    
    # Conduct research
    print("\n🔬 Conducting deep research with custom configuration...")
    context2 = await researcher2.conduct_research()
    print(f"✅ Research completed! Context length: {len(context2)} characters")
    
    # Generate report
    print("\n📝 Generating report...")
    report2 = await researcher2.write_report()
    print(f"✅ Report generated! Length: {len(report2)} characters")
    
    # Show costs
    total_costs2 = researcher2.get_costs()
    print(f"\n💰 Total Research Costs: ${total_costs2:.2f}")
    
    print("\n🎉 Examples completed successfully!")
    print("\n💡 Key Features of Deep Research Sub-Topic Report:")
    print("   • Combines deep research methodology with subtopic structure")
    print("   • Explores topics with unprecedented depth and breadth")
    print("   • Uses recursive exploration with multiple research paths")
    print("   • Synthesizes information from various research branches")
    print("   • Maintains proper citation and source tracking")
    print("   • Ideal for comprehensive, academic-style research reports")

if __name__ == "__main__":
    print("🚀 Starting Deep Research Sub-Topic Report Examples...")
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n⏹️  Example interrupted by user")
    except Exception as e:
        print(f"\n❌ Example failed with error: {e}")
        import traceback
        traceback.print_exc() 