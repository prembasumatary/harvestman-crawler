"""
gui.py - Module which provides a browser based UI
mode to HarvestMan using web.py. This module is part
of the HarvestMan program.

Created Anand B Pillai <abpillai at gmail dot com> Jun 01 2008

Copyright (C) 2008, Anand B Pillai.
"""

import sys, os
import web
import webbrowser
import time

from web import form, net, request

def get_templates_location():
    # Templates are located at harvestman/ui/templates folder...
    top = os.path.dirname(os.path.dirname(os.path.abspath(globals()['__file__'])))
    template_dir = os.path.join(top, 'ui','templates')
    return template_dir

# Global render object
g_render = web.template.render(get_templates_location())

PLUG_TEMPLATE="""\
       <plugin name="%s" enable="1" />
"""

PLUGINS_TEMPLATE="""\
    <plugins>
        %s
    </plugins>
"""


CONFIG_XML_TEMPLATE="""\
<?xml version="1.0" encoding="utf-8"?>

<HarvestMan xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xsi:schemaLocation="http://harvestmanontheweb.com/schemas/HarvestMan.xsd">

   <!--- Configuration file generated by HarvestMan Config Generator %(TIMESTAMP)s -->
   <config version="3.0" xmlversion="1.0">
     <projects>
      
      <project skip="0">

        <url>%(url)s</url>
        <name>%(projname)s</name>

        <basedir>%(basedir)s</basedir>
        <verbosity value="%(verbosity)s"/>
      </project>
      
     </projects>
     <network>
      <proxy>
        <proxyserver>%(proxy)s</proxyserver>
        <proxyuser>%(puser)s</proxyuser>
        <proxypasswd>%(ppasswd)s</proxypasswd>
        <proxyport value="%(proxyport)s"/>
      </proxy>
    </network>
    
    <download>
      <types>
        <html value="%(html)s"/>
        <images value="%(images)s"/>
        <movies value="%(movies)s"/>
        <flash value="%(flash)s"/>        
        <sounds value="%(sounds)s"/>
        <documents value="%(documents)s"/>        
        <javascript value="%(javascript)s"/>
        <javaapplet value="%(javaapplet)s"/>
        <querylinks value="%(getquerylinks)s"/>
      </types> 
      <cache status="%(pagecache)s">
        <datacache value="%(datacache)s"/>
      </cache>
      <protocol>
        <http compress="%(httpcompress)s" />
      </protocol>
      <misc>
        <retries value="%(retryfailed)s"/>
      </misc>
    </download>
    
    <control>
      <links>
        <imagelinks value="%(getimagelinks)s" />
        <stylesheetlinks value="%(getstylesheets)s"/>
        <offset start="%(linksoffsetstart)s" end="%(linksoffsetend)s" />
      </links>
      <extent>
        <fetchlevel value="%(fetchlevel)s"/>
        <depth value="%(depth)s"/>
        <extdepth value="%(extdepth)s"/>
        <subdomain value="%(subdomain)s"/>
        <ignoretlds value="%(ignoretlds)s"/>
      </extent>
      <limits>
        <maxfiles value="%(maxfiles)s"/>
        <maxfilesize value="%(maxfilesize)s"/>
        <maxbandwidth value="%(maxbandwidth)s"/>
        <connections value="%(connections)s"/>
        <timelimit value="%(timelimit)s"/>
      </limits>
      <rules>
        <robots value="%(robots)s"/>
        <urlpriority>%(urlpriority)s</urlpriority>
        <serverpriority>%(serverpriority)s</serverpriority>
      </rules>
      <filters>
        <urlfilter>%(urlfilter)s</urlfilter>
        <serverfilter>%(serverfilter)s</serverfilter>
        <wordfilter>%(wordfilter)s</wordfilter>
        <junkfilter value="%(junkfilter)s"/>
      </filters>
      %(PLUGIN)s
    </control>

    <parser>
      <feature name="a" enable="%(parser_enable_a)s" />
      <feature name="base" enable="%(parser_enable_base)s" />
      <feature name="frame" enable="%(parser_enable_frame)s" />
      <feature name="img" enable="%(parser_enable_img)s" />
      <feature name="form" enable="%(parser_enable_form)s" />
      <feature name="link" enable="%(parser_enable_link)s" />
      <feature name="body" enable="%(parser_enable_body)s" />
      <feature name="script" enable="%(parser_enable_script)s" />
      <feature name="applet" enable="%(parser_enable_applet)s" />
      <feature name="area" enable="%(parser_enable_area)s" />
      <feature name="meta" enable="%(parser_enable_meta)s" />
      <feature name="embed" enable="%(parser_enable_embed)s" />
      <feature name="object" enable="%(parser_enable_object)s" />
      <feature name="option" enable="%(parser_enable_option)s" />
    </parser>
      
    <system>
      <workers status="%(usethreads)s" size="%(threadpoolsize)s" timeout="%(timeout)s"/>
      <trackers value="%(maxtrackers)s" timeout="%(fetchertimeout)s" />
      <timegap value="%(sleeptime)s" random="%(randomsleep)s" />
    </system>
    
    <files>
      <urltreefile>%(urltreefile)s</urltreefile>
      <archive status="%(archive)s" format="%(archformat)s"/>
      <urlheaders status="%(urlheaders)s" />
      <localise value="%(localise)s"/>
    </files>
    
    <display>
      <browsepage value="%(browsepage)s"/>
    </display>
    
  </config>
  
</HarvestMan>
"""

