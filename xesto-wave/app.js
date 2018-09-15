import xesto from "xesto-wave-npm"
const client = xesto("c09fbe65eac44ceeaea2e351f4faace8");

client.connect().then( controller => {
  //This is a Leap.Controller object, and we can pass it gesture names to have
  //our app react to gestures!

  controller.on("SwipeLeft", () => {
    console.log("Woo! Swipe left!");
  });

  controller.connect();
});