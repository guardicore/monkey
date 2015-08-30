__author__ = 'itamar'

MONKEY_ARG = "m0nk3y"
DROPPER_ARG = "dr0pp3r"
DROPPER_CMDLINE = 'cmd /c %%(dropper_path)s %s' % (DROPPER_ARG, )
MONKEY_CMDLINE = 'cmd /c %%(monkey_path)s %s' % (MONKEY_ARG, )
DROPPER_CMDLINE_DETACHED = 'cmd /c start cmd /c %%(dropper_path)s %s' % (DROPPER_ARG, )
MONKEY_CMDLINE_DETACHED = 'cmd /c start cmd /c %%(monkey_path)s %s' % (MONKEY_ARG, )

from host import VictimHost