def render_stylesheet():
    css = """\
    <style>
    body {
           font-family: Arial;
           font-size: 12px;
         }
    form th {
           text-align: right;
           vertical-align:top;
         }

    .description {
       font-style: italic;
     }
    .help {
       font-style: italic;
       font-size: 12px;
       color: #343434;
     }
    </style>
    """

    return css


def render_tabs():

    content ="""\
    <html><head><title>HarvestMan Web Console</title>
    <head>
    <script type="text/javascript" src="content/tabberjs"></script>
    <link rel="stylesheet" href="content/example_css" TYPE="text/css" MEDIA="screen">
    <link rel="stylesheet" href="content/example_print_css" TYPE="text/css" MEDIA="print">
    <script type="text/javascript">

    /* Optional: Temporarily hide the "tabber" class so it does not "flash"
       on the page as plain HTML. After tabber runs, the class is changed
       to "tabberlive" and it will appear. */

       document.write('<style type="text/css">.tabber{display:none;}<\/style>');
     </script>
     </head>

    <body>
    <h1>HarvestMan Web Console</h1>

    <div class="tabber">

     <div class="tabbertab">
          <h2>Configuration</h2>
          <p>
            <ol>
              <li>User configuration</li>
              <li>System configuration</li>
              <li>New configuration</li>
            </ol>
          </p>
     </div>


     <div class="tabbertab">
          <h2>Projects</h2>
          <p>
            <ol>
              <li>Project History</li>
              <li>Current Project</li>
              <li>New Project</li>
            </ol>
          </p>          
     </div>

     <div class="tabbertab">

          <h2>Documentation</h2>
          <p>
            <ol>
              <li>Release Notes</li>
              <li>Change History</li>
              <li>API Documentation</li>
              <li>HOWTOs & Tutorials</li>
            </ol>
          </p>
     </div>     

     <div class="tabbertab">

          <h2>About</h2>
          <p>HarvestMan - Web crawling application/framework written in pure Python.</p>
          <p>WWW: <a href="http://www.harvestmanontheweb.com">HarvestMan on the Web</a></p>
     </div>
     
    </div>
    </body>
    </html>
    """

    return content
       
       

    
############## Start web.py custom widgets ####################################################
      
