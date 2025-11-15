# agents/workflow.py - AI Agent Workflow System

import os
from typing import TypedDict, Literal
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
import torch
import time

print("🔧 System Check...")
print(f"PyTorch: {torch.__version__}")
print(f"CUDA: {torch.cuda.is_available()}")
if torch.cuda.is_available():
    print(f"GPU: {torch.cuda.get_device_name(0)}")
print()

# ========== STATE DEFINITION ========== #

class WorkflowState(TypedDict, total=False):
    user_instruction: str
    tone: str
    style: str
    iteration: int
    draft_text: str
    reviewed_text: str
    image_prompt: str
    compliance_status: Literal["pending", "approved", "needs_changes"]
    compliance_feedback: str
    revision_notes: str

# ========== OPTIMIZED LLM SETUP ========== #

def make_llm_quantized(model_id: str, use_4bit: bool = True):
    """Create optimized LLM with quantization"""
    from langchain_huggingface import HuggingFacePipeline
    from transformers import (
        AutoModelForCausalLM, 
        AutoTokenizer, 
        pipeline, 
        BitsAndBytesConfig
    )
    
    print(f"🚀 Loading: {model_id}")
    
    # Quantization config
    if use_4bit:
        print("⚡ Applying: 4-bit quantization")
        bnb_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_use_double_quant=True,
            bnb_4bit_quant_type="nf4",
        )
    else:
        print("⚡ Applying: 8-bit quantization")
        bnb_config = BitsAndBytesConfig(
            load_in_8bit=True,
            llm_int8_threshold=6.0,
        )
    
    # Load tokenizer
    tokenizer = AutoTokenizer.from_pretrained(
        model_id,
        use_fast=True,
        padding_side='left',
        trust_remote_code=True
    )
    
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    
    # Load model with optimizations
    model = AutoModelForCausalLM.from_pretrained(
        model_id,
        quantization_config=bnb_config,
        device_map="auto",
        trust_remote_code=True,
        torch_dtype=torch.float16,
    )
    
    # Determine max tokens based on model size
    if "7b" in model_id.lower():
        max_tokens = 400
    elif "phi-2" in model_id.lower():
        max_tokens = 350
    else:
        max_tokens = 300
    
    # Optimized pipeline
    pipe = pipeline(
        "text-generation",
        model=model,
        tokenizer=tokenizer,
        max_new_tokens=max_tokens,
        temperature=0.7,
        do_sample=True,
        top_p=0.9,
        top_k=50,
        repetition_penalty=1.1,
        pad_token_id=tokenizer.pad_token_id,
        eos_token_id=tokenizer.eos_token_id,
        batch_size=1,
    )
    
    # Ensure chat template exists
    if not getattr(tokenizer, "chat_template", None):
        tokenizer.chat_template = "{% for m in messages %}{{ m['role'] }}: {{ m['content'] }}{% endfor %}"
    
    llm = HuggingFacePipeline(pipeline=pipe)
    return llm


# Initialize models globally (lazy loading)
_MODELS_LOADED = False
WRITER_LLM = None
REVIEWER_LLM = None
COMPLIANCE_LLM = None
COORDINATOR_LLM = None

def load_models():
    """Load all models (call this once at startup)"""
    global _MODELS_LOADED, WRITER_LLM, REVIEWER_LLM, COMPLIANCE_LLM, COORDINATOR_LLM
    
    if _MODELS_LOADED:
        return
    
    print("🚀 Loading Specialized Models...")
    print("\n📝 Writer Model (Zephyr-7B)...")
    WRITER_LLM = make_llm_quantized("HuggingFaceH4/zephyr-7b-beta", use_4bit=True)
    
    print("\n🔍 Reviewer Model (Phi-2)...")
    REVIEWER_LLM = make_llm_quantized("microsoft/phi-2", use_4bit=True)
    
    print("\n✅ Compliance Model (Zephyr-7B)...")
    COMPLIANCE_LLM = make_llm_quantized("HuggingFaceH4/zephyr-7b-beta", use_4bit=True)
    
    print("\n🎯 Coordinator Model (Phi-2)...")
    COORDINATOR_LLM = make_llm_quantized("microsoft/phi-2", use_4bit=True)
    
    print("\n✅ All Models Ready!\n")
    _MODELS_LOADED = True


def chat(llm, system_prompt: str, user_prompt: str, max_input_tokens: int = 1500) -> str:
    """Optimized LLM call with strict token limits"""
    combined = f"{system_prompt}\n\n{user_prompt}"
    tokenizer = llm.pipeline.tokenizer
    
    # Truncate input
    tokens = tokenizer.encode(combined, max_length=max_input_tokens, truncation=True)
    combined = tokenizer.decode(tokens, skip_special_tokens=True)
    
    try:
        output = llm.pipeline(
            combined,
            max_new_tokens=300,
            do_sample=True,
            top_p=0.9,
            top_k=50,
            temperature=0.7,
        )
        if isinstance(output, list) and "generated_text" in output[0]:
            return output[0]["generated_text"].strip()
        else:
            return str(output).strip()
    except Exception as e:
        print(f"⚠️  Error: {e}")
        return "[Generation failed]"


# ========== SPECIALIZED AGENTS ========== #

def coordinator_agent(state: WorkflowState) -> dict:
    """Fast coordinator using Phi-2"""
    iteration = state.get("iteration", 0)
    
    if iteration == 0:
        return {"iteration": 1, "revision_notes": ""}
    
    feedback = state.get("compliance_feedback", "")
    prompt = f"Based on this compliance feedback, list 3 key changes needed:\n{feedback}\n\nChanges:"
    revision_notes = chat(COORDINATOR_LLM, "You create concise revision lists.", prompt)
    
    return {
        "iteration": iteration + 1,
        "revision_notes": revision_notes,
    }


