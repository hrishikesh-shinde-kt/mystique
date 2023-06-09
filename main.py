import streamlit as st
import pandas as pd
import requests
import cairosvg

insurer_name_mapping = {
  "Star Health & Allied Insurance Co. Ltd." : "Star Health",
  "National Insurance Co. Ltd." : "",
  "The New india Assurance Co Ltd." : "",
  "The Orient al Insurance Co. Ltd." : "",
  "United india Insurance Co. Ltd." : "",
  "lAcko General Insurance Ltd." : "",
  "Bajaj Alianz General Insurance Co. Ltd." : "",
  "Bhasti AXA General insurance Co. Ltd." : "",
  "Cholamandalam MS General Insurance Co. Ltd." : "",
  "Edetweiss General Insurance Co. Ltd." : "",
  "Future Generali India insurance Co. Ltd." : "",
  "IGo Digit General Insurance Ltd." : "",
  "HDFC ERGO General Insurance Co. Ltd." : "HDFC",
  "ICICI Lombard General Insurance Co. Ltd." : "",
  "IFFCO Tokio General insurance Co. Ltd." : "",
  "Kotak Mahindra General Insurance Co. Ltd." : "",
  "Liberty General insurance Ltd." : "",
  "Magma HDI General insurance Co. Ltd." : "",
  "Navi General Insurance Limited" : "",
  "Raheja QBE General insurance Co. Ltd." : "",
  "Reliance General Insurance Co. Ltd." : "",
  "Royal Sundaram General Insurance Co. Ltd." : "",
  "SBI General Insurance Co. Ltd." : "",
  "Shriram General Insurance Co. Ltd." : "",
  "Tata ANG General Insurance Co. Ltd." : "",
  "Universal Sompo General Insurance Co. Ltd." : "",
  "Aditya Birla Health insurance Co. Ltd." : "",
  "Care Health Insurance Ltd." : "",
  "HDFC ERGO Health Insurance Co. Ltd." : "",
  "ManipalCigna Health Insurance Co. Ltd." : "",
  "Miva Bupa Health insurance Co. Ltd." : "",
  "Reliance Health Insurance Ltd." : "",
}

colors = {
  'header': '#cfe4f7',
  'odd_row': '#e7f1fa',
  'even_row': '#f2f9ff',
}

blue_shades = [
    {'selector': '',
     'props': [('border', '1px solid #c7d2ff')]},
    {'selector': 'th',
     'props': [('background-color', '#4c68ff'),
               ('color', 'white'),
               ('font-weight', 'bold')]},
    {'selector': 'td',
     'props': [('background-color', '#e5e9ff')]},
    {'selector': 'tr:nth-of-type(odd)',
     'props': [('background-color', '#d8dcff')]},
    {'selector': 'tr:nth-of-type(even)',
     'props': [('background-color', '#f2f4ff')]},
    {'selector': 'tr:hover',
     'props': [('background-color', '#c1c9ff')]},
]
blue_shades = [
  {
    'selector': 'table',
    'props': [
      ('width', '100%'),
      ('border-collapse', 'collapse'),
      ('border', f'1px solid {colors["header"]}')
    ]
  },
  {
    'selector': 'th',
    'props': [
      ('background-color', colors['header']),
      ('color', '#000'),
      ('font-weight', 'bold'),
      ('text-align', 'center'),
      ('border', f'1px solid {colors["header"]}')
    ]
  },
  {
    'selector': 'tr:nth-of-type(odd)',
    'props': [
      ('background-color', colors['odd_row']),
      ('border', f'1px solid {colors["header"]}')
    ]
  },
  {
    'selector': 'tr:nth-of-type(even)',
    'props': [
      ('background-color', colors['even_row']),
      ('border', f'1px solid {colors["header"]}')
    ]
  },
  {
    'selector': 'td',
    'props': [
      ('text-align', 'center'),
      ('padding', '8px'),
      ('border', f'1px solid {colors["header"]}')
    ]
  },
]
st.set_page_config(
  page_title="Health Insurance Portability",
  page_icon="media/favicon.png",
  layout="wide",  # sets page to wide mode as default. 
  # initial_sidebar_state="expanded"
)

# Adds logo and title on screen.
def add_logo():
  # Create a container for the logo and title
  # header = st.container()

  # # Add a logo to the left column
  # with header:
  #   col1, col2 = st.columns([1,3])
    
  #   # Load the SVG image
  #   svg_data = open('media/mystique_logo.svg', 'rb').read()

  #   # Convert the SVG to PNG format
  #   png_data = cairosvg.svg2png(svg_data)


  #   # png_data = renderPM(drawing, dpi=72, output=None, fmt='PNG')
    
  #   with col1:
  #     st.image(png_data, width=200)

  #   with col2:
  #     # st.title('Health Insurance Portability')
  #     st.markdown("<div style='text-align: center; display: flex; align-items: center'> <h1>Health Insurance Portability</h1> </div>", unsafe_allow_html=True)
  
  # st.image("http://placekitten.com/200/200", width=30)
  # st.write("# PDF-Uploader")
  # Load the SVG image
  svg_data = open('media/mystique_logo.svg', 'rb').read()

  # Convert the SVG to PNG format
  png_data = cairosvg.svg2png(svg_data)
  st.image(png_data, width=200)
  st.markdown("<div style='text-align: center;'> <h1>Health Insurance Portability</h1> </div>", unsafe_allow_html=True)

# Formats text.
def change_name_format(name):
  return name.replace("_", " ").title()

# Returns list of keys of a dictonary.
def get_column_name(keys):
  return [change_name_format(key) for key in keys.keys()]

# Changes table border style.
def set_table_border():
  css = """
      <style>
      table.dataframe {
          border-collapse: separate;
          border-spacing: 0px;
          border-color: #4d6bff;
          border-width: 4px;
          border-style: outset;
          border-radius: 8px;
      }
      </style>
  """

  st.markdown(css, unsafe_allow_html=True)

# Displays table(s) according to the response.
def show_table(response):
  response_item = response['response']['data']
  for item in response_item:
    if isinstance(response_item[item], dict):
      df = pd.DataFrame(
        [list(response_item[item].values())],
        columns = get_column_name(response_item[item])
      )
    else: 
      df = pd.DataFrame(
        [list(i.values()) for i in response_item[item]],
        columns = get_column_name(response_item[item][0])
      )
    st.header(change_name_format(item))
    set_table_border()
    hide_table_row_index = """
            <style>
              thead tr th:first-child {display:none}
              tbody th {display:none}
            </style>
            """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    styled_df = df.style.set_table_styles(blue_shades)
    st.table(styled_df)

# Main logic.

add_logo()

# Getting the list of options.
options = list(insurer_name_mapping.keys())
options.insert(0, None)

# Getting Policy type input.
option = st.selectbox(
  'Insurer Name',
  options
)
if option:
  # Getting pdf input.
  uploaded_pdf = st.file_uploader("Upload your pdf")
  company = insurer_name_mapping[option]
  if uploaded_pdf is not None:
    url = "https://pivot-port-poldoc-health.attributum.com/api/ml_process"
    files = {
      "input_file" : uploaded_pdf
    } 
    data = {
      "insurance_company" : company.lower(),
      "data_type" : "Generic"
    }
    # headers = {"Authorization": st.secrets["auth_key"]}
    headers = {"Authorization": "Api-Key T33fvOdn.n2AO1NH9GmU2jL9066FEOQvIw9zSLJSc"}

    # Post API call.
    if company != "":
      response = requests.post(url, files=files, data=data, headers=headers)

      if response:
        show_table(response.json())