class SizedTextbox(form.Textbox):
    """ A GUI class for a textbox which accepts an argument for
    its size """
    
    def __init__(self, name, size, title='', *validators, **attrs):
        super(SizedTextbox, self).__init__(name, *validators, **attrs)
        self.size = size
        self.val = self.value
        self.title = title
        
    def render(self):
        x = '<input type="text" name="%s" size="%d" title="%s"' % (net.websafe(self.name),
                                                                   self.size,
                                                                   net.websafe(self.title))
        if self.val !=None: x += ' value="%s"' % net.websafe(self.val)
        x += self.addatts()
        x += ' />'
        return x

class MyDropbox(form.Dropdown):
    """ A modified Dropdown class """
    
    def __init__(self, name, title='', args=None, *validators, **attrs):
        super(MyDropbox, self).__init__(name, args, *validators, **attrs)
        self.val = self.value
        self.title = title

    def render(self):
        x = '<select name="%s"%s title="%s">\n' % (net.websafe(self.name),
                                                   self.addatts(),
                                                   net.websafe(self.title))
        for arg in self.args:
            if type(arg) == tuple:
                value, desc= arg
            else:
                value, desc = arg, arg 

            if self.val == value: select_p = 'selected'
            else: select_p = ''
            x += '  <option %s>%s</option>\n' % (select_p, net.websafe(desc))
        x += '</select>\n'
        return x
        
class Label(form.Input):
    """ A class which provides a Label widget """
    
    def __init__(self, text,bold=False,italic=False,underlined=False, *validators, **attrs):
        self.name = ''
        self.text = text
        self.bold = bold
        self.italic = italic
        self.underlined = underlined
        super(Label, self).__init__('', *validators, **attrs)
        
    def render(self):
        text = '<p>%s</p>' % self.text
        if self.bold:
            text = '<b>%s</b>' % text
        if self.italic:
            text = '<i>%s</i>' % text
        if self.underlined:
            text = '<u>%s</u>' % text

        return text

    def validate(self, v):
        return True

############## End web.py custom widgets ####################################################

