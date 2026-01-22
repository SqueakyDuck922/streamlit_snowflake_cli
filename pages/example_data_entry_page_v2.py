import streamlit as st
import pandas as pd

st.title("Example Data Entry Page")

st.write("May need to first go to streamlitapp page, then this page")

# if "snowflake_session" not in st.session_state:
#     st.session_state["snowflake_session"] = fc.get_session()

session = st.session_state["snowflake_session"]

taxo_table = session.table('schema1.taxo_categories')


# +-------------------------+
# |    Selection Section    |
# +-------------------------+
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





# +------------------+
# |    Data Entry    |
# +------------------+
if submit_selection:

    st.write("debug: submit_selection")

    # Clear previous data entry state
    if 'taxo_record_data' in st.session_state:
        del st.session_state["taxo_record_data"]

    if selected_parent is not None:

        with st.form("data_entry_form"):

            selected_parent_id = taxo_table.filter(taxo_table.col('name')== selected_parent).to_pandas().values.tolist()[0][0]
            subcategories = taxo_table.filter(taxo_table.col('parent_id') == selected_parent_id).to_pandas()
            subcategory_ids = subcategories['ID'].tolist()
            subcategory_ids_str = ','.join(map(str, subcategory_ids))

            # st.write(subcategories)

            # Create dropdown options for relevant columns
            subcategory_options = subcategories['NAME'].tolist()

            # Initialize dataframe for data entry 
            if 'taxo_record_data' not in st.session_state:

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

                    st.session_state.taxo_record_data = pd.DataFrame(pre_populated_rows)


            # Build column configuration
            column_config = {
                "Subcategory": st.column_config.SelectboxColumn(
                    "Subcategory",
                    help="Select a subcategory",
                    options=subcategory_options,
                    required=True,
                    width="medium"
                ),
                "Value1": st.column_config.NumberColumn(
                    "Value1",
                    help="Enter an integer value for Value1",
                    required=True,
                    width="medium"
                ),
                "Value2": st.column_config.TextColumn(
                    "Value2",
                    help="Enter text value for Value2",
                    required=True,
                    width="medium"
                )
            }

            # Create the data editor
            edited_data = st.data_editor(
                st.session_state.taxo_record_data,
                column_config=column_config,
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True
            )


            submit_data_entry_form = st.form_submit_button('save data entry')
