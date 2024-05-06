from dotenv import load_dotenv
import os
import requests
import streamlit as st
import json

# Load API secrets
load_dotenv()
CLOUDFLARE_ACCOUNT_ID = os.environ.get("CF_ACCOUNT_ID")
CLOUDFLARE_API_TOKEN= os.environ.get("CF_API_TOKEN")

def gen_story(model, q1, q2, q3, q4, q5, sal_met):
    prompt = f"Return only a humorous science-fiction story somehow relating to {q1}, {q2}, {q3}, {q4}, {q5}. Return nothing else. The story should be rated {sal_met} have an introduction paragraph, a villain and conflict, and a conclusion paragraph"
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
    st.markdown('<p class="big-font"<p>Scifi fanfic generator⭐️🔫📝🤖</p>', unsafe_allow_html=True)
    st.write(":blue[This Python🐍 web🕸️ app is built👩🏻‍💻 w/ [Streamlit](https://streamlit.io/), [Cloudflare Workers AI](https://ai.cloudflare.com/)]")
    q1 = st.text_input(":red[Who is your favorite Star Wars⭐️🔫 character?]")
    q2 = st.multiselect(
        ':green[Your ideal vacation spot is]',
        ['grasslands🦁', 'mountains⛰️', 'tropical🏝️', 'jungle🌲', 'rainforests💧', 'cityscape🌆', 'caves', 'lakes🚤', 'ice canyons', 'urban🏢', 'swamp👹', 'reefs🐟', 'plains', 'volcanoes🌋', 'arid🌵', 'tundra🥶'],
        ['ice canyons', 'swamp👹', 'cityscape🌆'])
    q2 = str(q2)
    st.markdown("![do it meme](https://media1.giphy.com/media/3o84sw9CmwYpAnRRni/giphy.gif)")
    char_labels = ["Jabba the Hutt", "Admiral Ackbar", "Jar Jar Binks", "Count Dooku", "Obi-wan Kenobi", "Poe Dameron"]
    q3 = st.select_slider(':orange[On a scale from Jabba the Hutt to Poe Dameron, how 🔥 is the villain✈️ of your fanfic?]', options=char_labels)

    q4 = st.text_input(":yellow[Describe a starship⭐️🚀 to drive🚗]")
    q5 = st.text_input(":pink[Describe u✌️🥰]")
    sal_labels = ["R2D2--like the innocent astromech droid, suitable for all", "Chewbacca moaning--could go over young heads", "so uncivilized! May be inappropriate for species < 13", "Jar Jar || Jabba sans-clothes--may contain content !suitable for < 17 w/o parental consent"]
    salaciousness_met = st.select_slider(":orange[On a scale from R2-D2😇 to Jar Jar sans-clothes🔥, how salacious🥵 should the fanfic be😘?]", options= sal_labels)

    st.markdown("![screaming r2d2 gif](https://assets.teenvogue.com/photos/572a3302321c4faf6ae8a317/16:9/w_2580,c_limit/R2SCREAM.gif)") #screaming r2

    # All models at https://developers.cloudflare.com/workers-ai/models/
    img_model = st.selectbox(
    "Choose your character (Text-To-Image model):",
        options=(
            "@cf/lykon/dreamshaper-8-lcm",
            "@cf/bytedance/stable-diffusion-xl-lightning",
            "@cf/stabilityai/stable-diffusion-xl-base-1.0",
        ),
    )
    text_model = st.selectbox(
        "Choose your weapon (Text generation model):",
        options= (
            # "@cf/meta/llama-2-7b-chat-fp16",
            "@cf/meta/llama-2-7b-chat-int8",
            "@cf/meta/llama-3-8b-instruct",
            "@cf/mistral/mistral-7b-instruct-v0.2-lora"
        )
    )
    # url =f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/{text_model}"
    url =f"https://api.cloudflare.com/client/v4/accounts/{CLOUDFLARE_ACCOUNT_ID}/ai/run/{text_model}"
    if q1 is not None and q2 is not None and q3 is not None and q4 is not None and q5 is not None and salaciousness_met is not None and st.button('Generate🤖'):
        # load dataset once on page load/on server start
        with st.spinner('Processing📈...'):
            st.markdown("![i will finish what you started gif](https://y.yarn.co/2f4fabe4-6046-4bbd-96bd-3a3ccf9853c9_text.gif)")
            
            img_prompt = f"You are a world-renowned painter of lighthearted sci-fi art. Generate a humorous image relating to {q1} and {q2}"
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
            story = gen_story(text_model, q1, q2, q3, q4, q5, salaciousness_met)['result']['response']
            
            html_str = f"""
            <p style="font-family:Comic Sans; color:Pink; font-size: 18px;">{story}</p>
            """
            st.markdown(html_str, unsafe_allow_html=True)
    st.write("Made w/ ❤️ in Hawaii 🏝️🌺 && Portland ☔️🌳")
    st.write("✅ out the [code on GitHub](https://github.com/elizabethsiegle/star-wars-fanfic-generator-streamlit-astra-cf)")


if __name__ == "__main__":
    main()