class HarvestManConfigGenerator(object):
    """ A class for web-based, interactive configuration
    file generation for HarvestMan """

    def __init__(self):
        self.form = None
        
    def create_form(self):
        """ Create an HTML form for user input """
        
        myform = form.Form(
            Label("Project Configuration", True),
            SizedTextbox("URL", 100, 'Starting URL for the project',
                         form.Validator("", lambda x:len(x)),value='http://www.foo.com'),
            SizedTextbox("Name", 20,'Name for the project',
                         form.Validator("", lambda x:len(x)), value='foo'),
            SizedTextbox("Base Directory", 50, 'Directory for saving downloaded files',
                         form.Validator("", lambda x:len(x)), value='~/websites'),
            MyDropbox("Verbosity", "0=>No messages, 5=>Maximum messages",
                      [0,1,2,3,4,5], value=2),
            Label("Network Configuration", True),
            SizedTextbox("Proxy Server", 50, "Proxy server address for your network, if any"),
            SizedTextbox("Proxy Server Port",10, "Port number for the proxy server",
                         value=80),
            SizedTextbox("Proxy Server Username", 20,
                         "Username for authenticating the proxy server (leave blank for unauthenticated proxies)"),
            SizedTextbox("Proxy Server Password", 20,
                         "Password for authenticating the proxy server (leave blank for unauthenticated proxies)"),
            Label("Download Types/Caching/Protocol Configuration", True),
            MyDropbox("HTML", 'Save HTML pages ?', ["Yes","No"]),
            MyDropbox("Images",'Save images in pages ?',["Yes","No"]),
            MyDropbox("Video",'Save video URLs (movies) ?',["No","Yes"]),
            MyDropbox("Flash",'Save Adobe Flash URLs ?',["No","Yes"]),
            MyDropbox("Audio",'Save audio URLs (sounds) ?',["No","Yes"]),
            MyDropbox("Documents",'Save Microsoft Office, Openoffice, PDF and Postscript files ?',
                      ["Yes","No"]),
            MyDropbox("Javascript",'Save server-side javascript URLs ?',["Yes","No"]),
            MyDropbox("Javaapplet",'Save java applet class files ?',["Yes","No"]),        
            MyDropbox("Query Links",'Save links of the form "http://www.foo.com/query?param=val" ?',
                      ["Yes","No"]),                      
            MyDropbox("Caching",'Enable URL caching in HarvestMan ?',
                      ["Yes","No"]),    
            MyDropbox("Data Caching",'Enable caching of URL data in the cache (requires more space) ?',
                      ["No","Yes"]),
            MyDropbox("HTTP Compression",'Accept gzip compressed data from web servers ?',
                      ["Yes","No"]),
            SizedTextbox("Retry Attempts", 10,
                         'Number of additional download tries for URLs which produce errors',
                         value=1),
            Label("Download Limits/Extent Configuration", True),
            MyDropbox("Fetch Level",
                      'Fetch level for the crawl (see FAQ)',[0,1,2,3,4]),
            MyDropbox("Crawl Sub-domains",
                      'Crawls "http://bar.foo.com" when starting URL belongs to "http://foo.com"',
                      ["No","Yes"]),
            SizedTextbox("Maximum Files Limit",10,
                         'Stops crawl when number of files downloaded reaches this limit',
                         value=5000),
            SizedTextbox("Maximum File Size Limit",10,
                         'Ignore URLs whose size is larger than this limit',
                         value=5242880),    
            SizedTextbox("Maximum Connections Limit",10,
                         'Maximum number of simultaneously open HTTP connections',
                         value=5),
            SizedTextbox("Maximum Bandwidth Limit(kb)",10,
                         'Maximum number of bandwidth used for given HTTP connections',
                         value=0),
            SizedTextbox("Crawl Time Limit",10,
                         'Stops crawl after the crawl duration reaches this limit',
                         value=-1),
            Label("Download Rules/Filters Configuration", True),    
            MyDropbox("Robots Rules",
                      'Obey robots.txt and META ROBOTS rules ?', 
                      ["Yes","No"]),
            SizedTextbox("URL Filter String",100,'A filter string for URLs (see FAQ)'),
            # SizedTextbox("Server Filter String",100, 'A filter string for servers (see FAQ)'),
            SizedTextbox("Word Filter String",100,
                         'A generic word filter based on regular expressions to filter web pages'),
            MyDropbox("JunkFilter",'Enable the advertisement/banner/other junk URL filter ?',
                      ["Yes","No"]),
            Label("Download Plugins Configuration", True),
            Label("Add up-to 5 valid plugins in the boxes below",italic=True),
            SizedTextbox("Plugin 1",20,'Enter the name of your plugin module here, without the .py* suffix'),
            SizedTextbox("Plugin 2",20,'Enter the name of your plugin module here, without the .py* suffix'),
            SizedTextbox("Plugin 3",20,'Enter the name of your plugin module here, without the .py* suffix'),
            SizedTextbox("Plugin 4",20,'Enter the name of your plugin module here, without the .py* suffix'),
            SizedTextbox("Plugin 5",20,'Enter the name of your plugin module here, without the .py* suffix'),
            Label("Files Configuration", True),    
            SizedTextbox("Url Tree File", 20,
                         'A filename which will capture parent/child relationship of all processed URLs',
                         value=''),
            MyDropbox("Archive Saved Files", 'Archive all saved files to a single tar archive file ?',
                      ["No","Yes"]),
            MyDropbox("Archive Format",'Archive format (tar.bz2 or tar.gz)',["bzip","gzip"]),
            MyDropbox("Serialize URL Headers",'Serialize all URL headers to a file (urlheaders.db) ?',
                      ["Yes","No"]),
            MyDropbox("Localise Links",'Convert outward (web) pointing links to disk pointing links ?',
                      ["No","Yes"]),
            Label("Misc Configuration", True),        
            MyDropbox("Create Project Browse Page",'Create an HTML page which summarizes all crawled projects ?',
                      ["No","Yes"]),            
            Label("Advanced Configuration Settings", True),
            Label('These are configuration parameters which are useful only for advanced tweaking. Most users can ignore the following settings and use the defaults',italic=True),
            Label("Download Limits/Extent/Filters/Rules Configuration", True, True),            
            MyDropbox("Fetch Image Links Always",
                      'Ignore download rules when fetching images ?',["Yes","No"]),
            MyDropbox("Fetch Stylesheet Links Always",
                      'Ignore download rules when fetching stylesheets ?',["Yes","No"]),
            SizedTextbox("Links Offset Start", 10,
                         'Offset of child links measured from zero (useful for crawling web directories)',
                         value=0),
            SizedTextbox("Links Offset End", 10,
                         'Offset of child links measured from end (useful for crawling web directories)',
                         value=-1),    
            MyDropbox("URL Depth", 'Maximum depth of a URL in relation to the starting URL',
                      [10,9,8,7,6,5,4,3,2,1,0]),
            MyDropbox("External URL Depth",
                      'Maximum depth of an external URL in relation to its server root (useful for only fetchlevels >1)',
                      [0,1,2,3,4,5,6,7,8,9,10]),
            MyDropbox("Ignore TLDs (Top level domains)",
                      'Consider http://foo.com and http://foo.org as the same server (dangerous)',
                      ["No","Yes"]),    
            SizedTextbox("URL Priority String",100,'A priority string for URLs (see FAQ)'),
            # SizedTextbox("Server Priority String",100, 'A priority string for servers (see FAQ)'),    
            Label("Parser Configuration", True, True),

            Label("Enable/Disable parsing of the tags shown below",italic=True),
            MyDropbox("Tag <a>", 'Enable parsing of <a> tags ?',["Yes","No"]),
            MyDropbox("Tag <applet>", 'Enable parsing of <applet> tags ?',["Yes","No"]),
            MyDropbox("Tag <area>", 'Enable parsing of <area> tags ?',["Yes","No"]),
            MyDropbox("Tag <base>", 'Enable parsing of <base> tags ?',["Yes","No"]),
            MyDropbox("Tag <body>", 'Enable parsing of <body> tags ?',["Yes","No"]),
            MyDropbox("Tag <embed>", 'Enable parsing of <embed> tags ?',["Yes","No"]),
            MyDropbox("Tag <form>", 'Enable parsing of <form> tags ?',["Yes","No"]),
            MyDropbox("Tag <frame>", 'Enable parsing of <frame> tags ?',["Yes","No"]),
            MyDropbox("Tag <img>", 'Enable parsing of <img> tags ?',["Yes","No"]),
            MyDropbox("Tag <link>", 'Enable parsing of <link> tags ?',["Yes","No"]),
            MyDropbox("Tag <meta>", 'Enable parsing of <meta> tags ?',["Yes","No"]),
            MyDropbox("Tag <object>", 'Enable parsing of <object> tags ?',["Yes","No"]),
            MyDropbox("Tag <option>", 'Enable parsing of <option> tags ?',["No","Yes"]),
            MyDropbox("Tag <script>", 'Enable parsing of <script> tags ?',["Yes","No"]),
            Label("Crawler System Configuration", True, True),
            MyDropbox("Worker Threads", 'Enable worker (downloader) thread pool ?',["Yes","No"]),
            SizedTextbox("Worker Thread Count", 10, 'Size of the worker thread pool',value=10),
            SizedTextbox("Worker Thread Timeout", 10, 'Timeout for the worker thread pool',value=1200.0),    
            SizedTextbox("Tracker Thread Count", 10, 'Size of the tracker (crawler/fetcher) thread pool',
                         value=10),
            SizedTextbox("Tracker Thread Timeout", 10, 'Timeout for the tracker thread pool',
                         value=240.0),    
            SizedTextbox("Tracker Sleep Time", 10,
                         'Duration of sleep time for tracker threads between cycles of activity',
                         value=3.0),
            MyDropbox("Tracker Sleep Randomized", 'Randomize the tracker thread sleep time ?',
                      ["Yes","No"]))
            

        return myform


    def convert_val(self, val):
        if val=="Yes":
            return '1'
        else:
            return '0'
    
    def make_config_xml(self, form):
        
        # Make dictionary...
        params_dict = {'url': form['URL'].value,
                       'projname': form['Name'].value,
                       'basedir': form['Base Directory'].value,
                       'verbosity': form['Verbosity'].value,
                       'proxy': form['Proxy Server'].value,
                       'puser': form['Proxy Server Username'].value,
                       'ppasswd': form['Proxy Server Password'].value,
                       'proxyport': form['Proxy Server Port'].value,
                       'html': self.convert_val(form['HTML'].value),
                       'images': self.convert_val(form['Images'].value),
                       'movies': self.convert_val(form['Video'].value),
                       'flash': self.convert_val(form['Flash'].value),                       
                       'sounds': self.convert_val(form['Audio'].value),
                       'documents': self.convert_val(form['Documents'].value),
                       'javascript': self.convert_val(form['Javascript'].value),
                       'javaapplet': self.convert_val(form['Javaapplet'].value),
                       'getquerylinks': self.convert_val(form['Query Links'].value),
                       'pagecache': self.convert_val(form['Caching'].value),
                       'datacache': self.convert_val(form['Data Caching'].value),
                       'httpcompress': self.convert_val(form['HTTP Compression'].value),                                      
                       'retryfailed': form['Retry Attempts'].value,
                       'pagecache': self.convert_val(form['Caching'].value),                                      
                       'getimagelinks': self.convert_val(form['Fetch Image Links Always'].value),
                       'getstylesheets': self.convert_val(form['Fetch Stylesheet Links Always'].value),
                       'linksoffsetstart': form["Links Offset Start"].value,
                       'linksoffsetend': form["Links Offset End"].value,
                       'fetchlevel': form["Fetch Level"].value,
                       'depth': form["URL Depth"].value,
                       "extdepth": form["External URL Depth"].value,
                       "subdomain": self.convert_val(form["Crawl Sub-domains"].value),
                       'ignoretlds': self.convert_val(form["Ignore TLDs (Top level domains)"].value),
                       'maxfiles': form["Maximum Files Limit"].value,
                       'maxfilesize': form["Maximum File Size Limit"].value,
                       'connections': form["Maximum Connections Limit"].value,
                       'maxbandwidth': str(form["Maximum Bandwidth Limit(kb)"].value) +'kb',
                       'timelimit': form["Crawl Time Limit"].value,
                       'robots': self.convert_val(form["Robots Rules"].value),
                       'urlpriority': form["URL Priority String"].value,
                       # 'serverpriority': form["Server Priority String"].value,
                       'serverpriority': '',
                       'urlfilter': form['URL Filter String'].value,
                       #'serverfilter': form['Server Filter String'].value,
                       'serverfilter': '',
                       'wordfilter': form['Word Filter String'].value,
                       'junkfilter': self.convert_val(form["JunkFilter"].value),
                       'parser_enable_a': self.convert_val(form["Tag <a>"].value),
                       'parser_enable_applet': self.convert_val(form["Tag <applet>"].value),
                       'parser_enable_area': self.convert_val(form["Tag <area>"].value),
                       'parser_enable_base': self.convert_val(form["Tag <base>"].value),
                       'parser_enable_body': self.convert_val(form["Tag <body>"].value),
                       'parser_enable_embed': self.convert_val(form["Tag <embed>"].value),
                       'parser_enable_form': self.convert_val(form["Tag <form>"].value),
                       'parser_enable_frame': self.convert_val(form["Tag <frame>"].value),
                       'parser_enable_img': self.convert_val(form["Tag <img>"].value),
                       'parser_enable_link': self.convert_val(form["Tag <link>"].value),
                       'parser_enable_meta': self.convert_val(form["Tag <meta>"].value),
                       'parser_enable_object': self.convert_val(form["Tag <object>"].value),
                       'parser_enable_option': self.convert_val(form["Tag <option>"].value),
                       'parser_enable_script': self.convert_val(form["Tag <script>"].value),
                       'usethreads': self.convert_val(form["Worker Threads"].value),
                       'threadpoolsize': form["Worker Thread Count"].value,
                       'timeout': form["Worker Thread Timeout"].value,
                       'maxtrackers': form["Tracker Thread Count"].value,
                       'fetchertimeout': form["Tracker Thread Timeout"].value,
                       'sleeptime': form["Tracker Sleep Time"].value,
                       'randomsleep': self.convert_val(form["Tracker Sleep Randomized"].value),
                       'urltreefile': form["Url Tree File"].value,
                       'archive': self.convert_val(form["Archive Saved Files"].value),
                       'archformat': form["Archive Format"].value,
                       'urlheaders': self.convert_val(form["Serialize URL Headers"].value),
                       'localise': self.convert_val(form["Localise Links"].value),
                       'browsepage': self.convert_val(form["Create Project Browse Page"].value)}

        plugins = ""

        # Add plugins information
        plugin1 = form["Plugin 1"].value
        plugin2 = form["Plugin 2"].value
        plugin3 = form["Plugin 3"].value
        plugin4 = form["Plugin 4"].value
        plugin5 = form["Plugin 5"].value
        plugint = (plugin1, plugin2, plugin3, plugin4, plugin5)

        for plug in plugint:
            if plug != '':
                plugins += PLUG_TEMPLATE % plug

        if plugins != '':
            plugins = PLUGINS_TEMPLATE % plugins

        params_dict['PLUGIN'] = plugins
        params_dict['TIMESTAMP'] = ' '.join((time.ctime(), time.tzname[0]))

        return CONFIG_XML_TEMPLATE % params_dict

    def GET(self):
        
        form = self.create_form()
        print "<html><head><title>HarvestMan Configuration File Generator</title>"
        # Styles...
        print "%s\n" % render_stylesheet()
        print "</head>\n"
        print "<body>\n"
        print g_render.form(form)
        print "</body>"
        print "</html>"

    def POST(self): 

        form = self.create_form()
        if not form.validates(): 
            print g_render.form(form)
        else:
            print self.make_config_xml(form)

class HarvestManGUI(object):
    """ Main UI class for HarvestMan """

    def GET(self):
        print "%s" % render_tabs()

class HarvestManLoader(object):

    GET = request.autodelegate('GET_')

    def GET_tabberjs(self):
        path = os.path.join(get_templates_location(), 'content','tabber.js')
        print '%s' % open(path).read()

    def GET_example_css(self):
        path = os.path.join(get_templates_location(), 'content','example.css')
        print '%s' % open(path).read()

    def GET_example_print_css(self):
        path = os.path.join(get_templates_location(), 'content','example-print.css')
        print '%s' % open(path).read()        
        

urls = ('/', 'HarvestManGUI',
        '/content/(.*)', 'HarvestManLoader')

def run():
    """ Run the web UI """

    # UI runs on port 5940
    sys.argv = [sys.argv[0]]
    sys.argv.append("5940")
    print "Starting HarvestMan Web UI at port 5940..."
    web.internalerror = web.debugerror
    web.run(urls, globals(), web.reloader)

if __name__ == "__main__":
    run()


