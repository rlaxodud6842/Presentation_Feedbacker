from transformers import AutoModelForCausalLM, AutoTokenizer

class Qwen:
    def __init__(self) -> None:
        self.model_name = "Qwen/Qwen2.5-3B-Instruct"

        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_name,
            torch_dtype="auto",
            device_map="auto"
        )
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        
    def make_text(self,script) -> str:
        prompt = ("다음은 내 발표를 텍스트로 만든거야. 내 발표에서 어떤 부분이 조금 부족한지 5개만 집어서 말해줘")
        messages = [
            {"role": "system", "content": "You are a professional presenter who specializes in providing constructive feedback on presentation scripts."},
            {"role": "user", "content": prompt + script}
        ]
        text = self.tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=1024 #모델이 뱉어내는 최대 토큰
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response