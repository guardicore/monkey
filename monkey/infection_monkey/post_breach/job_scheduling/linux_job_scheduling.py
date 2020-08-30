TEMP_CRON = "$HOME/monkey-schedule-jobs"


def get_linux_commands_to_schedule_jobs():
    return [
        f'touch {TEMP_CRON} &&',
        f'crontab -l > {TEMP_CRON} &&',
        'echo \"# Successfully scheduled a job using crontab\" |',
        f'tee -a {TEMP_CRON} &&',
        f'crontab {TEMP_CRON} ;',
        f'rm {TEMP_CRON}'
    ]
