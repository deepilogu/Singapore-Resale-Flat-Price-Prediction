import streamlit as st
import pickle as pk
import numpy as np
def streamlit_config():

    # page configuration
    st.set_page_config(page_title='Singapore Resale flat')

    # page header transparent color
    page_background_color = """
    <style>

    [data-testid="stHeader"] 
    {
    background: rgba(0,0,0,0);
    }

    </style>
    """
    st.markdown(page_background_color, unsafe_allow_html=True)

    # title and position
    st.markdown(f'<h1 style="text-align: center;">Industrial Copper Modeling</h1>',
                unsafe_allow_html=True)

def style_submit_button():

    st.markdown("""
                    <style>
                    div.stButton > button:first-child {
                                                        background-color: #367F89;
                                                        color: white;
                                                        width: 70%}
                    </style>
                """, unsafe_allow_html=True)

def style_prediction():

    st.markdown(
            """
            <style>
            .center-text {
                text-align: center;
                color: #20CA0C
            }
            </style>
            """,
            unsafe_allow_html=True
        )

class options:
    town_values = ['ANG MO KIO', 'BEDOK', 'BISHAN', 'BUKIT BATOK', 'BUKIT MERAH',
       'BUKIT PANJANG', 'BUKIT TIMAH', 'CENTRAL AREA', 'CHOA CHU KANG',
       'CLEMENTI', 'GEYLANG', 'HOUGANG', 'JURONG EAST', 'JURONG WEST',
       'KALLANG/WHAMPOA', 'MARINE PARADE', 'PASIR RIS', 'QUEENSTOWN',
       'SENGKANG', 'SERANGOON', 'TAMPINES', 'TOA PAYOH', 'WOODLANDS',
       'YISHUN', 'SEMBAWANG', 'PUNGGOL', 'LIM CHU KANG']
    float_model_values = ['Improved', 'New Generation', 'Model A', 'Standard', 'Apartment',
       'Simplified', 'Model A-Maisonette', 'Maisonette',
       'Multi Generation', 'Adjoined flat', 'Premium Apartment',
       'Terrace', 'Improved-Maisonette', 'Premium Maisonette', '2-room',
       'Model A2', 'Type S1', 'Type S2', 'DBSS', 'Premium Apartment Loft',
       '3Gen', 'IMPROVED', 'NEW GENERATION', 'MODEL A', 'STANDARD',
       'SIMPLIFIED', 'MODEL A-MAISONETTE', 'APARTMENT', 'MAISONETTE',
       'TERRACE', '2-ROOM', 'IMPROVED-MAISONETTE', 'MULTI GENERATION',
       'PREMIUM APARTMENT']
    

    def encoded_values(x):
        with open(r'label_encoder.pkl', 'rb') as lc:
            label_encoder = pk.load(lc)
        return label_encoder.transform([x])[0]
    

class prediction:
    
    def regression():

        with st.form('Regression'):

            col1,col2,col3 = st.columns([0.5,0.1,0.5])

            with col1:
                flat_type = st.selectbox(label = "Flat Type", options= np.arange(1, 7))

                storey_range = st.number_input(label= "Storey Range" )

                remaining_lease = st.number_input(label= "Remaining Lease")
        
                

            
            with col3:
                floor_area_sqm = st.number_input(label= " Floor Area in sqm")

                town = st.selectbox(label="Town", options=options.town_values)

                flat_model = st.selectbox(label="Flat Model", options=options.float_model_values)

                button = st.form_submit_button(label='SUBMIT')
                style_submit_button()

    
            if button:
                with open(r'resale_flat_model.pkl', 'rb') as f:
                    model = pk.load(f)

                town_encoded = options.encoded_values(town)
                flat_model_encoded = options.encoded_values(flat_model)

                user_data = np.array([[flat_type, storey_range, floor_area_sqm, remaining_lease, town_encoded, flat_model_encoded]])
                
                resale_price = model.predict(user_data)
                # resale_price = np.exp(y_pred[0])
                resale_price= np.round(resale_price, 2)
                return resale_price

streamlit_config()

try:
    # resale_price = np.array()
    resale_price = prediction.regression()

except ValueError:

    col1,col2,col3 = st.columns([0.26,0.55,0.26])

    with col2:
        st.warning('##### Please check the values.')

if resale_price is not None:
    style_prediction()
    st.markdown(f'### <div class="center-text">Predicted Resale Price = {resale_price}</div>', unsafe_allow_html=True)
    