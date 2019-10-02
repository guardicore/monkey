import logging
import threading

logger = logging.getLogger(__name__)

# These are pseudo-singletons - global Locks. These locks will allow only one thread to generate a report at a time.
# Report generation can be quite slow if there is a lot of data, and the UI queries the Root service often; without
# the locks, these requests would accumulate, overload the server, eventually causing it to crash.
logger.debug("Initializing report generation lock.")
report_generating_lock = threading.Semaphore()
__attack_report_generating_lock = threading.Semaphore()
__regular_report_generating_lock = threading.Semaphore()


def safe_generate_reports():
    # Wait until report generation is available.
    logger.debug("Waiting for report generation...")
    # Entering the critical section.
    report_generating_lock.acquire()
    logger.debug("Report generation locked.")
    report = safe_generate_regular_report()
    attack_report = safe_generate_attack_report()
    # Leaving the critical section.
    report_generating_lock.release()
    logger.debug("Report generation released.")
    return report, attack_report


def safe_generate_regular_report():
    # Local import to avoid circular imports
    from monkey_island.cc.services.reporting.report import ReportService
    logger.debug("Waiting for regular report generation...")
    __regular_report_generating_lock.acquire()
    logger.debug("Regular report generation locked.")
    report = ReportService.generate_report()
    __regular_report_generating_lock.release()
    logger.debug("Regular report generation released.")
    return report


def safe_generate_attack_report():
    # Local import to avoid circular imports
    from monkey_island.cc.services.attack.attack_report import AttackReportService
    logger.debug("Waiting for attack report generation...")
    __attack_report_generating_lock.acquire()
    logger.debug("Attack report generation locked.")
    attack_report = AttackReportService.generate_new_report()
    __attack_report_generating_lock.release()
    logger.debug("Attack report generation released.")
    return attack_report


def is_report_being_generated():
    # From https://docs.python.org/2/library/threading.html#threading.Semaphore.acquire:
    # When invoked with blocking set to false, do not block.
    #   If a call without an argument would block, return false immediately;
    #   otherwise, do the same thing as when called without arguments, and return true.
    is_report_being_generated_right_now = not report_generating_lock.acquire(blocking=False)
    logger.debug("is_report_being_generated_right_now == " + str(is_report_being_generated_right_now))
    if not is_report_being_generated_right_now:
        # We're not using the critical resource; we just checked its state.
        report_generating_lock.release()
    return is_report_being_generated_right_now
