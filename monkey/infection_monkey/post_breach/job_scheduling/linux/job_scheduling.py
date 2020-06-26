TEMP_CRON = "$HOME/monkey-schedule-jobs"


def get_linux_commands_to_schedule_jobs():
    return [
        'touch {} &&'.format(TEMP_CRON),
        'crontab -l > {} &&'.format(TEMP_CRON),
        'echo \"# Successfully scheduled a job using crontab\" |',
        'tee -a {} &&'.format(TEMP_CRON),
        'crontab {}'.format(TEMP_CRON)
    ]
