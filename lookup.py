#!/usr/bin/env python3
#
# lookup.py <word> - look up word on treccani.it
#
# https://www.askpython.com/python-modules/requests-in-python
#
import requests
r = requests.get('https://www.treccani.it/vocabolario/ricerca/rozzo/')
print(r.text)

							<!-- module article search preview -->
							<section class="module-article-search_preview">    
								<h2 class="search_preview-title"><a target="_self" class="" href="/vocabolario/rozzo/">
									różżo
								</a></h2>
								<h3 class="search_preview-category">
									Vocabolario on line
								</h3>
								<div class="abstract">
																		<b>rozzo</b> 

<b>różżo</b> agg. [lat. *rŭdius, compar. neutro di rudis «<b>rozzo</b>»; v. rude]. – 1. a. raro. Ruvido, scabro: una lastra di pietra <b>rozza</b>. b. Di lavoro manuale o industriale, non compiutamente rifinito, appena [...]   capanna; La fanciulla regal di r. spoglie S’ammanta (T. Tasso); di opere d’arte: versi, disegni, fregi r.; scultura <b>rozza</b>. 2. fig. Di persona non raffinata dall’educazione e dalla cultura: Già ’l r. zappator del campo sgombra (Poliziano); per estens  ...
									<a class="link" href="/vocabolario/rozzo/">Leggi Tutto <span class="icon-freccia_next"></span></a>
									<div class="clr"></div>
								</div>

								
															</section>
							<!-- end module -->

look for first line
look for class="abstract"
look for <b>word</b>
skip blank lines
pull single line
split into parts
report desired part
done
