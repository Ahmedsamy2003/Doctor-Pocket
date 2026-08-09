"""
Doctor Pocket inference service.

Handles converting a user's question into a response
using the loaded Doctor Pocket model.
"""

import torch

from app.models.model_loader import (
    DOCTOR_POCKET_SYSTEM_PROMPT,
    get_model_and_tokenizer,
)


def generate_answer(
    question: str,
    max_new_tokens: int = 256,
) -> str:
    """
    Generate a Doctor Pocket response for a user's question.
    """

    model, tokenizer = get_model_and_tokenizer()

    messages = [
        {
            "role": "system",
            "content": DOCTOR_POCKET_SYSTEM_PROMPT,
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    # Use Qwen's chat template
    prompt = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True,
    )

    # Tokenize
    inputs = tokenizer(
        prompt,
        return_tensors="pt",
    )

    # Move inputs to the same device as the model
    inputs = {
        key: value.to(model.device)
        for key, value in inputs.items()
    }

    # Generate
    with torch.no_grad():

        output_ids = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.1,
            pad_token_id=tokenizer.pad_token_id,
        )

    # Remove the original prompt from the generated tokens
    generated_tokens = output_ids[
        0
    ][
        inputs["input_ids"].shape[1]:
    ]

    # Convert tokens back into text
    answer = tokenizer.decode(
        generated_tokens,
        skip_special_tokens=True,
    ).strip()

    return answer