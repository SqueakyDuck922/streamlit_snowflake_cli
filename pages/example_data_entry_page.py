import streamlit as st

st.title("Example Data Entry Page")

st.write("May need to first go to streamlitapp page, then this page")

# if "snowflake_session" not in st.session_state:
#     st.session_state["snowflake_session"] = fc.get_session()

session = st.session_state["snowflake_session"]

taxo_table = session.table('schema1.taxo_categories')



# categories = taxo_table.filter(taxo_table.col('parent_id') == selected_chapter_id).to_pandas()

# st.write(parent_categories)
# chapter_list = ['Operating Cashflow','Investing Cashflow','Financing Cashflow','Account Balance']

with st.form('selection_form'):

    parent_categories = taxo_table.filter(taxo_table.col('parent_id') == 0).to_pandas()

    selected_parent = st.pills(
        'Select a chapter:',
        options=parent_categories['NAME'].tolist()
        ) 

    # st.write(selected_parent)


    submit_selection = st.form_submit_button('confirm selection')



if submit_selection:

    if selected_parent is not None:

        with st.form("data_entry_form"):

            selected_parent_id = taxo_table.filter(taxo_table.col('name')== selected_parent).to_pandas().values.tolist()[0][0]

            subcategories = taxo_table.filter(taxo_table.col('parent_id') == selected_parent_id).to_pandas()

            st.write(subcategories)

            submit_data_entry_form = st.form_submit_button('save data entry')
