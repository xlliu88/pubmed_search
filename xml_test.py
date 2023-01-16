#!/usr/bin/python
#xml output test

from lxml import etree as ET
from lxml.builder import E   

page = E.html(
        E.head(
            E.title('Search result')
            ),
            E.body(
                E.span('Plant Cell. 2015 Dec;27(12):3321-35. doi: 10.1105/tpc.15.00454. Epub 2015 Nov 20.'),
                E.h3('The WRKY Transcription Factor WRKY71/EXB1 Controls Shoot Branching by Transcriptionally Regulating RAX Genes in Arabidopsis.', CLASS = 'title'),
                E.h4('Husbands AY1, Benkovics AH1, Nogueira FT1, Lodha M1, Timmermans MC.'),
                E.p('Flattened leaf architecture is not a default state but depends on positional information to precisely coordinate patterns of cell division in the growing primordium. This information is provided, in part, by the boundary between the adaxial (top) and abaxial (bottom) domains of the leaf, which are specified via an intricate gene regulatory network whose precise circuitry remains poorly defined. Here, we examined the contribution of the ASYMMETRIC LEAVES (AS) pathway to adaxial-abaxial patterning in Arabidopsis thaliana and demonstrate that AS1-AS2 affects this process via multiple, distinct regulatory mechanisms. AS1-AS2 uses Polycomb-dependent and -independent mechanisms to directly repress the abaxial determinants MIR166A, YABBY5, and AUXIN RESPONSE FACTOR3 (ARF3), as well as a nonrepressive mechanism in the regulation of the adaxial determinant TAS3A. These regulatory interactions, together with data from prior studies, lead to a model in which the sequential polarization of determinants, including AS1-AS2, explains the establishment and maintenance of adaxial-abaxial leaf polarity. Moreover, our analyses show that the shared repression of ARF3 by the AS and trans-acting small interfering RNA (ta-siRNA) pathways intersects with additional AS1-AS2 targets to affect multiple nodes in leaf development, impacting polarity as well as leaf complexity. These data illustrate the surprisingly multifaceted contribution of AS1-AS2 to leaf development showing that, in conjunction with the ta-siRNA pathway, AS1-AS2 keeps the Arabidopsis leaf both flat and simple.'),
                E.a('http://www.ncbi.nlm.nih.gov/pubmed/26589551',href = 'http://www.ncbi.nlm.nih.gov/pubmed/26589551')
                ),
            E.br()
        )   

lines = ET.tostring(page, pretty_print=False)
with open('./document/output.html','wb') as output:
    output.write(lines)
    

'''
Example from help document
page = (
          E.html(
              E.head(
                  E.title("This is a sample document")
             ),
             E.body(
                  E.h1("Hello!", CLASS("title")),
                  E.p("This is a paragraph with ", B("bold"), " text in it!"),
                  E.p("This is another paragraph, with a ",
                      A("link", href="http://www.python.org"), "."),
                  E.p("Here are some reservered characters: <spam&egg>."),
                  ET.XML("<p>And finally, here is an embedded XHTML fragment.</p>"),
              )
          )
      )
'''