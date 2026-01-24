import streamlit as st
import pandas as pd


# Initialize session state
if "stage" not in st.session_state:
    st.session_state.stage = "selection"  # "selection" or "editor"
if "user_selections" not in st.session_state:
    st.session_state.user_selections = {}
if "dataframe" not in st.session_state:
    st.session_state.dataframe = None


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


    st.session_state.editor_initial_data = pd.DataFrame(pre_populated_rows)
    st.session_state.stage = "editor"

    return 


st.title("Example Data Entry Page v4")
st.write("May need to first go to streamlitapp page, then this page")



session = st.session_state["snowflake_session"]

taxo_table = session.table('schema1.taxo_categories')


parent_categories = taxo_table.filter(taxo_table.col('parent_id') == 0).to_pandas()


with st.form("entry_form"):


    st.write("session_state.stage:", st.session_state.stage)

    # +-------------------------+
    # |    Selection Section    |
    # +-------------------------+

    if st.session_state.stage == "selection":

        st.write("Step 1: Select chapter and category")
        
        selected_parent = st.pills(
            'Select a chapter:',
            options=parent_categories['NAME'].tolist(),
            key='selected_parent'
        )

        confirm_selection = st.form_submit_button('confirm selection')

        if confirm_selection:
            st.write(f"Selected chapter: {selected_parent}")

            st.session_state.selected_parent_id = taxo_table.filter(taxo_table.col('name')== selected_parent).to_pandas().values.tolist()[0][0]
            load_editor_initial_data(st.session_state.selected_parent_id)

            st.rerun()

    else:
        st.write("Step 2: Edit Your Data")
        
        # Display the selected chapter as read-only
        if 'selected_parent' in st.session_state and st.session_state.selected_parent:
            st.info(f"📖 Selected Chapter: {st.session_state.selected_parent}")
        
        if st.session_state.editor_initial_data is not None:
            # st.write(st.session_state.editor_initial_data)


            # Create dropdown options for relevant columns
            subcategories = taxo_table.filter(taxo_table.col('parent_id') == st.session_state.selected_parent_id).to_pandas()
            subcategory_options = subcategories['NAME'].tolist()

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
            st.session_state.editor_initial_data ,
            column_config=column_config,
            num_rows="dynamic",
            use_container_width=True,
            hide_index=True
        )

        submit_data = st.form_submit_button('submit data')

# Reset button - positioned below the form
if st.button("🔄 Reset Selection", type="secondary"):
    # Clear all session state variables related to the form
    st.session_state.stage = "selection"
    st.session_state.user_selections = {}
    st.session_state.dataframe = None
    if 'selected_parent' in st.session_state:
        del st.session_state.selected_parent
    if 'selected_parent_id' in st.session_state:
        del st.session_state.selected_parent_id
    if 'editor_initial_data' in st.session_state:
        del st.session_state.editor_initial_data
    st.rerun()
    