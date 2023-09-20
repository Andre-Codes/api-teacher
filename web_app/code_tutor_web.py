import gpt_service_web as gpt
import streamlit as st


st.set_page_config(page_title="💻👨‍🏫 Code Tutor - Learn Code")

# initalize the class with role context
ct = gpt.CodeTutor(
    role_context = "code_help", 
    explain_level = 'concise', 
    comment_level = 'normal'
)

def generate_response(prompt, only_code):
    with st.spinner('Forming an answer ...'):
        return ct.get_response(
            prompt = prompt, 
            only_code = only_code, 
            format_style = format_style
        )

def display_content(content, custom_header=None):
    # ct.complete_prompt
    st.divider()
    with st.container():
        if custom_header:
            st.markdown(f"{custom_header}")
        st.markdown(content)

def extra_lesson(user_prompt, role_context):
    with st.spinner('Next lesson...'):
        prompt2 = gpt.INSTRUCTIONS['role_contexts'][role_context]['instruct_2']
        messages = [user_prompt, ct.response_content, prompt2]
        return ct.get_response(prompt=messages)

def handle_code_convert(user_prompt, language):
    format_style = 'code_convert'
    header = f"# {language} Translation"
    user_prompt = f"to {language}: {user_prompt}"
    return format_style, header, user_prompt

# BEGIN WIDGETS
# Side bar controls
# Open API Key
ct.api_key = st.sidebar.text_input(
    label = "Open API Key :key:", 
    type = "password",
    help = "Get your API key from https://openai.com/"
) or ct.api_key

# Advanced settings expander
adv_settings = st.sidebar.expander(
    label = "Advanced Settings :gear:", 
    expanded = False
)

# Add Open API key and Advanced Settings widgets to the expander
with adv_settings:
    ct.model = st.selectbox("Model", ["gpt-3.5-turbo", "gpt-4"])
    ct.temperature = st.slider(
        "Temperature", 0.0, 1.0, 0.2, 0.1
    )
    ct.temperature = round(ct.temperature * 10) / 10

convert_languages = gpt.INSTRUCTIONS['role_contexts']['code_convert']['languages']
convert_file_formats = gpt.INSTRUCTIONS['role_contexts']['code_convert']['file_formats']
convert_options = convert_languages + convert_file_formats

custom_header = None

# Sidebar with dropdown
roles = gpt.CodeTutor.get_role_contexts()
roles = {gpt.INSTRUCTIONS['role_contexts'][role]['display_name']: role for role in roles}

selected_friendly_role = st.sidebar.selectbox(
    'Lesson Context :memo:', 
    roles.keys()
)

selected_json_role = roles[selected_friendly_role]

ct.role_context = selected_json_role

st.title(":teacher: Code Tutor")

prompt_box = st.empty()

# Create two columns
col1, col2, col3, col4 = st.columns(4)

with col1:
    answer_button = st.button(
        f":blue[{gpt.INSTRUCTIONS['role_contexts'][selected_json_role]['button_phrase']}]:sparkles:", 
        help="Generate an answer"
    )
with col2:
    just_code_toggle = st.toggle(
        "Just code", 
        help="The result will contain only code. This is enforced when selecting 'Convert Code'.", 
        key='just_code'
    )
with col3:
    extra_lesson_toggle = st.toggle(
        "Extra lesson", 
        help="Provide additional information to the related question. The selected AI role directly affects this."
    )

user_prompt = prompt_box.text_area(
    label="How can I help?",
    height=185,
    placeholder=gpt.INSTRUCTIONS['role_contexts'][selected_json_role]['prompt_placeholder'], 
    key='prompt'
)

if selected_json_role == 'code_convert':
    # Display selection box for languages to convert to
    convert_language = st.sidebar.selectbox(
    "Convert to:", convert_options, format_func=lambda x: f"{x} (file format)" if x in convert_file_formats else x
    )
    format_style, custom_header, user_prompt = handle_code_convert(user_prompt, convert_language)
else:
    format_style = 'markdown'

# 
if answer_button:
    content = generate_response(user_prompt, just_code_toggle)
    display_content(content, custom_header=custom_header)
    
    if extra_lesson_toggle:
        more_content = extra_lesson(user_prompt, ct.role_context)
        display_content(more_content, custom_header="Further Explanation")
