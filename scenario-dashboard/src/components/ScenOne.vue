<template>
  <HelloWorld scenName="scen1" header="Scenario: Intelligent emergency braking warning"
   overview='#### Overview
   
   Three cars are driving on one road. Car1 brakes abruptly due to a dangerous situation (emergency brake) and notifies Car2 (driving behind Car1) and Car3 (coming from the opposite lane) to adjust their accelerations intelligently in order to be able to react in time and appropriately to the possible dangerous situation ahead.'
   img="emergency_braking_scenario_overview.drawio.png"
 />
</template>

<script>
import HelloWorld from "@/components/HelloWorld.vue";

export default {
  name: 'ScenOne',
  components: {
    HelloWorld,
  },
};
</script>
