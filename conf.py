# -*- coding: utf-8 -*-

from string import Template
import sys, os, codecs

# Read index.rst configurations
lines = codecs.open('index.rst', 'r', 'utf-8').readlines()
rstconf = {}

rstconf['project'] = 'project'
rstconf['copyright'] = 'copyright'
rstconf['version'] = ''
rstconf['release'] = ''
rstconf['title'] = 'title'
rstconf['subtitle'] = 'subtitle'
rstconf['authors'] = 'authors'
rstconf['publisher'] = 'ContPub'
rstconf['basename'] = 'project'
rstconf['identifier'] = 'http://contpub.org/'
rstconf['language'] = 'en'
rstconf['keywords'] = 'contpub, ebook'

rstconf['latex_parindent'] = '0em'
rstconf['latex_paper_size'] = 'a4'
rstconf['latex_font_size'] = '12pt'
rstconf['latex_documents_target_name'] = None
rstconf['latex_documents_title'] = None
rstconf['latex_documents_author'] = None
rstconf['latex_docclass'] = 'manual'
rstconf['latex_logo'] = None
rstconf['latex_contentsname'] = 'Contents'

rstconf['html_theme'] = 'default'
rstconf['html_title'] = None

rstconf['epub_basename'] = None
rstconf['epub_theme'] = 'epub'
rstconf['epub_title'] = None
rstconf['epub_author'] = None
rstconf['epub_publisher'] = None
rstconf['epub_copyright'] = None
rstconf['epub_identifier'] = None
rstconf['epub_scheme'] = None
rstconf['epub_cover'] = None
rstconf['epub_language'] = None
rstconf['epub_tocdepth'] = 1

rstconf['mobi_theme'] = 'mobi'

for line in lines:
	if line[:4] == '   @':
		idx = line.find(':')
		rstconf[line[4:idx]] = line[idx+2:len(line)-1]

if rstconf['latex_documents_target_name'] is None:
	rstconf['latex_documents_target_name'] = rstconf['basename']+'.tex'
if rstconf['latex_documents_title'] is None:
	rstconf['latex_documents_title'] = rstconf['title']
if rstconf['latex_documents_author'] is None:
	rstconf['latex_documents_author'] = rstconf['authors']

if rstconf['html_title'] is None:
    rstconf['html_title'] = rstconf['title']

if rstconf['epub_basename'] is None:
	rstconf['epub_basename'] = rstconf['basename']
if rstconf['epub_title'] is None:
	rstconf['epub_title'] = rstconf['title']
if rstconf['epub_author'] is None:
	rstconf['epub_author'] = rstconf['authors']
if rstconf['epub_publisher'] is None:
	rstconf['epub_publisher'] = rstconf['publisher']
if rstconf['epub_copyright'] is None:
	rstconf['epub_copyright'] = rstconf['copyright']
if rstconf['epub_identifier'] is None:
	rstconf['epub_identifier'] = rstconf['identifier']
if rstconf['epub_scheme'] is None:
	rstconf['epub_scheme'] = rstconf['identifier']
if rstconf['epub_language'] is None:
	rstconf['epub_language'] = rstconf['language']

#sys.path.insert(0, os.path.abspath('.'))

# -- General configuration -----------------------------------------------------

sys.path.append(os.path.abspath('sphinxext'))

#needs_sphinx = '1.0'
extensions = ['sphinx.ext.pngmath', 'sphinx.ext.graphviz']

templates_path = ['_templates']

source_suffix = '.rst'
#source_encoding = 'utf-8-sig'
master_doc = 'index'
project = rstconf['project']
copyright = rstconf['copyright']
version = rstconf['version']
release = rstconf['release']
language = rstconf['language']
#today = ''
#today_fmt = '%B %d, %Y'

exclude_patterns = ['_build']

#default_role = None
#add_function_parentheses = True
#add_module_names = True
#show_authors = False
pygments_style = 'trac' #default is sphinx
highlight_language = 'none'

#modindex_common_prefix = []

# -- Options for LaTeX output --------------------------------------------------

#latex_paper_size = 'letter'
latex_paper_size = rstconf['latex_paper_size']

# The font size ('10pt', '11pt' or '12pt').
#latex_font_size = '10pt'
latex_font_size = rstconf['latex_font_size']

latex_documents = [
  ('index',
   rstconf['latex_documents_target_name'],
   rstconf['latex_documents_title'],
   rstconf['latex_documents_author'],
   rstconf['latex_docclass']),
]

