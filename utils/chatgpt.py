from config import OPENAPI_TOKEN
import aiohttp
import random


prompt_templates = [
    'Сгенерируй не банальное текстовое описание {symbols_count} символов для товара на маркетплейсе {name}, обязательно используй в тексте слова: "{keys}" не меняя порядок слов',
    'Напиши продающее текстовое описание на {symbols_count} символов символов для товара на маркетплейсе {name}, обязательно используй в тексте слова: "{keys}" не меняя порядок слов',
    'Придумай лучшее описание на {symbols_count} символов для товара на маркетплейсе {name}, обязательно используй в тексте слова: "{keys}" не меняя порядок слов']


async def gen_text(text_data):
    prompt = random.choice(prompt_templates).format(symbols_count=text_data["symbols_count"],
                                                    name=text_data["name"],
                                                    keys=text_data["keys"])
    async with aiohttp.ClientSession() as session:
        async with session.post('https://api.openai.com/v1/completions',
                                headers={'Authorization': f'Bearer {OPENAPI_TOKEN}',
                                         'Content-Type': 'application/json'},
                                json={'model': 'text-davinci-003',
                                      "prompt": prompt,
                                      "max_tokens": 1024,
                                      "temperature": 0.5,
                                      "top_p": 1,
                                      "frequency_penalty": 0,
                                      "presence_penalty": 0
                                      }) as resp:
            response = await resp.json()
            return response["choices"][0]["text"]
