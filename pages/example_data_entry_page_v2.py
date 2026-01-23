import streamlit as st
import pandas as pd

# When have way to detect just moved to page, instead of rerun of page, then should run the below: 
# st.session_state.current_edited_data = None

st.write("Currently current_edited_data is not cleared after moving away from page and back, therefore liable to get false positives for unsaved changes.")


# Initialize session state
if 'persistent_data' not in st.session_state:
    st.session_state.persistent_data = {
        'selected_parent': None,
        'taxo_record_data': None,
        'subcategory_options': None,
        'forms_initialized': False
    }
    st.write("not initialized")




# Initialize edited_data tracking in session state
if 'current_edited_data' not in st.session_state:
    st.session_state.current_edited_data = None


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



def selection_form_submit():
    """Callback for form1 submission"""

    # Check if there are unsaved changes before allowing new selection
    if check_for_unsaved_changes():
        st.error("🚫 You have unsaved changes in the data entry form below. Please save or discard them before selecting a new chapter.")


    # Store the selection
    st.session_state.persistent_data['selection_form_selection'] = st.session_state.selected_parent





    # Load data for data_entry_form ############################################

    selected_parent = st.session_state.persistent_data['selection_form_selection']
    selected_parent_id = taxo_table.filter(taxo_table.col('name')== selected_parent).to_pandas().values.tolist()[0][0]
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


        st.session_state.persistent_data['taxo_record_data']= pd.DataFrame(pre_populated_rows)
        # st.session_state.current_edited_data = st.session_state.persistent_data['taxo_record_data'].copy()


    # CRITICAL: Set forms_initialized to True here
    st.session_state.persistent_data['forms_initialized'] = True



    # Create dropdown options for relevant columns
    st.session_state.persistent_data['subcategory_options'] = subcategories['NAME'].tolist()
  



def check_for_unsaved_changes():
    """Check if there are unsaved changes in the data entry form"""
    if (st.session_state.current_edited_data is not None and 
        st.session_state.persistent_data['taxo_record_data'] is not None):
        try:
            # Compare the edited data with the original data
            return not st.session_state.current_edited_data.equals(
                st.session_state.persistent_data['taxo_record_data']
            )
        except:
            return False
    return False

          


# has_unsaved_changes = check_for_unsaved_changes()

st.write(st.session_state.current_edited_data)

# # Display warning outside the form if there are unsaved changes
# if has_unsaved_changes:
#     st.error("🚫 You have unsaved changes in the data entry form below. Please save or discard them before selecting a new chapter.")

with st.form('selection_form'):

    parent_categories = taxo_table.filter(taxo_table.col('parent_id') == 0).to_pandas()

    selected_parent = st.pills(
        'Select a chapter:',
        options=parent_categories['NAME'].tolist(),
        key='selected_parent'
        ) 

    # st.write(selected_parent)


    # submit_selection = st.form_submit_button(
    #     'confirm selection',
    #     on_click=selection_form_submit,
    #     disabled=has_unsaved_changes  # Disable button if there are unsaved changes
    #     )
    
    submit_selection = st.form_submit_button(
        'confirm selection',
        on_click=selection_form_submit
        )



st.write("after form 1")




# +------------------+
# |    Data Entry    |
# +------------------+

# FORM 2 (conditionally shown)
# if submit_selection:
# if st.session_state.persistent_data['forms_initialized']:
if 'selection_form_selection' in st.session_state.persistent_data:

    st.write("debug: submit_selection")
    st.write(st.session_state.persistent_data['selection_form_selection'])

    # Clear previous data entry state
    # if 'taxo_record_data' in st.session_state:
    #     del st.session_state["taxo_record_data"]

    if selected_parent is not None:

        with st.form("data_entry_form"):


            # Build column configuration
            column_config = {
                "Subcategory": st.column_config.SelectboxColumn(
                    "Subcategory",
                    help="Select a subcategory",
                    options=st.session_state.persistent_data['subcategory_options'],
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
                st.session_state.persistent_data['taxo_record_data'], # st.session_state.taxo_record_data,
                column_config=column_config,
                num_rows="dynamic",
                use_container_width=True,
                hide_index=True
            )

            # Store edited data in session state for change detection
            st.session_state.current_edited_data = edited_data
            


            submit_data_entry_form = st.form_submit_button('save data entry')

            if submit_data_entry_form:
                st.write("Data entry submitted:")
                # st.write(edited_data)


                # Check if data has changed and display warning
                data_has_changed = check_for_unsaved_changes()
                if data_has_changed:
                    st.warning("Changes detected and will be saved.")

                    # Here you would typically save the edited_data to your database
                
                    # Update the original data with the saved data
                    st.session_state.persistent_data['taxo_record_data'] = edited_data.copy()
                    # Clear the edited data tracker to reset unsaved changes
                    st.session_state.current_edited_data = edited_data.copy()
                    
                    st.success("✅ Data saved successfully! You can now select a new chapter if needed.")


                else:
                    st.info("ℹ️ No changes detected")





with st.expander("Debug - Session State"):
    st.write("Current persistent_data:")
    st.json(st.session_state.persistent_data)
