import json

from common.data.zero_trust_consts import EVENT_TYPE_MONKEY_LOCAL, EVENT_TYPE_ISLAND, \
    STATUS_POSITIVE, STATUS_CONCLUSIVE, TEST_ENDPOINT_SECURITY_EXISTS
from monkey_island.cc.models import Monkey
from monkey_island.cc.models.zero_trust.event import Event
from monkey_island.cc.models.zero_trust.finding import Finding

ANTI_VIRUS_KNOWN_PROCESS_NAMES = [
    u"AvastSvc.exe",
    u"AvastUI.exe",
    u"avcenter.exe",
    u"avconfig.exe",
    u"avgcsrvx.exe",
    u"avgidsagent.exe",
    u"avgnt.exe",
    u"avgrsx.exe",
    u"avguard.exe",
    u"avgui.exe",
    u"avgwdsvc.exe",
    u"avp.exe",
    u"avscan.exe",
    u"bdagent.exe",
    u"ccuac.exe",
    u"egui.exe",
    u"hijackthis.exe",
    u"instup.exe",
    u"keyscrambler.exe",
    u"mbam.exe",
    u"mbamgui.exe",
    u"mbampt.exe",
    u"mbamscheduler.exe",
    u"mbamservice.exe",
    u"MpCmdRun.exe",
    u"MSASCui.exe",
    u"MsMpEng.exe",
    u"rstrui.exe",
    u"spybotsd.exe",
    u"zlclient.exe",
    u"SymCorpUI.exe",
    u"ccSvcHst.exe",
    u"ccApp.exe",
    u"LUALL.exe",
    u"SMC.exe",
    u"SMCgui.exe",
    u"Rtvscan.exe",
    u"LuComServer.exe",
    u"ProtectionUtilSurrogate.exe",
    u"ClientRemote.exe",
    u"SemSvc.exe",
    u"SemLaunchSvc.exe",
    u"sesmcontinst.exe",
    u"LuCatalog.exe",
    u"LUALL.exe",
    u"LuCallbackProxy.exe",
    u"LuComServer_3_3.exe",
    u"httpd.exe",
    u"dbisqlc.exe",
    u"dbsrv16.exe",
    u"semapisrv.exe",
    u"snac64.exe",
    u"AutoExcl.exe",
    u"DoScan.exe",
    u"nlnhook.exe",
    u"SavUI.exe",
    u"SepLiveUpdate.exe",
    u"Smc.exe",
    u"SmcGui.exe",
    u"SymCorpUI.exe",
    u"symerr.exe",
    u"ccSvcHst.exe",
    u"DevViewer.exe",
    u"DWHWizrd.exe",
    u"RtvStart.exe",
    u"roru.exe",
    u"WSCSAvNotifier"
]


def test_antivirus_existence(telemetry_json):
    current_monkey = Monkey.get_single_monkey_by_guid(telemetry_json['monkey_guid'])
    if 'process_list' in telemetry_json['data']:
        process_list_event = Event.create_event(
            title="Process list",
            message="Monkey on {} scanned the process list".format(current_monkey.hostname),
            event_type=EVENT_TYPE_MONKEY_LOCAL)
        events = [process_list_event]

        av_processes = filter_av_processes(telemetry_json)

        for process in av_processes:
            events.append(Event.create_event(
                title="Found AV process",
                message="The process '{}' was recognized as an Anti Virus process. Process "
                        "details: {}".format(process[1]['name'], json.dumps(process[1])),
                event_type=EVENT_TYPE_ISLAND
            ))

        if len(av_processes) > 0:
            test_status = STATUS_POSITIVE
        else:
            test_status = STATUS_CONCLUSIVE
        Finding.save_finding(test=TEST_ENDPOINT_SECURITY_EXISTS, status=test_status, events=events)


def filter_av_processes(telemetry_json):
    all_processes = telemetry_json['data']['process_list'].items()
    av_processes = []
    for process in all_processes:
        process_name = process[1]['name']
        # This is for case-insensitive `in`. Generator expression is to save memory.
        if process_name.upper() in (known_av_name.upper() for known_av_name in ANTI_VIRUS_KNOWN_PROCESS_NAMES):
            av_processes.append(process)
    return av_processes
