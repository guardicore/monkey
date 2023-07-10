import NETWORK_SCAN_CONFIGURATION_SCHEMA from "./networkScan.js";
import CREDENTIALS from "./credentials";
import EXPLOITATION_CONFIGURATION_SCHEMA from "./exploitation";

const PROPAGATION_CONFIGURATION_SCHEMA = {
  title: "Propagation",
  type: "object",
  properties: {
    exploitation: EXPLOITATION_CONFIGURATION_SCHEMA,
    credentials: CREDENTIALS,
    general: {
      title: "General",
      type: "object",
      properties: {
        maximum_depth: {
          title: "Maximum scan depth",
          type: "integer",
          minimum: 0,
          default: 2,
          description:
            "Amount of hops allowed for the monkey to spread from the " +
            "Island server. \n" +
            " \u26A0" +
            " Note that setting this value too high may result in the " +
            "Monkey propagating too far, " +
            'if "Scan Agent\'s networks" is enabled.\n' +
            "Setting this to 0 will disable all scanning and exploitation.",
        },
      },
    },
    network_scan: NETWORK_SCAN_CONFIGURATION_SCHEMA,
  },
};
export default PROPAGATION_CONFIGURATION_SCHEMA;
