from groq import Groq
import json

client = Groq(api_key="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")

prompt_berita = "presiden halimah di tolak warga etnis china sultan brunei ancam beli singapura."

completion = client.chat.completions.create(
    model="groq/compound",
    messages=[
        {
            "role": "system",
            "content": (
                "Kamu adalah asisten pencari bukti berita. "
                "Diberikan sebuah klaim/berita, buatkan JSON array berisi 10 objek. "
                "Setiap objek wajib memiliki: "
                "judul (string), tanggal (string, format YYYY-MM-DD jika ada), "
                "author (string, bisa 'Unknown' jika tidak ada), "
                "sumber (string, nama media), "
                "dan link (string, URL valid). "
                "content (string semua isi websitenya), "
                "Pastikan output valid JSON, tanpa tambahan teks lain."
            )
        },
        {
            "role": "user",
            "content": prompt_berita
        }
    ],
    temperature=0,
    max_completion_tokens=1500,
    top_p=1,
    stream=False
)

# Ambil hasil
result_text = completion.choices[0].message.content

# Coba parse JSON
try:
    data = json.loads(result_text)
    print(json.dumps(data, indent=2, ensure_ascii=False))
except json.JSONDecodeError:
    print("Output bukan JSON valid:\n", result_text)
