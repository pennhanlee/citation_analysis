def growth_index(frontier, total_doc, max_year, min_year):
    no_of_doc_rf = len(frontier.index)
    rf_percentage = no_of_doc_rf / total_doc
    data_collection_period = max_year - min_year
    sum_of_growth = 0
    for x in range(0, data_collection_period):
        up_to_current_year = max_year - x
        up_to_previous_year = up_to_current_year - 1
        current_year_count = len(frontier[frontier["Year"] <= up_to_current_year])
        previous_year_count = len(frontier[frontier["Year"] <= up_to_previous_year])
        if (previous_year_count > 0):
            sum_of_growth = sum_of_growth + (current_year_count - previous_year_count) / previous_year_count
        else:
            break
    growth_index = rf_percentage * (sum_of_growth / (data_collection_period - 1) * 100)
    return growth_index

def impact_index(rf_times_cited, rf_doc):
    impact_index = rf_times_cited / rf_doc
    return impact_index

def sci_based_index(rf_jif, rf_doc):
    sci_based_index = rf_jif / rf_doc
    return sci_based_index