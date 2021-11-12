import geopandas as gpd
import pandas_bokeh
import pandas as pd
import os

def plot_abundance_for_list_of_postal_codes(pc: list, show_figure=False):
    """
    Takes list of postal codes (pc) as strings and plots their 
    abundance on a map
    returns a bokeh plot
    
    show_figure parameter allows to open figure in nwe browser window (True)
    or not (False)
    """
    here = os.path.dirname(__file__)
    main_folder_dir = os.path.join(here, "../../../")
    # load geojsons
    cp_barna  = gpd.read_file(main_folder_dir+"ds-codigos-postales-master/data/BARCELONA.geojson" )
    cp_lleida = gpd.read_file(main_folder_dir+"ds-codigos-postales-master/data/LLEIDA.geojson" )
    cp_tarragona = gpd.read_file(main_folder_dir+"ds-codigos-postales-master/data/TARRAGONA.geojson" )
    cp_girona = gpd.read_file(main_folder_dir+"ds-codigos-postales-master/data/GIRONA.geojson" )
    cp = gpd.GeoDataFrame(pd.concat([cp_barna, cp_lleida, cp_tarragona, cp_girona], ignore_index=True), crs=cp_barna.crs)

    # how often does each cp appear in pc?
    occurrences = [pc.count(x) for x in pc]
 
    # Sample data to plot
    df=pd.DataFrame({'COD_POSTAL': pc, 'A':occurrences})

    # Join ontario dataset with sample data
    new_df = gpd.GeoDataFrame(cp.merge(df, on=['COD_POSTAL']), crs=cp_barna.crs)

    return new_df.plot_bokeh(simplify_shapes=0, category="A", colormap="Spectral", legend = "vaccinated per postal codes", hovertool_columns=["COD_POSTAL"], show_figure=show_figure) 
    
if __name__ == "__main__":
    """
    provide some sample input for the plot function,
    to allow for a quick preview of only this plot
    """
    pc = ['08157', '08247', '17091', '17210', '08035']
    plot_abundance_for_list_of_postal_codes(pc, show_figure=True)
    
