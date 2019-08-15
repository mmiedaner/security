# -*- coding: utf-8 -*-

import matplotlib.backends.backend_pdf

class PdfAdaptor:
    
    def write_to_pdf(self, figures, file_name):
        pdf = matplotlib.backends.backend_pdf.PdfPages(file_name)
        
        # xrange ??
        for fig in range(1, len(figures)):
            matplotlib.backends.backend_pdf.Figure().set_figure(fig)
            pdf.savefig( fig )
            
        
        pdf.close()

