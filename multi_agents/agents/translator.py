from .utils.views import print_agent_output
from .utils.llms import call_model


class TranslatorAgent:
    """Agent responsible for translating research reports into Indonesian language."""

    def __init__(self, websocket=None, stream_output=None, headers=None):
        self.websocket = websocket
        self.stream_output = stream_output
        self.headers = headers or {}

    async def translate_report(self, research_state: dict) -> dict:
        """
        Translate the final research report into Indonesian language.

        :param research_state: Dictionary containing the complete research report
        :return: Dictionary with translated report components
        """
        task = research_state.get("task")
        model = task.get("model")
        
        if self.websocket and self.stream_output:
            await self.stream_output("logs", "translating", "Translating research report to Indonesian...", self.websocket)
        else:
            print_agent_output("Translating research report to Indonesian...", agent="TRANSLATOR")

        # Translate each component of the report
        translated_components = {}
        
        # Translate title
        if research_state.get("title"):
            translated_components["title"] = await self._translate_text(
                research_state.get("title"), model, "title"
            )
        
        # Translate introduction
        if research_state.get("introduction"):
            translated_components["introduction"] = await self._translate_text(
                research_state.get("introduction"), model, "introduction"
            )
        
        # Translate conclusion
        if research_state.get("conclusion"):
            translated_components["conclusion"] = await self._translate_text(
                research_state.get("conclusion"), model, "conclusion"
            )
        
        # Translate table of contents
        if research_state.get("table_of_contents"):
            translated_components["table_of_contents"] = await self._translate_text(
                research_state.get("table_of_contents"), model, "table of contents"
            )
        
        # Translate research data sections
        if research_state.get("research_data"):
            translated_components["research_data"] = await self._translate_research_data(
                research_state.get("research_data"), model
            )
        
        # Translate headers
        if research_state.get("headers"):
            translated_components["headers"] = await self._translate_headers(
                research_state.get("headers"), model
            )

        return translated_components

    async def _translate_text(self, text: str, model: str, component_name: str) -> str:
        """
        Translate a single text component to Indonesian.

        :param text: Text to translate
        :param model: Model to use for translation
        :param component_name: Name of the component being translated
        :return: Translated text
        """
        prompt = [
            {
                "role": "system",
                "content": "You are a professional translator specializing in academic and research content. "
                           "Your task is to translate research content from English to Indonesian while "
                           "maintaining academic tone, preserving technical terms appropriately, "
                           "and keeping the original formatting and structure intact."
            },
            {
                "role": "user",
                "content": f"Please translate the following {component_name} to Indonesian. "
                           f"Maintain the original formatting, markdown syntax, and hyperlinks. "
                           f"Keep technical terms in English if there's no suitable Indonesian equivalent. "
                           f"Here's the text to translate:\n\n{text}"
            }
        ]

        try:
            translated_text = await call_model(prompt=prompt, model=model)
            return translated_text
        except Exception as e:
            print_agent_output(f"Error translating {component_name}: {e}", agent="TRANSLATOR")
            return text  # Return original text if translation fails

    async def _translate_research_data(self, research_data: list, model: str) -> list:
        """
        Translate research data sections to Indonesian.

        :param research_data: List of research data sections
        :param model: Model to use for translation
        :return: List of translated research data sections
        """
        translated_data = []
        
        for i, section in enumerate(research_data):
            if isinstance(section, dict):
                # Handle dictionary case
                translated_section = {}
                for key, value in section.items():
                    if isinstance(value, str):
                        translated_section[key] = await self._translate_text(
                            value, model, f"research section {i+1}"
                        )
                    else:
                        translated_section[key] = value
                translated_data.append(translated_section)
            else:
                # Handle string case
                translated_data.append(await self._translate_text(
                    str(section), model, f"research section {i+1}"
                ))
        
        return translated_data

    async def _translate_headers(self, headers: dict, model: str) -> dict:
        """
        Translate header labels to Indonesian.

        :param headers: Dictionary of header labels
        :param model: Model to use for translation
        :return: Dictionary of translated header labels
        """
        translated_headers = {}
        
        for key, value in headers.items():
            if isinstance(value, str):
                translated_headers[key] = await self._translate_text(
                    value, model, f"header '{key}'"
                )
            else:
                translated_headers[key] = value
        
        return translated_headers

    async def run(self, research_state: dict) -> dict:
        """
        Execute the translation process.

        :param research_state: Dictionary containing research state information
        :return: Dictionary with translated report components
        """
        task = research_state.get("task", {})
        translate_enabled = task.get("translate_to_indonesian", False)
        
        if not translate_enabled:
            if self.websocket and self.stream_output:
                await self.stream_output("logs", "translation_skipped", "Translation to Indonesian is disabled, skipping translation step.", self.websocket)
            else:
                print_agent_output("Translation to Indonesian is disabled, skipping translation step.", agent="TRANSLATOR")
            return research_state
        
        translated_components = await self.translate_report(research_state)
        
        # Create a new research state with translated content
        translated_research_state = research_state.copy()
        translated_research_state.update(translated_components)
        
        if self.websocket and self.stream_output:
            await self.stream_output("logs", "translation_complete", "Translation to Indonesian completed successfully!", self.websocket)
        else:
            print_agent_output("Translation to Indonesian completed successfully!", agent="TRANSLATOR")
        
        return translated_research_state 