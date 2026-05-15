# LLM Orchestrator - Natural Language to Workflow Configuration

A prototype demonstrating how LLMs translate natural language instructions into structured workflow operations through intent classification and DSL generation.

## Project Motive

Enterprise workflow systems require complex configuration changes through JSON/XML manipulation. This prototype explores natural language interfaces for workflow configuration using LLM-driven intent classification and structured DSL generation.

**Example**: "Clone Send for Review into Send for Internal Review and Send for External Review" → Validated DSL → Executed transformation → Updated configuration.

## Architecture Rationale

**Two-Phase LLM Pattern**
```
User Input → Intent Classifier → Tool Selection → DSL Generator → Execution
```
- Intent classification is cheaper/faster than full DSL generation
- Each tool has its own prompt engineering and schema
- Adding operations only requires updating the tool registry

**Dynamic Tool Registry**
- Tools self-register on import (plugin architecture)
- Each tool brings its own Pydantic schema
- Extensible: new tool = new file in `/tools`

**DSL as Intermediate Representation**
- Decouples natural language from execution
- Type-safe validation before execution
- Auditable and composable for multi-step operations

**Schema-Driven Prompts**
- Pydantic models define validation rules and LLM output constraints
- Reduces hallucination by constraining valid fields
- Self-documenting through schema injection

## What's Implemented

**Core Components**

1. **Intent Classifier** - Analyzes user intent and routes to appropriate tool
2. **LLM Service** - Generates DSL from natural language with tool-specific prompts
3. **Tool Registry** - Dynamic tool discovery and registration system
4. **DSL Models** - Pydantic schemas for type-safe operations (CloneAction, UpdateActionProperty)
5. **Action Tools** - Executable operations (clone, update) with base class abstraction
6. **Action Utilities** - Pure functions for config transformations

**Data Flow**

```
Natural Language
    ↓
Intent Classifier (LLM)
    ↓
Tool Selection
    ↓
DSL Generator (LLM + Tool Schema)
    ↓
Pydantic Validation
    ↓
Tool Execution
    ↓
Updated Configuration
    ↓
API Payload
```

## Key Learnings

**Structured Output Generation**
- LLMs reliably generate schema-conforming JSON with proper prompting
- Schema definitions + examples + validation = robust pipeline
- Pydantic ensures semantic correctness, not just valid JSON

**Architecture Insights**
- Two-phase approach (classify → generate) more maintainable than single prompt
- Tool abstraction enables easier testing and hot-reloading
- Intermediate DSL provides debugging visibility and composability
- Intent classification needs no fine-tuning, just clear tool descriptions

**Prompt Engineering**
- Explicit field lists prevent hallucination
- Examples improve consistency significantly
- Negative instructions ("don't do X") matter as much as positive ones

**Production Reality**
- Token costs: two LLM calls per operation
- Latency: ~2-3s total for sequential calls
- Type safety via Pydantic is non-negotiable
- Handle edge cases: markdown wrappers, multiple response formats

## Future Extensions

**Core Enhancements**
- Additional operations: delete, reorder, bulk updates
- Multi-step operations with transaction support
- Pre-execution dry-run and diff preview
- Conversation memory for context retention

**System Improvements**
- Async execution with FastAPI and job queues
- Comprehensive testing framework (unit, integration, prompt regression)
- Visual interface with chat UI and real-time preview

**Enterprise Features**
- Fine-tuned models for organization-specific patterns
- Audit logging and role-based access control
- Natural language queries across workflows
- Template library for reusable patterns

## Tech Stack

- **LLM**: OpenAI GPT-4o-mini (intent + DSL generation)
- **Validation**: Pydantic v2 (type-safe schemas)
- **Language**: Python 3.x
- **Architecture Pattern**: Tool Registry + DSL Interpreter

## Usage Example

```bash
$ python main.py
Enter instruction:
> Clone SendforReview into Send for Internal Review and Send for External Review

Classified intent: clone_action
Using tool: clone_action - Create new actions from an existing one

Generated DSL:
{
  "type": "clone_action",
  "sourceAction": "SendforReview",
  "newLabels": ["Send for Internal Review", "Send for External Review"]
}

Final API Payload: [updated configuration with new actions]
```

## What I Learned

**Structured Output Generation**: LLMs become reliable code generators with strict schemas (Pydantic), clear prompts, concrete examples, and aggressive validation.

**LLMs as Components**: Treat them as system components with clear contracts rather than magic boxes. Constraints enable predictability.

**Architecture Matters**: Two-phase approach (classify → generate) is more reliable and debuggable than end-to-end prompting.

**Type Safety is Essential**: Pydantic validation prevents runtime failures and data corruption when LLM outputs drive execution.

**Prompt Engineering is Engineering**: Requires the same rigor as code—testing, iteration, and version control.

---

*Built as an exploration of LLM-driven configuration management and natural language interfaces for enterprise systems.*
