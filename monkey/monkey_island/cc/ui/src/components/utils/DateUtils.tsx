export function parseTimeToDateString(time) {
    // If the time is a string timestamp
    let parsedTimeDate = Date.parse(time);

    // If the time is a unix timestamp
    if (isNaN(parsedTimeDate)) {
        parsedTimeDate = time;
    }

    let timeDate = new Date();
    timeDate.setTime(parsedTimeDate);

    return timeDate.toLocaleString('en-us');
}
