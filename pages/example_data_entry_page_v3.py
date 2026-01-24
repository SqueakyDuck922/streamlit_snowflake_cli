import streamlit as st
import pandas as pd



def load_editor_initial_data(selected_parent_id):
   


    # Load data for data_entry_form ############################################

    subcategories = taxo_table.filter(taxo_table.col('parent_id') == selected_parent_id).to_pandas()
    subcategory_ids = subcategories['ID'].tolist()
    subcategory_ids_str = ','.join(map(str, subcategory_ids))


    ## Check for existing data entries ############################################

    existing_data_loaded = False

    if subcategory_ids_str:
        existing_entries_query = f"""
        select taxo_id, value1, value2
        from v_taxo_records
        where taxo_id in ({subcategory_ids_str})
        """ 

        existing_entries = session.sql(existing_entries_query).to_pandas()

        if len(existing_entries) > 0:

            # TODO load existing entries into form fields
            st.write("Existing entries found")

    
    # If no existing data, pre-populate with one row per subcategory
    if not existing_data_loaded:
        pre_populated_rows = []
        for _, subcategory_row in subcategories.iterrows():
            subcategory_name = subcategory_row['NAME']

            row_data = {
                'Subcategory': subcategory_name,
                'value1': None,
                'value2': None
            }

            pre_populated_rows.append(row_data)

    return pd.DataFrame(pre_populated_rows)




st.title("Example Data Entry Page v3")

st.write("May need to first go to streamlitapp page, then this page")



session = st.session_state["snowflake_session"]

taxo_table = session.table('schema1.taxo_categories')


parent_categories = taxo_table.filter(taxo_table.col('parent_id') == 0).to_pandas()



# +-------------------------+
# |    Selection Section    |
# +-------------------------+

selected_parent = st.pills(
    'Select a chapter:',
    options=parent_categories['NAME'].tolist(),
    key='selected_parent'
    ) 


selection_button = st.button("Confirm Selection")


if selection_button:

    selected_parent_id = taxo_table.filter(taxo_table.col('name')== selected_parent).to_pandas().values.tolist()[0][0]

    # This returns selected_parent despite having not stored it in session_state
    st.write(f"You selected: {st.session_state.selected_parent}")
    st.write(selected_parent_id)

    editor_initial_data = load_editor_initial_data(selected_parent_id)

    st.write(editor_initial_data)