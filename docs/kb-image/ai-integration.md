# kb-image AI Integration & Prompts

`kb-image` leverages local multimodal large language models (LLMs) to scan, describe, and index images.

---

## Ollama Connection

- **Endpoint**: The system looks for an Ollama server running at `http://192.168.0.25:11414` by default. This value can be modified in `kb_image/config.py` or overridden via environment configuration.
- **Model**: Default vision model is `llava` (or another specified multimodal model).

---

## AI Pipeline Steps

### 1. Image Description
The model is fed the base64-encoded image along with a prompt requesting a detailed, objective description of what is depicted.
- **System Prompt**:
  > *"You are an AI assistant that describes images. Provide a thorough, detailed, and objective description of this image. Focus on the main subjects, action, setting, colors, text visible, and layout. Avoid subjective interpretations."*

### 2. Semantic Tag Generation
Once the description is generated, a separate prompt uses Ollama to extract single-word semantic tags based on the generated description.
- **Tagger Prompt**:
  > *"Generate a list of 5-10 single-word keywords or tags that represent the content described here: [Description]. Respond ONLY with a comma-separated list of lowercase words."*
- **Database Storage**: The resulting tags are split, cleaned, and stored in the database's `tags` column as a JSON array.
