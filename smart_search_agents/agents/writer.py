from typing import Dict, Any, Optional, List
import os
import json
from .utils.views import print_agent_output
from .utils.llms import call_model
from .utils.file_formats import write_text_to_md, write_md_to_pdf, write_md_to_word
from .utils.utils import sanitize_filename


class WriterAgent:
    def __init__(self, websocket=None, stream_output=None, tone=None, headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.tone = tone
        self.headers = headers or {}

    async def process(self, state: Dict[str, Any]) -> Dict[str, Any]:
        """Process the research results and generate a comprehensive report following guidelines"""
        
        research_report = state.get("research_report", "")
        pre_agent_output = state.get("pre_agent_output", {})
        task = state.get("task", {})
        task_id = state.get("task_id", None)
        custom_report_prompt = pre_agent_output.get("custom_report_prompt", "default_report")
        
        if self.websocket and self.stream_output:
            await self.stream_output("logs", "writer_agent", "Starting report writing based on research", self.websocket)
        else:
            print_agent_output("Starting report writing based on research", agent="WRITER_AGENT")
        
        # Extract task parameters
        query = task.get("query", "")
        guidelines = task.get("guidelines", [])
        publish_formats = task.get("publish_formats", {"markdown": True})
        model = task.get("model", "gpt-4o")
        
        # Generate the final report following guidelines and custom format
        final_report = await self._generate_final_report(
            research_report, query, guidelines, model, custom_report_prompt
        )
        
        # Generate output files based on publish_formats
        output_files = await self._generate_output_files(final_report, publish_formats, task_id)
        
        writer_output = {
            "report_generated": True,
            "guidelines_followed": True,
            "output_files": output_files,
            "sources_included": True
        }
        
        if self.websocket and self.stream_output:
            await self.stream_output("logs", "writer_agent", "Report writing completed", self.websocket)
        else:
            print_agent_output("Report writing completed", agent="WRITER_AGENT")
        
        # Update state with writer output and final report
        state["writer_agent_output"] = writer_output
        state["final_report"] = final_report
        
        return state

    async def _generate_final_report(
        self, 
        research_report: str, 
        query: str, 
        guidelines: List[str], 
        model: str,
        custom_report_prompt: str
    ) -> str:
        """Generate the final report following the specified guidelines and custom format"""
        
        # Create the prompt for the writer agent
        prompt = self._create_writer_prompt(research_report, query, guidelines, custom_report_prompt)
        print("Writer prompt: ", prompt)
        
        try:
            # Call the model to generate the final report
            final_report = await call_model(prompt, model)
            return final_report
            
        except Exception as e:
            error_msg = f"Error generating final report: {str(e)}"
            if self.websocket and self.stream_output:
                await self.stream_output("logs", "error", error_msg, self.websocket)
            else:
                print_agent_output(error_msg, agent="WRITER_AGENT")
            return research_report  # Fallback to original report

    def _create_writer_prompt(
        self, 
        research_report: str, 
        query: str, 
        guidelines: List[str],
        custom_report_prompt: str
    ) -> List[Dict[str, str]]:
        """Create the prompt for the writer agent with custom format instructions"""
        
        guidelines_text = "\n".join([f"- {guideline}" for guideline in guidelines])
        
        # Get format-specific instructions based on the custom report prompt from pre-agent
        format_instructions = self._get_format_instructions(custom_report_prompt, query)
        
        prompt = [
            {
                "role": "system",
                "content": f"""You are an expert research report writer. Your task is to reformat an existing research report into a specific format structure.

IMPORTANT GUIDELINES:
{guidelines_text}

FORMAT INSTRUCTIONS:
{format_instructions}

SPECIFIC INSTRUCTIONS:
1. Maintain all original content and sources from the research report
2. Only reorganize and reformat the content to match the specified format structure
3. Keep all existing hyperlinks and citations intact
4. Preserve the accuracy and reliability of the information
5. Write in the language specified in the guidelines (if any)"""
            },
            {
                "role": "user",
                "content": f"""RESEARCH QUESTION: {query}

EXISTING RESEARCH REPORT:
{research_report}

Please reformat the above research report according to the specified format structure while preserving all content and sources."""
            }
        ]
        
        return prompt

    def _get_format_instructions(self, format_type: str, query: str) -> str:
        """Get format-specific instructions based on the report type"""
        
        format_instructions = {
            "comparison": f"""Present the information as a comparison format:
- Create a comparison table or structured comparison
- Compare different options, products, or approaches related to: {query}
- Use clear headings and bullet points for easy comparison
- Include pros and cons for each option
- Provide a recommendation based on the comparison""",
            
            "qna": f"""Present the information as a Q&A format:
- Structure the response as questions and answers
- Break down the query into specific questions
- Provide clear, direct answers to each question
- Use numbered questions and detailed answers
- Include relevant sources for each answer""",
            
            "step_by_step": f"""Present the information as a step-by-step guide:
- Break down the process into clear, numbered steps
- Provide detailed instructions for each step
- Include tips, warnings, or important notes where relevant
- Use a logical progression from start to finish
- Include any prerequisites or requirements""",
            
            "itinerary": f"""Present the information as a detailed itinerary:
- Create a day-by-day or hour-by-hour schedule
- Include specific times, locations, and activities
- Provide practical details like transportation, costs, and tips
- Include alternative options or backup plans
- Add relevant information about each location or activity""",
            
            "default_report": f"""Present the information as a comprehensive research report:
- Use a standard report structure with introduction, main content, and conclusion
- Organize information logically with clear sections
- Include relevant data, statistics, and supporting evidence
- Provide a balanced view with multiple perspectives
- End with a summary or key takeaways"""
        }
        
        return format_instructions.get(format_type, format_instructions["default_report"])

    async def _generate_output_files(self, final_report: str, publish_formats: Dict[str, bool], task_id: Optional[str] = None) -> Dict[str, str]:
        """Generate output files based on the specified formats"""
        
        output_files = {}
        
        # Create output directory
        output_dir = "outputs/"
        if task_id:
            output_dir = f"outputs/run_{task_id}_{self.task.get('query')[0:40]}"

        os.makedirs(output_dir, exist_ok=True)
        
        # Generate files based on publish_formats
        if publish_formats.get("markdown", False):
            try:
                md_path = await write_text_to_md(final_report, output_dir)
                output_files["markdown"] = md_path
            except Exception as e:
                print_agent_output(f"Error generating markdown: {str(e)}", agent="WRITER_AGENT")
        
        if publish_formats.get("pdf", False):
            try:
                pdf_path = await write_md_to_pdf(final_report, output_dir)
                if pdf_path:
                    output_files["pdf"] = pdf_path
            except Exception as e:
                print_agent_output(f"Error generating PDF: {str(e)}", agent="WRITER_AGENT")
        
        if publish_formats.get("docx", False):
            try:
                docx_path = await write_md_to_word(final_report, output_dir)
                if docx_path:
                    output_files["docx"] = docx_path
            except Exception as e:
                print_agent_output(f"Error generating DOCX: {str(e)}", agent="WRITER_AGENT")
        
        return output_files
