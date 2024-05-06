from dotenv import load_dotenv
import os
import requests
import streamlit as st
import json

# Load API secrets
load_dotenv()
CLOUDFLARE_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN= os.environ.get("CF_API_TOKEN")

def gen_poem(model, name, q2, q3, q4, q5):
    prompt = f"Return only a poem for mother's day for {name} somehow relating to {q2}, {q3}, {q4}, {q5}. Return nothing else."
    print(f'prompt {prompt}')
    payload = {
        "max_tokens": 2000,
        "prompt": prompt,
        "raw": False,
        "stream": False
    }
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}"
    }
    url =f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/{model}"
    response = requests.request("POST", url, json=payload, headers=headers)
    parsed_data = json.loads(response.text)
    print(f'parsed_data {parsed_data}')
    result2 = parsed_data['result']['response']
    print(f'result2 {result2}')
    return parsed_data

# Set up Streamlit app
def main():
    st.markdown("""
        <style>
            .big-font {
                font-size:40px !important;
                color:green;
            }
        </style>
    """, unsafe_allow_html=True)
    st.markdown('<p class="big-font"<p>Mother\'s Day Poem and Gift Generator🎁💐</p>', unsafe_allow_html=True)
    st.write(":blue[This Python🐍 web🕸️ app is built👩🏻‍💻 w/ [Streamlit](https://streamlit.io/) && [Cloudflare Workers AI](https://ai.cloudflare.com/)]")
    name = st.text_input(":red[What is your mom\'s name?]")
    q2 = st.multiselect(
        ':green[Your mom\'s ideal vacation spot is]',
        ['Hawaii🏝️', 'Tahoe', 'Paris', 'Tokyo'],
        ['Hawaii🏝️'])
    q2 = str(q2)
    st.markdown("![do it meme](https://media1.giphy.com/media/3o84sw9CmwYpAnRRni/giphy.gif)")
    warm_labels = ["popcorn", "piping hot ramen", "Anakin burning on Geonosis"]
    q3 = st.select_slider(':orange[On a scale from popcorn to Anakin burning on Geonosis, how warm🔥 does your mom make you feel?]', options=warm_labels)

    q4 = st.text_input(":pink[Describe your mom✌️🥰]")
    sal_labels = ["har gow", "shiu mai", "potsticker🥟", ]
    q5 = st.select_slider(":orange[On a scale from R2-D2😇 to Jar Jar sans-clothes🔥, how cute should the poem be😘?]", options= sal_labels)
    # All models at https://developers.cloudflare.com/workers-ai/models/
    img_model = st.selectbox(
    "Choose your character😘 (Text-To-Image model):",
        options=(
            "@cf/lykon/dreamshaper-8-lcm",
            "@cf/bytedance/stable-diffusion-xl-lightning",
            "@cf/stabilityai/stable-diffusion-xl-base-1.0",
        ),
    )
    text_model = st.selectbox(
        "Choose your flower🌸 (Text generation model):",
        options= (
            "@cf/meta/llama-2-7b-chat-fp16",
            "@cf/meta/llama-2-7b-chat-int8",
            "@cf/meta/llama-3-8b-instruct",
            "@cf/mistral/mistral-7b-instruct-v0.2-lora"
        )
    )
    # url =f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/{text_model}"
    url =f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/{text_model}"
    if name is not None and q2 is not None and q3 is not None and q4 is not None and st.button('Generate🤖'):
        # load dataset once on page load/on server start
        with st.spinner('Processing📈...'):
            img_prompt = f"You are a world-renowned painter of matronly art. Generate a cute, airy, light image without any people in it relating to {q4} and {q2}"
            #img_prompt = f"Generate a seductive image of Jar Jar Binks"
            img_url =f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/{img_model}"
            headers = {
                "Authorization": f"Bearer {CLOUDFLARE_API_TOKEN}",
            }
            resp = requests.post(
                img_url,
                headers=headers,
                json={"prompt": img_prompt},
            )
            st.image(resp.content, caption=f"AI-generated image from {img_model}") #bytes lmao
            story = gen_poem(text_model, name, q2, q3, q4, q5)['result']['response']
            
            html_str = f"""
            <p style="font-family:Comic Sans; color:Pink; font-size: 18px;">{story}</p>
            """
            st.markdown(html_str, unsafe_allow_html=True)
    st.write("Made w/ ❤️ in Hawaii 🏝️🌺, Portland ☔️🌳, && SF🌁")
    st.write("✅ out the [code on GitHub](https://github.com/elizabethsiegle/scifi-fanfic-generator-streamlit-cf/tree/mothersday)")


if __name__ == "__main__":
    main()