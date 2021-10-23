const EVT_Token = artifacts.require("EVT_Token");
const RSVP_Event = artifacts.require("RSVP_Event");
const EventSafe = artifacts.require("EventSafe");

module.exports = async function (deployer) {
  await deployer.deploy(EVT_Token);
  await deployer.deploy(EventSafe);
  await deployer.deploy(RSVP_Event, 50000);
};