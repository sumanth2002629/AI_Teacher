import torch
from transformers import AutoModelForSpeechSeq2Seq, AutoProcessor, pipeline
import text_to_pdf as text_to_pdf


def aud_to_text(aud_file):
    device = "cuda:0" if torch.cuda.is_available() else "cpu"
    torch_dtype = torch.float16 if torch.cuda.is_available() else torch.float32

    model_id = "openai/whisper-small"

    model = AutoModelForSpeechSeq2Seq.from_pretrained(
        model_id, torch_dtype=torch_dtype, low_cpu_mem_usage=True, use_safetensors=True
    )
    model.to(device)

    processor = AutoProcessor.from_pretrained(model_id)

    pipe = pipeline(
        "automatic-speech-recognition",
        model=model,
        tokenizer=processor.tokenizer,
        feature_extractor=processor.feature_extractor,
        max_new_tokens=128,
        chunk_length_s=30,
        batch_size=16,
        return_timestamps=True,
        torch_dtype=torch_dtype,
        device=device,
    )

    # dataset = load_dataset("distil-whisper/librispeech_long", "clean", split="validation")
    # sample = dataset[0]["audio"]

    result = pipe(aud_file, generate_kwargs={"language": "english"})
    return result
# print(result)
def whispertxt_to_pdf(whistxt,file_name): 
    final_text = ""

    for sentence in whistxt["chunks"]:
        start = sentence["timestamp"][0]
        end = sentence["timestamp"][1]

        text = sentence["text"]

        final_text += "start: "+str(start)+" "+"end: "+str(end)+" "+text+"\n \n"

    sentences = final_text.split("\n")

    text_to_pdf.write_list_to_pdf(file_name,sentences)
    # return final_text

if __name__=="__main__":
    text = aud_to_text("Cosmos.mp3")
    print(whispertxt_to_pdf(text,"files/transcript.pdf"))




