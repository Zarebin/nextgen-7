# from transformers import AutoTokenizer, XLMRobertaModel
# import torch
#
# tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
# model = XLMRobertaModel.from_pretrained("xlm-roberta-base")
#
# inputs = tokenizer("Hello, my dog is cute", return_tensors="pt")
# outputs = model(**inputs)
#
# last_hidden_states = outputs.last_hidden_state
#
# print(last_hidden_states)
# see https://huggingface.co/docs/transformers/model_doc/xlm-roberta#transformers.XLMRobertaForTokenClassification


from transformers import AutoTokenizer, XLMRobertaModel
import torch
from torch import nn


class OgDescriptionDetector(nn.Module):
    def __init__(self):
        super().__init__()
        self.tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base")
        self.lm_model = XLMRobertaModel.from_pretrained("xlm-roberta-base")

        self.start_ff = nn.Linear(self.lm_model.config.hidden_size, 1)
        self.end_ff = nn.Linear(self.lm_model.config.hidden_size, 1)

    def forward(self, text):
        with torch.no_grad():
            lm_inputs = self.tokenizer(text, return_tensors="pt", add_special_tokens=False, padding='longest')
            embeddings = self.lm_model(**lm_inputs).last_hidden_state
            linear_input = embeddings.detach()
        # linear_input shape is (batch, longest_seq, model_hidden_size)
        b, s, h = linear_input.shape

        linear_input = linear_input.reshape(b * s, h)

        start_probs = self.start_ff(linear_input)
        end_probs = self.end_ff(linear_input)

        start_probs.reshape(b, s, 1)
        end_probs.reshape(b, s, 1)

        return start_probs, end_probs
