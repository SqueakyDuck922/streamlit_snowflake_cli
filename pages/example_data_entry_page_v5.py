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


    st.session_state.editor_initial_data = pd.DataFrame(pre_populated_rows)
    st.session_state.stage = "editor"

    return 




st.title("Example Data Entry Page v5")
st.write("May need to first go to streamlitapp page, then this page")



session = st.session_state["snowflake_session"]

taxo_table = session.table('schema1.taxo_categories')

load_editor_initial_data(selected_parent_id=1)  # Example parent_id

# st.write(st.session_state.editor_initial_data )


st.session_state.selected_parent_id = 1

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


st.data_editor(
    st.session_state.editor_initial_data ,
    use_container_width=True,
    num_rows="fixed",
    # disabled=st.session_state["ctcview_readonly_cols"],
    # column_order=st.session_state["ctcview_col_names"],
    column_config=column_config,
    hide_index=True,
    key="ctcview_df_editor",
    # on_change=ctcview_df_on_change,
    # args=[
    #     st.session_state["project_id"],
    #     st.session_state["review_id"],
    #     filter_CT,
    #     st.session_state["ctcview_filter_WPs"],
    #     st.session_state["ctcview_filter_PSPOwners"],
    #     st.session_state["ctcview_show_PSPOwners"],
    #     st.session_state["ctcview_unhide"],
    # ],
    row_height=20
    # height=st.session_state["table_height"] if is_customizable_ui else None,
)