def text_generator_agent(state: WorkflowState) -> dict:
    """Generate text using Zephyr-7B (best writer)"""
    sys = "You are an expert social media copywriter. Create engaging, creative, and compelling social media content."
    
    revisions = state.get('revision_notes', '')
    prompt = f"""Create an Instagram post:
Product: {state.get("user_instruction", "")}
Tone: {state.get("tone", "")}
Style: {state.get("style", "")}
{f'Apply these revisions: {revisions}' if revisions else ''}

Write the caption:"""
    
    draft = chat(WRITER_LLM, sys, prompt, max_input_tokens=2000)
    return {"draft_text": draft}


def reviewer_agent(state: WorkflowState) -> dict:
    """Review and polish using Phi-2"""
    sys = "You are an expert editor. Review and improve the text for grammar, clarity, and engagement. Output only the edited text."
    prompt = f"Edit and improve this social media caption:\n\n{state.get('draft_text', '')}\n\nEdited version:"
    
    refined = chat(REVIEWER_LLM, sys, prompt, max_input_tokens=1800)
    return {"reviewed_text": refined}


def image_generator_agent(state: WorkflowState) -> dict:
    """Generate image prompt using Zephyr-7B"""
    sys = "You are an expert at creating detailed, vivid image prompts for AI image generation."
    prompt = f"""Create a detailed image generation prompt for this social media post:

{state.get('reviewed_text', '')}

Image prompt:"""
    
    img_prompt = chat(WRITER_LLM, sys, prompt, max_input_tokens=1500)
    return {"image_prompt": img_prompt}


def compliance_agent(state: WorkflowState) -> dict:
    """Compliance check using Zephyr-7B"""
    sys = """You are a content compliance officer. Check content for:
- Inappropriate language
- False claims
- Harmful content
- Brand safety issues

Reply with either:
- "APPROVED" if content is safe
- "NEEDS_CHANGES: [specific reason]" if issues found"""
    
    text = state.get('reviewed_text', '')
    img = state.get('image_prompt', '')
    
    prompt = f"""Review this content for compliance:

TEXT:
{text}

IMAGE PROMPT:
{img}

Decision:"""
    
    raw = chat(COMPLIANCE_LLM, sys, prompt, max_input_tokens=2000)
    
    lower = raw.lower()
    if "approved" in lower and "needs" not in lower:
        return {
            "compliance_status": "approved",
            "compliance_feedback": "Content approved"
        }
    else:
        return {
            "compliance_status": "needs_changes",
            "compliance_feedback": raw
        }


# ========== GRAPH SETUP ========== #

def should_continue(state: WorkflowState) -> Literal["coordinator", "end"]:
    """Stop after approval or max iterations"""
    iteration = state.get("iteration", 0)
    status = state.get("compliance_status", "pending")
    
    if status == "approved" or iteration >= 3:
        return "end"
    return "coordinator"


# Build the workflow graph
def build_workflow():
    """Build and return the workflow graph"""
    graph = StateGraph(WorkflowState)
    
    # Add nodes
    graph.add_node("coordinator", coordinator_agent)
    graph.add_node("text_generator", text_generator_agent)
    graph.add_node("reviewer", reviewer_agent)
    graph.add_node("image_generator", image_generator_agent)
    graph.add_node("compliance", compliance_agent)
    
    # Flow
    graph.set_entry_point("coordinator")
    graph.add_edge("coordinator", "text_generator")
    graph.add_edge("text_generator", "reviewer")
    graph.add_edge("reviewer", "image_generator")
    graph.add_edge("image_generator", "compliance")
    graph.add_conditional_edges("compliance", should_continue, 
                               {"coordinator": "coordinator", "end": END})
    
    memory = MemorySaver()
    return graph.compile(checkpointer=memory)


# Global workflow instance
_workflow = None

def get_workflow():
    """Get or create the workflow"""
    global _workflow
    if _workflow is None:
        _workflow = build_workflow()
    return _workflow


def generate_content(user_instruction: str, tone: str, style: str) -> dict:
    """
    Main function to generate social media content
    
    Args:
        user_instruction: Description of the product/campaign
        tone: Desired tone (e.g., "fun, friendly, eco-conscious")
        style: Desired style (e.g., "short caption with 3-4 hashtags")
    
    Returns:
        dict with keys: reviewed_text, image_prompt, compliance_status, iteration, elapsed_time
    """
    # Ensure models are loaded
    if not _MODELS_LOADED:
        load_models()
    
    initial_state: WorkflowState = {
        "user_instruction": user_instruction,
        "tone": tone,
        "style": style,
        "iteration": 0,
    }
    
    start = time.time()
    workflow = get_workflow()
    
    final_state = workflow.invoke(
        initial_state,
        config={"configurable": {"thread_id": f"thread-{int(time.time())}"}}
    )
    
    elapsed = time.time() - start
    
    return {
        "reviewed_text": final_state.get("reviewed_text", ""),
        "image_prompt": final_state.get("image_prompt", ""),
        "compliance_status": final_state.get("compliance_status", "pending"),
        "compliance_feedback": final_state.get("compliance_feedback", ""),
        "iteration": final_state.get("iteration", 0),
        "elapsed_time": round(elapsed, 2)
    }
