# Deep Research Sub-Topic Research Report ✨ NEW ✨

## Overview

The **Deep Research Sub-Topic Research Report** is a new report type that combines the power of deep research methodology with the structured approach of subtopic reports. This innovative approach provides comprehensive, multi-layered research that explores topics with unprecedented depth and breadth while maintaining organized, coherent report structure.

## Key Features

- **🔬 Deep Research Methodology**: Uses recursive exploration with both breadth (multiple parallel research paths) and depth (sequential iterations)
- **📊 Subtopic Structure**: Organizes findings into well-structured subtopics for better readability
- **🌐 Multi-Level Investigation**: Explores topics from foundational concepts to advanced insights
- **🔗 Cross-Branch Synthesis**: Integrates findings from various research branches into a coherent narrative
- **📚 Proper Citations**: Maintains comprehensive source tracking and citation management
- **⚡ Concurrent Processing**: Utilizes async/await patterns for efficient parallel research

## How It Works

### 1. Deep Research Process
The system employs a tree-like exploration pattern:
- **Breadth**: Generates multiple search queries to explore different aspects of your topic
- **Depth**: Recursively dives deeper, following leads and uncovering connections
- **Concurrent Processing**: Runs multiple research paths simultaneously
- **Smart Context Management**: Aggregates and synthesizes findings across all branches

### 2. Subtopic Integration
- Organizes deep research findings into structured subtopics
- Ensures content uniqueness and prevents overlap between sections
- Maintains proper citation and source tracking throughout
- Creates coherent narrative flow from foundational to advanced insights

## Usage

### Basic Usage

```python
from gpt_researcher import GPTResearcher
from gpt_researcher.utils.enum import ReportType, Tone
import asyncio

async def main():
    # Initialize researcher with deep research subtopic report type
    researcher = GPTResearcher(
        query="What are the latest developments in quantum computing?",
        report_type=ReportType.DeepResearchSubtopicReport.value,
        tone=Tone.Analytical,
        verbose=True
    )
    
    # Conduct research
    context = await researcher.conduct_research()
    
    # Generate report
    report = await researcher.write_report()
    print(report)

if __name__ == "__main__":
    asyncio.run(main())
```

### Advanced Configuration

```python
researcher = GPTResearcher(
    query="What are the environmental impacts of electric vehicles?",
    report_type=ReportType.DeepResearchSubtopicReport.value,
    tone=Tone.Informative,
    verbose=True,
    # Deep research configuration
    deep_research_breadth=4,  # Number of parallel research paths
    deep_research_depth=3,    # How many levels deep to explore
    total_words=2000,         # Target word count
)
```

### CLI Usage

```bash
python cli.py "What are the latest developments in artificial intelligence?" \
    --report_type deep_research_subtopic_report \
    --tone analytical
```

## Configuration Parameters

### Deep Research Parameters

- **`deep_research_breadth`**: Number of parallel research paths at each level (default: 4)
- **`deep_research_depth`**: How many levels deep to explore (default: 2)
- **`deep_research_concurrency`**: Maximum number of concurrent research operations (default: 4)

### Report Parameters

- **`total_words`**: Target word count for the report (default: 1200)
- **`tone`**: Writing tone (Objective, Analytical, Informative, etc.)
- **`report_format`**: Citation format (APA, MLA, etc.)

## Environment Variables

You can configure deep research behavior through environment variables:

```bash
export DEEP_RESEARCH_BREADTH=4
export DEEP_RESEARCH_DEPTH=2
export DEEP_RESEARCH_CONCURRENCY=4
export TOTAL_WORDS=2000
```

## Report Structure

The generated report follows this structure:

1. **Main Topic Header** (H1)
2. **Subtopics** (H2) - Each covering a specific aspect
3. **Subsections** (H3) - Detailed exploration within each subtopic
4. **Cross-references** - Connections between different research branches
5. **Citations** - Proper source attribution throughout

## Example Output

```
# Latest Developments in Quantum Computing

## Quantum Hardware Advancements

### Superconducting Qubits
Recent breakthroughs in superconducting qubit technology have...

### Topological Qubits
Microsoft's approach to topological qubits shows promise...

## Quantum Algorithms and Applications

### Quantum Machine Learning
The intersection of quantum computing and AI has led to...

### Cryptography and Security
Post-quantum cryptography developments include...

## Industry and Commercialization

### Major Players and Investments
Companies like IBM, Google, and startups are...

### Real-world Applications
Current practical applications include...
```

## Comparison with Other Report Types

| Feature | Standard Report | Deep Research | Deep Research Sub-Topic |
|---------|----------------|---------------|------------------------|
| Research Depth | Basic | Advanced | Advanced |
| Structure | Linear | Hierarchical | Structured Subtopics |
| Breadth | Limited | Extensive | Extensive |
| Organization | Simple | Complex | Well-organized |
| Citation Tracking | Basic | Advanced | Advanced |
| Content Uniqueness | N/A | N/A | Enforced |

## Best Practices

1. **Start with Broad Queries**: Begin with general topics and let the system explore specifics
2. **Monitor Progress**: Use verbose mode to understand the research flow
3. **Adjust Parameters**: Tune breadth and depth based on your needs:
   - More breadth = wider coverage
   - More depth = deeper insights
4. **Resource Management**: Consider concurrency limits based on your system capabilities

## Limitations

- Higher API usage and costs due to multiple concurrent queries
- Longer processing time compared to standard reports
- May require more system resources for parallel processing
- Best suited for complex topics requiring comprehensive analysis

## Use Cases

- **Academic Research**: Comprehensive literature reviews and analysis
- **Market Research**: Deep competitive analysis and industry insights
- **Technical Documentation**: In-depth technical exploration and synthesis
- **Policy Analysis**: Multi-faceted policy research and recommendations
- **Scientific Review**: Comprehensive scientific literature analysis

## Troubleshooting

### Common Issues

1. **High Costs**: Reduce `deep_research_breadth` and `deep_research_depth`
2. **Long Processing Time**: Lower concurrency settings
3. **Memory Issues**: Reduce total word count and research parameters
4. **API Rate Limits**: Lower concurrency and add delays between requests

### Performance Optimization

- Use appropriate concurrency settings for your system
- Monitor API usage and costs
- Adjust research parameters based on topic complexity
- Consider using cached results for repeated queries

## Contributing

To contribute to the Deep Research Sub-Topic Report feature:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

## Support

For questions and support regarding the Deep Research Sub-Topic Report:

- Check the main project documentation
- Review the example scripts
- Open an issue on GitHub
- Join the community discussions

---

**Happy researching! 🎉**

The Deep Research Sub-Topic Research Report represents a significant advancement in AI-powered research capabilities, combining the best of deep research methodology with structured report generation for comprehensive, well-organized research outputs. 