latex_logo = rstconf['latex_logo']
latex_contentsname = rstconf['latex_contentsname']

#latex_use_parts = False
#latex_show_pagerefs = False
#latex_show_urls = False

latex_preamble = Template('''
%% \\usepackage[cm-default]{fontspec}

\\usepackage{indentfirst}
\\setlength{\\parindent}{$parindent}

\\usepackage{fontspec}
%% \\usepackage{xunicode}
\\usepackage{xcolor}
\\usepackage{titlesec}
\\usepackage{fancyvrb,relsize}

\\usepackage{hyperref}
\\hypersetup{%
pdftitle = {$pdftitle},
pdfsubject = {$pdfsubject},
pdfkeywords = {$pdfkeywords},
pdfauthor = {$pdfauthor},
pdfcreator = {ContPub},
pdfproducer = {TeX Live},
}
%% \\pdfinfo{/CreationDate (D:19990909000000-01'00')}

%% use xeCJK

\\usepackage[slantfont,boldfont,CJKaddspaces,CJKchecksingle,CJKnumber,fallback]{xeCJK}

%% \\usepackage{xltxtra}
%% \\usepackage{CJKfntef}
%% \\setCJKfallbackfamilyfont{\CJKrmdefault}{Apple LiSung}

\\XeTeXlinebreaklocale "zh"
\\XeTeXlinebreakskip = 0pt plus 1pt
\\defaultfontfeatures{Mapping=tex-text}

\\setCJKmainfont[BoldFont={Adobe Heiti Std},ItalicFont={Adobe Fangsong Std},BoldItalicFont={Adobe Kaiti Std}]{Adobe Song Std}
\\setCJKsansfont[BoldFont={Adobe Fan Heiti Std},ItalicFont={Adobe Fangsong Std},BoldItalicFont={Adobe Kaiti Std}]{Adobe Song Std}
\\setCJKmonofont{Adobe Ming Std} 
\\setCJKromanfont[BoldFont={Adobe Heiti Std},ItalicFont={Adobe Fangsong Std},BoldItalicFont={Adobe Kaiti Std}]{Adobe Song Std}

\\setmainfont[BoldFont={Myriad Pro}]{Adobe Garamond Pro}
\\setsansfont[BoldFont={Myriad Pro}]{Adobe Garamond Pro}
\\setmonofont{Courier Std}
\\setromanfont[BoldFont={Myriad Pro}]{Adobe Garamond Pro}

\\renewcommand{\\baselinestretch}{1.25}
\\DefineVerbatimEnvironment{Verbatim}{Verbatim}{fontsize=\\relsize{-1}}

\\usepackage{enumitem}
\\setitemize{leftmargin=2em}
\\setenumerate{leftmargin=2em}

''').substitute(pdftitle=rstconf['title'], pdfsubject=rstconf['subtitle'], pdfkeywords=rstconf['keywords'], pdfauthor=rstconf['authors'], parindent=rstconf['latex_parindent'])

#latex_appendices = []
#latex_domain_indices = True

latex_elements = {
#'papersize': '',
#'pointsize': '',
'babel': '\\usepackage{polyglossia}',
#'fontpkg': '',
#'fncychap': '',
#'preamble': '',
#'footer': '',
#'inputenc': '',
#'fontenc': '',
#'maketitle': '',
#'tableofcontents': '',
#'printindex': '',
'releasename': ''
#'docclass' 'classoptions' 'title' 'date' 'release' 'author' 'logo' 'releasename' 'makeindex' 'shorthandoff'
}

# -- Options for HTML output --------------------------------------------------
html_title = rstconf['html_title']
html_show_sourcelink = False
html_show_copyright = False
html_show_sphinx = False
html_static_path = ['_static']
html_theme = rstconf['html_theme']
html_theme_path = ["."]

# -- Options for ePub output --------------------------------------------------
epub_basename = rstconf['epub_basename']
epub_theme = rstconf['epub_theme']
epub_title = rstconf['epub_title']
epub_author = rstconf['epub_author']
epub_publisher = rstconf['epub_publisher']
epub_copyright = rstconf['epub_copyright']
epub_identifier = rstconf['epub_identifier']
epub_scheme = rstconf['epub_scheme']
if not rstconf['epub_cover'] is None:
    epub_cover = (rstconf['epub_cover'], 'epub-cover.html')
else:
    epub_cover = ()
epub_language = rstconf['epub_language']
epub_tocdepth = rstconf['epub_tocdepth']

# -- Options for mobi output --------------------------------------------------
mobi_theme = rstconf['mobi_theme']
