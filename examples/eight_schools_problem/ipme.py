import ipme

if __name__=="__main__":
    infer_datapath='inference_8_schools_centered.npz'
	#infer_datapath='inference_8_schools_non_centered.npz'
    imd_diag = ipme.Diagram(infer_datapath, predictive_checks = ['y'])
    imd_diag.get_diagram().show()