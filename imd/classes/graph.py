from ..interfaces.grid import Grid
from .variable_cell import VariableCell

import panel as pn

class Graph(Grid):
    def _create_grids(self): 
        """
            Creates one Cell object per variable. Cell object is the smallest  
            visualization unit in the grid. Moreover, it creates one Panel GridSpec
            object per space.

            Sets:
            --------
                - "self._cells" List
                - "self._grids" Dict
        """ 
        graph_grid_map = self._create_graph_grid_mapping() 
        for row, map_data in graph_grid_map.items():
            level = map_data[0]
            vars_list = map_data[1]
            level_previous = -1
            if (row-1) in graph_grid_map:
                level_previous = graph_grid_map[row-1][0]
            if level != level_previous:
                col = int((Grid._MAX_NUM_OF_COLS_PER_ROW - len(vars_list)*Grid._COLS_PER_VAR) / 2.)
            else: 
                col = int((Grid._MAX_NUM_OF_COLS_PER_ROW - Grid._MAX_NUM_OF_VARS_PER_ROW*Grid._COLS_PER_VAR) / 2.)
            for i,var_name in enumerate(vars_list):
                start_point = ( row, int(col + i*Grid._COLS_PER_VAR) )  
                end_point = ( row+1, int(col + (i+1)*Grid._COLS_PER_VAR) )
                #col_l = int(col_f + (i+1)*Grid._COLS_PER_VAR)
                grid_bgrd_col = level    
                c = VariableCell(var_name)                         
                self._cells.append(c)
                ##Add to grid
                cell_spaces = c.get_spaces()
                for space in cell_spaces:
                    if space not in self._grids:
                        self._grids[space] = pn.GridSpec(sizing_mode='stretch_both')
                    self._grids[space][ start_point[0]:end_point[0], start_point[1]:end_point[1] ] = pn.Column(c.get_plot(space), \
                    width=220, height=220)

    def _create_graph_grid_mapping(self):
        """
            Maps the graph levels and the variables to Panel GridSpec rows/cols. 
            Both <grid_row>=0 and <graph_level>=0 correspond to higher row/level.

            Returns:
            --------
                A Dict {<grid_row>: (<graph_level>, List of varnames) } 
        """ 
        _varnames_per_graph_level = self._data.get_varnames_per_graph_level()
        num_of_vars_per_graph_level = [len(_varnames_per_graph_level[k]) for k in sorted(_varnames_per_graph_level)]
        graph_grid_map = {}
        for level, num_vars in enumerate(num_of_vars_per_graph_level):
            row = level
            indx = 0
            while num_vars > Grid._MAX_NUM_OF_VARS_PER_ROW:
                while row in graph_grid_map:
                    row+=1
                graph_grid_map[row] = (level,_varnames_per_graph_level[level][indx:indx+Grid._MAX_NUM_OF_VARS_PER_ROW])
                row += 1
                indx += Grid._MAX_NUM_OF_VARS_PER_ROW
                num_vars -= Grid._MAX_NUM_OF_VARS_PER_ROW
            while row in graph_grid_map:
                row+=1
            graph_grid_map[row] = (level,_varnames_per_graph_level[level][indx:indx+num_vars])
        return graph_grid_map
